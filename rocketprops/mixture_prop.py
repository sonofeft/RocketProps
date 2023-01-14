# Create a Propellant object as a mixture of existing Propellant objects
from math import log10
from scipy import optimize
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value
from rocketprops.mixing_functions import Li_Tcm, mixing_simple, DIPPR9H_cond, Filippov_cond


def solve_Tnbp( tL, pvapL ):
    """
    Given Temperature list, tL and Vapor Pressure list, pvapL, solve for Tnpb
    tL = temperature list, degR
    pvapL = vapor pressure list, psia
    Return:
    Tnbp = normal boiling point, degR
    """
    
    Pvap_terp = InterpProp( tL, pvapL, extrapOK=True)
    
    def func( T ):
        return 14.6959 - max(0.0, Pvap_terp( T ))
    
    sol = optimize.root_scalar(func, bracket=[tL[0], tL[-1]], method='brentq')
    # print( 'sol.root=',sol.root )
    return sol.root


def build_mixture( prop_name='', prop_objL=None, mass_fracL=None):
    """_summary_

    Args:
        prop_objL (_type_, optional): list of Propellant objects to be mixed. Defaults to None.
        mass_fracL (_type_, optional): list of WEIGHT Fractions for each Propellant object. Defaults to None.

    Returns: Propellant object of mixture
    """

    if prop_objL is None or mass_fracL is None:
        raise Exception('Must input BOTH prop_objL AND mass_fracL')
    if not prop_name:
        raise Exception('Must give mixture a prop_name.')

    # Normalize mass_fracL to make sure it adds up to 1.0
    total = sum( mass_fracL )
    mass_fracL = [ f/total for f in mass_fracL ]

    # calculate mole fractions
    moleL = [ f_mass/P.MolWt for (f_mass, P) in zip(mass_fracL, prop_objL) ]
    mole_total = sum( moleL )
    mole_fracL = [m/mole_total for m in moleL]

    tmpD = {} # index=template name, value=string or numeric value

    dataSrc = 'Mixture Rules'     

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.3
    tmpD['omega'] = mixing_simple(mole_fracL, [P.omega for P in prop_objL]) 

    tmpD['dataSrc'] = dataSrc
    tmpD['class_name'] = prop_name + '_mixture'
    tmpD['prop_name'] = prop_name + '_mixture'

    # Vc = MolWt / SGc # (cm**3/gmole)
    VcL = [ P.MolWt/P.SGc for P in prop_objL ]

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.1
    # tmpD['Tc'] = mixing_simple(mole_fracL, [P.Tc for P in prop_objL])  # degR

    # thermo package: https://thermo.readthedocs.io/
    TcL = [P.Tc for P in prop_objL]
    Tc = Li_Tcm(mole_fracL, TcL, VcL)
    tmpD['Tc'] = Tc # (zs, Tcs, Vcs)

    # Zc is the mechanical compressibility for mixtures as well.
    tmpD['Zc'] = mixing_simple(mole_fracL, [P.Zc for P in prop_objL])

    # get mixture critical volume
    Vcm =  mixing_simple( mole_fracL, VcL )
    Vcm = get_value( Vcm, 'cm**3', 'inch**3')

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.2
    R = 18540.0 / 453.59237 # psi-in**3 / gmole-degR
    tmpD['Pc'] = tmpD['Zc'] * R * Tc / Vcm 


    # make mixture reference point the mole average of constituents
    T = mixing_simple(mole_fracL, [P.T for P in prop_objL])
    tmpD['T'] = T  # degR
    tmpD['P'] = mixing_simple(mole_fracL, [P.P for P in prop_objL])  # psia

    MolWt = sum( [mole_frac*P.MolWt for (mole_frac,P) in zip(mole_fracL, prop_objL)] )
    tmpD['MolWt'] = MolWt

    # Vm = MolWt / SG # (cm**3/gmole)
    VmL = [ P.MolWt/P.SGLiqAtTdegR(T) for P in prop_objL ]
    Vm = mixing_simple( mole_fracL, VmL )
    # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
    tmpD['SG'] = MolWt / Vm  


    tmpD['Cp'] = mixing_simple(mole_fracL, [P.Cp for P in prop_objL])
    tmpD['Hvap'] = mixing_simple(mole_fracL, [P.Hvap for P in prop_objL])
    
    tmp_condL = [P.CondAtTdegR(T) for P in prop_objL]
    if len(mass_fracL) == 2:
        # Recommended in Perry Handbook 8th Ed. page 2-512
        tmpD['cond'] =  Filippov_cond( mass_fracL, tmp_condL )
    else:
        tmpD['cond'] =  DIPPR9H_cond( mass_fracL, tmp_condL )

    # sigmas_TbL = [P.SurfAtTdegR( P.Tnbp ) for P in prop_objL]
    # TbsL = [P.Tnbp for P in prop_objL]
    # tmpD['surf'] =  Diguilio_Teja_surften(T, mole_fracL, sigmas_TbL, TbsL, TcL)

    surfL = [P.SurfAtTdegR(T) for P in prop_objL]
    tmpD['surf'] =  mixing_simple( mass_fracL, surfL )

    #  D. Perry's Chemical Engineering Handbook. 6th Ed
    viscL = [P.ViscAtTdegR(T) for P in prop_objL]
    tmpD['visc'] = mixing_simple( mass_fracL, viscL)

    tmpD['Tfreeze'] = None
    tmpD['Ttriple'] = None



    # start building the arrays of values
    NsatPts = 21

    # Use Raoult's Law to calculate vapor pressure vs temperature
    TfreezeL = [P.Tfreeze for P in prop_objL]
    Tlo = min( TfreezeL )
    Thi = max( TcL )
    if Thi > Tc:
        Thi = Tc
    dT = (Thi - Tlo) / (NsatPts - 1)

    
    trL = []
    tL  = []
    pL  = []
    viscL = []
    condL = []
    cpL = []
    hvapL = []
    surfL = []    
    SG_liqL = []
    SG_vapL = []

    print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))

    # get out-of-bounds properties
    def clamped_property(T, prop_obj, method):
        if T <= prop_obj.Tfreeze:
            Pvap = method( prop_obj.Tfreeze )
        elif T >= prop_obj.Tc:
            Pvap = method( prop_obj.Tc )
        else:
            Pvap = method( T )
        return Pvap

    # iterate over temperature range
    for i in range( NsatPts ):
        T =  Tlo + i*dT
        if i == NsatPts-1:
            T = Thi

        tL.append( T )
        trL.append( T/Tc )
        pL.append( sum( [y*clamped_property(T, P, P.PvapAtTdegR) for (y,P) in zip(mole_fracL, prop_objL)] ) ) # Raoult's Law

        cpL.append( mixing_simple(mole_fracL, [clamped_property(T, P, P.CpAtTdegR) for P in prop_objL]) )
        hvapL.append( mixing_simple(mole_fracL, [clamped_property(T, P, P.HvapAtTdegR) for P in prop_objL]) )

        surfL.append( mixing_simple(mole_fracL, [clamped_property(T, P, P.SurfAtTdegR) for P in prop_objL]) )
        viscL.append( mixing_simple(mole_fracL, [clamped_property(T, P, P.ViscAtTdegR) for P in prop_objL]) )
        
        # thermal conductivity
        tmp_condL = [P.CondAtTdegR(T) for P in prop_objL]
        if len(mass_fracL) == 2:
            # Recommended in Perry Handbook 8th Ed. page 2-512
            condL.append(  Filippov_cond( mass_fracL, tmp_condL ) )
        else:
            condL.append(   DIPPR9H_cond( mass_fracL, tmp_condL ) )

        # liquid density
        VmL = [ P.MolWt/P.SGLiqAtTdegR(T) for P in prop_objL ]
        Vm = mixing_simple( mole_fracL, VmL )
        # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
        SG_liqL.append( MolWt / Vm )



    tmpD['Tnbp'] = solve_Tnbp( tL, pL )

    tmpD['NsatPts'] = NsatPts
    tmpD['trL'] = repr(trL)
    tmpD['tL'] = repr(tL)
    tmpD['log10pL'] = repr( [log10(p) for p in pL] )
    
    tmpD['log10viscL'] = repr( [log10(v) for v in viscL] )
    tmpD['condL'] = repr(condL)
    tmpD['cpL'] = repr(cpL)
    tmpD['hvapL'] = repr(hvapL)
    tmpD['surfL'] = repr(surfL)
    tmpD['SG_liqL'] = repr(SG_liqL)
    tmpD['log10SG_vapL'] = repr( [log10(v) for v in SG_vapL] )


    # =============== Temporary output =====================
    kL = sorted( tmpD.keys(), key=str.lower )
    for k in kL:
        try:
            sL = tmpD[k].split(',')
            print( '%20s'%k, ','.join(sL[:2]),'...', ','.join(sL[-2:]) )
        except:
            print( '%20s'%k, tmpD[k] )

    # show T limits
    print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))
    print( 'Tfreeze of pure propellants:', TfreezeL)
    print( 'Tc of pure propellants:', TcL)


if __name__ == "__main__":
    
    from rocketprops.rocket_prop import get_prop

    mmh_prop = get_prop('MMH')
    n2h4_prop = get_prop('N2H4')

    build_mixture( prop_name='M20', prop_objL=[mmh_prop, n2h4_prop],  mass_fracL=[20, 80])
