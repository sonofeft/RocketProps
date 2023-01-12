from rocketprops.scaling_funcs import ambrose_Psat, solve_omega
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
from rocketprops.rocket_prop import get_prop as get_rocket_prop

pObj = get_rocket_prop( 'ethane', suppress_warning=True )
print('Testing: solve_omega( Tc, Pc )')
P07 = pObj.PvapAtTr( 0.7 )
omega_calc = solve_omega( pObj.Tc, pObj.Pc, P07, 0.7*pObj.Tc )

print('for %s omega_calc=%g,   omega=%g'%(pObj.name, omega_calc, pObj.omega))
print()

fig = plt.figure( figsize=(8,8) )
TrLo, TrHi = pObj.Tr_data_range()
Tlo, Thi = pObj.Tc*TrLo, pObj.Tc*TrHi

dt = (Thi - Tlo) / 100.0

# some Pvap curves have an issue
corrfact = pObj.Pc/pObj.PvapAtTr(1.0)

tL = [Tlo + i*dt for i in range(71)] # only make 70% of RocketProp range
prL = [corrfact*pObj.PvapAtTr(t/pObj.Tc) for t in tL]
print('Tlo =%g, Thi =%g'%(Tlo, Thi))
print('Tplo=%g, Tphi=%g'%(tL[0], tL[-1]))

plt.semilogy( tL, prL, '-', label=pObj.name, linewidth=5 )

pr_calcL = [ambrose_Psat( t, pObj.Tc, pObj.Pc, pObj.omega ) for t in tL]
plt.semilogy( tL, prL, '-', label='Ambrose' )

if tL[-1] < pObj.Tc * 0.99:
    Trmid = tL[-1]/pObj.Tc
    t_extL = [pObj.Tc*(Trmid + i*(1-Trmid)/50.) for i in range(51)]
    pr_calcL = [ambrose_Psat( t, pObj.Tc, pObj.Pc, pObj.omega ) for t in t_extL]
    plt.semilogy( t_extL, pr_calcL, '-', label='Extrapolate' )

plt.xlabel( 'Tr' )
plt.ylabel( 'Psat (psia)' )
plt.grid()
plt.legend()
plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,g}')) # 2 decimal places
plt.gca().yaxis.set_minor_formatter(StrMethodFormatter('{x:,g}')) # 2 decimal places

plt.show()




