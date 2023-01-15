# Create a Propellant object as a mixture of existing Propellant objects
from math import log10
from scipy import optimize
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value
from rocketprops.mixing_functions import Li_Tcm, mixing_simple, DIPPR9H_cond, Filippov_cond
from rocketprops.mixing_functions import isMMH_N2H4_Blend, isMON_Ox, isFLOX_Ox
from rocketprops.mixing_functions import Mnn_Freeze_terp, MON_Freeze_terp  #, ScaledGasZ
from rocketprops.rocket_prop import get_prop
# from rocketprops._prop_template import template

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


def build_mixture( prop_name=''): #, prop_objL=None, mass_fracL=None):
    """
    Build a mixture of MMH + N2H4 (e.g. M20), N2O4 + NO (e.g. MON25) or LOX + F2 (e.g. FLOX70)

    Args:

    Returns: Propellant object of mixture
    """
    # prop_objL  list of Propellant objects to be mixed. 
    # mass_fracL list of WEIGHT Fractions for each Propellant object.

    mmhPcent = isMMH_N2H4_Blend( prop_name )
    noPcent  = isMON_Ox( prop_name )
    f2Pcent  = isFLOX_Ox( prop_name )

    if mmhPcent:
        mmh_prop = get_prop('MMH')
        n2h4_prop = get_prop('N2H4')
        prop_objL=[mmh_prop, n2h4_prop]
        mass_fracL=[mmhPcent, 100-mmhPcent]  # will normalize below

        Tfreeze = Mnn_Freeze_terp( mmhPcent )
    # elif prop_name == 'MHF3':
    #     mmh_prop = get_prop('MMH')
    #     n2h4_prop = get_prop('N2H4')
    #     mmhPcent = 86.0 # MHF3 is 86% MMH
    #     prop_objL=[mmh_prop, n2h4_prop]
    #     mass_fracL=[mmhPcent, 100-mmhPcent]  # will normalize below

    #     Tfreeze = Mnn_Freeze_terp( mmhPcent )
    elif noPcent:
        mon_lo_prop = get_prop('MON10')
        mon_hi_prop = get_prop('MON25')
        prop_objL=[mon_lo_prop, mon_hi_prop]  # will normalize below

        mass_fracL=[20, 80]
        Tfreeze = MON_Freeze_terp( noPcent )
        raise Exception('MON logic needs work')
    elif f2Pcent:
        lox_prop = get_prop('LOX')
        lf2_prop = get_prop('LF2')
        prop_objL=[lf2_prop, lox_prop]
        mass_fracL=[f2Pcent, 100-f2Pcent]  # will normalize below

        # Assume we don't need an accurate freeze temperature
        Tfreeze = (f2Pcent*lf2_prop.Tfreeze + (100.0-f2Pcent)*lox_prop.Tfreeze) / 100.0
    else:
        raise Exception('Mixtures only implemented for MMH+N2H4 or MON oxidizer or FLOX oxidizer')


    if len(prop_objL) > 2:
        raise Exception('ONLY Binary mixtures allowed.')

    # Change reference fluids to allow extrapolation
    def change_terp_extrap( terp_obj ):
        terp_obj.extrapOK = 1
        terp_obj.linear = 1
        if terp_obj.linear:
            terp_obj.Nterp = 1
        else:
            terp_obj.Nterp = 2

    for Pobj in prop_objL:
        
        change_terp_extrap( Pobj.log10p_terp )
        change_terp_extrap( Pobj.log10visc_terp )
        change_terp_extrap( Pobj.cond_terp )
        change_terp_extrap( Pobj.cp_terp )
        change_terp_extrap( Pobj.hvap_terp )
        change_terp_extrap( Pobj.surf_terp )
        change_terp_extrap( Pobj.SG_liq_terp )
        change_terp_extrap( Pobj.log10SG_vap_terp )

    # Normalize mass_fracL to make sure it adds up to 1.0
    total = sum( mass_fracL )
    mass_fracL = [ f/total for f in mass_fracL ]

    # calculate mole fractions
    moleL = [ f_mass/Pobj.MolWt for (f_mass, Pobj) in zip(mass_fracL, prop_objL) ]
    mole_total = sum( moleL )
    mole_fracL = [m/mole_total for m in moleL]
    # print( 'mole_fracL =', mole_fracL)

    tmpD = {} # index=parameter name, value=string or numeric value

    dataSrc = 'Mixture Rules'     

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.3
    omega = mixing_simple(mole_fracL, [Pobj.omega for Pobj in prop_objL]) 
    tmpD['omega'] = omega

    tmpD['dataSrc'] = dataSrc
    # tmpD['class_name'] = prop_name 
    tmpD['prop_name'] = prop_name 

    MolWt = sum( [mole_frac*Pobj.MolWt for (mole_frac,Pobj) in zip(mole_fracL, prop_objL)] )
    tmpD['MolWt'] = MolWt

    # make mixture reference point the mole average of constituents
    T = mixing_simple(mole_fracL, [Pobj.T for Pobj in prop_objL])
    tmpD['T'] = T  # degR
    tmpD['P'] = mixing_simple(mole_fracL, [Pobj.P for Pobj in prop_objL])  # psia

    # Vc = MolWt / SGc # (cm**3/gmole)
    VcL = [ Pobj.MolWt/Pobj.SGc for Pobj in prop_objL ]

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.1
    # Switch to Li method from mixing_simple:  tmpD['Tc'] = mixing_simple(mole_fracL, [Pobj.Tc for Pobj in prop_objL])  # degR

    # thermo package: https://thermo.readthedocs.io/
    TcL = [Pobj.Tc for Pobj in prop_objL]
    Tc = Li_Tcm(mole_fracL, TcL, VcL)
    tmpD['Tc'] = Tc # (zs, Tcs, Vcs)

    Tr = T / Tc

    # Zc is the mechanical compressibility for mixtures as well as pure fluids
    Zc = mixing_simple(mole_fracL, [Pobj.Zc for Pobj in prop_objL])
    tmpD['Zc'] = Zc


    # get mixture critical volume
    Vcm =  mixing_simple( mole_fracL, VcL )
    Vcm = get_value( Vcm, 'cm**3', 'inch**3')

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.2
    R = 18540.0 / 453.59237 # psi-in**3 / gmole-degR (i.e. 453.59 converts lbmole to gmole)
    Pc = Zc  * R * Tc / Vcm 
    tmpD['Pc'] = Pc


    # get Pvap at T
    Pvap = sum( [y* Pobj.PvapAtTdegR(T) for (y,Pobj) in zip(mole_fracL, prop_objL)] )
    tmpD['Pvap'] = Pvap

    # Vm = MolWt / SG # (cm**3/gmole)
    VmL = [ Pobj.MolWt/Pobj.SGLiqAtTdegR(T) for Pobj in prop_objL ]
    Vm = mixing_simple( mole_fracL, VmL )
    # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
    tmpD['SG'] = MolWt / Vm  


    tmpD['Cp'] = mixing_simple(mole_fracL, [Pobj.CpAtTr(Tr) for Pobj in prop_objL])
    tmpD['Hvap'] = mixing_simple(mole_fracL, [Pobj.HvapAtTr(Tr) for Pobj in prop_objL])
    
    tmp_condL = [Pobj.CondAtTr(Tr) for Pobj in prop_objL]
    if len(mass_fracL) == 2:
        # Recommended in Perry Handbook 8th Ed. page 2-512
        tmpD['cond'] =  Filippov_cond( mass_fracL, tmp_condL )
    else:
        tmpD['cond'] =  DIPPR9H_cond( mass_fracL, tmp_condL )

    # sigmas_TbL = [Pobj.SurfAtTdegR( Pobj.Tnbp ) for Pobj in prop_objL]
    # TbsL = [Pobj.Tnbp for Pobj in prop_objL]
    # tmpD['surf'] =  Diguilio_Teja_surften(T, mole_fracL, sigmas_TbL, TbsL, TcL)

    surfL = [Pobj.SurfAtTr(Tr) for Pobj in prop_objL]
    tmpD['surf'] =  mixing_simple( mass_fracL, surfL )

    #  D. Perry's Chemical Engineering Handbook. 6th Ed
    viscL = [Pobj.ViscAtTr(Tr) for Pobj in prop_objL]
    tmpD['visc'] = mixing_simple( mass_fracL, viscL)

    tmpD['Tfreeze'] = Tfreeze
    tmpD['Ttriple'] = Tfreeze



    # start building the arrays of values
    NsatPts = 21

    # Use Raoult's Law to calculate vapor pressure vs temperature
    TfreezeL = [Pobj.Tfreeze for Pobj in prop_objL]
    Tlo = Tfreeze
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

    # print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))

    # iterate over temperature range
    for i in range( NsatPts ):
        T =  Tlo + i*dT
        Tr = T / Tc
        if i == NsatPts-1:
            T = Thi
            Tr = 1.0

        tL.append( T )
        trL.append( T/Tc )
        pL.append( sum( [y* Pobj.PvapAtTdegR(T) for (y,Pobj) in zip(mole_fracL, prop_objL)] ) ) # Raoult's Law

        cpL.append( mixing_simple(mole_fracL, [ Pobj.CpAtTr(Tr) for Pobj in prop_objL]) )

        hvapL.append( mixing_simple(mole_fracL, [ Pobj.HvapAtTr(Tr) for Pobj in prop_objL]) )
        
        surfL.append( mixing_simple(mass_fracL, [ Pobj.SurfAtTr(Tr) for Pobj in prop_objL]) )
        
        viscL.append( mixing_simple(mass_fracL, [ Pobj.ViscAtTr(Tr) for Pobj in prop_objL]) )
        
        # thermal conductivity
        tmp_condL = [Pobj.CondAtTr(Tr) for Pobj in prop_objL]
        if len(mass_fracL) == 2:
            # Recommended in Perry Handbook 8th Ed. page 2-512
            condL.append(  Filippov_cond( mass_fracL, tmp_condL ) )
        else:
            condL.append(   DIPPR9H_cond( mass_fracL, tmp_condL ) )

        # liquid density
        VmL = [ Pobj.MolWt/Pobj.SGLiqAtTr(Tr) for Pobj in prop_objL ]
        
        Vm = mixing_simple( mole_fracL, VmL )
        # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
        SG_liqL.append( MolWt / Vm )

        Z = mixing_simple(mole_fracL, [Pobj.ZVapAtTr(Tr) for Pobj in prop_objL])

        MW = sum( [y*Pobj.MolWt* Pobj.PvapAtTr(Tr) \
                   for (y,Pobj) in zip(mole_fracL, prop_objL)] ) / pL[-1]

        # print( 'MW =',MW, '  MolWt =', MolWt)
        SGg = pL[-1] * MW / (18540.0 * T * (Z/27.67990471)) # g/ml
        # SGg = pL[-1] * MolWt / (18540.0 * T * (Z/27.67990471)) # g/ml
        
        SG_vapL.append( SGg )



    tmpD['Tnbp'] = solve_Tnbp( tL, pL )

    tmpD['NsatPts'] = NsatPts
    tmpD['trL'] = trL
    tmpD['tL'] = tL
    tmpD['log10pL'] =  [log10(p) for p in pL]
    
    tmpD['log10viscL'] =  [log10(v) for v in viscL]
    tmpD['condL'] = condL
    tmpD['cpL'] = cpL
    tmpD['hvapL'] = hvapL
    tmpD['surfL'] = surfL
    tmpD['SG_liqL'] = SG_liqL
    tmpD['log10SG_vapL'] =  [log10(v) for v in SG_vapL]


    # =============== Temporary output =====================
    if 0:
        kL = sorted( tmpD.keys(), key=str.lower )
        for k in kL:
            try:
                sL = tmpD[k].split(',')
                if len(sL) > 1:
                    print( '%20s'%k, ','.join(sL[:2]),'...', ','.join(sL[-2:]) )
                else:
                    print( '%20s'%k, tmpD[k] )
            except:
                print( '%20s'%k, tmpD[k] )

        # show T limits
        print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))
        print( 'Tfreeze of pure propellants:', TfreezeL, '  of blend =', Tfreeze)
        print( 'Tc of pure propellants:', TcL, '  of blend =', Tc)
        # src = template.format( **tmpD )
        # print( src )

        # from math import log10
        # from rocketprops.rocket_prop import Propellant
        # from rocketprops.unit_conv_data import get_value
        # from rocketprops.InterpProp_scipy import InterpProp

        # exec( src )
        print()
        # print( repr(tmpD) )

    return tmpD


if __name__ == "__main__":
    from rocketprops.plot_multi_props import make_plots
    from rocketprops.prop_from_dict import Prop

    tmpD = build_mixture( prop_name='M20' )
    # tmpD = build_mixture( prop_name='MON15' )
    # tmpD = build_mixture( prop_name='FLOX70' )

    C = Prop( valueD=tmpD )
    print('T = %g R = %g K'%( C.T, C.T/1.8 ))
    print('SurfaceTension = %g lbf/in'%C.surf, ' = ', get_value(C.surf, 'lbf/in', 'mN/m'), 'mN/m' )
    
    print()
    print('Tr_data_range =', C.Tr_data_range())
    print('  T_data_range=',C.T_data_range())
    print('  P_data_range=', C.P_data_range())
    
    # C.plot_sat_props()
    make_plots( prop_nameL=[ 'MMH', 'N2H4'], prop_objL=[C], abs_T=1, ref_scaled=False)

