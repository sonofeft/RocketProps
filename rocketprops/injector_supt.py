from math import sqrt, pi
from rocketprops.unit_conv_data import get_value

def calc_inj_velocity( pObj, dPpsia=50.0, TdegR=530.0, Ppsia=1000.0):
    """
    Calculate the injection velocity of a propellant.

    :param pObj: propellant object
    :param dPpsia: pressure drop across orifice, psid
    :param TdegR: temperature of propellant, degR
    :param Ppsia: inlet pressure to orifice, psia
    :type pObj: Propellant
    :type dPpsia: float
    :type TdegR: float
    :type Ppsia: float
    :return: injection velocity, ft/sec
    :rtype: float
    """

    Pave = Ppsia - dPpsia/2.0
    SGave = pObj.SG_compressed( TdegR, Pave )
    
    rho = get_value( SGave, 'SG', 'lbm/in**3' )
    
    in_per_sec = sqrt( 24.0 * 32.174 * dPpsia / rho ) # in/sec
    ft_per_sec = in_per_sec / 12.0
    
    return ft_per_sec

def calc_orifice_flow_rate(pObj, CdOrf=0.75, DiamInches=0.01,
                           dPpsia=50.0, TdegR=530.0, Ppsia=1000.0):
    """        
    Calculate mass flow rate through a single injector orifice.

    :param pObj: propellant object
    :param CdOrf: discharge coefficient of orifice
    :param DiamInches: diameter of orifice, inch
    :param dPpsia: pressure drop across orifice, psid
    :param TdegR: temperature of propellant, degR
    :param Ppsia: inlet pressure to orifice, psia
    :type pObj: Propellant
    :type CdOrf: float
    :type DiamInches: float
    :type dPpsia: float
    :type TdegR: float
    :type Ppsia: float
    :return: mass flow rate of single orifice, lbm/sec
    :rtype: float
    """

    Pave = Ppsia - dPpsia/2.0
    SGave = pObj.SG_compressed( TdegR, Pave )
    
    rho = get_value( SGave, 'SG', 'lbm/in**3' )
    
    in_per_sec = sqrt( 24.0 * 32.174 * dPpsia / rho ) # in/sec
    
    wdotOrif = in_per_sec * rho * CdOrf * DiamInches**2 * pi / 4.0
    
    return wdotOrif # lbm/sec
    
if __name__ == "__main__":
    from rocketprops.rocket_prop import get_prop

    print("""
    ...Calculate the propellant injection velocity...""")
    pObj = get_prop('N2O4')
    TdegR=530.0
    Ppsia=1000.0
    dPpsia=50.0
    ft_per_sec = calc_inj_velocity( pObj, dPpsia=dPpsia, TdegR=TdegR, Ppsia=Ppsia)
    print( 'ft_per_sec =',ft_per_sec, '=', get_value(ft_per_sec, 'ft/s', 'm/s'), 'm/s' )
    
    # check calc in metric
    Pave = Ppsia - dPpsia/2.0
    SGave = pObj.SG_compressed( TdegR, Pave )
    gh_m = get_value(dPpsia,'psia','N/m**2') / get_value(SGave,'SG','kg/m**3') 
    m_per_sec = sqrt( 2 * gh_m )
    print('     gh_m=%g'%gh_m, '   m_per_sec =', m_per_sec,'m/s')
    
    print("""
    ...Calculate the propellant orifice mass flow rate...""")
    
    wdot = calc_orifice_flow_rate(pObj, CdOrf=0.75, DiamInches=0.01,
                           dPpsia=dPpsia, TdegR=TdegR, Ppsia=Ppsia)
    print( 'Orifice flow rate = %g lbm/sec'%wdot )
