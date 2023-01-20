import os
from math import log10
from rocketprops.scaling_funcs import ambrose_Psat, solve_omega, Rowlinson_Poling_Cp, \
                                      Pitzer_Hvap, ScaledRackett_SG, \
                                      Pitzer_surften, Nicola_thcond, Squires_visc

from rocketprops._prop_template import template
from rocketprops.PR_eos import PReos
from rocketprops.rocket_prop import here
# from rocketprops.unit_conv_data import get_value

""" 
Signatures of functions
def ambrose_Psat( T, Tc, Pc, omega )
def solve_omega( Tc, Pc, Psat_ref, Tref )
def Rowlinson_Poling_Cp(T, Tc, omega, Cpgm, MW)
def Pitzer_Hvap(T, Tc, MW, omega)
def Edalat_Pvap(T, Tc, Pc, omega)
def ScaledRackett_SG( TdegR, Tc, omega, Tref, SGref )
def Pitzer_surften(T, Tc, Pc, omega)
def Nicola_thcond(T, M, Tc, Pc, omega)
def Squires_visc( TdegR, Tref, PoiseRef )
"""
R = 8.3144598 # J/mol-K  =  m^3-Pa / mol-K  =  J/mol-K

def add_propellant( prop_name='A50',
                    Tref        = 527.67, # degR
                    Pref        = 14.6959, # psia
                    SG_ref       = 0.9035471601513377, # SG
                    Cp_ref       = 0.7282323251759043, # BTU/lbm/delF
                    Hvap_ref     = 346.5000380753298, # BTU/lbm
                    cond_ref     = 0.1661065246970707, # BTU/hr/ft/delF
                    surf_ref     = 0.00016987300288460853, # lbf/in
                    visc_ref     = 0.009208681003236614, # poise (P)
                    Pc_psia       = 1731, # psia
                    Tc_degR       = 1092.67, # degR
                    Tnbp_degR     = 617.6700000000001, # degR
                    Tfreeze_degR  = 481.67, # degR
                    Ttriple_degR  = 481.67, # degR
                    MolWt    = 41.802, # g/gmole
                    save_file=False):

    tmpD = {} # index=template name, value=string or numeric value

    dataSrc = 'Scaled Reference Point'        
    omega  = solve_omega( Tc_degR, Pc_psia, 14.7, Tnbp_degR ) # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
    tmpD['omega'] = omega

    Pvap = ambrose_Psat( Tref, Tc_degR, Pc_psia, omega ) # psia
    tmpD['Pvap'] = Pvap

    tmpD['dataSrc'] = dataSrc
    tmpD['class_name'] = prop_name + '_scaled'
    tmpD['prop_name'] = prop_name + '_scaled'

    tmpD['T'] = Tref
    tmpD['P'] = Pref
    tmpD['SG'] = SG_ref
    tmpD['Cp'] = Cp_ref
    tmpD['Hvap'] = Hvap_ref
    tmpD['cond'] =  cond_ref
    tmpD['surf'] = surf_ref
    tmpD['visc'] = visc_ref

    tmpD['Pc'] = Pc_psia
    tmpD['Tc'] = Tc_degR
    tmpD['Tnbp'] = Tnbp_degR
    tmpD['Tfreeze'] = Tfreeze_degR
    tmpD['Ttriple'] = Ttriple_degR
    tmpD['MolWt'] = MolWt

    # Zc is the mechanical compressibility for mixtures as well.
    Zc = 0.3074013086987 # Peng-Robinson EOS (Soave-Redlich-Kwong=1/3)
    tmpD['Zc'] = Zc

    # start building the arrays of values
    NsatPts = 21

    Tlo = max( tmpD['Ttriple'], tmpD['Tfreeze'] )
    Thi = tmpD['Tc'] 
    dT = (Thi - Tlo) / (NsatPts - 1)
    
    trL = []
    tL  = []
    pL  = []
    viscL = []
    condL = []
    cpL = []
    hvapL = []
    surfL = []    
    SG_liqL = []
    SG_vapL = []

    #Cp_wo_gas = Rowlinson_Poling_Cp(Tref, Tc_degR, omega, 0.0, MolWt)
    Cpgm = 4*R # ideal gas polytomic value   # max(0.0, Cp_ref - Cp_wo_gas)
    # print( 'Cp_wo_gas=%g, Cpgm=%g, Cp_ref=%g'%(Cp_wo_gas, Cpgm, Cp_ref) )
    cp_calc = Rowlinson_Poling_Cp(Tref, Tc_degR, omega, Cpgm, MolWt)
    cp_corr_fact = Cp_ref / cp_calc

    cond_calc = Nicola_thcond(Tref, MolWt, Tc_degR, Pc_psia, omega)
    cond_corr_fact = cond_ref / cond_calc

    hvap_calc = Pitzer_Hvap(Tref, Tc_degR, MolWt, omega)
    hvap_corr_fact = Hvap_ref / hvap_calc

    surf_calc = Pitzer_surften(Tref, Tc_degR, Pc_psia, omega)
    surf_corr_fact = surf_ref / surf_calc

    eos = PReos(fluid_name=prop_name, 
                T_R=Tref, P_psia=Pref, omega=omega,
                Tc_R=Tc_degR, Pc_psia=Pc_psia, Tnbp_R=Tnbp_degR, MolWt=MolWt)

    # RGAS = 83.145 # bar-cm**3 / gmole-K
    # SGc = MolWt * get_value(Pc_psia, 'psia', 'bar') / RGAS / (Tc_degR/1.8) / eos.Zc
    # Vc = MolWt / SGc # (cm**3/gmole)
    # Vc = get_value(Vc, 'cm**3', 'm**3')

    # SGm = SG_ref
    # Vm = MolWt / SGm # (cm**3/gmole)
    # Vm = get_value(Vm, 'cm**3', 'm**3')

    # print( 'Vc =', Vc)
    # cp_calc = Przedziecki_Sridhar_visc(Tref, Tfreeze_degR, Tc_degR, Pc_psia, Vc, Vm, omega, MolWt)
    # cp_corr_fact = Cp_ref / cp_calc

    for i in range( NsatPts ):
        T = min(Thi, Tlo + i*dT)
        Tr = min(1.0, T / Tc_degR )
        if i == NsatPts-1:
            Tr = 1.0
        
        trL.append( Tr )
        tL.append( T )
        pL.append( ambrose_Psat( T, Tc_degR, Pc_psia, omega ) )
        
        
        viscL.append( Squires_visc( T, Tref, visc_ref ) )
        condL.append( cond_corr_fact * Nicola_thcond(T, MolWt, Tc_degR, Pc_psia, omega) )
        
        cpL.append( cp_corr_fact * Rowlinson_Poling_Cp(T, Tc_degR, omega, Cpgm, MolWt) )
        # cpL.append( cp_corr_fact * Przedziecki_Sridhar_visc(T, Tfreeze_degR, Tc_degR, Pc_psia, Vc, Vm, omega, MolWt) )
            
        if Tr < 1.0:
            hvapL.append( hvap_corr_fact * Pitzer_Hvap(T, Tc_degR, MolWt, omega) )
            surfL.append( surf_corr_fact * Pitzer_surften(T, Tc_degR, Pc_psia, omega) )    
        else:
            hvapL.append( 0.0 )
            surfL.append( 0.0 )    
            
        
        if Tr < 1.0:
            SG_liqL.append( ScaledRackett_SG( T, Tc_degR, omega, Tref, SG_ref ) )

            eos.set_TP(T, pL[-1])
            SG_vapL.append( eos.SGgas )
        else:
            SG_liqL.append(  ScaledRackett_SG( Tc_degR, Tc_degR, omega, Tref, SG_ref )   )
            SG_vapL.append( SG_liqL[-1]  )
        

    tmpD['NsatPts'] = NsatPts
    tmpD['trL'] = repr(trL)
    tmpD['tL'] = repr(tL)
    tmpD['log10pL'] = repr( [log10(p) for p in pL] )
    
    tmpD['log10viscL'] = repr( [log10(v) for v in viscL] )
    tmpD['condL'] = repr(condL)
    tmpD['cpL'] = repr(cpL)
    tmpD['hvapL'] = repr(hvapL)
    tmpD['surfL'] = repr(surfL)
    tmpD['SG_liqL'] = repr(SG_liqL)
    tmpD['log10SG_vapL'] = repr( [log10(v) for v in SG_vapL] )


    # for k,v in tmpD.items():
    #     print(k, v)
    # ============== save template to file ===================
    src = template.format( **tmpD )
    # print( src )
    fname = prop_name + '_scaled_prop.py'

    if save_file:
        save_path = os.path.join( here, 'props', fname)
        print( 'Saving "%s"'%save_path )
        with open(save_path, 'w') as fOut:
            fOut.write( src )


if __name__ == "__main__":

    add_propellant()

