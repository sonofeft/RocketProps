from math import log10
from rocketprops.unit_conv_data import get_value

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, perox_Pcrit_psia_terp, 
                                                          perox_critical_risk_degC_terp, perox_max_storage_degC_terp)
from rocketprops.peroxidexx.peroxidexx_main_data import perox_freeze_pt_degC_terp, perox_boil_pt_degC_terp

from rocketprops.peroxidexx.peroxidexx_cond import get_eng_cond_at_TdegR # Cond_Peroxide_Liquid # get_eng_cond_at_TdegR
from rocketprops.peroxidexx.peroxidexx_hvap import get_eng_hvap_at_TdegR #  Hvap_Peroxide_Liquid # get_eng_hvap_at_TdegR
from rocketprops.peroxidexx.peroxidexx_cp import get_eng_cp_at_TdegR #  CP_Peroxide_Liquid # get_eng_cp_at_TdegR
from rocketprops.peroxidexx.peroxidexx_pvap import get_eng_pvap_at_TdegR #  Pvap_Peroxide_Liquid # get_eng_pvap_at_TdegR
from rocketprops.peroxidexx.peroxidexx_sg import get_eng_sg_at_TdegR  # SG_Peroxide_Liquid # get_eng_sg_at_TdegR
from rocketprops.peroxidexx.peroxidexx_surf import get_eng_surf_at_TdegR # Surf_Peroxide_Liquid # get_eng_surf_at_TdegR
from rocketprops.peroxidexx.peroxidexx_visc import get_eng_visc_at_TdegR # Visc_Peroxide_Liquid # get_eng_visc_at_TdegR


P_1_ATM = 14.6959

def effective_mw(weight_percent_h2o2):
    m_h2o2 = 34.0147
    m_h2o = 18.015
    
    w_h2o2 = weight_percent_h2o2 / 100.0
    w_h2o = 1.0 - w_h2o2
    
    # Calculate moles
    n_h2o2 = w_h2o2 / m_h2o2
    n_h2o = w_h2o / m_h2o
    
    # Calculate mole fractions
    x_h2o2 = n_h2o2 / (n_h2o2 + n_h2o)
    x_h2o = n_h2o / (n_h2o2 + n_h2o)
    
    # Calculate M_mix
    return (x_h2o2 * m_h2o2) + (x_h2o * m_h2o)

def get_eng_prop_plot(conc_wt=100, prop_name="Pvap", Tmin=500, Tmax=600, num_points=12):

    dT = (Tmax - Tmin) / (num_points - 1)
    TL = []
    propL = []
    for n in range( num_points ):
        T = Tmin + n * dT 
        prop = get_eng_propD( conc_wt=conc_wt, degR=T )[prop_name]
        TL.append( T )
        propL.append( prop )

    return TL, propL

def get_eng_property( prop_name='SG', conc_wt=90, degR=500):
    return get_eng_propD( conc_wt=conc_wt, degR=degR )[prop_name]

def get_eng_propD( conc_wt=90, degR=500):

    T_C = get_value( degR, 'degR', 'degC')

    propD = {} # htpObj.get_properties( conc_wt=conc_wt, temp_c=T_C)


    eng_propD = {} # key=property name, value=property in RocketProp units

    eng_propD['conc'] = conc_wt
    eng_propD['T'] = degR

    eng_propD['Tc'] = get_value( perox_Tcrit_degC_terp(conc_wt), 'degC', 'degR' )
    eng_propD['Pc'] = perox_Pcrit_psia_terp( conc_wt )

    eng_propD['Tnbp'] = get_value( perox_boil_pt_degC_terp(conc_wt), 'degC', 'degR' )
    eng_propD['Tfreeze'] = get_value( perox_freeze_pt_degC_terp( conc_wt ), 'degC', 'degR' )
    # eng_propD['Tfreeze'] = get_value( propD['Freezing_Point_C'], 'degC', 'degR' )
    eng_propD['Triple'] = eng_propD['Tfreeze']

    eng_propD['SG'] = get_eng_sg_at_TdegR(conc_wt, degR) # propD['Specific_Gravity']
    eng_propD['cond'] = get_eng_cond_at_TdegR(conc_wt, degR) # get_value( propD['Thermal_Conductivity_W_mK'], 'W/m/K', 'BTU/hr/ft/delF' )
    eng_propD['Cp'] =  get_eng_cp_at_TdegR(conc_wt, degR) # get_value( propD['Specific_Heat_kJ_kgK'], 'kJ/kg/delK', 'BTU/lbm/delF' )
    eng_propD['surf'] = get_eng_surf_at_TdegR(conc_wt, degR) #  get_value( propD['Surface_Tension_mN_m'], 'mN/m', 'lbf/in' )
    eng_propD['Hvap'] =  get_eng_hvap_at_TdegR(conc_wt, degR)  # get_value( propD['Heat_of_Vap_kJ_kg'], 'kJ/kg', 'BTU/lbm' )

    eng_propD['visc'] = get_eng_visc_at_TdegR(conc_wt, degR) #  get_value( propD['Viscosity_cP'], 'cp', 'poise' )
    eng_propD['Pvap'] = get_eng_pvap_at_TdegR(conc_wt, degR) #  propD['Vapor_Pressure_psia']
    eng_propD['SGc'] = get_eng_sg_at_TdegR(conc_wt, eng_propD['Tc']) #   propD['Critical_Density_SG']

    propD['Tdecomp_onset_C'] = perox_critical_risk_degC_terp( conc_wt )
    propD['Tmax_storage_C'] = perox_max_storage_degC_terp( conc_wt )
    eng_propD['Tdecomp_onset_R'] = get_value( propD['Tdecomp_onset_C'], 'degC', 'degR' )
    eng_propD['Tmax_storage_R'] = get_value( propD['Tmax_storage_C'], 'degC', 'degR' )


    MolWt = effective_mw( conc_wt )
    eng_propD['MolWt'] = MolWt

    Tc = eng_propD['Tc']
    Pc = eng_propD['Pc']
    SGc = eng_propD['SGc']
    eng_propD['Zc']   = Pc * MolWt / (18540.0 * Tc * (SGc/27.67990471))

    eng_propD['omega'] =  -1.0 - log10( get_eng_pvap_at_TdegR(conc_wt, 0.7 * Tc) / Pc )   #propD['Acentric_Factor']

    eng_propD['MolWt'] = MolWt

    if eng_propD['Pvap'] > P_1_ATM:
        eng_propD['P'] = eng_propD['Pvap']
    else:
        eng_propD['P'] = P_1_ATM

    return eng_propD


if __name__ == "__main__":
    # --- USAGE EXAMPLE ---
    # Assuming 'htp_data_file' is your file containing the lists
    
    eng_propsD = get_eng_propD( conc_wt=98, degR=540)

    keyL = sorted( eng_propsD.keys() )
    for k in keyL:
         print( k, eng_propsD[k] )

    print( '='*66 )

    TL, propL = get_eng_prop_plot(conc_wt=100, prop_name="Pvap", Tmin=500, Tmax=600, num_points=12)
    print( 'TL =', TL)
    print( 'propL =', propL)

         

 

