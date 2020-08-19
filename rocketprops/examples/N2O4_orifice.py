from rocketprops.rocket_prop import get_prop
from rocketprops.injector_supt import calc_inj_velocity, calc_orifice_flow_rate

"""
Calculate the injection velocity of an injector orifice and its mass flow rate
"""
pObj = get_prop( 'N2O4' )
ft_per_sec = calc_inj_velocity( pObj, dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)
print( 'velocity =',ft_per_sec, 'ft/s' )

wdot = calc_orifice_flow_rate(pObj, CdOrf=0.75, DiamInches=0.01,
                       dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)
print( 'Orifice flow rate =',wdot , 'lbm/sec' )


