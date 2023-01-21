from math import sqrt, exp, log
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value

    
# Freezing point of mixture of MMH with N2H4
wtPcentMMHL =       [0.0,    16.1057,26.3705,35.4891,43.3123,50.8364,59.9052, 86.0,    100.0]
#pcentMMH_FreezeKL = [274.678,269.95, 266.316,262.641,259.168,255.493,250.647, 219.261, 220.761] # degK
pcentMMH_FreezeRL = [494.4204, 485.91, 479.3688, 472.7538, 466.5024, 459.8874, 451.1646, 394.6698, 397.3698] # degR
#                   N2H4                                                              MMH

Mnn_Freeze_terp_lo = InterpProp( wtPcentMMHL[:-1], pcentMMH_FreezeRL[:-1] )
Mnn_Freeze_terp_hi = InterpProp( wtPcentMMHL[-2:], pcentMMH_FreezeRL[-2:] )


def Mnn_Freeze_terp( wtPcentMMH ): #= InterpProp( wtPcentMMHL, pcentMMH_FreezeRL )
    if wtPcentMMH <= 86.0:
        return Mnn_Freeze_terp_lo( wtPcentMMH )
    else:
        return Mnn_Freeze_terp_hi( wtPcentMMH )

wtPcentONL       = [0.0,    2.54567, 5.03106,7.51645,10.0684,12.5477,15.0717,17.0373,18.8689,20.0974,22.0183,22.6214,23.8275,25.1454,26.6196,27.6917,28.8085,29.7913,30.7294,31.5335,32.293,33.0077,33.7895,35.018,37.5197,40.0213]
MONfreezeL_degRL = [471.241,466.135, 461.159,455.529,449.709,443.27,436.026,429.945,423.596,418.23,409.824,406.336,399.897,391.223,380.223,370.297,360.281,350.354,340.338,330.054,320.306,310.111,298.486,303.315,308.502,310.737]
#MONfreezeKL = [261.8, 258.96, 256.2, 253.07, 249.84, 246.26, 242.24, 238.86, 235.33, 232.35, 227.68, 225.74, 222.16, 217.35, 211.24, 205.72, 200.16, 194.64, 189.08, 183.36, 177.95, 172.28, 165.83, 168.51, 171.39, 172.63]
MON_Freeze_terp = InterpProp( wtPcentONL, MONfreezeL_degRL )

wtPcentUdmhL = [0.0,  0.509356, 5.5297, 10.5275, 15.5006, 20.4669, 25.3909, 30.2954, 35.169, 40.0084, 44.8015, 49.5659, 54.2762, 58.9317, 100.0]
Axx_Freeze_degRL = [494.42, 494.973, 494.6094, 493.9272, 492.9858, 491.8734, 490.4586, 488.8638, 487.0782, 485.0856, 482.8608, 480.4902, 477.9126, 475.0776, 388.73]
Axx_Freeze_terp = InterpProp( wtPcentUdmhL, Axx_Freeze_degRL )

# def tfreeze_udmh_in_n2h4( wt_pcent_udmh ):
#     '''
#     Curve Fit Results from XYmath 07/20/2020
#     Can be called with wt_pcent_udmh=float or wt_pcent_udmh=numpy array

#     y = c0 + c1*wt_pcent_udmh + c2*wt_pcent_udmh**2
#         c0 = 275.0284644722944
#         c1 = -0.033382796654452374
#         c2 = -0.0026244277482150996
#         wt_pcent_udmh = wt_pcent_udmh
#         y = Tfreeze
#         Correlation Coefficient = 0.9999904489898558
#         Standard Deviation = 0.015507810687155406
#         Percent Standard Deviation = 0.005716790173686035%
#     y = 275.0284644722944 - 0.033382796654452374*wt_pcent_udmh - 0.0026244277482150996*wt_pcent_udmh**2

