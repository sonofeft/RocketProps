from math import  exp
from scipy.optimize import brentq
from rocketprops.InterpProp_scipy import InterpProp
from scipy.interpolate import Akima1DInterpolator, interp1d
from rocketprops.unit_conv_data import get_value


# --- 2. MIXTURE CALCULATIONS ---
def get_molWt_mix( pcent_H2O2 ):
    """Calculates Molecular Weight of H2O2/H2O mixture."""
    w = pcent_H2O2 / 100.0
    if w <= 0: return 18.0153
    if w >= 1: return 34.0147
    n_h2o2 = w / 34.0147
    n_h2o = (1 - w) / 18.0153
    x_h2o2 = n_h2o2 / (n_h2o2 + n_h2o)
    return (x_h2o2 * 34.0147) + ((1 - x_h2o2) * 18.0153)


# ======================= SAFETY DATA =======================
# Source: NASA Safety Standard for Hydrogen Peroxide & PeroxyChem Technical Bulletin.
conc_safety = [3, 10, 35, 50, 70, 85, 90, 98, 100]
T_critical_risk_C = [100, 100, 95, 85, 75, 60, 50, 40, 35]
T_storage_max_C = [40.0, 35.0, 30.0, 25.0, 35.0, 30.0, 25.0, 20.0, 15.0]
danger_notes = [
    "Stable; minimal gas evolution",
    "Stable; slight pressure in sealed bottles",
    "Industrial grade; requires vented caps",
    "Standard pulp/paper grade; venting critical",
    "Slow pressure buildup in tanks",
    "Rapid gas evolution; vent hazard",
    "High sensitivity; self-heating",
    "Extreme risk; spontaneous trigger",
    "Highly unstable; lab-only use"
]
# ======================= SAFETY Interpolators =======================

perox_max_storage_degC_terp = InterpProp( conc_safety, T_storage_max_C, extrapOK=True )

perox_critical_risk_degC_terp = InterpProp( conc_safety, T_critical_risk_C, extrapOK=True )

# 2. Create the nearest-neighbor interpolator
# Use 'nearest' to snap to the closest concentration
# Use 'extrapolate' to handle values like 1% or 101%
note_interp = interp1d(conc_safety, [0,1,2,3,4,5,6,7,8], kind='nearest', fill_value="extrapolate")

def perox_get_danger_note(c):
    # Find the closest index
    idx = int(note_interp(c))
    return danger_notes[idx]


# ======================= CRITICAL PROPERTIES =======================
# Source: NIST / NASA Liquid Propellant Manual.
conc_crit = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]
Tc_K = [647.1, 649.8, 656.2, 678.5, 690.1, 705.5, 717.5, 721.7, 728.4, 730.2]
Pc_bar = [220.6, 220.5, 220.2, 219.4, 218.9, 218.1, 217.4, 217.2, 216.9, 216.8]
Dc_SG = [0.322, 0.326, 0.335, 0.368, 0.387, 0.412, 0.440, 0.449, 0.464, 0.468]

# ================= Critical Property Interpolators ====================

perox_Tcrit_degC_terp = InterpProp( conc_crit, [get_value(Tc, 'degK', 'degC') for Tc in Tc_K], extrapOK=True )

perox_Pcrit_psia_terp = InterpProp( conc_crit, [get_value(Pc, 'bar', 'psia') for Pc in Pc_bar], extrapOK=True )

perox_Dcrit_SG_terp = InterpProp( conc_crit, Dc_SG, extrapOK=True )

# ======================= Freezing and Boiling Properties ====================
# H2O2 Concentration (%) - Added 45.2 and 61.2
# Source: Eutectic values derived from Schumb et al. phase diagram data.
conc_list_w_eutectics = [0, 3, 10, 35, 45.2, 50, 61.2, 70, 85, 90, 98, 100] # pcent_H2O2

# Freezing Points (°C)
# Note the dips at 45.2% (-52.7°C) and 61.2% (-56.5°C)
freezing_pt_list = [ 0.00, -1.50, -5.50, -33.00, -52.70, -52.20, -56.50, -40.30, -17.50, -11.50, -2.50, -0.43] # degC

# Specific Heat Capacity (Cp) at the Freezing Point (kJ/kg·K)
# Note: These values represent the liquid phase just before solidification
cp_at_freezing_list = [4.21, 4.157, 4.026, 3.585, 3.332, 3.328, 3.167, 3.115, 2.921, 2.846, 2.723, 2.687]

