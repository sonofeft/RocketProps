
.. h2o2_prop

H2O2
====


Pure 100% peroxide is rarely used in rocketry due to its extreme sensitivity. 
Most "high-end" systems (like the Black Arrow or X-15) used 85% to 95%.

Critical Risk Thresholds
------------------------

There is a "Red Line" temperature for storing high-concentration HTP.
Beyond this point, the rate of decomposition increases exponentially, often exceeding the 
ability of the liquid to shed heat to the environment. 
This leads to Thermal Runaway.

The chart below illustrates the temperature range at which aqueous mixtures of peroxide can be used.

In that chart, the curve marked "Critical Risk" is considered a Tactical Emergency. 
If your tank sensors hit these numbers, the standard procedure (per AFRPL-TR-67-144) 
is usually to dump the propellant or initiate a "water deluge" to drown the reaction.

Contact with metals, dirt, or organic materials can trigger violent, immediate decomposition.

NOTE:

   3% to 70%: Assumes standard industrial stabilizers. These allow for storage at 25°C–35°C with only minor venting.

   85% to 90% (HTP): Specifically assumes the "Propellant Grade" (MIL-P-16005) stabilizers. 
   Without these, even trace amounts of aluminum, iron, or copper from the tank walls would trigger a decomposition chain well below 50°C.

   100% (Anhydrous)  :math:`\text{H}_2\text{O}_2` : Schumb and Satterfield noted that truly anhydrous, unstabilized peroxide 
   is so sensitive that it can decompose from light exposure or the roughness of a glass surface at room temperature (20∘C).   

    
.. image:: ./_static/Aq_peroxide_safety.png
   :width: 80%
   :target: ./_static/Aq_peroxide_safety.png
        
`Click Image to View Fill Size`


SAFETY LIMITATION: Consistent with Schumb et al. (1955) and AFRPL-TR-67-144, 
properties near the critical point are extrapolated. 
:math:`\text{H}_2\text{O}_2` is inherently unstable 
at these elevated temperatures; the presence of even trace contaminants will trigger instantaneous "runaway" decomposition.





Reference Points
----------------

H2O2 == Peroxide




`Hover over column headers to see definitions, values to see alternate units`

