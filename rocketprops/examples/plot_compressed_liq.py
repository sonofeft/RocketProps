import matplotlib.pyplot as plt
from rocketprops.rocket_prop import get_prop
from engcoolprop.ec_fluid import EC_Fluid
from rocketprops.unit_conv_data import get_value

name = 'Oxygen'
name = 'Propane'
#name = 'Methane'
#name = 'Methanol'
#name = 'Ethanol'
#name = 'Ammonia'
ec = EC_Fluid(name)
p = get_prop(name)

Tmin, Tmax = p.T_data_range()
Tmin += 5
Tmax = min( Tmax, ec.Tc ) - 5.0
print( 'p.Tc=%g,  ec.Tc=%g'%(p.Tc,  ec.Tc) )

fig = plt.figure()
COLORL = ['g','c','b','orange','m','r']
i = 0

errLL = []
plt.title( p.pname )
for P in [100, 200, 500, 1000, 2000]:
    tL = []
    sg_rpL = []
    sg_ecL = []
    errL = []
    terrL = []
    
    Tcutoff = p.TdegRAtPsat(P)
    
    for T in range( int(Tmin), int(Tmax), 1 ):
        if T < Tcutoff:
            
            #sg_rp = p.SG_compressedCOSTALD( T, P)
            #sg_rp = p.SG_compressed( T, P)
            #sg_rp = p.SG_compressedCZ2( T, P )
            sg_rp = p.SG_compressedNasrfar(T, P)
            
            ec.setTP( T=T, P=P )
            sg_ec = get_value( ec.rho, 'lbm/in**3', 'SG' )
            
            if sg_rp is not None and sg_ec is not None:
                sg_rpL.append( sg_rp )
                sg_ecL.append( sg_ec )
                tL.append( T / p.Tc )
                terrL.append( T / p.Tc )
                errL.append( 100.0*(sg_rp - sg_ec)/ sg_ec  )
        
    plt.plot( tL, sg_rpL, '-', label='RocketProps P=%g'%P, color=COLORL[i%len(COLORL)])
    plt.plot( tL, sg_ecL, '--', label='CoolProp P=%g'%P, color=COLORL[i%len(COLORL)])
    i += 1
    errLL.append( (terrL, errL, P) )

plt.legend()
plt.grid()

# ============== error plot ============
fig = plt.figure()
i = 0
plt.title( p.pname )

for tL, errL, P in errLL:
    plt.plot( tL, errL, '-', label='Error at P=%g'%P, color=COLORL[i%len(COLORL)])
    i += 1
plt.legend()
plt.grid()
    

plt.show()
        
    