# Calculated Heat of Vaporization at the Freezing Point (kJ/kg)
# Values account for the increased enthalpy required at sub-zero temperatures.
# hvap_fp_list_kj_kgL = [
#     2501.0,  # 0%   (Pure Water at 0.00°C)
#     2450.5,  # 3%   
#     2335.2,  # 10%  
#     1980.8,  # 35%  
#     1835.4,  # 45.2% (Eutectic 1)
#     1770.1,  # 50%  
#     1640.6,  # 61.2% (Eutectic 2)
#     1545.2,  # 70%  
#     1435.8,  # 85%  
#     1405.3,  # 90%  
#     1365.7,  # 98%  
#     1393.1   # 100% (Pure H2O2 at -0.43°C)
# ]

# # interpolator of Hvap (kJ/kg) given pcent_H2O2
# perox_hvap_at_tfreeze_terp = InterpProp( conc_list_w_eutectics, hvap_fp_list_kj_kgL, extrapOK=True)

# Dynamic Viscosity at the Freezing Point (cP or mPa·s)
# visc_at_freezing_list = [1.79, 1.88, 2.12, 4.85, 9.92, 9.65, 11.20, 6.84, 3.65, 3.12, 2.25, 2.10]
# Explicit Viscosity at Boundaries (mPa·s / cP)
# Source: Extracted from Schumb (1955) viscosity-temperature-concentration charts
# visc_at_freezing_list = [1.79, 1.91, 2.15, 6.20, 15.50, 14.80, 22.10, 8.50, 2.85, 2.45, 2.15, 2.05] # <-- more accurate
# visc_at_boiling_list = [0.28, 0.29, 0.31, 0.35, 0.36, 0.37, 0.39, 0.41, 0.43, 0.45, 0.47, 0.48]

# Updated Freezing Point Data (Consistent with Schumb-MIT 1955)
# Reflects the exponential thickening at low-temp eutectics
visc_at_freezing_list = [1.79, 1.94, 2.35, 8.40, 38.50, 36.20, 65.00, 18.20, 4.10, 3.20, 2.10, 1.85]

# Updated Boiling Point Data (Consistent with T_boil for each concentration)
visc_at_boiling_list = [0.28, 0.28, 0.29, 0.31, 0.32, 0.32, 0.31, 0.30, 0.27, 0.26, 0.25, 0.25]


# Surface Tension at Boundaries (mN/m)
# Source: Derived from Schumb (1955) surface tension vs temperature correlations
surf_at_freezing_list = [75.6, 76.1, 77.2, 82.5, 86.2, 86.0, 88.5, 85.2, 83.5, 83.0, 83.1, 83.1]
surf_at_boiling_list  = [58.9, 59.1, 59.5, 60.1, 60.2, 60.8, 61.5, 62.1, 61.4, 61.5, 61.5, 61.6]




# Data Segments For Freezing points (from Gemini)
seg_a_c = [0, 3, 10, 35, 45.2]
seg_a_t = [0.00, -1.50, -5.50, -33.00, -52.70]

seg_b_c = [45.2, 50, 61.2]
seg_b_t = [-52.70, -52.20, -56.50]

seg_c_c = [61.2, 70, 85, 90, 98, 100]
seg_c_t = [-56.50, -40.30, -17.50, -11.50, -2.50, -0.43]

# In order to capture inflection points of freeze curve, must build large interpolator
# Create 3 independent interpolators
interp_a = Akima1DInterpolator(seg_a_c, seg_a_t)
interp_b = Akima1DInterpolator(seg_b_c, seg_b_t)
interp_c = Akima1DInterpolator(seg_c_c, seg_c_t)

def get_freezing_point_piecewise(c):
    if c < 45.2:
        return float(interp_a(c))
    elif c < 61.2:
        return float(interp_b(c))
    else:
        return float(interp_c(c))
big_concL      = []
big_freeze_ptL = []
for n in range(1001):
    big_concL.append( n/10.0 )
    big_freeze_ptL.append( get_freezing_point_piecewise( big_concL[-1] ) )


# Vapor Pressure at Freezing Point in psia
# Calculated via Clausius-Clapeyron/Antoine at the respective FP temperatures
vp_at_fp_psia = [
    0.08871,  # 0%   (Pure Water at 0°C)
    0.07765,  # 3%   (-1.5°C)
    0.05659,  # 10%  (-5.1°C)
    0.00703,  # 35%  (-33.0°C)
    0.00122,  # 50%  (-52.2°C) - The "Eutectic Dip"
    0.0015,  # 70%  (-40.3°C)
    0.007, #  0.0035,  # 85%  (-17.5°C)
    0.008, #  0.004,  # 90%  (-11.5°C)
    0.007, #  0.0051,  # 98%  (-2.5°C)
    0.00535   # 100% (-0.4°C)
]