.. raw:: html

    <table width="100%">
    <tr><th></th>
        <th title="Reference Temperature">Tref</th>
        <th title="Reference Pressure">Pref</th>
        <th title="Specific Gravity">SG</th>
        <th title="Specific Heat">Cp</th>
        <th title="Heat of Vaporization">dHvap</th>
        <th title="Viscosity">Visc</th>
        <th title="Thermal Conductivity">Cond</th>
        <th title="Surface Tension">Surf</th>
    <tr><th>Source</th><th>R</th><th>psia</th><th>g/ml</th><th>BTU/lbm-R</th><th>BTU/lbm</th><th>poise</th><th>BTU/hr-ft-R</th><th>lbf/in</th></tr>


    <tr  style="background-color:#FFFF00"><td><a class="reference external" href="https://pypi.python.org/pypi/rocketprops">RocketProps</a></td><td  title="518.67 degR
    288.15 degK
    59 degF
    15 degC">518.7</td><td  title="0.0180115 psia
    0.00122561 atm
    0.00124185 bar
    0.000124185 MPa">0.0</td><td  title="1.45002 SG
    90.5219 lbm/ft**3
    0.0523853 lbm/inch**3
    1450.02 kg/m**3">1.4500</td><td  title="0.656853 BTU/lbm/F
    0.657292 cal/g/C
    0.000657292 kcal/g/C
    2750.11 J/kg/K">0.657</td><td  title="672.764 BTU/lbm
    374.008 cal/g
    0.374008 kcal/g
    1564.85 J/g">672.8</td><td  title="0.0136347 poise
    1.36347 cpoise
    0.00136347 Pa*s
    7.6351e-05 lbm/s/inch
    0.274863 lbm/hr/inch
    4.9085 kg/hr/m
    0.049085 kg/hr/cm">1.363e-02</td><td  title="0.25436 BTU/hr/ft/delF
    5.88796e-06 BTU/s/inch/delF
    0.00105217 cal/s/cm/delC
    0.105217 cal/s/m/delC
    0.00440229 W/cm/delC">0.2544</td><td  title="0.000464598 lbf/in
    0.0813637 N/m
    81.3637 mN/m
    81.3637 dyne/cm">4.646e-04</td></tr>
    <tr ><td><a class="reference external" href="./sources.html#crc-chemphyshandbook">CRC_ChemPhysHandbook</a></td><td  title="536.67 degR
    298.15 degK
    77 degF
    25 degC">536.7</td><td  title="14.7 psia
    1.00028 atm
    1.01353 bar
    0.101353 MPa">14.7</td><td  title="1.44 SG
    89.8963 lbm/ft**3
    0.0520233 lbm/inch**3
    1440 kg/m**3">1.4400</td><td >---</td><td  title="652.21 BTU/lbm
    362.581 cal/g
    0.362581 kcal/g
    1517.04 J/g">652.2</td><td >---</td><td >---</td><td >---</td></tr>
    <tr ><td><a class="reference external" href="./sources.html#schumb-mit">Gemini/Schumb</a></td><td  title="527.67 degR
    293.15 degK
    68 degF
    20 degC">527.7</td><td  title="0.0262 psia
    0.0017828 atm
    0.00180643 bar
    0.000180643 MPa">0.0</td><td  title="1.44357 SG
    90.1193 lbm/ft**3
    0.0521524 lbm/inch**3
    1443.57 kg/m**3">1.4436</td><td  title="0.661944 BTU/lbm/F
    0.662387 cal/g/C
    0.000662387 kcal/g/C
    2771.43 J/kg/K">0.662</td><td  title="669.175 BTU/lbm
    372.012 cal/g
    0.372012 kcal/g
    1556.5 J/g">669.2</td><td  title="0.0124599 poise
    1.24599 cpoise
    0.00124599 Pa*s
    6.97723e-05 lbm/s/inch
    0.25118 lbm/hr/inch
    4.48557 kg/hr/m
    0.0448557 kg/hr/cm">1.246e-02</td><td  title="0.257694 BTU/hr/ft/delF
    5.96514e-06 BTU/s/inch/delF
    0.00106597 cal/s/cm/delC
    0.106597 cal/s/m/delC
    0.00446 W/cm/delC">0.2577</td><td  title="0.000458543 lbf/in
    0.0803032 N/m
    80.3032 mN/m
    80.3032 dyne/cm">4.585e-04</td></tr>
    <tr ><td><a class="reference external" href="./_static/Aerojet_Propellant_Properties.pdf">Aerojet</a></td><td  title="527.67 degR
    293.15 degK
    68 degF
    20 degC">527.7</td><td  title="14.6959 psia
    0.999997 atm
    1.01325 bar
    0.101325 MPa">14.7</td><td  title="1.45052 SG
    90.5528 lbm/ft**3
    0.0524032 lbm/inch**3
    1450.52 kg/m**3">1.4505</td><td  title="0.634006 BTU/lbm/F
    0.63443 cal/g/C
    0.00063443 kcal/g/C
    2654.46 J/kg/K">0.634</td><td  title="596 BTU/lbm
    331.333 cal/g
    0.331333 kcal/g
    1386.3 J/g">596.0</td><td  title="0.0101336 poise
    1.01336 cpoise
    0.00101336 Pa*s
    5.67453e-05 lbm/s/inch
    0.204283 lbm/hr/inch
    3.64808 kg/hr/m
    0.0364808 kg/hr/cm">1.013e-02</td><td  title="0.278195 BTU/hr/ft/delF
    6.4397e-06 BTU/s/inch/delF
    0.00115077 cal/s/cm/delC
    0.115077 cal/s/m/delC
    0.00481482 W/cm/delC">0.2782</td><td >---</td></tr>

    </table>





Fluid Properties
----------------

H2O2 == Peroxide




