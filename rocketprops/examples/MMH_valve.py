from rocketprops.rocket_prop import get_prop
from rocketprops.valve_supt import cv_valve_dp, kv_valve_dp

"""
Calculate the pressure drop across an MMH valve with given mass flow rate
"""
pObj = get_prop( 'MMH' )

# Imperial valve flow coefficient, Cv
dp = cv_valve_dp( pObj, Cv=1.0, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
print('Cv = 1.0           deltaP = %g psid'%dp)

# Metric valve flow coefficient, Kv
Kv = 1.0 / 1.1560992283526375  # Conversion factor for Cv to Kv
dp = kv_valve_dp( pObj, Kv=Kv, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
print('Kv = 1.0/convFact  deltaP = %g psid'%dp)