# # Updated Vapor Pressure at Freezing Point (psia)
# # Consistent with Schumb-MIT 100% anchor and Raoult's Law blending
# vp_at_fp_psia = [
#     0.08860, # 0%   (0.0C)
#     0.07721, # 3%   (-1.5C)
#     0.05395, # 10%  (-5.5C)
#     0.00632, # 35%  (-33.0C)
#     0.00068, # 45.2% (-52.7C)
#     0.00078, # 50%  (-52.2C)
#     0.00054, # 61.2% (-56.5C)
#     0.00215, # 70%  (-40.3C)
#     0.00405, # 85%  (-17.5C)
#     0.00448, # 90%  (-11.5C)
#     0.00495, # 98%  (-2.5C)
#     0.00518  # 100% (-0.43C)
# ]

# Pvap_at_Tfreeze = perox_pvap_at_tfreeze_terp( pcent_H2O2 )
perox_pvap_at_tfreeze_terp = InterpProp( [0, 3, 10, 35, 50, 70, 85, 90, 98, 100], vp_at_fp_psia, extrapOK=True)

perox_visc_at_tfreeze_terp = InterpProp( conc_list_w_eutectics, visc_at_freezing_list, extrapOK=True)
perox_visc_at_tboil_terp   = InterpProp( conc_list_w_eutectics, visc_at_boiling_list, extrapOK=True)


# Surface Tension at Boundaries (mN/m)
# Source: Derived from Schumb (1955) surface tension vs temperature correlations
perox_surf_at_tfreeze_terp = InterpProp( conc_list_w_eutectics, surf_at_freezing_list, extrapOK=True)
perox_surf_at_tboil_terp   = InterpProp( conc_list_w_eutectics, surf_at_boiling_list, extrapOK=True)


# Density at Freezing Point (g/cm³)
density_fp_list = [ 1.001, 1.012, 1.041, 1.154, 1.205, 1.229, 1.288, 1.341, 1.398, 1.417, 1.449, 1.470] # SG

# Boiling Points / Critical Risk Points (°C)
boiling_pt_list = [ 100.0, 100.8, 102.5, 108.2, 111.8, 114.1, 120.2, 125.5, 137.4, 141.2, 148.5, 150.2]# degC

# Density at Boiling Point (g/cm³)
density_bp_list = [ 0.959, 0.969, 0.991, 1.070, 1.101, 1.119, 1.157, 1.187, 1.231, 1.245, 1.264, 1.276] # SG

# ================= Freezing and Boiling Interpolators ====================

#  Tfreeze =  perox_freeze_pt_degC_terp( pcent_H2O2 ) NOTE: built with large interpolator
#  (Uses "big_" lists to better capture sharp eutectic points)
perox_freeze_pt_degC_terp = InterpProp( big_concL, big_freeze_ptL, extrapOK=True)  #, terp_type="1D" )

#  Tnbp = perox_boil_pt_degC_terp( pcent_H2O2 )
perox_boil_pt_degC_terp = InterpProp( conc_list_w_eutectics, boiling_pt_list, extrapOK=True )


# SG at freezing point
perox_SG_at_freeze_pt_terp = InterpProp( conc_list_w_eutectics, density_fp_list, extrapOK=True)

# SG at boiling point
perox_SG_at_boil_pt_terp = InterpProp( conc_list_w_eutectics, density_bp_list, extrapOK=True)

# Cp at freezing point
perox_Cp_at_freeze_pt_terp = InterpProp( conc_list_w_eutectics, cp_at_freezing_list, extrapOK=True)


# ========== Make Pvap_Peroxide_Liquid class ==============

def edalat_p_sat(T, Tc, Pc, omega):
    r'''
    This code taken from thermo package: https://thermo.readthedocs.io/en/latest/index.html
    
    Calculates vapor pressure of a fluid at arbitrary temperatures using a
    CSP relationship by [1]_. Requires a chemical's critical temperature,
    pressure, and acentric factor. Claimed to have a higher accuracy than the
    Lee-Kesler CSP relationship.

    Parameters
    ----------
    T : float
        Absolute Temperature of fluid [K or R]
    Tc : float
        Absolute Critical temperature of fluid [K or R]
    Pc : float
        Critical pressure of fluid [Pa or psia]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Psat : float
        Vapor pressure, [Pa or psia] (same as Pc)

    found an average error of 6.06% on 94 compounds and 1106 data points.
    '''

    Tr = T / Tc
    tau = 1 - Tr
    
    # Your specialized H2O2/H2O tuned coefficients
    a = -6.1559 - 4.0855 * omega
    c = -0.8747 - 7.8874 * omega
    d = 1.0 / (-0.4893 - 0.9912 * omega + 3.1551 * omega**2)
    b = 1.5737 - 1.0540 * omega - 4.4365E-3 * d
    
    ln_pr = (a*tau + b*tau**1.5 + c*tau**3 + d*tau**6) / Tr
    return Pc * exp(ln_pr)

