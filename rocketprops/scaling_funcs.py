from numpy import exp, log, log10
from scipy import optimize
from rocketprops.unit_conv_data import get_value

R = 8.3144598 # J/mol-K

def ambrose_Psat( T, Tc, Pc, omega ):
    """
    Use Ambrose/Walton correlation to calc Psat at T.
    :param T  : temperature (same units as Tc)
    :param Tc : critical temperature (same units as T)
    :param Pc : critical pressure (psia OR desired output units)
    :param omega : Pitzer acentric factor
    :type T  : float
    :type Tc : float
    :type Pc : float
    :type omega: float
    :return: Saturation Pressure
    :rtype: float
    """
    Tr = T / Tc
    tau = 1.0 - Tr
    
    f0 = (-5.97616*tau + 1.29874*tau**1.5 - 0.60394*tau**2.5 - 1.06841*tau**5)/Tr
    f1 = (-5.03365*tau + 1.11505*tau**1.5 - 5.41217*tau**2.5 - 7.46628*tau**5)/Tr
    f2 = (-0.64771*tau + 2.41539*tau**1.5 - 4.26979*tau**2.5 + 3.25259*tau**5)/Tr
    
    ln_Pvr = f0 + omega*f1 + omega**2*f2
    
    return Pc * exp( ln_Pvr )

def solve_omega( Tc, Pc, P07, Tr=0.7 ):
    """
    Given Tc and Pc, solve for omega
    omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
    Assume that P07 is the pressure at reduced temperature=0.7 
    UNLESS, a different value of Tr is input
    """
    
    T07 = Tr * Tc
    #print('Solving Tc=%s, Pc=%s, P07=%s'%(Tc, Pc, P07) )
    
    def func( omega ):
        return P07 - ambrose_Psat( T07, Tc, Pc, omega )
    
    sol = optimize.root_scalar(func, bracket=[-5, 5.0], method='brentq')
    #print( 'sol.root=',sol.root )
    return sol.root



def Rowlinson_Poling_Cp(T, Tc, omega, Cpgm, MW):
    r'''    
    This code taken from thermo package: https://thermo.readthedocs.io/
    
    Calculate liquid constant-pressure heat capacity
    ==> This equation is not terribly accurate.

    Parameters
    ----------
    T : float
        Temperature of fluid [K] <-- input degR
    Tc : float
        Critical temperature of fluid [K] <-- input degR
    omega : float
        Acentric factor for fluid, [-]
    Cpgm : float
        Constant-pressure gas heat capacity, [J/mol/K]
    MW : float
        Molecular Weight [g/mol]

    Returns
    -------
    Cplm : float
        Liquid constant-pressure heat capacity, [J/mol/K] --> BTU/lbm/delF
    '''
    T = get_value(T, 'degR', 'degK')
    Tc = get_value(Tc, 'degR', 'degK')
    R = 8.3144598
    
    Tr = T/Tc
    denom = max(0.001, 1.0-Tr) # modification by CET for Tr >= 1.0
    #print('In Rowlinson_Poling(T=%s, Tc=%s, omega=%s, Cpgm=%s, MW=%s)'%(T, Tc, omega, Cpgm, MW))
    
    Cplm = Cpgm + R*(1.586 + 0.49/denom + omega*(4.2775
    + 6.3*(1-Tr)**(1/3.)/Tr + 0.4355/denom))
    
    # convert J/mol/K to BTU/lbm/delF
    return Cplm / ( 1.8 * MW * 1055.06 )

        
def Pitzer_Hvap(T, Tc, MW, omega):
    r'''
    This code taken from thermo package: https://thermo.readthedocs.io/
    
    Calculates enthalpy of vaporization at arbitrary temperatures using a
    fit by [2]_ to the work of Pitzer [1]_; requires a chemical's critical
    temperature and acentric factor.

    Parameters
    ----------
    T : float
        Temperature of fluid [K] <-- input degR converted to degK
    Tc : float
        Critical temperature of fluid [K] <-- input degR converted to degK
    MW : float
         Molecular Weight [g/gmole]
    omega : float
        Acentric factor [-]

    Returns
    -------
    Hvap : float
        Enthalpy of vaporization, [J/mol] --> BTU/lbm

    Notes
    -----
    The recommended range is 0.6 to 1 Tr. Users should expect up to 5% error.
    T must be under Tc, or an exception is raised.
    '''
    T = get_value(T, 'degR', 'degK')
    Tc = get_value(Tc, 'degR', 'degK')
    R = 8.3144598
    
    Tr = T/Tc
    hvap_JperM = R*Tc * (7.08*(1. - Tr)**0.354 + 10.95*omega*(1. - Tr)**0.456)
    
    return hvap_JperM * 0.429923 / MW # BTU/lbm


