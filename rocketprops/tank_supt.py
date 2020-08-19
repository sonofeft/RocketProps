from rocketprops.unit_conv_data import get_value

def calc_tank_volume( pObj, kg_expelled=50.0,
                      TmaxC=50.0, expPcent=98.0, ullPcent=3.0):
    """
    Calculate the volume of a propellant tank given operating requirements.
    
    :param pObj: propellant object
    :param kg_expelled: mass of expelled propellant in kg
    :param TmaxC: max operating/storage/transport temperature in deg C
    :param expPcent: expulsion efficiency in percent
    :param ullPcent: percent of total tank volume that is ullage at TmaxC
    :type pObj: Propellant
    :type kg_expelled: float
    :type TmaxC: float
    :type expPcent: float
    :type ullPcent: float
    :return: (volume of tank (ml), loaded propellant mass (kg), residual propellant mass (kg))
    :rtype: (float, float, float)
    """

    # put temperature units into degR
    Thot  = get_value( TmaxC, 'degC', 'degR' )
    
    SGhot = pObj.SGLiqAtTdegR( Thot )
    cc_expelled = kg_expelled * 1000.0 / SGhot

    # residual and ullage fractions apply to entire tank volume, not just propellant volume
    expulsionEff = expPcent / 100.0 
    residualFraction = 1.0 - expulsionEff
    ullageFraction = ullPcent / 100.0

    cc_Total = cc_expelled / (1.0 - residualFraction - ullageFraction)
    kg_loaded = cc_Total * (1.0 - ullageFraction) * SGhot / 1000.0
    kg_residual = kg_loaded - kg_expelled

    return cc_Total, kg_loaded, kg_residual

if __name__ == "__main__":
    from rocketprops.rocket_prop import get_prop
    """
    Calculate the required volume of a Hydrazine (N2H4) tank.
    Assume:
        required usable propellant is 50 kg
        vehicle max operating/storage/transport temperature is 50 deg C.
        minimum ullage volume is 3%.
        expulsion efficiency = 98%.
    """
    pObj = get_prop('hydrazine')
    
    cc_Total, kg_loaded, kg_residual = calc_tank_volume( pObj, kg_expelled=50.0,
                                                         TmaxC=50.0, expPcent=98.0, ullPcent=3.0 )

    print('cc_Total    = %g cc'%cc_Total)
    print('loaded   propellant mass = %g kg'%kg_loaded )
    print('residual propellant mass = %g kg'%kg_residual )
    print('loaded / expelled mass =', kg_loaded / 50.0)

    Thot  = get_value( 50.0, 'degC', 'degR' )
    SGhot = pObj.SGLiqAtTdegR( Thot )
    
    print('kg residual = SGhot * 0.02 * cc_Total / 1000 =', SGhot * 0.02 * cc_Total / 1000, 'kg'  )

    cc_expelled = 50.0 * 1000.0 / SGhot
    print('cc_expelled =',cc_expelled, '  mass expelled = %g g'%(SGhot*cc_expelled,) )
    print('cc_expelled / cc_Total =', cc_expelled / cc_Total)
    
