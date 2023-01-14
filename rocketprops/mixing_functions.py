from math import sqrt

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


def COSTALD(T, Tc, Vc, omega):
    r'''Calculate saturation liquid density using the COSTALD CSP method.

    A popular and accurate estimation method. If possible, fit parameters are
    used; alternatively critical properties work well.

    Units are that of critical or fit constant volume.

    Parameters
    ----------
    T : float
        Temperature of fluid [K]
    Tc : float
        Critical temperature of fluid [K]
    Vc : float
        Critical volume of fluid [m^3/mol].
        This parameter is alternatively a fit parameter
    omega : float
        (ideally SRK) Acentric factor for fluid, [-]
        This parameter is alternatively a fit parameter.

    Returns
    -------
    Vs : float
        Saturation liquid volume

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


def COSTALD_mixture(xs, T, Tcs, Vcs, omegas):
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
    return COSTALD(T, Tcm, Vm, omega)



def Rackett_mixture(T, xs, MWs, Tcs, Pcs, Zrs):
    r'''Calculate mixture liquid density using the Rackett-derived mixing rule
    as shown in [2]_.

    Parameters
    ----------
    T : float
        Temperature of liquid [K]
    xs: list
        Mole fractions of each component, []
    MWs : list
        Molecular weights of each component [g/mol]
    Tcs : list
        Critical temperatures of each component [K]
    Pcs : list
        Critical pressures of each component [Pa]
    Zrs : list
        Rackett parameters of each component []

    Returns
    -------
    Vm : float
        Mixture liquid volume [m^3/mol]

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
    return (R*bigsum*Zr**(1.0 + (1.0 - Tr)**(2.0/7.0)))*MW



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