#      (x,y) Data Pairs from 07/20/2020 Used in Curve Fit 
#      (x,y) = (0.509356,274.985),(5.5297,274.783),(10.5275,274.404),
#         (15.5006,273.881),(20.4669,273.263),(25.3909,272.477),(30.2954,271.591),
#         (35.169,270.599),(40.0084,269.492),(44.8015,268.256),(49.5659,266.939),
#         (54.2762,265.507),(58.9317,263.932)

#     '''
#     try:
#         if wt_pcent_udmh<0 or wt_pcent_udmh>60:
#             print( 'WARNING... wt_pcent_udmh is outside range in tfreeze_udmh_in_n2h4' )
#             print( '  wt_pcent_udmh =',wt_pcent_udmh,' wt_pcent_udmh range = (0 to 60)' )
#     except:
#         if np.min(wt_pcent_udmh)<0 or np.max(wt_pcent_udmh)>60:
#             print( 'WARNING... wt_pcent_udmh array contains elements outside data range in tfreeze_udmh_in_n2h4' )
#             outsideArr = wt_pcent_udmh[ (wt_pcent_udmh<0) | (wt_pcent_udmh>60) ]
#             print( '  wt_pcent_udmh violations =',outsideArr,' wt_pcent_udmh range = (0 to 60)' )
    
#     return 1.8*(275.0284644722944 - 0.033382796654452374*wt_pcent_udmh - 0.0026244277482150996*wt_pcent_udmh**2)




def is_blend( name, blend_prefix, verbose=False ):
    """
    If is blend, return the percentage of additive.
    If NOT blend, return False
    """    
    if name[: len(blend_prefix) ] != blend_prefix:
        if verbose:
            print( '   failed prefix' )
        return False
        
    pcent_str = name[ len(blend_prefix): ]
    try:
        pcent = float( pcent_str )
        if pcent < 0.0:
            return False
        elif pcent > 100.0:
            return False
        return pcent
    except:
        if verbose:
            print( '   failed float of pcent_str' )
    
    return False

def isN2H4_UDMH_Blend( name, verbose=False ):
    # check for a N2H4 + UDMH blend
    
    # must start with capital "A"    
    n2h4Pcent = is_blend( name, 'A', verbose=verbose )
    if n2h4Pcent:
        if verbose:
            print('"%s"'%name, 'IS "A" Blend', 'n2h4Pcent =', n2h4Pcent )
        return n2h4Pcent
    else:
        if verbose:
            print('"%s"'%name, 'NOT Blend' )

    return False


def isMMH_N2H4_Blend( name, verbose=False ):
    # check for an MMH + N2H4 blend
    
    # must start with capital "M"    
    mmhPcent = is_blend( name, 'M', verbose=verbose )
    if mmhPcent:
        if verbose:
            print('"%s"'%name, 'IS "M" Blend', 'mmhPcent =', mmhPcent )
        return mmhPcent
    else:
        if verbose:
            print('"%s"'%name, 'NOT Blend' )

    return False


def isMON_Ox( name, verbose=False ):
    # check for MON oxidizer (MON1 to MON30)
    
    # must start with capital "MON"    
    noPcent = is_blend( name, 'MON', verbose=verbose )
    if noPcent:
        if verbose:
            print('"%s"'%name, 'IS "MON" Blend', 'noPcent =', noPcent )
        return noPcent
    else:
        if verbose:
            print('"%s"'%name, 'NOT Blend' )

    return False

def isFLOX_Ox( name, verbose=False ):
    # check for FLOX oxidizer (e.g. FLOX70 or FLOX82.5)
    # must start with capital "FLOX"    
    f2Pcent = is_blend( name, 'FLOX', verbose=verbose )
    if f2Pcent:
        if verbose:
            print('"%s"'%name, 'IS "FLOX" Blend', 'f2Pcent =', f2Pcent )
        return f2Pcent
    else:
        if verbose:
            print('"%s"'%name, 'NOT Blend' )

    return False
    