def Edalat_Pvap(T, Tc, Pc, omega):
    r'''
    This code taken from thermo package: https://thermo.readthedocs.io/
    
    Calculates vapor pressure of a fluid at arbitrary temperatures using a
    CSP relationship by [1]_. Requires a chemical's critical temperature,
    pressure, and acentric factor. Claimed to have a higher accuracy than the
    Lee-Kesler CSP relationship.

    Parameters
    ----------
    T : float
        Temperature of fluid [K] <-- input degR converted to degK
    Tc : float
        Critical temperature of fluid [K] <-- input degR converted to degK
    Pc : float
        Critical pressure of fluid [Pa] <-- input psia converted to Pa
    omega : float
        Acentric factor [-]

    Returns
    -------
    Psat : float
        Vapor pressure, [Pa] --> psia

    found an average error of 6.06% on 94 compounds and 1106 data points.
    '''
    T = get_value(T, 'degR', 'degK')
    Tc = get_value(Tc, 'degR', 'degK')
    Pc = get_value(Pc, 'psia', 'Pa')
    tau = 1. - T/Tc
    a = -6.1559 - 4.0855*omega
    c = -0.8747 - 7.8874*omega
    d = 1./(-0.4893 - 0.9912*omega + 3.1551*omega**2)
    b = 1.5737 - 1.0540*omega - 4.4365E-3*d
    lnPr = (a*tau + b*tau**1.5 + c*tau**3 + d*tau**6)/(1.-tau)
    #print('exp( lnPr ) =',exp( lnPr ))
    Psat_Pa = exp( lnPr ) * Pc

    return get_value(Psat_Pa, 'Pa', 'psia')


def Rackett_SG( TdegR, Tc, SGc, omega ):
    """Rackett eqn 4-11.3 in 5th Ed. of Gases and Liquids."""
        
    Vc    = 1.0 / SGc  # ml/gmole
    
    n = ( 1.0 - TdegR/Tc )**(2./7.)
    V = Vc * (0.29056 - 0.08775*omega)**n
    sg_calc  = 1.0 / V
    
    return sg_calc
    
def ScaledRackett_SG( TdegR, Tc, omega, Tref, SGref ):
    """Rackett eqn 4-11.3 in 5th Ed. of Gases and Liquids."""
    
    Vref  = 1.0 / SGref# ml/gmole
    
    n = ( 1.0 - TdegR/Tc )**(2./7.)  -  ( 1.0 - Tref/Tc )**(2./7.)
    V = Vref * (0.29056 - 0.08775*omega)**n
    sg_calc  = 1.0 / V
    
    return sg_calc

        
def Pitzer_surften(T, Tc, Pc, omega):
    r'''
    This code taken from thermo package: https://thermo.readthedocs.io/
    
    Calculates air-water surface tension
    Parameters
    ----------
    T : float
        Temperature of fluid  <-- degR
    Tc : float
        Critical temperature of fluid  <-- degR
    Pc : float
        Critical pressure of fluid  <-- psia
    omega : float
        Acentric factor for fluid, [-]

    Returns
    -------
    sigma : float
        Liquid surface tension, N/m --> lbf/in

    Notes
    -----
    The source of this equation has not been reviewed.
    Internal units of pressure are bar, surface tension of mN/m.
    '''
    T = get_value(T, 'degR', 'degK')
    Tc = get_value(Tc, 'degR', 'degK')
    Pc = get_value(Pc, 'psia', 'bar')
    
    Tr = T/Tc
    
    #R23 = 8.3145**(2./3.) # 
    R23 = 83.145**(2./3.) # = 19.05
    
    term1 = Pc**(2./3.) * Tc**(1./3.)
    term2 = (1.86 + 1.18*omega) / R23  # 19.05
    term3 = ( (3.75 + 0.91*omega) / (0.291 - 0.08*omega) )**(2./3.)
    term4 = ( 1.0 - Tr )**(11./9.)
    sigma = term1 * term2 * term3 * term4 # dny/cm
    
    return get_value(sigma, "dyne/cm", 'lbf/in')


def Nicola_thcond(T, M, Tc, Pc, omega):
    r'''
    This code taken from thermo package: https://thermo.readthedocs.io/
    
    Estimates the thermal conductivity of a liquid as a function of
    temperature using the CSP method of [1]_. A statistically derived
    equation using any correlated terms.

    Requires temperature, molecular weight, critical temperature and pressure,
    and acentric factor.

    Parameters
    ----------
    T : float
        Temperature of the fluid [K] <-- input degR converted to degK
    M : float
        Molecular weight of the fluid [g/mol]
    Tc : float
        Critical temperature of the fluid [K] <-- input degR converted to degK
    Pc : float
        Critical pressure of the fluid [Pa] <-- input psia converted to Pa
    omega : float
        Acentric factor of the fluid [-]

    Returns
    -------
    kl : float
        Estimated liquid thermal conductivity [W/m/k] --> BTU/hr/ft/delF
        --> W/m/k converted to BTU/hr/ft/delF for output

    Notes
    -----
    A statistical correlation. A revision of an original correlation.
    '''
    
    T = get_value(T, 'degR', 'degK')
    Tc = get_value(Tc, 'degR', 'degK')
    Pc = get_value(Pc, 'psia', 'Pa')    
    #print('In Nicola: T=%s, M=%s, Tc=%s, Pc=%s, omega=%s'%(T, M, Tc, Pc, omega))
    
    Tr = T/Tc
    Pc = Pc/1E5
    thcond_Wmk = 0.5147*(-0.2537*Tr + 0.0017*Pc + 0.1501*omega + (1./M)**0.2999)
    
    return get_value(thcond_Wmk, 'W/m/K', 'BTU/hr/ft/delF')
    

def Squires_visc( TdegR, Tref, PoiseRef ):
    """
    Squires Figure 9-13,  equation 9-10.3 in 5th Ed. of Gases and Liquids.
    """
    T_K = get_value(TdegR, 'degR', 'degK')
    Tref_K = get_value(Tref, 'degR', 'degK')
    cp_ref = PoiseRef * 100.0
    
    vtopow = cp_ref**-0.2661 + (T_K - Tref_K) / 233.0
    
    cp = vtopow ** (-1.0/.2661)
    return cp / 100.0
