
from rocketprops.mixing_functions import Rackett_mixture_Vm, Li_Tcm
from rocketprops.rocket_prop import get_prop

n2h4_prop = get_prop('N2H4')
mhf3_prop = get_prop('MHF3')
mmh_prop = get_prop('MMH')

def pTr(Pobj, T, Tr):
    """Make a pseudo temperature for each object to smooth high Tr values"""
    limit = 0.7
    # Tr_p = max(limit, min(1.0, T / Pobj.Tc))
    Tr_p =  T / Pobj.Tc
    if Tr_p < limit:
        return Tr_p
    
    Tc_mix = T / Tr
    T_at_limit = limit * Pobj.Tc
    Tr_mix_at_Tr_p_limit = T_at_limit / Tc_mix

    Tr_range = 1.0 - limit

    return limit + Tr_range * (Tr-Tr_mix_at_Tr_p_limit)/(1.0-Tr_mix_at_Tr_p_limit)


prop_objL = [mmh_prop, n2h4_prop]
mass_fracL=[0.2, 0.8]


moleL = [ f_mass/Pobj.MolWt for (f_mass, Pobj) in zip(mass_fracL, prop_objL) ]
mole_total = sum( moleL )
mole_fracL = [m/mole_total for m in moleL]
print( 'mole_fracL =', mole_fracL)
print( 'mass_fracL =', mass_fracL)

T       = 527.67 # degR
TcL = [Pobj.Tc for Pobj in prop_objL]
# Vc = MolWt / SGc # (cm**3/gmole)
VcL = [ Pobj.MolWt/Pobj.SGc for Pobj in prop_objL ]

Tc = Li_Tcm(mole_fracL, TcL, VcL)
Tr = T / Tc
print( 'Tc =', Tc, '   Tr =', Tr)

PcL = [Pobj.Pc for Pobj in prop_objL]
ZcL = [Pobj.Zc for Pobj in prop_objL]
mwL = [Pobj.MolWt for Pobj in prop_objL]

# cm**3/gmole
VmL = [ Pobj.MolWt/Pobj.SGLiqAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL ]

surfL = [Pobj.SurfAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]


Vm = Rackett_mixture_Vm(T, mole_fracL, mwL, TcL, PcL, ZcL)
print( 'VmL =', VmL)
print( 'Vm =', Vm)