`Hover over column headers to see definitions, values to see alternate units`

.. raw:: html

    <table width="100%">
    <tr><th></th>
        <th title="Molecular Weight">MolWt</th>
        <th title="Critical Temperature">Tc</th>
        <th title="Critical Pressure">Pc</th>
        <th title="Critical Density">SGc</th>
        <th title="Critical Compressibility Factor">Zc</th>
        <th title="Normal Boiling Point">Tnbp</th>
        <th title="Melting/Freezing Point">Tmelt</th>
        <th title="Pitzer Acentric Factor">omega</th></tr>
    <tr><th>Source</th><th>g/gmole</th><th>R</th><th>psia</th><th>g/ml</th><th>(-)</th><th>R</th><th>R</th><th>(-)</th></tr>


    <tr  style="background-color:#FFFF00"><td><a class="reference external" href="https://pypi.python.org/pypi/rocketprops">RocketProps</a></td><td>34.015</td><td  title="1314.36 degR
    730.2 degK
    854.69 degF
    457.05 degC">1314.4</td><td  title="3144.42 psia
    213.965 atm
    216.8 bar
    21.68 MPa">3144.4</td><td  title="0.468 SG
    29.2163 lbm/ft**3
    0.0169076 lbm/inch**3
    468 kg/m**3">0.4680</td><td>0.2596</td><td  title="762.03 degR
    423.35 degK
    302.36 degF
    150.2 degC">762.0</td><td  title="490.896 degR
    272.72 degK
    31.226 degF
    -0.43 degC">490.9</td><td>0.38954</td></tr>
    <tr ><td><a class="reference external" href="./sources.html#crc-chemphyshandbook">CRC_ChemPhysHandbook</a></td><td>34.015</td><td  title="1310.4 degR
    728 degK
    850.73 degF
    454.85 degC">1310.4</td><td  title="3190.83 psia
    217.123 atm
    220 bar
    22 MPa">3190.8</td><td >---</td><td>---</td><td  title="762.12 degR
    423.4 degK
    302.45 degF
    150.25 degC">762.1</td><td  title="490.896 degR
    272.72 degK
    31.226 degF
    -0.43 degC">490.9</td><td>---</td></tr>
    <tr ><td><a class="reference external" href="./sources.html#refprop-source">Gemini/Refprop</a></td><td>34.015</td><td  title="1314.27 degR
    730.15 degK
    854.6 degF
    457 degC">1314.3</td><td  title="3144.42 psia
    213.965 atm
    216.8 bar
    21.68 MPa">3144.4</td><td  title="0.468 SG
    29.2163 lbm/ft**3
    0.0169076 lbm/inch**3
    468 kg/m**3">0.4680</td><td>0.2596</td><td  title="762.12 degR
    423.4 degK
    302.45 degF
    150.25 degC">762.1</td><td  title="490.86 degR
    272.7 degK
    31.19 degF
    -0.45 degC">490.9</td><td>0.59100</td></tr>
    <tr ><td><a class="reference external" href="./sources.html#schumb-mit">Gemini/Schumb</a></td><td>34.015</td><td  title="1314.36 degR
    730.2 degK
    854.69 degF
    457.05 degC">1314.4</td><td  title="3144.42 psia
    213.965 atm
    216.8 bar
    21.68 MPa">3144.4</td><td  title="0.468 SG
    29.2163 lbm/ft**3
    0.0169076 lbm/inch**3
    468 kg/m**3">0.4680</td><td>0.2596</td><td  title="762.03 degR
    423.35 degK
    302.36 degF
    150.2 degC">762.0</td><td  title="490.896 degR
    272.72 degK
    31.226 degF
    -0.43 degC">490.9</td><td>0.38954</td></tr>
    <tr ><td><a class="reference external" href="./_static/Aerojet_Propellant_Properties.pdf">Aerojet</a></td><td>34.016</td><td  title="1314.67 degR
    730.372 degK
    855 degF
    457.222 degC">1314.7</td><td  title="3146 psia
    214.073 atm
    216.909 bar
    21.6909 MPa">3146.0</td><td  title="0.461164 SG
    28.7895 lbm/ft**3
    0.0166606 lbm/inch**3
    461.164 kg/m**3">0.4612</td><td>0.2635</td><td  title="762.07 degR
    423.372 degK
    302.4 degF
    150.222 degC">762.1</td><td  title="490.87 degR
    272.706 degK
    31.2 degF
    -0.444444 degC">490.9</td><td>0.32031</td></tr>

    </table>





