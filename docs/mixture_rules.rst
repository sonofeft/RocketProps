.. mixture_rules

Mixture Rules
=============

For each propellant mixture, RocketProps starts with two well-documented propellants 
and uses the properties of those two propellants to calculate expected properties of the mixture.

Mixtures of N2H4 and MMH, for example, use N2H4 and MHF3 having MMH weight fractions below 86%,
and would use MHF3 and MMH for MMH weight fractions above 86%. (Note that MHF3 is a mixture of 86% MMH + 14% N2H4)

The table below shows the reference propellants used to calculate mixtures of base and additive propellants
within each weight percent additive range.

.. raw:: html

    <table>
    <tr>
        <th >Base Propellant</th>
        <th >Additive</th>
        <th >Additive Wt% Range</th>
        <th >1st Ref Propellant</th>
        <th >2nd Ref Propellant</th>
    </tr>

    <tr> <td>N2H4</td> <td>MMH</td> <td>0 to 86</td> <td>N2H4</td> <td>MHF3</td> </tr>
    <tr> <td>N2H4</td> <td>MMH</td> <td>86 to 100</td> <td>MHF3</td> <td>MMH</td> </tr>
    <tr> <td>UDMH</td> <td>N2H4</td> <td>0 to 50</td> <td>UDMH</td> <td>A50</td> </tr>
    <tr> <td>UDMH</td> <td>N2H4</td> <td>50 to 100</td> <td>A50</td> <td>N2H4</td> </tr>
    <tr> <td>N2O4</td> <td>NO</td> <td>0 to 10</td> <td>N2O4</td> <td>MON10</td> </tr>
    <tr> <td>N2O4</td> <td>NO</td> <td>10 to 25</td> <td>MON10</td> <td>MON25</td> </tr>
    <tr> <td>N2O4</td> <td>NO</td> <td>25 to 30</td> <td>MON25</td> <td>MON30</td> </tr>
    <tr> <td>LF2</td> <td>LOX</td> <td>0 to 100</td> <td>LF2</td> <td>LOX</td> </tr>

    </table>

Freezing Point
--------------

The freezing point of each mixture is determined as outlined in :ref:`Mixture Freezing Points`

Acentric Factor
---------------

The value of the mixture `Acentric Factor <https://en.wikipedia.org/wiki/Acentric_factor>`_
, omega, is calculated using a mole fraction simple mixing rule as recommended by Eqn 5-3.3 of 
:ref:`Gas&Liq 5th Ed Source`

.. math::
    \text{omega}_{mix} = \sum_i \text{mole_frac}_i \cdot \text{omega}_i


Molecular Weight
----------------

By definition, the value of the mixture Molecular Weight, MW, is calculated using a mole fraction simple mixing rule.

.. math::
    \text{MW}_{mix} = \sum_i \text{mole_frac}_i \cdot \text{MW}_i    

Reference T & P
---------------

In order to create a properties summary such as the M20 
:ref:`Example Mixture Summary<Example Mixture Summary>`
the mixture needs to have a reference temperature (:math:`\text{T}_{mix}`) and pressure (:math:`\text{P}_{mix}`)
at which to calculate reference properties.

In case the reference :math:`\text{T}_i` and :math:`\text{P}_i` for the base propellants are 
different, the mixture :math:`\text{T}_{mix}` and :math:`\text{P}_{mix}` are calculated as a mole fraction simple mixing rule
of the :math:`\text{T}_i` and :math:`\text{P}_i` of each base propellant.

.. math::
    \text{T}_{mix} = \sum_i \text{mole_frac}_i \cdot \text{T}_i    

.. math::
    \text{P}_{mix} = \sum_i \text{mole_frac}_i \cdot \text{P}_i    

Reference properties for each base propellant are calculated at
:math:`\text{T}_{mix}` and :math:`\text{P}_{mix}`
and are combined with an appropriate mixing rule to compute the mixture reference properties.

Critical Temperature
--------------------

Calculation of mixture critical temperature (:math:`\text{T}_{cm}`) uses the Li correlation from
Caleb Bell, Yoel Rene Cortes-Pena, and Contributors (2016-2021). Chemicals: Chemical properties component of Chemical Engineering Design Library (ChEDL)
https://chemicals.readthedocs.io/chemicals.critical.html#critical-temperature-of-mixtures.

Although Kay's rule Eqn 5-3.1 from :ref:`Gas&Liq 5th Ed Source` (i.e. simple mole fraction mixing rule) 
is often sufficient. Better accuracy can usually be expected from the Li correlation.

.. math::
    T_{cm} = \sum_{i=1}^n \Phi_i T_{ci}\\
    \Phi = \frac{x_i V_{ci}}{\sum_{j=1}^n x_j V_{cj}}

:
    Li, C. C. "Critical Temperature Estimation for Simple Mixtures."
    The Canadian Journal of Chemical Engineering 49, no. 5
    (October 1, 1971): 709-10. doi:10.1002/cjce.5450490529.

Critical Compressibility Factor
-------------------------------

