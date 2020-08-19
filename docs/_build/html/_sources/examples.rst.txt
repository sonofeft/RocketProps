
.. examples


Examples
========

The following examples demonstrate the use of RocketProps.

Propellant Tank Volume
----------------------

There is a function within RocketProps to calculate the required volume of a propellant tank.

Use **rocketprops.tank_supt.calc_tank_volume** as in the code below.

.. code-block:: python

    from rocketprops.tank_supt import calc_tank_volume
    from rocketprops.rocket_prop import get_prop
    """
    Calculate the required volume of a Hydrazine (N2H4) tank.
    Assume:
        required usable propellant is 50 kg
        vehicle max operating/storage/transport temperature is 50 deg C.
        minimum ullage volume is 3%.
        expulsion efficiency = 98%.
    """
    pObj = get_prop('N2H4')

    cc_Total, kg_loaded, kg_residual = calc_tank_volume( pObj, kg_expelled=50.0,
                                                         TmaxC=50.0, expPcent=98.0, ullPcent=3.0 )
    print('cc_Total    = %g cc'%cc_Total)
    print('loaded   propellant mass = %g kg'%kg_loaded )
    print('residual propellant mass =  %g kg'%kg_residual )

Output from the above script is::

    cc_Total    = 53510.4 cc
    loaded   propellant mass = 51.0526 kg
    residual propellant mass =  1.05263 kg

Propellant Line
---------------

Propellant line calculations are supported by  **rocketprops.line_supt**.

Given a desired flow rate of propellant, calculate the diameter and pressure drop
in a propellant line.

Can input mass flow rate and line velocity, or mass flow rate and inside diameter.

.. code-block:: python

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


Output from the above script is::

    Inside Diam=0.334523 inches, Pressure Drop =9.66264 psid
    Velocity = 13 ft/sec, Pressure Drop =9.66264 psid


Injector Orifice
----------------

Some injector orifice calculations are supported with **rocketprops.injector_supt**.

The script below calculates the injection velocity and mass flow rate for a sample N2O4 injector.

.. code-block:: python

    from rocketprops.rocket_prop import get_prop
    from rocketprops.injector_supt import calc_inj_velocity, calc_orifice_flow_rate

    """
    Calculate the injection velocity of an injector orifice and its mass flow rate
    """
    pObj = get_prop( 'N2O4' )
    ft_per_sec = calc_inj_velocity( pObj, dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)
    print( 'velocity =',ft_per_sec, 'ft/s' )

    wdot = calc_orifice_flow_rate(pObj, CdOrf=0.75, DiamInches=0.01,
                           dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)
    print( 'Orifice flow rate =',wdot , 'lbm/sec' )

Output from the above script is::

    velocity = 71.7716993053127 ft/s
    Orifice flow rate = 0.00264060215451235 lbm/sec