def mixing_simple(fracs, props):
    r'''Calculates a property based on weighted averages of properties. 
    Weights could be mole fractions, volume fractions, mass fractions, or anything else.

    Parameters
    ----------
    fracs : array-like
        Fractions or Percentage of a mixture (mass or molar)
    props: array-like
        Properties

    Returns
    -------
    prop : value
        Calculated property
    '''
    # Normalize fracs to make sure it adds up to 1.0
    total = sum( fracs )
    fracs = [ f/total for f in fracs ]

    return sum( [fracs[i]*props[i] for i in range(len(fracs))] )

def trunc_log(x, trunc=-744.4400719213812):
    # 5e-324 is the smallest floating point number above zero and its log is -744.4400719213812
    if x == 0.0:
        return trunc
    return log(x)

def mixing_logarithmic(fracs, props):
    r'''Simple function calculates a property based on weighted averages of
    logarithmic properties.

    .. math::
        y = exp(\sum_i \text{frac}_i \cdot \ln(\text{prop}_i))

    Parameters
    ----------
    fracs : array-like
        Fractions of a mixture
    props: array-like
        Properties

    Returns
    -------
    prop : value
        Calculated property

    Notes
    -----
    Does not work on negative values.
    Returns None if any fractions or properties are missing or are not of the
    same length.

    Examples
    --------
    >>> mixing_logarithmic([0.1, 0.9], [0.01, 0.02])
    0.01866065983073615
    '''
    try:
        tot = 0.0
        for i in range(len(fracs)):
            tot += fracs[i]*trunc_log(props[i])
        return exp(tot)
    except:
        return None



def COSTALD_Vmolar(T, Tc, Vc, omega):
    r'''Calculate saturation liquid density using the COSTALD CSP method.

    A popular and accurate estimation method. If possible, fit parameters are
    used; alternatively critical properties work well.

    Units are that of critical or fit constant volume.

    Parameters
    ----------
    T : float
        Temperature of fluid , any absolute unite
    Tc : float
        Critical temperature of fluid, same units as T
    Vc : float
        Critical volume of fluid, any units
        This parameter is alternatively a fit parameter
    omega : float
        (ideally SRK) Acentric factor for fluid, [-]
        This parameter is alternatively a fit parameter.

    Returns
    -------
    Vs : float
        Saturation liquid volume, same units as Vc

    Notes
    -----
    196 constants are fit to this function in [1]_.
    Range: 0.25 < Tr < 0.95, often said to be to 1.0

    This function has been checked with the API handbook example problem.

    Examples
    --------
    Propane, from an example in the API Handbook:

    >>> Vm_to_rho(COSTALD(272.03889, 369.83333, 0.20008161E-3, 0.1532), 44.097)
    530.3009967969844

    References
    ----------
    .. [1] Hankinson, Risdon W., and George H. Thomson. "A New Correlation for
       Saturated Densities of Liquids and Their Mixtures." AIChE Journal
       25, no. 4 (1979): 653-663. doi:10.1002/aic.690250412
    '''
    if T > Tc:
        T = Tc
    Tr = T/Tc
    tau = 1.0 - Tr
    tau_cbrt = (tau)**(1.0/3.)
    V_delta = (-0.296123 + Tr*(Tr*(-0.0480645*Tr - 0.0427258) + 0.386914))/(Tr - 1.00001)
    V_0 = tau_cbrt*(tau_cbrt*(tau_cbrt*(0.190454*tau_cbrt - 0.81446) + 1.43907) - 1.52816) + 1.0
    return Vc*V_0*(1.0 - omega*V_delta)


