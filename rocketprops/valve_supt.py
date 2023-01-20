from math import sqrt, pi
from rocketprops.unit_conv_data import get_value
from rocketprops.colebrook import colebrook_ffact

def calib_valve_dp( pObj, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0,
                   refWaterWdot=0.214, refWaterDP=30.0):
    """
    Calculate valve pressure drop for a valve that has been calibrated
    with a water flow test.

    :param pObj: propellant object
    :param wdotPPS: propellant mass flow rate in line, lbm/sec
    :param TdegR: propellant temperature of propellant, degR
    :param Ppsia: propellant inlet pressure to valve, psia
    :param refWaterWdot: reference water flow rate, lbm/sec
    :param refWaterDP: reference water pressure drop, psid
    :type pObj: Propellant
    :type wdotPPS: float
    :type TdegR: float
    :type Ppsia: float
    :type refWaterWdot: float
    :type refWaterDP: float
    :return: propellant pressure drop , psid
    :rtype: float
    """

    SG = pObj.SG_compressed( TdegR, Ppsia )
    Dens = get_value( SG, 'SG', 'lbm/ft**3' )
    
    Kw = sqrt( refWaterWdot**2 / refWaterDP )
    
    # calculate pressure drop
    deltaP = wdotPPS**2 * 62.4 / Dens / Kw**2

    return deltaP

def cv_valve_dp( pObj, Cv=1.0, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0):
    """
    Calculate valve pressure drop for a valve with a known imperial flow coefficient, Cv.
    
    Imperial flow coefficient (Cv) is the amount of water (in gallons per minute) at 60 degF 
    that will flow through a fully open valve with a difference of 1 psi between 
    the inlet and the outlet.
    
    :param pObj: propellant object
    :param Cv: valve flow coefficient
    :param wdotPPS: propellant mass flow rate in line, lbm/sec
    :param TdegR: propellant temperature of propellant, degR
    :param Ppsia: propellant inlet pressure to valve, psia
    :type pObj: Propellant
    :type Cv: float
    :type wdotPPS: float
    :type TdegR: float
    :type Ppsia: float
    :return: propellant pressure drop , psid
    :rtype: float    
    """
    SG = pObj.SG_compressed( TdegR, Ppsia )
    rho = get_value( SG, 'SG', 'lbm/in**3' )
    
    Qgpm = get_value( wdotPPS / rho, 'inch**3/s', 'gpm')
    
    deltaP = SG * (Qgpm/Cv)**2
    #print('Qgpm=%g'%Qgpm, '  SG=%g'%SG, '  deltaP=%g'%deltaP, '   Cv=%g'%Cv)
    return deltaP

def kv_valve_dp( pObj, Kv=1.0, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0):
    """
    Calculate valve pressure drop for a valve with a known metric flow coefficient, Kv.
    
    Metric flow coefficient (Kv) is the amount of water (in m**3/hr) at 4 degC
    that will flow through a fully open valve with a difference of 1 bar between 
    the inlet and the outlet.
    
    :param pObj: propellant object
    :param Kv: valve flow coefficient
    :param wdotPPS: propellant mass flow rate in line, lbm/sec
    :param TdegR: propellant temperature of propellant, degR
    :param Ppsia: propellant inlet pressure to valve, psia
    :type pObj: Propellant
    :type Kv: float
    :type wdotPPS: float
    :type TdegR: float
    :type Ppsia: float
    :return: propellant pressure drop , psid
    :rtype: float    
    """
    # Note, could have converted Kv into Cv
    #Cv = 1.1560992283526375 * Kv
    #return cv_valve_dp( pObj, Cv=Cv, wdotPPS=wdotPPS, TdegR=TdegR, Ppsia=Ppsia)
    
    SG = pObj.SG_compressed( TdegR, Ppsia )
    rho = get_value( SG, 'SG', 'lbm/in**3' )
    
    Qm3h = get_value( wdotPPS / rho, 'inch**3/s', 'm**3/hr')
    
    dPbar = SG * (Qm3h/Kv)**2
    deltaP = get_value( dPbar, 'bar', 'psid' )
    #print('Qm3h=%g'%Qm3h, '  SG=%g'%SG, '  dPbar=%g'%dPbar, '   Kv=%g'%Kv, '  deltaP=%g'%deltaP)
    return deltaP
    
    
if __name__ == "__main__":
    import sys 
    from rocketprops.rocket_prop import get_prop
    pObj = get_prop('hydrazine')
    
    print('MOOG Latch valve Model 52-266')
    dP = calib_valve_dp( pObj, wdotPPS=0.2, TdegR=530.0, Ppsia=243.0,
                   refWaterWdot=0.3, refWaterDP=9.0)
    print('pressure drop = %.2f psid'%dP)
    
    print()
    dp =cv_valve_dp( pObj, Cv=1.0, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
    print('Cv deltaP =',dp)
    
    print()
    dp =kv_valve_dp( pObj, Kv=1.0/1.1560992283526375, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
    print('Kv deltaP =',dp)
    
    if 0:
        # calculate all the digits to convert from Kv to Cv
        cvmin = 1.1
        cvmax = 1.2
        for _ in range(200):
            cvconst = (cvmin+cvmax)/2.0
            Kv = 1.0 / cvconst
            dp =kv_valve_dp( pObj, Kv=Kv, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
            if dp < 12.783670167132671:
                cvmin = cvconst
            else:
                cvmax = cvconst
        print( 'Cv =', cvconst,' * Kv ' )
    
