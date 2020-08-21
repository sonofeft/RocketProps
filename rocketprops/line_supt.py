from math import sqrt, pi
from rocketprops.unit_conv_data import get_value
from rocketprops.colebrook import colebrook_ffact

def calc_line_id_dp( pObj, TdegR=530.0, Ppsia=1000.0,
                     wdotPPS=0.5, velFPS=13.0, 
                     roughness=5.0E-6,  Kfactors=2.0, len_inches=50.0):
    """
    Calculate the inner diameter and pressure drop in propellant line.

    :param pObj: propellant object
    :param TdegR: temperature of propellant, degR
    :param Ppsia: inlet pressure to orifice, psia
    :param wdotPPS: mass flow rate in line, lbm/sec
    :param velFPS: velocity of liquid in line, ft/sec
    :param roughness: line roughness, inches
    :param Kfactors: number of velocity heads lost due to bends, valves, etc.
    :param len_inches: length of line, inches
    :type pObj: Propellant
    :type TdegR: float
    :type Ppsia: float
    :type wdotPPS: float
    :type velFPS: float
    :type roughness: float
    :type Kfactors: float
    :type len_inches: float
    :return: tuple of inside diameter and pressure drop (dinsid, deltaP), (inch, psid)
    :rtype: (float, float)
    """

    SG = pObj.SG_compressed( TdegR, Ppsia )
    rho = get_value( SG, 'SG', 'lbm/in**3' )
    Dens = get_value( SG, 'SG', 'lbm/ft**3' )
    
    Q = wdotPPS / rho
    Ac = Q / (velFPS * 12.0)
    
    rinsid = sqrt( Ac / pi )
    dinsid = rinsid * 2.0

    # calculate pressure drop
    visc = pObj.Visc_compressed(TdegR, Ppsia)
    mu = get_value( visc, 'poise', 'lbm/s/ft')
    ReNum= 144.0 * rho * velFPS * dinsid / mu
    
    ff = colebrook_ffact(roughness, dinsid, ReNum)

    deltaP = (ff * len_inches/dinsid + Kfactors) * wdotPPS**2 / (dinsid**4 * 0.27622 * Dens)

    return dinsid, deltaP
    

def calc_line_vel_dp( pObj, TdegR=530.0, Ppsia=1000.0,
                     wdotPPS=0.5, IDinches=0.335, 
                     roughness=5.0E-6,  Kfactors=2.0, len_inches=50.0):
    """
    Calculate the line velocity and pressure drop in propellant line.

    :param pObj: propellant object
    :param TdegR: temperature of propellant, degR
    :param Ppsia: inlet pressure to orifice, psia
    :param wdotPPS: mass flow rate in line, lbm/sec
    :param IDinches: inside diameter of line, in
    :param roughness: line roughness, inches
    :param Kfactors: number of velocity heads lost due to bends, valves, etc.
    :param len_inches: length of line, inches
    :type pObj: Propellant
    :type TdegR: float
    :type Ppsia: float
    :type wdotPPS: float
    :type velFPS: float
    :type roughness: float
    :type Kfactors: float
    :type len_inches: float
    :return: tuple of velocity and pressure drop (velFPS, deltaP), (ft/s, psid)
    :rtype: (float, float)
    """

    SG = pObj.SG_compressed( TdegR, Ppsia )
    rho = get_value( SG, 'SG', 'lbm/in**3' )
    Dens = get_value( SG, 'SG', 'lbm/ft**3' )
    
    Q = wdotPPS / rho            # in**3/s
    Ac = pi * IDinches**2 / 4.0  # in**2
    velFPS = Q / (Ac * 12.0)     # ft/sec

    # calculate pressure drop
    visc = pObj.Visc_compressed(TdegR, Ppsia)   # poise
    mu = get_value( visc, 'poise', 'lbm/s/ft')  # lbm/s-ft
    ReNum= 144.0 * rho * velFPS * IDinches / mu
    
    ff = colebrook_ffact(roughness, IDinches, ReNum)

    deltaP = (ff * len_inches/IDinches + Kfactors) * wdotPPS**2 / (IDinches**4 * 0.27622 * Dens)

    return velFPS, deltaP
    
    
if __name__ == "__main__":
    from rocketprops.rocket_prop import get_prop
    pObj = get_prop('hydrazine')

    ID, deltaP = calc_line_id_dp( pObj, TdegR=530.0, Ppsia=240.0,
                                  wdotPPS=0.5, velFPS=13, 
                                  roughness=5.0E-6,  Kfactors=5.0, len_inches=50.0)
    print( 'Inside Diam=%g inches, Pressure Drop =%g psid'%(ID, deltaP) )
    
    vel, dp = calc_line_vel_dp( pObj, TdegR=530.0, Ppsia=240.0,
                     wdotPPS=0.5, IDinches=ID, 
                     roughness=5.0E-6,  Kfactors=5.0, len_inches=50.0)
    print( 'Velocity = %g ft/sec, Pressure Drop =%g psid'%(vel, deltaP) )
    
    
    