
from rocketprops.mixing_functions import COSTALD_Vmolar, COSTALD_mixture_Vmolar
from rocketprops.rocket_prop import get_prop
from scipy import optimize


mmh_prop = get_prop('MMH')
n2h4_prop = get_prop('N2H4')

mole_fracL = [0.14812820307772806, 0.8518717969222719]
MolWt = 34.12310911739159
omega_calcL = []
TcL = []
VcL = []

T = 527.67 # degR
for P in [mmh_prop, n2h4_prop]:

    SG = P.SGLiqAtTdegR(T)
    Vc = P.MolWt/P.SGc
    omega = P.omega
    print( P.name)

    def func( ohm ):
        VmCalc = COSTALD_Vmolar(T, P.Tc, Vc, ohm)
        SG_calc = P.MolWt / VmCalc
        # print( '   ... ohm =', ohm,  'SG=%g'%SG, 'SG_calc=%g'%SG_calc)
        return SG - SG_calc
    sol = optimize.root_scalar(func, bracket=[omega/3.0, 3.0*omega], method='brentq')
    omega_calc = sol.root
    print( 'omega_calc =', omega_calc)

    VmCalc = COSTALD_Vmolar(T, P.Tc, Vc, omega_calc)
    SG_calc = P.MolWt / VmCalc
    print( 'SG=%g,  SG_calc=%g'%(SG, SG_calc),  '   omega=%g,  omega_calc=%g'%(omega, omega_calc))

    print()

    omega_calcL.append( omega_calc )
    VcL.append( Vc )
    TcL.append( P.Tc )

VmCalc = COSTALD_mixture_Vmolar(mole_fracL, T, TcL, VcL, omega_calcL)
SG_calc = MolWt / VmCalc
print( 'Mixture SG_calc =', SG_calc, '   old ref SG=', 0.97423, '  simple mix SG=0.981029')