Vapor Pressure
--------------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Psat.png
   :target: ./_static/H2O2_Psat.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`thermo Source`
| :ref:`Copilot Source`
| :ref:`NIST Webbook`
| :ref:`AFRPL-TR-67-144 Source`
| :ref:`Schumb-MIT Source`
| :ref:`Gemini Source`
| :ref:`Wagner Fit Source`



.. image:: ./_static/H2O2_Psat_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Psat_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_Pvap.png
   :target: ./_static/Aq_peroxide_Pvap.png



Density
-------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_SG.png
   :target: ./_static/H2O2_SG.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Aerojet Source`
| :ref:`thermo Source`
| :ref:`Copilot Source`
| :ref:`Schumb-MIT Source`
| :ref:`Gemini Source`
| :ref:`Rackett Scaling Source`



.. image:: ./_static/H2O2_SG_Tc.png
   :width: 20%
   :target: ./_static/H2O2_SG_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_SG.png
   :target: ./_static/Aq_peroxide_SG.png


Heat Capacity
-------------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Cp.png
   :target: ./_static/H2O2_Cp.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Aerojet Source`
| :ref:`Copilot Source`
| :ref:`Schumb-MIT Source`
| :ref:`Gemini Source`



.. image:: ./_static/H2O2_Cp_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Cp_Tc.png



.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_Cp.png
   :target: ./_static/Aq_peroxide_Cp.png


Viscosity
---------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Visc.png
   :target: ./_static/H2O2_Visc.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Aerojet Source`
| :ref:`thermo Source`
| :ref:`Copilot Source`
| :ref:`Squires Source`
| :ref:`Schumb-MIT Source`
| :ref:`Gemini Source`


.. image:: ./_static/H2O2_Visc_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Visc_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`
    
.. image:: ./_static/Aq_peroxide_visc.png
   :target: ./_static/Aq_peroxide_visc.png


Heat of Vaporization
--------------------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Hvap.png
   :target: ./_static/H2O2_Hvap.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Aerojet Source`
| :ref:`Pitzer Hvap Source`
| :ref:`thermo Source`
| :ref:`Gemini Source`
| :ref:`AFRPL-TR-67-144 Source`


.. image:: ./_static/H2O2_Hvap_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Hvap_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_Hvap.png
   :target: ./_static/Aq_peroxide_Hvap.png

Thermal Conductivity
--------------------




.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Cond.png
   :target: ./_static/H2O2_Cond.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Aerojet Source`
| :ref:`Nicola Source`
| :ref:`Copilot Source`
| :ref:`Gemini Source`


.. image:: ./_static/H2O2_Cond_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Cond_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_cond.png
   :target: ./_static/Aq_peroxide_cond.png


Surface Tension
---------------

    

.. raw:: html

    <div class="columns">
        <div style="width:75%;float:left" >
    
.. image:: ./_static/H2O2_Surf.png
   :target: ./_static/H2O2_Surf.png
    

.. raw:: html

    </div><div ><br><br>

| RocketProps Selected Curve
| :ref:`Schumb-MIT Source`
| :ref:`thermo Source`
| :ref:`Copilot Source`
| :ref:`Gemini Source`


.. image:: ./_static/H2O2_Surf_Tc.png
   :width: 20%
   :target: ./_static/H2O2_Surf_Tc.png


.. raw:: html

    </div></div>
    <div style="clear:both"></div>

    
`Click Image to View Fill Size`

    
.. image:: ./_static/Aq_peroxide_surf.png
   :target: ./_static/Aq_peroxide_surf.png


