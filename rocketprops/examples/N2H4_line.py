from rocketprops.line_supt import calc_line_id_dp, calc_line_vel_dp
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
