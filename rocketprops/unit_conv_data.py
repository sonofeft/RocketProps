#from __future__ import print_function
#print('NOTE:  Remove __future__ statement in unit_conv_data.py')

categoryD = {}    # index=category name, value=list of members (e.g. 'Area':['inch**2', 'ft**2', 'cm**2', 'm**2'])
cat_defaultD = {} # index=category name, value=default units (e.g. 'Area':'inch**2')
unit_catD = {}    # index=units name, value=category (e.g. 'inch':'Length')
conv_factD = {}   # index=units name, value=float conversion value to default units (e.g. 'cm':1.0/2.54)
offsetD = {}      # index=units name, value=float offset value (e.g. 'cm':0.0)

# N = 1 kg-m/sec**2,  g = 9.80665 m/sec**2


# Read As: 1 default unit = conv_factD target units
# === Acceleration ===
categoryD["Acceleration"] = ['ft/s**2', 'm/s**2', 'cm/s**2', 'gee', 'mile/hr/s']
cat_defaultD["Acceleration"] = 'ft/s**2'
unit_catD["ft/s**2"]  = "Acceleration"
conv_factD["ft/s**2"] = float(1)
offsetD["ft/s**2"]    = float(0)
unit_catD["m/s**2"]  = "Acceleration"
conv_factD["m/s**2"] = float(0.3048)
offsetD["m/s**2"]    = float(0)
unit_catD["cm/s**2"]  = "Acceleration"
conv_factD["cm/s**2"] = float(30.48)
offsetD["cm/s**2"]    = float(0)
unit_catD["gee"]  = "Acceleration"
conv_factD["gee"] = float(0.031080948777)
offsetD["gee"]    = float(0)
unit_catD["mile/hr/s"]  = "Acceleration"
conv_factD["mile/hr/s"] = float(0.681818181818)
offsetD["mile/hr/s"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Angle ===
categoryD["Angle"] = ['deg', 'rad', 'grad', 'circle', 'revolution', 'arcmin', 'arcsec']
cat_defaultD["Angle"] = 'deg'
unit_catD["deg"]  = "Angle"
conv_factD["deg"] = float(1)
offsetD["deg"]    = float(0)
unit_catD["rad"]  = "Angle"
conv_factD["rad"] = float(0.0174532925199)
offsetD["rad"]    = float(0)
unit_catD["grad"]  = "Angle"
conv_factD["grad"] = float(1.11111111111)
offsetD["grad"]    = float(0)
unit_catD["circle"]  = "Angle"
conv_factD["circle"] = float(0.00277777777778)
offsetD["circle"]    = float(0)
unit_catD["revolution"]  = "Angle"
conv_factD["revolution"] = float(0.00277777777778)
offsetD["revolution"]    = float(0)
unit_catD["arcmin"]  = "Angle"
conv_factD["arcmin"] = float(60)
offsetD["arcmin"]    = float(0)
unit_catD["arcsec"]  = "Angle"
conv_factD["arcsec"] = float(3600)
offsetD["arcsec"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === AngVelocity ===
categoryD["AngVelocity"] = ['rpm', 'deg/s', 'rad/s', 'deg/min', 'rad/min']
cat_defaultD["AngVelocity"] = 'rpm'
unit_catD["rpm"]  = "AngVelocity"
conv_factD["rpm"] = float(1)
offsetD["rpm"]    = float(0)
unit_catD["deg/s"]  = "AngVelocity"
conv_factD["deg/s"] = float(6)
offsetD["deg/s"]    = float(0)
unit_catD["rad/s"]  = "AngVelocity"
conv_factD["rad/s"] = float(0.10471975512)
offsetD["rad/s"]    = float(0)
unit_catD["deg/min"]  = "AngVelocity"
conv_factD["deg/min"] = float(360)
offsetD["deg/min"]    = float(0)
unit_catD["rad/min"]  = "AngVelocity"
conv_factD["rad/min"] = float(6.28318530718)
offsetD["rad/min"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Area ===
categoryD["Area"] = ['inch**2', 'ft**2', 'cm**2', 'm**2', 'mile**2', 'acre']
cat_defaultD["Area"] = 'inch**2'
unit_catD["inch**2"]  = "Area"
conv_factD["inch**2"] = float(1)
offsetD["inch**2"]    = float(0)
unit_catD["ft**2"]  = "Area"
conv_factD["ft**2"] = float(0.00694444444444)
offsetD["ft**2"]    = float(0)
unit_catD["cm**2"]  = "Area"
conv_factD["cm**2"] = float(6.4516)
offsetD["cm**2"]    = float(0)
unit_catD["m**2"]  = "Area"
conv_factD["m**2"] = float(0.00064516)
offsetD["m**2"]    = float(0)
unit_catD["mile**2"]  = "Area"
conv_factD["mile**2"] = float(2.49097668605e-10)
offsetD["mile**2"]    = float(0)
unit_catD["acre"]  = "Area"
conv_factD["acre"] = float(1.59422507907e-07)
offsetD["acre"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === DeltaT ===
categoryD["DeltaT"] = ['delF', 'delC', 'delR', 'delK']
cat_defaultD["DeltaT"] = 'delF'
unit_catD["delF"]  = "DeltaT"
conv_factD["delF"] = float(1)
offsetD["delF"]    = float(0)
unit_catD["delC"]  = "DeltaT"
conv_factD["delC"] = float(5.0/9.0)
offsetD["delC"]    = float(0)
unit_catD["delR"]  = "DeltaT"
conv_factD["delR"] = float(1)
offsetD["delR"]    = float(0)
unit_catD["delK"]  = "DeltaT"
conv_factD["delK"] = float(5.0/9.0)
offsetD["delK"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Density ===
categoryD["Density"] = ['lbm/inch**3', 'lbm/ft**3', 'slug/ft**3', 'g/ml', 'specific_gravity', 'kg/m**3', 'lbm/galUS', 'ounce/galUS']
cat_defaultD["Density"] = 'lbm/inch**3'
unit_catD["lbm/inch**3"]  = "Density"
conv_factD["lbm/inch**3"] = float(1)
offsetD["lbm/inch**3"]    = float(0)
unit_catD["lbm/in**3"]  = "Density"
conv_factD["lbm/in**3"] = float(1)
offsetD["lbm/in**3"]    = float(0)
unit_catD["lbm/ft**3"]  = "Density"
conv_factD["lbm/ft**3"] = float(1728)
offsetD["lbm/ft**3"]    = float(0)
unit_catD["slug/ft**3"]  = "Density"
conv_factD["slug/ft**3"] = float(53.7078794867)
offsetD["slug/ft**3"]    = float(0)
unit_catD["g/ml"]  = "Density"
conv_factD["g/ml"] = float(27.6799047102)
offsetD["g/ml"]    = float(0)
unit_catD["specific_gravity"]  = "Density"
conv_factD["specific_gravity"] = float(27.6799047102)
offsetD["specific_gravity"]    = float(0)
unit_catD["kg/m**3"]  = "Density"
conv_factD["kg/m**3"] = float(27679.9047102)
offsetD["kg/m**3"]    = float(0)
unit_catD["lbm/galUS"]  = "Density"
conv_factD["lbm/galUS"] = float(231)
offsetD["lbm/galUS"]    = float(0)
unit_catD["ounce/galUS"]  = "Density"
conv_factD["ounce/galUS"] = float(3696)
offsetD["ounce/galUS"]    = float(0)
unit_catD["SG"]  = "Density"
conv_factD["SG"] = float(27.6799047102)
offsetD["SG"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Energy ===
categoryD["Energy"] = ['BTU', 'ft*lbf', 'W*hr', 'kW*hr', 'cal', 'kcal', 'J', 'kJ', 'erg']
cat_defaultD["Energy"] = 'BTU'
unit_catD["BTU"]  = "Energy"
conv_factD["BTU"] = float(1)
offsetD["BTU"]    = float(0)
unit_catD["ft*lbf"]  = "Energy"
conv_factD["ft*lbf"] = float(778.169262266)
offsetD["ft*lbf"]    = float(0)
unit_catD["W*hr"]  = "Energy"
conv_factD["W*hr"] = float(0.293071070172)
offsetD["W*hr"]    = float(0)
unit_catD["kW*hr"]  = "Energy"
conv_factD["kW*hr"] = float(0.000293071070172)
offsetD["kW*hr"]    = float(0)
unit_catD["cal"]  = "Energy"
conv_factD["cal"] = float(252.164400722)
offsetD["cal"]    = float(0)
unit_catD["kcal"]  = "Energy"
conv_factD["kcal"] = float(0.252164400722)
offsetD["kcal"]    = float(0)
unit_catD["J"]  = "Energy"
conv_factD["J"] = float(1055.05585262)
offsetD["J"]    = float(0)
unit_catD["kJ"]  = "Energy"
conv_factD["kJ"] = float(1.05505585262)
offsetD["kJ"]    = float(0)
unit_catD["erg"]  = "Energy"
conv_factD["erg"] = float(10550558526.2)
offsetD["erg"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === EnergySpec ===
categoryD["EnergySpec"] = ['BTU/lbm', 'cal/g', 'kcal/g', 'kcal/kg', 'J/g', 'kJ/kg', 'J/kg', 'kW*hr/kg']
cat_defaultD["EnergySpec"] = 'BTU/lbm'
unit_catD["BTU/lbm"]  = "EnergySpec"
conv_factD["BTU/lbm"] = float(1)
offsetD["BTU/lbm"]    = float(0)
unit_catD["cal/g"]  = "EnergySpec"
conv_factD["cal/g"] = float(0.555927342256)
offsetD["cal/g"]    = float(0)
unit_catD["kcal/g"]  = "EnergySpec"
conv_factD["kcal/g"] = float(0.000555927342256)
offsetD["kcal/g"]    = float(0)
unit_catD["kcal/kg"]  = "EnergySpec"
conv_factD["kcal/kg"] = float(0.555927342256)
offsetD["kcal/kg"]    = float(0)
unit_catD["J/g"]  = "EnergySpec"
conv_factD["J/g"] = float(2.326)
offsetD["J/g"]    = float(0)
unit_catD["kJ/kg"]  = "EnergySpec"
conv_factD["kJ/kg"] = float(2.326)
offsetD["kJ/kg"]    = float(0)

unit_catD["J/kg"]  = "EnergySpec"
conv_factD["J/kg"] = float(2326)
offsetD["J/kg"]    = float(0)

unit_catD["kW*hr/kg"]  = "EnergySpec"
conv_factD["kW*hr/kg"] = float(0.000646111111111)
offsetD["kW*hr/kg"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Force ===
categoryD["Force"] = ['lbf', 'N', 'kN', 'dyn'] # N = 1 kg-m/sec**2
cat_defaultD["Force"] = 'lbf'
unit_catD["lbf"]  = "Force"
conv_factD["lbf"] = float(1)
offsetD["lbf"]    = float(0)
unit_catD["N"]  = "Force"
conv_factD["N"] = float(4.44822161526)
offsetD["N"]    = float(0)
unit_catD["kN"]  = "Force"
conv_factD["kN"] = float(0.00444822161526)
offsetD["kN"]    = float(0)
unit_catD["dyn"]  = "Force"
conv_factD["dyn"] = float(444822.161526)
offsetD["dyn"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === HeatCapacity ===
categoryD["HeatCapacity"] = ['BTU/lbm/delF', 'cal/g/delC', 'kcal/g/delC', 'J/kg/delK', 'kJ/kg/delK']
cat_defaultD["HeatCapacity"] = 'BTU/lbm/delF'
unit_catD["BTU/lbm/delF"]  = "HeatCapacity"
conv_factD["BTU/lbm/delF"] = float(1)
offsetD["BTU/lbm/delF"]    = float(0)
unit_catD["cal/g/delC"]  = "HeatCapacity"
conv_factD["cal/g/delC"] = float(1.00066921606)
offsetD["cal/g/delC"]    = float(0)
unit_catD["kcal/g/delC"]  = "HeatCapacity"
conv_factD["kcal/g/delC"] = float(0.00100066921606)
offsetD["kcal/g/delC"]    = float(0)
unit_catD["J/kg/delK"]  = "HeatCapacity"
conv_factD["J/kg/delK"] = float(4186.8)
offsetD["J/kg/delK"]    = float(0)
unit_catD["kJ/kg/delK"]  = "HeatCapacity"
conv_factD["kJ/kg/delK"] = float(4.1868)
offsetD["kJ/kg/delK"]    = float(0)

unit_catD["BTU/lbm/degF"]  = "HeatCapacity"
conv_factD["BTU/lbm/degF"] = float(1)
offsetD["BTU/lbm/degF"]    = float(0)
unit_catD["cal/g/degC"]  = "HeatCapacity"
conv_factD["cal/g/degC"] = float(1.00066921606)
offsetD["cal/g/degC"]    = float(0)
unit_catD["kcal/g/degC"]  = "HeatCapacity"
conv_factD["kcal/g/degC"] = float(0.00100066921606)
offsetD["kcal/g/degC"]    = float(0)
unit_catD["J/kg/degK"]  = "HeatCapacity"
conv_factD["J/kg/degK"] = float(4186.8)
offsetD["J/kg/degK"]    = float(0)
unit_catD["kJ/kg/degK"]  = "HeatCapacity"
conv_factD["kJ/kg/degK"] = float(4.1868)
offsetD["kJ/kg/degK"]    = float(0)

unit_catD["BTU/lbm/F"]  = "HeatCapacity"
conv_factD["BTU/lbm/F"] = float(1)
offsetD["BTU/lbm/F"]    = float(0)
unit_catD["cal/g/C"]  = "HeatCapacity"
conv_factD["cal/g/C"] = float(1.00066921606)
offsetD["cal/g/C"]    = float(0)
unit_catD["kcal/g/C"]  = "HeatCapacity"
conv_factD["kcal/g/C"] = float(0.00100066921606)
offsetD["kcal/g/C"]    = float(0)
unit_catD["J/kg/K"]  = "HeatCapacity"
conv_factD["J/kg/K"] = float(4186.8)
offsetD["J/kg/K"]    = float(0)
unit_catD["kJ/kg/K"]  = "HeatCapacity"
conv_factD["kJ/kg/K"] = float(4.1868)
offsetD["kJ/kg/K"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === HxCoeff ===
categoryD["HxCoeff"] = ['BTU/inch**2/s/delF', 'BTU/ft**2/hr/delF', 'cal/cm**2/s/delC', 'kcal/m**2/hr/delC', 'W/m**2/delC']
cat_defaultD["HxCoeff"] = 'BTU/inch**2/s/delF'
unit_catD["BTU/inch**2/s/delF"]  = "HxCoeff"
conv_factD["BTU/inch**2/s/delF"] = float(1)
offsetD["BTU/inch**2/s/delF"]    = float(0)
unit_catD["BTU/ft**2/hr/delF"]  = "HxCoeff"
conv_factD["BTU/ft**2/hr/delF"] = float(518400)
offsetD["BTU/ft**2/hr/delF"]    = float(0)
unit_catD["cal/cm**2/s/delC"]  = "HxCoeff"
conv_factD["cal/cm**2/s/delC"] = float(70.3540085094)
offsetD["cal/cm**2/s/delC"]    = float(0)
unit_catD["kcal/m**2/hr/delC"]  = "HxCoeff"
conv_factD["kcal/m**2/hr/delC"] = float(2532744.30634)
offsetD["kcal/m**2/hr/delC"]    = float(0)
unit_catD["W/m**2/delC"]  = "HxCoeff"
conv_factD["W/m**2/delC"] = float(2943611.71603)
offsetD["W/m**2/delC"]    = float(0)

unit_catD["BTU/inch**2/s/degF"]  = "HxCoeff"
conv_factD["BTU/inch**2/s/degF"] = float(1)
offsetD["BTU/inch**2/s/degF"]    = float(0)
unit_catD["BTU/ft**2/hr/degF"]  = "HxCoeff"
conv_factD["BTU/ft**2/hr/degF"] = float(518400)
offsetD["BTU/ft**2/hr/degF"]    = float(0)
unit_catD["cal/cm**2/s/degC"]  = "HxCoeff"
conv_factD["cal/cm**2/s/degC"] = float(70.3540085094)
offsetD["cal/cm**2/s/degC"]    = float(0)
unit_catD["kcal/m**2/hr/degC"]  = "HxCoeff"
conv_factD["kcal/m**2/hr/degC"] = float(2532744.30634)
offsetD["kcal/m**2/hr/degC"]    = float(0)
unit_catD["W/m**2/degC"]  = "HxCoeff"
conv_factD["W/m**2/degC"] = float(2943611.71603)
offsetD["W/m**2/degC"]    = float(0)

unit_catD["BTU/inch**2/s/F"]  = "HxCoeff"
conv_factD["BTU/inch**2/s/F"] = float(1)
offsetD["BTU/inch**2/s/F"]    = float(0)
unit_catD["BTU/ft**2/hr/F"]  = "HxCoeff"
conv_factD["BTU/ft**2/hr/F"] = float(518400)
offsetD["BTU/ft**2/hr/F"]    = float(0)
unit_catD["cal/cm**2/s/C"]  = "HxCoeff"
conv_factD["cal/cm**2/s/C"] = float(70.3540085094)
offsetD["cal/cm**2/s/C"]    = float(0)
unit_catD["kcal/m**2/hr/C"]  = "HxCoeff"
conv_factD["kcal/m**2/hr/C"] = float(2532744.30634)
offsetD["kcal/m**2/hr/C"]    = float(0)
unit_catD["W/m**2/C"]  = "HxCoeff"
conv_factD["W/m**2/C"] = float(2943611.71603)
offsetD["W/m**2/C"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Length ===
categoryD["Length"] = ['inch', 'mil', 'ft', 'yd', 'mm', 'cm', 'm', 'km', 'mile', 'nautical_mile', 'angstrom', 'astronomical_unit', 'light_year']
cat_defaultD["Length"] = 'inch'
unit_catD["inch"]  = "Length"
conv_factD["inch"] = float(1)
offsetD["inch"]    = float(0)
unit_catD["mil"]  = "Length"
conv_factD["mil"] = float(1000)
offsetD["mil"]    = float(0)
unit_catD["ft"]  = "Length"
conv_factD["ft"] = float(0.0833333333333)
offsetD["ft"]    = float(0)
unit_catD["yd"]  = "Length"
conv_factD["yd"] = float(0.0277777777778)
offsetD["yd"]    = float(0)
unit_catD["mm"]  = "Length"
conv_factD["mm"] = float(25.4)
offsetD["mm"]    = float(0)
unit_catD["cm"]  = "Length"
conv_factD["cm"] = float(2.54)
offsetD["cm"]    = float(0)
unit_catD["m"]  = "Length"
conv_factD["m"] = float(0.0254)
offsetD["m"]    = float(0)
unit_catD["km"]  = "Length"
conv_factD["km"] = float(2.54e-05)
offsetD["km"]    = float(0)
unit_catD["mile"]  = "Length"
conv_factD["mile"] = float(1.57828282828e-05)
offsetD["mile"]    = float(0)
unit_catD["nautical_mile"]  = "Length"
conv_factD["nautical_mile"] = float(1.37149377616e-05)
offsetD["nautical_mile"]    = float(0)
unit_catD["angstrom"]  = "Length"
conv_factD["angstrom"] = float(254000000)
offsetD["angstrom"]    = float(0)
unit_catD["astronomical_unit"]  = "Length"
conv_factD["astronomical_unit"] = float(1.69788512916e-13)
offsetD["astronomical_unit"]    = float(0)
unit_catD["light_year"]  = "Length"
conv_factD["light_year"] = float(2.6847819948e-18)
offsetD["light_year"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Mass ===
categoryD["Mass"] = ['lbm', 'slug', 'g', 'kg', 'metric_ton', 'short_ton', 'long_ton', 'gal_H2O']
cat_defaultD["Mass"] = 'lbm'
unit_catD["lbm"]  = "Mass"
conv_factD["lbm"] = float(1)
offsetD["lbm"]    = float(0)
unit_catD["slug"]  = "Mass"
conv_factD["slug"] = float(0.031080948777)
offsetD["slug"]    = float(0)
unit_catD["g"]  = "Mass"
conv_factD["g"] = float(453.59237)
offsetD["g"]    = float(0)
unit_catD["kg"]  = "Mass"
conv_factD["kg"] = float(0.45359237)
offsetD["kg"]    = float(0)
unit_catD["metric_ton"]  = "Mass"
conv_factD["metric_ton"] = float(0.00045359237)
offsetD["metric_ton"]    = float(0)
unit_catD["short_ton"]  = "Mass"
conv_factD["short_ton"] = float(0.0005)
offsetD["short_ton"]    = float(0)
unit_catD["long_ton"]  = "Mass"
conv_factD["long_ton"] = float(0.000446428571429)
offsetD["long_ton"]    = float(0)
unit_catD["gal_H2O"]  = "Mass"
conv_factD["gal_H2O"] = float(0.120048019208)
offsetD["gal_H2O"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === MassFlow ===
categoryD["MassFlow"] = ['lbm/s', 'kg/s', 'g/s', 'lbm/min', 'kg/min', 'g/min', 'lbm/hr', 'kg/hr', 'g/hr']
cat_defaultD["MassFlow"] = 'lbm/s'
unit_catD["lbm/s"]  = "MassFlow"
conv_factD["lbm/s"] = float(1)
offsetD["lbm/s"]    = float(0)
unit_catD["kg/s"]  = "MassFlow"
conv_factD["kg/s"] = float(0.45359237)
offsetD["kg/s"]    = float(0)
unit_catD["g/s"]  = "MassFlow"
conv_factD["g/s"] = float(453.59237)
offsetD["g/s"]    = float(0)
unit_catD["lbm/min"]  = "MassFlow"
conv_factD["lbm/min"] = float(60)
offsetD["lbm/min"]    = float(0)
unit_catD["kg/min"]  = "MassFlow"
conv_factD["kg/min"] = float(27.2155422)
offsetD["kg/min"]    = float(0)
unit_catD["g/min"]  = "MassFlow"
conv_factD["g/min"] = float(27215.5422)
offsetD["g/min"]    = float(0)
unit_catD["lbm/hr"]  = "MassFlow"
conv_factD["lbm/hr"] = float(3600)
offsetD["lbm/hr"]    = float(0)
unit_catD["kg/hr"]  = "MassFlow"
conv_factD["kg/hr"] = float(1632.932532)
offsetD["kg/hr"]    = float(0)
unit_catD["g/hr"]  = "MassFlow"
conv_factD["g/hr"] = float(1632932.532)
offsetD["g/hr"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Power ===
categoryD["Power"] = ['hp', 'Btu/s', 'Btu/hr', 'cal/s', 'W', 'kW', 'MW', 'ft*lbf/s']
cat_defaultD["Power"] = 'hp'
unit_catD["hp"]  = "Power"
conv_factD["hp"] = float(1)
offsetD["hp"]    = float(0)
unit_catD["Btu/s"]  = "Power"
conv_factD["Btu/s"] = float(0.706787226618)
offsetD["Btu/s"]    = float(0)
unit_catD["Btu/hr"]  = "Power"
conv_factD["Btu/hr"] = float(2544.43401582)
offsetD["Btu/hr"]    = float(0)
unit_catD["cal/s"]  = "Power"
conv_factD["cal/s"] = float(178.226577438)
offsetD["cal/s"]    = float(0)
unit_catD["W"]  = "Power"
conv_factD["W"] = float(745.7)
offsetD["W"]    = float(0)
unit_catD["kW"]  = "Power"
conv_factD["kW"] = float(0.7457)
offsetD["kW"]    = float(0)
unit_catD["MW"]  = "Power"
conv_factD["MW"] = float(0.0007457)
offsetD["MW"]    = float(0)
unit_catD["ft*lbf/s"]  = "Power"
conv_factD["ft*lbf/s"] = float(550.000094716)
offsetD["ft*lbf/s"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Pressure ===
categoryD["Pressure"] = ['psia', 'atm', 'MPa', 'kPa', 'Pa', 'psf', 'bar', 'torr', 'inHg', 'mmHg', 'lbf/inch**2', 'lbf/ft**2', 'N/cm**2', 'N/m**2']
cat_defaultD["Pressure"] = 'psia'
unit_catD["psia"]  = "Pressure"
conv_factD["psia"] = float(1)
offsetD["psia"]    = float(0)
unit_catD["psid"]  = "Pressure"
conv_factD["psid"] = float(1)
offsetD["psid"]    = float(0)
unit_catD["atm"]  = "Pressure"
conv_factD["atm"] = float(0.0680459639099)
offsetD["atm"]    = float(0)
unit_catD["MPa"]  = "Pressure"
conv_factD["MPa"] = float(0.00689475729317)
offsetD["MPa"]    = float(0)
unit_catD["kPa"]  = "Pressure"
conv_factD["kPa"] = float(6.89475729317)
offsetD["kPa"]    = float(0)
unit_catD["Pa"]  = "Pressure"
conv_factD["Pa"] = float(6894.75729317)
offsetD["Pa"]    = float(0)
unit_catD["psf"]  = "Pressure"
conv_factD["psf"] = float(144)
offsetD["psf"]    = float(0)
unit_catD["bar"]  = "Pressure"
conv_factD["bar"] = float(0.0689475729317)
offsetD["bar"]    = float(0)
unit_catD["torr"]  = "Pressure"
conv_factD["torr"] = float(51.7149325715)
offsetD["torr"]    = float(0)
unit_catD["inHg"]  = "Pressure"
conv_factD["inHg"] = float(2.036021)
offsetD["inHg"]    = float(0)
unit_catD["mmHg"]  = "Pressure"
conv_factD["mmHg"] = float(51.71493)
offsetD["mmHg"]    = float(0)
unit_catD["lbf/inch**2"]  = "Pressure"
conv_factD["lbf/inch**2"] = float(1)
offsetD["lbf/inch**2"]    = float(0)
unit_catD["lbf/ft**2"]  = "Pressure"
conv_factD["lbf/ft**2"] = float(144)
offsetD["lbf/ft**2"]    = float(0)
unit_catD["N/cm**2"]  = "Pressure"
conv_factD["N/cm**2"] = float(0.689475729317)
offsetD["N/cm**2"]    = float(0)
unit_catD["N/m**2"]  = "Pressure"
conv_factD["N/m**2"] = float(6894.75729317)
offsetD["N/m**2"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Surface Tension ===
categoryD["SurfaceTension"] = ['lbf/in', 'N/m', 'mN/m', 'dyne/cm']
cat_defaultD["SurfaceTension"] = 'lbf/in'
unit_catD["lbf/in"]  = "SurfaceTension"
conv_factD["lbf/in"] = float(1)
offsetD["lbf/in"]    = float(0)
unit_catD["N/m"]  = "SurfaceTension"
conv_factD["N/m"] = float(175.126836986)
offsetD["N/m"]    = float(0)
unit_catD["mN/m"]  = "SurfaceTension"
conv_factD["mN/m"] = 1000.0 * float(175.126836986)
offsetD["mN/m"]    = float(0)
unit_catD["dyne/cm"]  = "SurfaceTension"
conv_factD["dyne/cm"] = float(175126.83698643)
offsetD["dyne/cm"]    = float(0)
unit_catD["lbf/ft"]  = "SurfaceTension"
conv_factD["lbf/ft"] = float(12)
offsetD["lbf/ft"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Temperature ===
# conv_factD["degK"](5.0/9.0) * 'degR' = 'degK'
categoryD["Temperature"] = ['degR', 'degF', 'degK', 'degC']
cat_defaultD["Temperature"] = 'degR'
unit_catD["degR"]  = "Temperature"
conv_factD["degR"] = float(1)
offsetD["degR"]    = float(0)
unit_catD["degF"]  = "Temperature"
conv_factD["degF"] = float(1)
offsetD["degF"]    = float(-459.67)
unit_catD["degK"]  = "Temperature"
conv_factD["degK"] = float(5.0/9.0)
offsetD["degK"]    = float(0)
unit_catD["degC"]  = "Temperature"
conv_factD["degC"] = float(5.0/9.0)
offsetD["degC"]    = float(-273.15)

# Read As: 1 default unit = conv_factD target units
# === ThermalCond ===
categoryD["ThermalCond"] = ['BTU/hr/ft/delF', 'BTU/s/inch/delF', 'cal/s/cm/delC', 'cal/s/m/delC', 'W/cm/delC']
cat_defaultD["ThermalCond"] = 'BTU/hr/ft/delF'
unit_catD["BTU/hr/ft/delF"]  = "ThermalCond"
conv_factD["BTU/hr/ft/delF"] = float(1)
offsetD["BTU/hr/ft/delF"]    = float(0)
unit_catD["BTU/s/inch/delF"]  = "ThermalCond"
conv_factD["BTU/s/inch/delF"] = float(2.31481481481e-05)
offsetD["BTU/s/inch/delF"]    = float(0)
unit_catD["cal/s/cm/delC"]  = "ThermalCond"
conv_factD["cal/s/cm/delC"] = float(0.00413655512995)
offsetD["cal/s/cm/delC"]    = float(0)
unit_catD["cal/s/m/delC"]  = "ThermalCond"
conv_factD["cal/s/m/delC"] = float(0.413655512995)
offsetD["cal/s/m/delC"]    = float(0)
unit_catD["W/cm/delC"]  = "ThermalCond"
conv_factD["W/cm/delC"] = float(0.0173073466637)
offsetD["W/cm/delC"]    = float(0)
unit_catD["W/m/K"]  = "ThermalCond"
conv_factD["W/m/K"] = float(1.73073466637)
offsetD["W/m/K"]    = float(0)

unit_catD["BTU/hr/ft/degF"]  = "ThermalCond"
conv_factD["BTU/hr/ft/degF"] = float(1)
offsetD["BTU/hr/ft/degF"]    = float(0)
unit_catD["BTU/s/inch/degF"]  = "ThermalCond"
conv_factD["BTU/s/inch/degF"] = float(2.31481481481e-05)
offsetD["BTU/s/inch/degF"]    = float(0)
unit_catD["cal/s/cm/degC"]  = "ThermalCond"
conv_factD["cal/s/cm/degC"] = float(0.00413655512995)
offsetD["cal/s/cm/degC"]    = float(0)
unit_catD["cal/s/m/degC"]  = "ThermalCond"
conv_factD["cal/s/m/degC"] = float(0.413655512995)
offsetD["cal/s/m/degC"]    = float(0)
unit_catD["W/cm/degC"]  = "ThermalCond"
conv_factD["W/cm/degC"] = float(0.0173073466637)
offsetD["W/cm/degC"]    = float(0)

unit_catD["BTU/hr/ft/F"]  = "ThermalCond"
conv_factD["BTU/hr/ft/F"] = float(1)
offsetD["BTU/hr/ft/F"]    = float(0)
unit_catD["BTU/s/inch/F"]  = "ThermalCond"
conv_factD["BTU/s/inch/F"] = float(2.31481481481e-05)
offsetD["BTU/s/inch/F"]    = float(0)
unit_catD["cal/s/cm/C"]  = "ThermalCond"
conv_factD["cal/s/cm/C"] = float(0.00413655512995)
offsetD["cal/s/cm/C"]    = float(0)
unit_catD["cal/s/m/C"]  = "ThermalCond"
conv_factD["cal/s/m/C"] = float(0.413655512995)
offsetD["cal/s/m/C"]    = float(0)
unit_catD["W/cm/C"]  = "ThermalCond"
conv_factD["W/cm/C"] = float(0.0173073466637)
offsetD["W/cm/C"]    = float(0)


unit_catD["BTU/s/ft/delF"]  = "ThermalCond"
conv_factD["BTU/s/ft/delF"] = float(1/3600.0)
offsetD["BTU/s/ft/delF"]    = float(0)
unit_catD["BTU/s/ft/degF"]  = "ThermalCond"
conv_factD["BTU/s/ft/degF"] = float(1/3600.0)
offsetD["BTU/s/ft/degF"]    = float(0)
unit_catD["BTU/s/ft/F"]  = "ThermalCond"
conv_factD["BTU/s/ft/F"] = float(1/3600.0)
offsetD["BTU/s/ft/F"]    = float(0)


# Read As: 1 default unit = conv_factD target units
# === Time ===
categoryD["Time"] = ['s', 'ms', 'min', 'hr', 'day', 'year', 'millisec', 'microsec', 'nanosec']
cat_defaultD["Time"] = 's'
unit_catD["s"]  = "Time"
conv_factD["s"] = float(1)
offsetD["s"]    = float(0)
unit_catD["ms"]  = "Time"
conv_factD["ms"] = float(1000)
offsetD["ms"]    = float(0)
unit_catD["min"]  = "Time"
conv_factD["min"] = float(0.0166666666667)
offsetD["min"]    = float(0)
unit_catD["hr"]  = "Time"
conv_factD["hr"] = float(0.000277777777778)
offsetD["hr"]    = float(0)
unit_catD["day"]  = "Time"
conv_factD["day"] = float(1.15740740741e-05)
offsetD["day"]    = float(0)
unit_catD["year"]  = "Time"
conv_factD["year"] = float(3.16887646408e-08)
offsetD["year"]    = float(0)
unit_catD["millisec"]  = "Time"
conv_factD["millisec"] = float(1000)
offsetD["millisec"]    = float(0)
unit_catD["microsec"]  = "Time"
conv_factD["microsec"] = float(1000000)
offsetD["microsec"]    = float(0)
unit_catD["nanosec"]  = "Time"
conv_factD["nanosec"] = float(1000000000)
offsetD["nanosec"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Velocity ===
categoryD["Velocity"] = ['ft/s', 'inch/s', 'cm/s', 'm/s', 'km/hr', 'mile/hr']
cat_defaultD["Velocity"] = 'ft/s'
unit_catD["ft/s"]  = "Velocity"
conv_factD["ft/s"] = float(1)
offsetD["ft/s"]    = float(0)
unit_catD["inch/s"]  = "Velocity"
conv_factD["inch/s"] = float(12)
offsetD["inch/s"]    = float(0)
unit_catD["cm/s"]  = "Velocity"
conv_factD["cm/s"] = float(30.48)
offsetD["cm/s"]    = float(0)
unit_catD["m/s"]  = "Velocity"
conv_factD["m/s"] = float(0.3048)
offsetD["m/s"]    = float(0)
unit_catD["km/hr"]  = "Velocity"
conv_factD["km/hr"] = float(1.09728)
offsetD["km/hr"]    = float(0)
unit_catD["mile/hr"]  = "Velocity"
conv_factD["mile/hr"] = float(0.681818181818)
offsetD["mile/hr"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Viscosity_Dynamic ===
categoryD["Viscosity_Dynamic"] = ['poise', 'cpoise', 'Pa*s', 'lbm/s/inch', 'lbm/hr/inch', 'lbm/s/ft', 'lbm/hr/ft', 'kg/s/m', 'kg/hr/m', 'kg/s/cm', 'kg/hr/cm']
cat_defaultD["Viscosity_Dynamic"] = 'poise'
unit_catD["poise"]  = "Viscosity_Dynamic"
conv_factD["poise"] = float(1)
offsetD["poise"]    = float(0)
unit_catD["cpoise"]  = "Viscosity_Dynamic"
conv_factD["cpoise"] = float(100)
offsetD["cpoise"]    = float(0)
unit_catD["cp"]  = "Viscosity_Dynamic"
conv_factD["cp"] = float(100)
offsetD["cp"]    = float(0)
unit_catD["Pa*s"]  = "Viscosity_Dynamic"
conv_factD["Pa*s"] = float(0.1)
offsetD["Pa*s"]    = float(0)
unit_catD["cp"]  = "Viscosity_Dynamic"
conv_factD["cp"] = float(100)
offsetD["cpoise"]    = float(0)
unit_catD["lbm/s/inch"]  = "Viscosity_Dynamic"
conv_factD["lbm/s/inch"] = float(0.0055997414595)
offsetD["lbm/s/inch"]    = float(0)
unit_catD["lbm/hr/inch"]  = "Viscosity_Dynamic"
conv_factD["lbm/hr/inch"] = float(20.1590692542)
offsetD["lbm/hr/inch"]    = float(0)
unit_catD["lbm/s/ft"]  = "Viscosity_Dynamic"
conv_factD["lbm/s/ft"] = float(0.067196897514)
offsetD["lbm/s/ft"]    = float(0)
unit_catD["lbm/hr/ft"]  = "Viscosity_Dynamic"
conv_factD["lbm/hr/ft"] = float(241.90883105)
offsetD["lbm/hr/ft"]    = float(0)
unit_catD["kg/s/m"]  = "Viscosity_Dynamic"
conv_factD["kg/s/m"] = float(0.1)
offsetD["kg/s/m"]    = float(0)
unit_catD["kg/hr/m"]  = "Viscosity_Dynamic"
conv_factD["kg/hr/m"] = float(360)
offsetD["kg/hr/m"]    = float(0)
unit_catD["kg/s/cm"]  = "Viscosity_Dynamic"
conv_factD["kg/s/cm"] = float(0.001)
offsetD["kg/s/cm"]    = float(0)
unit_catD["kg/hr/cm"]  = "Viscosity_Dynamic"
conv_factD["kg/hr/cm"] = float(3.6)
offsetD["kg/hr/cm"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Viscosity_Kinematic ===
categoryD["Viscosity_Kinematic"] = ['ft**2/s', 'ft**2/hr', 'stokes', 'centistokes', 'm**2/s']
cat_defaultD["Viscosity_Kinematic"] = 'ft**2/s'
unit_catD["ft**2/s"]  = "Viscosity_Kinematic"
conv_factD["ft**2/s"] = float(1)
offsetD["ft**2/s"]    = float(0)
unit_catD["ft**2/hr"]  = "Viscosity_Kinematic"
conv_factD["ft**2/hr"] = float(3600)
offsetD["ft**2/hr"]    = float(0)
unit_catD["stokes"]  = "Viscosity_Kinematic"
conv_factD["stokes"] = float(929.0304)
offsetD["stokes"]    = float(0)
unit_catD["centistokes"]  = "Viscosity_Kinematic"
conv_factD["centistokes"] = float(92903.04)
offsetD["centistokes"]    = float(0)
unit_catD["m**2/s"]  = "Viscosity_Kinematic"
conv_factD["m**2/s"] = float(0.09290304)
offsetD["m**2/s"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === Volume ===
categoryD["Volume"] = ['inch**3', 'ft**3', 'cm**3', 'liter', 'm**3', 'yd**3', 'barOil', 'cup', 'pint', 'quart', 'galUS', 'galUK']
cat_defaultD["Volume"] = 'inch**3'
unit_catD["inch**3"]  = "Volume"
conv_factD["inch**3"] = float(1)
offsetD["inch**3"]    = float(0)
unit_catD["ft**3"]  = "Volume"
conv_factD["ft**3"] = float(0.000578703703704)
offsetD["ft**3"]    = float(0)
unit_catD["cm**3"]  = "Volume"
conv_factD["cm**3"] = float(16.387064)
offsetD["cm**3"]    = float(0)
unit_catD["liter"]  = "Volume"
conv_factD["liter"] = float(0.016387064)
offsetD["liter"]    = float(0)
unit_catD["m**3"]  = "Volume"
conv_factD["m**3"] = float(1.6387064e-05)
offsetD["m**3"]    = float(0)
unit_catD["yd**3"]  = "Volume"
conv_factD["yd**3"] = float(2.14334705075e-05)
offsetD["yd**3"]    = float(0)
unit_catD["barOil"]  = "Volume"
conv_factD["barOil"] = float(0.000103071531643)
offsetD["barOil"]    = float(0)
unit_catD["cup"]  = "Volume"
conv_factD["cup"] = float(0.0692640692641)
offsetD["cup"]    = float(0)
unit_catD["pint"]  = "Volume"
conv_factD["pint"] = float(0.034632034632)
offsetD["pint"]    = float(0)
unit_catD["quart"]  = "Volume"
conv_factD["quart"] = float(0.017316017316)
offsetD["quart"]    = float(0)
unit_catD["galUS"]  = "Volume"
conv_factD["galUS"] = float(0.004329004329)
offsetD["galUS"]    = float(0)
unit_catD["galUK"]  = "Volume"
conv_factD["galUK"] = float(0.00360465014991)
offsetD["galUK"]    = float(0)

# Read As: 1 default unit = conv_factD target units
# === VolumeFlow ===
categoryD["VolumeFlow"] = ['inch**3/s', 'inch**3/min', 'inch**3/hr', 'ft**3/s', 'ft**3/min', 'ft**3/hr', 'ml/s', 'ml/min', 'ml/hr', 'm**3/s', 'l/s', 'galUS/s', 'galUS/min', 'galUS/hr', 'galUS/day']
cat_defaultD["VolumeFlow"] = 'inch**3/s'
unit_catD["inch**3/s"]  = "VolumeFlow"
conv_factD["inch**3/s"] = float(1)
offsetD["inch**3/s"]    = float(0)
unit_catD["inch**3/min"]  = "VolumeFlow"
conv_factD["inch**3/min"] = float(60)
offsetD["inch**3/min"]    = float(0)
unit_catD["inch**3/hr"]  = "VolumeFlow"
conv_factD["inch**3/hr"] = float(3600)
offsetD["inch**3/hr"]    = float(0)
unit_catD["ft**3/s"]  = "VolumeFlow"
conv_factD["ft**3/s"] = float(0.000578703703704)
offsetD["ft**3/s"]    = float(0)
unit_catD["ft**3/min"]  = "VolumeFlow"
conv_factD["ft**3/min"] = float(0.0347222222222)
offsetD["ft**3/min"]    = float(0)
unit_catD["ft**3/hr"]  = "VolumeFlow"
conv_factD["ft**3/hr"] = float(2.08333333333)
offsetD["ft**3/hr"]    = float(0)
unit_catD["ml/s"]  = "VolumeFlow"
conv_factD["ml/s"] = float(16.387064)
offsetD["ml/s"]    = float(0)
unit_catD["ml/min"]  = "VolumeFlow"
conv_factD["ml/min"] = float(983.22384)
offsetD["ml/min"]    = float(0)
unit_catD["ml/hr"]  = "VolumeFlow"
conv_factD["ml/hr"] = float(58993.4304)
offsetD["ml/hr"]    = float(0)
unit_catD["m**3/s"]  = "VolumeFlow"
conv_factD["m**3/s"] = float(1.6387064e-05)
offsetD["m**3/s"]    = float(0)
unit_catD["m**3/hr"]  = "VolumeFlow"
conv_factD["m**3/hr"] = float(3600*1.6387064e-05)
offsetD["m**3/hr"]    = float(0)
unit_catD["l/s"]  = "VolumeFlow"
conv_factD["l/s"] = float(0.016387064)
offsetD["l/s"]    = float(0)
unit_catD["galUS/s"]  = "VolumeFlow"
conv_factD["galUS/s"] = float(0.004329004329)
offsetD["galUS/s"]    = float(0)
unit_catD["gpm"]  = "VolumeFlow"
conv_factD["gpm"] = float(0.25974025974)
offsetD["gpm"]    = float(0)
unit_catD["galUS/min"]  = "VolumeFlow"
conv_factD["galUS/min"] = float(0.25974025974)
offsetD["galUS/min"]    = float(0)
unit_catD["galUS/hr"]  = "VolumeFlow"
conv_factD["galUS/hr"] = float(15.5844155844)
offsetD["galUS/hr"]    = float(0)
unit_catD["galUS/day"]  = "VolumeFlow"
conv_factD["galUS/day"] = float(374.025974026)
offsetD["galUS/day"]    = float(0)

# Read As: 1 default unit = conv_factD target units
def get_value( inp_val=20.0, inp_units='degC', out_units='degK'):
    """Convert inp_val from inp_units to out_units and return.
        :param inp_val   : input value to be converted
        :param inp_units : units of inp_val
        :param out_units : desired output units
        :type inp_val   : float
        :type inp_units : str
        :type out_units : str
        :return: value converted from inp_units to out_units
        :rtype: float
    """
    # convert inp_val to default units
    def_unit_val = (inp_val - offsetD[inp_units]) / conv_factD[inp_units]
    # convert from default units to requested output units
    return def_unit_val * conv_factD[out_units] + offsetD[out_units]
    
# ============== some common conversions ===================
def get_degK( val, inp_units ):
    """ val uses input units... e.g. 25, 'degC' """
    return get_value( inp_val=float( val ), inp_units=inp_units, out_units='degK')
    
def get_degR( val, inp_units ):
    """ val uses input units... e.g. 25, 'degC' """
    return get_value(  inp_val=float( val ), inp_units=inp_units, out_units='degR')

if __name__ == "__main__":

    categoryL = list( categoryD.keys() )
    categoryL.sort(key=str.lower)
    for i,cat in enumerate(categoryL):
        print( '%s(%i %s)'%(cat, len(categoryD[cat]), cat_defaultD[cat]), end=' ' )
        if i>0 and i%5==0:
            print()
    print()
    
    MAX_UNIT_CHARS = 0
    for unit in conv_factD.keys():
        MAX_UNIT_CHARS = max( MAX_UNIT_CHARS, len(unit) )

    UNIT_FMT_STR = '%%%is'%MAX_UNIT_CHARS

    print( 'MAX_UNIT_CHARS =',MAX_UNIT_CHARS )
    
    for units in ['degC','degF','degK','degR']:
        print( '20C =', '%g'%get_value( 20.0, 'degC', units), units )
        
    for units in ['degC','degF','degK','degR']:
        print( '20 %s ='%units, '%g'%get_degK( 20.0, units ), 
               'degK  = ', '%g'%get_degR( 20.0, units ), 'degR' )
    
    
    print( 'Check SurfaceTension:', get_value(1.0, 'lbf/in', 'N/m'), get_value(1.0, 'lbf/in', 'dyne/cm') )
    
