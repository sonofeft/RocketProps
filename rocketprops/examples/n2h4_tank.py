from rocketprops.tank_supt import calc_tank_volume
from rocketprops.rocket_prop import get_prop
"""
Calculate the required volume of a Hydrazine (N2H4) tank.
Assume:
    required usable propellant is 50 kg
    vehicle max operating/storage/transport temperature is 50 deg C.
    minimum ullage volume is 3%.
    expulsion efficiency = 98%.
"""
pObj = get_prop('N2H4')

cc_Total, kg_loaded, kg_residual = calc_tank_volume( pObj, kg_expelled=50.0,
                                                     TmaxC=50.0, expPcent=98.0, ullPcent=3.0 )
print('cc_Total    = %g cc'%cc_Total)
print('loaded   propellant mass = %g kg'%kg_loaded )
print('residual propellant mass =  %g kg'%kg_residual )