Eqn 5-3.2 from :ref:`Gas&Liq 5th Ed Source` recommends simple mole fraction mixing rule to calculate 
the mixture critical compressibility factor  (:math:`\text{Z}_{cm}`)


.. math::
    \text{Z}_{cm} = \sum_i \text{mole_frac}_i \cdot \text{Z}_i    

Critical Pressure
-----------------

The simplest rule which can give acceptable :math:`\text{P}_{cm}` values
for two-parameter or three-parameter CSP (corresponding states principle) 
is the modified rule of Prausnitz and Gunn (1958); Eqn 5-3.2 from :ref:`Gas&Liq 5th Ed Source`.


.. math::
    \text{P}_{cm} = \frac{\text{Z}_{cm} \cdot R \cdot  \text{T}_{cm}}{\text{V}_{cm}}

Vapor Pressure
--------------

The mixture vapor pressure :math:`\text{P}_{vapm}` is assumed to follow `Raoult's Law <https://en.wikipedia.org/wiki/Raoult%27s_law>`_ 
for vapor pressure.

.. math::
    \text{P}_{vapm} = \sum_i \text{mole_frac}_i \cdot \text{P}_{vapi}    

Heat Capacity
-------------

Mixture heat capacity :math:`\text{C}_{pm}` can be estimated with a simple mixing rule as noted in Eqn 2-55 
of `Perry's Chemical Engineers' Handbook 8th Edition by Don Green and Robert Perry <https://www.accessengineeringlibrary.com/content/book/9780071422949>`_

Note that in Perry's, the Cp has units of energy/mole and therefore uses mole fraction in the simple mixing equation. 
Since RocketProps uses energy/mass, mass fraction is used in the simple mixing equation.

.. math::
    \text{C}_{pm} = \sum_i \text{mass_frac}_i \cdot \text{C}_{pi}    

Heat of Vaporization
--------------------

Mixture heat of vaporization :math:`\text{H}_{vapm}` is "tricky". Also note that, like heat capacity :math:`\text{C}_{pm}`, heat of vaporization, :math:`\text{H}_{vapm}` in RocketProps 
uses energy/mass for :math:`\text{H}_{vapm}` and is therefore based on mass fraction, not mole fraction.

The most common use of :math:`\text{H}_{vapm}` is in evaluating propellant droplet evaporation in a thrust chamber
in order to calculate thrust chamber performance and combustion stability.

When a droplet first begins to evaporate, the instantaneous :math:`\text{H}_{vapm}` is based on the mass fraction of vapor given off
for each of the mixtures constituents, not the liquid mass fractions. After a droplet has completely evaporated, the net  :math:`\text{H}_{vapm}` 
is based on the starting liquid droplet mass fraction.

Calculating the energy release characteristics in a thrust chamber is well beyond the scope of RocketProps.
For that reason, RocketProps assumes complete droplet evaporation and calculates mixture heat of vaporization :math:`\text{H}_{vapm}`
based on initial droplet mass fraction.


.. math::
    \text{H}_{vapm} = \sum_i \text{mass_frac}_i \cdot \text{H}_{vapi}    

Thermal Conductivity
--------------------


Calculation of mixture thermal conductivity (:math:`\lambda_m`) uses the Filippov correlation from
Caleb Bell, Yoel Rene Cortes-Pena, and Contributors (2016-2021). 
Chemicals: Chemical properties component of Chemical Engineering Design Library (ChEDL)
https://chemicals.readthedocs.io/chemicals.thermal_conductivity.html#liquid-mixing-rules.

Note that the Filippov correlation applies to binary mixtures only and that RocketProps currently only supports binary mixtures.

.. math::
    \lambda_m = w_1 \lambda_1 + w_2\lambda_2
    - 0.72 w_1 w_2(\lambda_2-\lambda_1)

For future RocketProps mixtures that might move beyond binary mixtures, the DIPPR9H correlation, 
also from the ChEDL, is included.


.. math::
    \lambda_m^{-2} = \frac{\sum_i z_i {MW}_i \lambda_i^{-2}}
    {\sum_i z_i {MW}_i}

Surface Tension
---------------

Calculation of mixture surface tension (:math:`\sigma_m`) uses the Winterfeld_Scriven_Davis correlation from
Caleb Bell, Yoel Rene Cortes-Pena, and Contributors (2016-2021). 
Chemicals: Chemical properties component of Chemical Engineering Design Library (ChEDL)
https://chemicals.readthedocs.io/chemicals.interface.html#mixing-rules.


.. math::
    \sigma_m = \sum_i \sum_j \frac{1}{V_L^{L2}}\left(x_i V_i \right)
    \left( x_jV_j\right)\sqrt{\sigma_i\cdot \sigma_j}


Viscosity
---------

The Chemical Engineering Design Library (ChEDL) for liquid mixture viscosity (:math:`\mu_m`)
recommends logarithmic mixing with weight fractions
https://chemicals.readthedocs.io/chemicals.viscosity.html#liquid-mixing-rules is:

With that in mind, mixture viscosity in RocketProps is calculated as:



.. math::
    \mu_m = \sum_i \text{massfrac}_i \cdot \ln(\mu_i)