def COSTALD_mixture_Vmolar(xs, T, Tcs, Vcs, omegas):
    r'''Calculate mixture liquid density using the COSTALD CSP method.

    A popular and accurate estimation method. If possible, fit parameters are
    used; alternatively critical properties work well.

    The mixing rules giving parameters for the pure component COSTALD
    equation are:

    Parameters
    ----------
    xs: list
        Mole fractions of each component
    T : float
        Temperature of fluid [K]
    Tcs : list
        Critical temperature of fluids [K]
    Vcs : list
        Critical volumes of fluids [m^3/mol].
        This parameter is alternatively a fit parameter
    omegas : list
        (ideally SRK) Acentric factor of all fluids, [-]
        This parameter is alternatively a fit parameter.

    Returns
    -------
    Vs : float
        Saturation liquid mixture volume

    Notes
    -----
    Range: 0.25 < Tr < 0.95, often said to be to 1.0
    No example has been found.
    Units are that of critical or fit constant volume.

    Examples
    --------
    >>> COSTALD_mixture([0.4576, 0.5424], 298.,  [512.58, 647.29], [0.000117, 5.6e-05], [0.559,0.344])
    2.7065887732713534e-05

    References
    ----------
    .. [1] Hankinson, Risdon W., and George H. Thomson. "A New Correlation for
       Saturated Densities of Liquids and Their Mixtures." AIChE Journal
       25, no. 4 (1979): 653-663. doi:10.1002/aic.690250412
    '''
    root_two = 1.4142135623730951
    
    N = len(xs)
    sum1, sum2, sum3, omega = 0.0, 0.0, 0.0, 0.0
    for i in range(N):
        sum1 += xs[i]*Vcs[i]
        p = Vcs[i]**(1.0/3.)
        v = xs[i]*p
        sum2 += v
        sum3 += v*p
        omega += xs[i]*omegas[i]

    Vm = 0.25*(sum1 + 3.0*sum2*sum3)
    Vm_inv_root = root_two*(Vm)**-0.5
    vec = [0.0]*N
    for i in range(N):
        vec[i] = (Tcs[i]*Vcs[i])**0.5*xs[i]*Vm_inv_root

    Tcm = 0.0
    for i in range(N):
        for j in range(i):
            Tcm += vec[i]*vec[j]
        Tcm += 0.5*vec[i]*vec[i]
    return COSTALD_Vmolar(T, Tcm, Vm, omega)