def find_omega(T_exp, P_exp, Tc, Pc):
    def objective(w):
        return edalat_p_sat(T_exp, Pc=Pc, Tc=Tc, omega=w) - P_exp
    
    # This should now bridge the zero beautifully
    return brentq(objective, 0.2, 0.7)


def r_to_c(r):
    return (r - 491.67) * 5/9

def set_ax2_degC(ax1):
    ax2 = ax1.twiny()
    
    #def T_to_Tr(T):
    #    return T / Tc
    #def Tr_to_T(Tr):
    #    return Tr * Tc
    #ax1.callbacks.connect("ylim_changed", T_to_Tr) 
    
    xlo, xhi = ax1.get_xlim()
    ax2.set_xlim( (r_to_c(xlo), r_to_c(xhi)) )
        
    ax2.set_xlabel('Temperature (degC)')
    ax2.xaxis.set_label_coords(0.5,0.95)

def terp_transition(tL, terp1, terp2, Ttransition=None, Tc2=1.0,
                    TfinalTransition=None):
    """Transition from interpolator #1 to #2 smoothly"""
    # if Ttransition is None, use midpoint of terp1
    if Ttransition is None:
        Ttransition = (terp1.x[0] + terp1.x[-1]) / 2.0
    
    if TfinalTransition is None:
        TfinalTransition = terp1.x[-1]
    
    vL = []
    for t in tL:
        if t <= Ttransition:
            val = terp1(t)
        elif t >= TfinalTransition:
            val = terp2( t/Tc2 )
        else:
            wt2 = (t - Ttransition) / (TfinalTransition - Ttransition)
            wt1 = 1.0 - wt2
            val = wt1*terp1(t) + wt2*terp2(t/Tc2)
        vL.append( val )
    return vL


# ............ plot the curves ..............
if __name__ == "__main__":

    # perox_boil_pt_degC_terp.plot( Npts=100, do_show=False, title='Peroxide Tnbp',  show_deriv=False,
    #                              xlabel='pcent_H2O2', ylabel='Tnbp (degC)' )

    # perox_SG_at_freeze_pt_terp.plot( title='Peroxide SG at Tfreeze', do_show=False, show_deriv=False,
    #                                  xlabel='pcent_H2O2', ylabel='Density (SG)' )

    # perox_SG_at_boil_pt_terp.plot( title='Peroxide SG at Tnbp', do_show=False, show_deriv=False,
    #                                  xlabel='pcent_H2O2', ylabel='Density (SG)' )

    # perox_Tcrit_degC_terp.plot( title='Peroxide Critical Temperature', do_show=False, show_deriv=False,
    #                                  xlabel='pcent_H2O2', ylabel='Tcritical (degC)' )

    # perox_Pcrit_psia_terp.plot( title='Peroxide Critical Pressure', do_show=False, show_deriv=False,
    #                                  xlabel='pcent_H2O2', ylabel='Pcritical (psia)' )

    # perox_Dcrit_SG_terp.plot( title='Peroxide Critical Density', do_show=True, show_deriv=False,
    #                                  xlabel='pcent_H2O2', ylabel='Dcritical (SG)' )

    if 0:
        perox_max_storage_degC_terp.plot( title='Peroxide Max Storage Temperature', do_show=False, show_deriv=False,
                                        xlabel='pcent_H2O2', ylabel='Max Storage Temperature (degC)' )
        
        perox_freeze_pt_degC_terp.plot( Npts=1000, do_show=False, title='Peroxide Tfreeze',  show_deriv=False,
                                    xlabel='pcent_H2O2', ylabel='Tfreeze (degC)', new_fig=False )

        perox_critical_risk_degC_terp.plot( title='Peroxide Critical Risk Temperature', do_show=True, show_deriv=False,
                                        xlabel='pcent_H2O2', ylabel='Critical Risk Temperature (degC)', new_fig=False )


    # --- Testing ---
    test_concs = [2, 8, 42, 78, 93, 99, 99.5]
    for tc in test_concs:
        print(f"Conc {tc:>4}% | Note: {perox_get_danger_note(tc)}")

    # perox_pvap_at_tfreeze_terp.plot(title='Peroxide Pvap at Tfreeze', do_show=True, show_deriv=True,
    #                                  xlabel='pcent_H2O2', ylabel='Pvap (psia)' )
        