import os
from math import log10

from rocketprops.peroxidexx.peroxidexx_pvap import get_eng_pvap_at_TdegR

# from rocketprops.peroxidexx.peroxidexx_main_data import find_omega


from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.mixing_functions import isPeroxide_Ox
from rocketprops.rocket_prop import Prop
from rocketprops.prop_names import prop_names

from rocketprops.peroxidexx.peroxidexx_eng_units import get_eng_propD

def make_peroxide_Prop( pname='Peroxide_70'):

    if pname == "H2O2":
        pcent_H2O2 = 100
    else:
        pcent_H2O2 = isPeroxide_Ox( pname, verbose=True)
        print( 'pcent_H2O2 =', pcent_H2O2)

        # if not prop_names.is_primary_name( 'Peroxide' ):
        #     prop_names.add_primary_name( 'Peroxide' )

        prop_names.add_associated_name( 'Peroxide', pname )

    NsatPts = 21

    eD = get_eng_propD( conc_wt=pcent_H2O2, degR=500)
    Tdecomp_onset_R = eD['Tdecomp_onset_R']
    Tmax_storage_R  = eD['Tmax_storage_R']
    Tperoxide_freeze  = eD['Tfreeze']

    Tref = min( Tmax_storage_R, 527.67 ) # 20C or max storage
    PvapRef = get_eng_pvap_at_TdegR( pcent_H2O2, Tref)
    Pref = max(14.7, PvapRef )

    # First decide on fixed/critical properties
    eng_prop_refD = get_eng_propD( conc_wt=pcent_H2O2, degR=Tref)
    Tc = eng_prop_refD['Tc']
    Pc = eng_prop_refD['Pc']
    SGc = eng_prop_refD['SGc']

    # Tfreeze = get_value( perox_freeze_pt_degC_terp( pcent_H2O2 ), 'degC', 'degR' )
    # Tnbp = get_value( perox_boil_pt_degC_terp( pcent_H2O2 ), 'degC', 'degR' )
    Tnbp = eng_prop_refD['Tnbp']
    Tfreeze = eng_prop_refD['Tfreeze']


    Ttriple = Tfreeze

    # print( 'Tfreeze, Tnbp, Tc, Pc',Tfreeze,Tnbp, Tc, Pc )

    MolWt = eng_prop_refD['MolWt']
    Zc   = Pc * MolWt / (18540.0 * Tc * (SGc/27.67990471))


    def build_trL( Tfreeze, Tc ):
        
        Tr_init = Tfreeze / Tc
        dtr = (1.0 - Tr_init) / ( NsatPts - 1.0 )
        
        trL = [Tr_init + i*dtr for i in range( NsatPts )]
        
        trL[-1] = 1.0 # remove any roundoff error
        return trL


    # build temperature list
    trL = build_trL( Tfreeze, Tc )
    trL = [float(tr) for tr in trL] # make sure of simple float values
    tL = [tr*Tc for tr in trL]

    # ============ set all reference values ===================
    PvapRef = eng_prop_refD['Pvap']
    SGref = eng_prop_refD['SG']
    CpRef = eng_prop_refD['Cp']
    viscRef = eng_prop_refD['visc']
    HvapRef = eng_prop_refD['Hvap']
    condRef = eng_prop_refD['cond']
    surfRef = eng_prop_refD['surf']

    # ============= Build all value lists =======================
    vp_log10L = []
    condL     = []
    cpL       = []
    hvapL     = []
    surfL     = []
    sgL       = []
    log10_viscL  = []

    for t in tL:
        eD = get_eng_propD( conc_wt=pcent_H2O2, degR=t)

        vp_log10L.append( float(log10(eD['Pvap'])) )
        log10_viscL.append(  float(log10(eD['visc'])) )
        condL.append(     float(eD['cond'] ))
        cpL.append(       float(eD['Cp'] ))
        hvapL.append(     float(eD['Hvap'] ))
        surfL.append(     float(eD['surf'] ))
        sgL.append(       float(eD['SG'] ))

    # calculate omega from vapor pressure
    # log10p_terp = InterpProp(tL, vp_log10L, extrapOK=EXTRAP_OK)
    # Pvap_07 = 10.0**log10p_terp(0.7 * Tc)
    # omega = -1.0 - log10( Pvap_07 / Pc )
    # print('omega =',omega, '   SGc=',SGc)

    omega = eng_prop_refD['omega']
    # omega = find_omega( Tnbp/1.8, 14.6959, Tc/1.8, Pc)
    # print('omega =',omega, '   SGc=',SGc)

    # ------------ use vp_log10L to calc gas SG ---------------
    def get_z_with_zc_anchored_Z(P, T, Pc, Tc, Zc, omega):
        Tr = T / Tc
        Pr = P / Pc
        
        # 1. Calculate the standard B coefficients
        def get_B_coeffs(temp_r):
            b0 = 0.083 - (0.422 / (temp_r**1.6))
            b1 = 0.139 - (0.172 / (temp_r**4.2))
            return b0, b1

        # 2. Find the "Error Factor" at the critical point (Tr=1)
        # This ensures the model hits Zc exactly when P=Pc and T=Tc
        b0_crit, b1_crit = get_B_coeffs(1.0)
        theoretical_Z_at_crit = 1.0 + (b0_crit + omega * b1_crit)
        
        # Scaling factor to align the model with your known Zc
        # This effectively "stretches" the Virial curve to your anchor point
        scale = (Zc - 1.0) / (theoretical_Z_at_crit - 1.0)
        
        # 3. Calculate actual B for current conditions
        b0, b1 = get_B_coeffs(Tr)
        
        # 4. Final Z calculation
        # We clip Pr/Tr to 1.0 to keep it in the "gas-only" regime
        deviation = (min(Pr, 1.0) / Tr) * (b0 + (omega * b1)) * scale
        Z = 1.0 + deviation
        # print( "P=%g, T=%g, Pc=%g, Tc=%g, Zc=%g, omega=%g, Z=%g"%(P, T, Pc, Tc, Zc, omega, Z) )
        # print( "                             b0=%g, b1=%g"%(b0, b1) )
        
        return max(Z, Zc) # Ensure Z never drops below the critical floor
    
    log10SG_vapL = []
    vpL = [10**y for y in vp_log10L]
    for t,p  in zip( tL, vpL ):
        Z = get_z_with_zc_anchored_Z(p, t, Pc, Tc, Zc, omega)

        lbm_p_ci = p * MolWt / ( 18540.0 * t * Z)
        SGg = lbm_p_ci * 27.67990471
        
        log10SG_vapL.append( log10(SGg) )


    # ========================================
    tmpD = {} # index=template name, value=string value

    tmpD['dataSrc'] = "RocketProps"
    tmpD['prop_name'] = pname

    tmpD['T'], tmpD['T_dataSrc'] = Tref, "RocketProps"
    tmpD['P'], tmpD['P_dataSrc'] = Pref, "RocketProps"
    tmpD['Pvap'], tmpD['Pvap_dataSrc'] = PvapRef, "RocketProps"
    tmpD['Pc'], tmpD['Pc_dataSrc'] = Pc, "RocketProps"
    tmpD['Tc'], tmpD['Tc_dataSrc'] = Tc, "RocketProps"
    tmpD['Zc'], tmpD['Zc_dataSrc'] = Zc, "RocketProps"
    tmpD['omega'], tmpD['omega_dataSrc'] = omega, "RocketProps"
    tmpD['SG'], tmpD['SG_dataSrc'] = SGref, "RocketProps"

    tmpD['visc'], tmpD['visc_dataSrc'] = viscRef, "RocketProps"
    tmpD['cond'], tmpD['cond_dataSrc'] = condRef, "RocketProps"
    tmpD['Tnbp'], tmpD['Tnbp_dataSrc'] = Tnbp, "RocketProps"
    tmpD['Ttriple'], tmpD['Ttriple_dataSrc'] = Ttriple, "RocketProps"
    tmpD['Tfreeze'], tmpD['Tfreeze_dataSrc'] = Tfreeze, "RocketProps"
    tmpD['Cp'], tmpD['Cp_dataSrc'] = CpRef, "RocketProps"
    tmpD['MolWt'], tmpD['MolWt_dataSrc'] = MolWt, "RocketProps"
    tmpD['Hvap'], tmpD['Hvap_dataSrc'] = HvapRef, "RocketProps"
    tmpD['surf'], tmpD['surf_dataSrc'] = surfRef, "RocketProps"
    tmpD['NsatPts'], tmpD['NsatPts_dataSrc'] = NsatPts, "RocketProps"

    tmpD['trL'], tmpD['trL_dataSrc'] = trL, "RocketProps"
    tmpD['tL'], tmpD['tL_dataSrc'] = tL, "RocketProps"
    tmpD['log10pL'], tmpD['log10pL_dataSrc'] = vp_log10L, "RocketProps"
    tmpD['condL'], tmpD['condL_dataSrc'] = condL, "RocketProps"
    tmpD['cpL'], tmpD['cpL_dataSrc'] = cpL, "RocketProps"
    tmpD['hvapL'], tmpD['hvapL_dataSrc'] = hvapL, "RocketProps"
    tmpD['surfL'], tmpD['surfL_dataSrc'] = surfL, "RocketProps"
    tmpD['SG_liqL'], tmpD['SG_liqL_dataSrc'] = sgL, "RocketProps"
    tmpD['log10SG_vapL'], tmpD['log10SG_vapL_dataSrc'] = log10SG_vapL, "RocketProps"
    tmpD['log10viscL'], tmpD['log10viscL_dataSrc'] = log10_viscL, "RocketProps"

    tmpD['SG_compressed'] = ''


    return Prop( valueD=tmpD )

if __name__ == "__main__":

    prop_obj = make_peroxide_Prop( pname='H2O2')

    prop_obj.summ_print()

    prop_obj.plot_sat_props()