def Rackett_mixture_Vm(T, xs, MWs, Tcs, Pcs, Zrs):
    r'''Calculate mixture liquid density using the Rackett-derived mixing rule
    as shown in [2]_.

    Parameters
    ----------
    T : float
        Temperature of liquid [K] <--- degR
    xs: list
        Mole fractions of each component, []
    MWs : list
        Molecular weights of each component [g/mol]
    Tcs : list
        Critical temperatures of each component [K] <--- degR
    Pcs : list
        Critical pressures of each component [Pa] <--- psia
    Zrs : list
        Rackett parameters of each component []

    Returns
    -------
    Vm : float
        Mixture liquid volume [m^3/mol] ---> cm**/gmole

    Notes
    -----
    Model for pure compounds in [1]_ forms the basis for this model, shown in
    [2]_. Molecular weights are used as weighing by such has been found to
    provide higher accuracy in [2]_. The model can also be used without
    molecular weights, but results are somewhat different.

    As with the Rackett model, critical compressibilities may be used if
    Rackett parameters have not been regressed.

    Critical mixture temperature, and compressibility are all obtained with
    simple mixing rules.

    Examples
    --------
    Calculation in [2]_ for methanol and water mixture. Result matches example.

    >>> Rackett_mixture(T=298., xs=[0.4576, 0.5424], MWs=[32.04, 18.01], Tcs=[512.58, 647.29], Pcs=[8.096E6, 2.209E7], Zrs=[0.2332, 0.2374])
    2.6252894930056885e-05

    References
    ----------
    .. [1] Rackett, Harold G. "Equation of State for Saturated Liquids."
       Journal of Chemical & Engineering Data 15, no. 4 (1970): 514-517.
       doi:10.1021/je60047a012
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    T = T/1.8
    Tcs = [_t/1.8 for _t in Tcs]

    Pcs = [get_value(_p, 'psia', 'Pa') for _p in Pcs]

    bigsum, Tc, Zr, MW = 0.0, 0.0, 0.0, 0.0

    R = 8.3144598 # J/mol-K  =  m^3-Pa / mol-K  =  J/mol-K

    # Fastest for numba and PyPy and CPython
    for i in range(len(xs)):
        x0 = Tcs[i]*xs[i]
        Tc += x0
        Zr += Zrs[i]*xs[i]
        MW += MWs[i]*xs[i]
        bigsum += x0/(Pcs[i]*MWs[i])
    Tr = T/Tc
    return (R*bigsum*Zr**(1.0 + (1.0 - Tr)**(2.0/7.0)))*MW * 1e6 # convert [m^3/mol] to cm**3/gmole



def Li_Tcm(zs, Tcs, Vcs):
    r'''Calculates critical temperature of a mixture according to
    mixing rules in [1]_. Better than simple mixing rules.

    Parameters
    ----------
    zs : array-like
        Mole fractions of all components
    Tcs : array-like
        Critical temperatures of all components, [K]
    Vcs : array-like
        Critical volumes of all components, [m^3/mol]

    Returns
    -------
    Tcm : float
        Critical temperatures of the mixture, [K]

    Notes
    -----
    Reviewed in many papers on critical mixture temperature.

    Second example is from Najafi (2015), for ethylene, Benzene, ethylbenzene.
    This is similar to but not identical to the result from the article. The
    experimental point is 486.9 K.

    2rd example is from Najafi (2015), for:
    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.
    Its result is identical to that calculated in the article.

    Examples
    --------
    Nitrogen-Argon 50/50 mixture

    >>> Li([0.5, 0.5], [126.2, 150.8], [8.95e-05, 7.49e-05])
    137.40766423357667

    butane/pentane/hexane 0.6449/0.2359/0.1192 mixture, exp: 450.22 K.

    >>> Li([0.6449, 0.2359, 0.1192], [425.12, 469.7, 507.6],
    ... [0.000255, 0.000313, 0.000371])
    449.68261498555444

    References
    ----------
    .. [1] Li, C. C. "Critical Temperature Estimation for Simple Mixtures."
       The Canadian Journal of Chemical Engineering 49, no. 5
       (October 1, 1971): 709-10. doi:10.1002/cjce.5450490529.
    '''
    N = len(zs)
    denominator_inv = 0.0
    for i in range(N):
        denominator_inv += zs[i]*Vcs[i]
    denominator_inv = 1.0/denominator_inv
    Tcm = 0.0
    for i in range(N):
        Tcm += zs[i]*Vcs[i]*Tcs[i]*denominator_inv
    return Tcm


def Winterfeld_Scriven_Davis_surf(xs, sigmas, rhoms):
    r'''Calculates surface tension of a liquid mixture according to
    mixing rules in [1]_ and also in [2]_.

    .. math::
        \sigma_M = \sum_i \sum_j \frac{1}{V_L^{L2}}\left(x_i V_i \right)
        \left( x_jV_j\right)\sqrt{\sigma_i\cdot \sigma_j}

    Parameters
    ----------
    xs : array-like
        Mole fractions of all components, [-]
    sigmas : array-like
        Surface tensions of all components, [N/m] <--- lbf/in
    rhoms : array-like
        Molar densities of all components, [mol/m^3] <--- (cm**3/gmole)

    Returns
    -------
    sigma : float
        Air-liquid surface tension of mixture, [N/m]

    Notes
    -----
    DIPPR Procedure 7C: Method for the Surface Tension of Nonaqueous Liquid
    Mixtures

    Becomes less accurate as liquid-liquid critical solution temperature is
    approached. DIPPR Evaluation:  3-4% AARD, from 107 nonaqueous binary
    systems, 1284 points. Internally, densities are converted to kmol/m^3. The
    Amgat function is used to obtain liquid mixture density in this equation.

    Raises a ZeroDivisionError if either molar volume are zero, and a
    ValueError if a surface tensions of a pure component is negative.

    Examples
    --------
    >>> Winterfeld_Scriven_Davis([0.1606, 0.8394], [0.01547, 0.02877],
    ... [8610., 15530.])
    0.02496738845043982

    References
    ----------
    .. [1] Winterfeld, P. H., L. E. Scriven, and H. T. Davis. "An Approximate
       Theory of Interfacial Tensions of Multicomponent Systems: Applications
       to Binary Liquid-Vapor Tensions." AIChE Journal 24, no. 6
       (November 1, 1978): 1010-14. doi:10.1002/aic.690240610.
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    '''
    rhoms = [_r/1e6 for _r in rhoms] # convert cm**/gmole to [m^3/mol]
    sigmas = [ get_value(s, 'lbf/in', 'N/m') for s in sigmas]

    N = len(xs)
    Vms = [0.0]*N
    rho = 0.0
    for i in range(N):
        Vms[i] = 1e3/rhoms[i]
        rho += xs[i]*Vms[i]
#    rho = 1./rho
    root_two = 1.4142135623730951
    rho = root_two/rho # factor out rt2
    # For speed, transform the Vms array to contain
#    xs[i]*Vms[i]*sigmas_05[i]*rho
    tot = 0.0
    for i in range(N):
        val = sqrt(sigmas[i])*xs[i]*rho*Vms[i]
        Vms[i] = val
        tot += val*val
    tot *= 0.5
    for i in range(N):
        # Symmetric - can be slightly optimized
        temp = 0.0
        for j in range(i):
            temp += Vms[j]
        tot += Vms[i]*temp

    return get_value(tot, 'N/m', 'lbf/in')
    # return tot



def Filippov_cond(ws, ks):
    r'''Calculates thermal conductivity of a binary liquid mixture according to
    mixing rules in [2]_ as found in [1]_.

    Parameters
    ----------
    ws : float
        Mass fractions of components
    ks : float
        Liquid thermal conductivites of all components, (any units)

    Returns
    -------
    kl : float
        Thermal conductivity of liquid mixture, (same units as ks)

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The original source has not been reviewed.
    Only useful for binary mixtures.

    Examples
    --------
    >>> Filippov([0.258, 0.742], [0.1692, 0.1528])
    0.15929167628799998

    References
    ----------
    .. [1] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E. The
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    .. [2] Filippov, L. P.: Vest. Mosk. Univ., Ser. Fiz. Mat. Estestv. Nauk,
       (8I0E): 67-69A955); Chem. Abstr., 50: 8276 A956).
       Filippov, L. P., and N. S. Novoselova: Vestn. Mosk. Univ., Ser. F
       iz. Mat. Estestv.Nauk, CI0B): 37-40A955); Chem. Abstr., 49: 11366 A955).
    '''
    len_ks = len(ks)
    if len_ks != len(ws) or len_ks != 2:
        raise ValueError("Filippov method is only defined for mixtures of two components")
    return ws[0]*ks[0] + ws[1]*ks[1] - 0.72*ws[0]*ws[1]*(ks[1] - ks[0])


def DIPPR9H_cond(ws, ks):
    r'''Calculates thermal conductivity of a liquid mixture according to
    mixing rules in [1]_ and also in [2]_.

    This is also called the Vredeveld (1973) equation. A review in [3]_ finds
    this the best model on average. However, they did caution that in some
    cases a linear mole-fraction mixing rule performs better. This equation
    according to Poling [1]_ should not be used if some components have
    thermal conductivities more than twice other components. They also say this
    should not be used with water.

    Parameters
    ----------
    ws : float
        Mass fractions of components
    ks : float
        Liquid thermal conductivites of all components, any units

    Returns
    -------
    kl : float
        Thermal conductivity of liquid mixture, same units as ks

    Notes
    -----
    This equation is entirely dimensionless; all dimensions cancel.
    The example is from [2]_; all results agree.
    The original source has not been reviewed.

    DIPPR Procedure 9H: Method for the Thermal Conductivity of Nonaqueous Liquid Mixtures

    Average deviations of 3%. for 118 nonaqueous systems with 817 data points.
    Max deviation 20%. According to DIPPR.

    In some sources, this equation is given with the molecular weights included:

    Examples
    --------
    >>> DIPPR9H([0.258, 0.742], [0.1692, 0.1528])
    0.15657104706719646

    References
    ----------
    .. [1] Reid, Robert C.; Prausnitz, John M.; Poling, Bruce E. The
       Properties of Gases and Liquids. McGraw-Hill Companies, 1987.
    .. [2] Danner, Ronald P, and Design Institute for Physical Property Data.
       Manual for Predicting Chemical Process Design Data. New York, N.Y, 1982.
    .. [3] Focke, Walter W. "Correlating Thermal-Conductivity Data for Ternary
       Liquid Mixtures." International Journal of Thermophysics 29, no. 4
       (August 1, 2008): 1342-60. https://doi.org/10.1007/s10765-008-0465-2.
    '''
    kl = 0.0
    for i in range(len(ws)):
        kl += ws[i]/(ks[i]*ks[i])
    return 1.0/sqrt(kl)

    
if __name__ == "__main__":
    for name in ['M20', "20M", 'MM2', 'm020', 'M10', 'm20 ', 'M101', 'M99']:
        isMMH_N2H4_Blend( name, verbose=True )
        isMMH_N2H4_Blend( name )
        
    print( '-'*22 )

    for name in ['M20', "MON25", "mon10", "MON5.5", "MON20 "]:
        isMON_Ox( name, verbose=True )
        isMON_Ox( name )

        
    print( '-'*22 )

    for name in ['M20', "FLOX25", "FLOX82.5", "flox5.5", "FLOX20 "]:
        isFLOX_Ox( name, verbose=True )
        isFLOX_Ox( name )
        
    print( '-'*22 )

    for name in ['M20', "A25", "A82.5", "a5.5", "A20 "]:
        isN2H4_UDMH_Blend( name, verbose=True )
        isN2H4_UDMH_Blend( name )


    def ScaledGasZ( TdegR, Ppsia, Tc, Pc, Zc, omega ):
        """Based on BVirial_Pitzer_Curl from thermo.
        see: https://study.com/academy/answer/using-the-correlation-for-the-second-virial-coefficient-pitzer-correlation-find-the-molar-volume-of-1-propanol-vapour-at-508-8-k-and-12-bar-giving-your-answer-to-the-nearest-cm-3-mol-the-critical.html
        """
        
        Tr = TdegR / Tc 
        Pr = Ppsia / Pc
        
        def calc_b0b1( Tr ):
            # Pitzer_Curl
            B0 = 0.1445 - 0.33/Tr - 0.1385/Tr**2 - 0.0121/Tr**3
            B1 = 0.073 + 0.46/Tr - 0.5/Tr**2 - 0.097/Tr**3 - 0.0073/Tr**8
            
            # Tsonopoulos
            #B0 = 0.1445 - 0.33/Tr - 0.1385/Tr**2 - 0.0121/Tr**3 - 0.000607/Tr**8
            #B1 = 0.0637 + 0.331/Tr**2 - 0.423/Tr**3 - 0.008/Tr**8        
            
            # Abbot version of second virial const.
            #B0 = 0.083 - 0.422/Tr**1.6
            #B1 = 0.139 - 0.172/Tr**4.2
            
            return B0, B1
            
        def calc_B( Tr, omega ):
            B0, B1 = calc_b0b1( Tr )
            B = B0 + omega * B1
            return B
                
        def calc_z( Tr, Pr, omega ):
            B = calc_B( Tr, omega )
            Z = 1.0 + B * Pr / Tr
            return Z
        
        Bc_calc = calc_B( 1.0, omega )
        Bc_inp = Zc - 1.0
        scale_fact = Bc_inp / Bc_calc
        
        B = calc_B( Tr, omega )
        Z = 1.0 + scale_fact * B * Pr / Tr
        return Z

    Z = ScaledGasZ( 527.67, 14.7, 776, 1441, .3, .3 )
    print( 'Z =', Z)
