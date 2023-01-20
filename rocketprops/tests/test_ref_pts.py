
import unittest
# import unittest2 as unittest # for versions of python < 2.7

"""
        Method                            Checks that
self.assertEqual(a, b)                      a == b   
self.assertNotEqual(a, b)                   a != b   
self.assertTrue(x)                          bool(x) is True  
self.assertFalse(x)                         bool(x) is False     
self.assertIs(a, b)                         a is b
self.assertIsNot(a, b)                      a is not b
self.assertIsNone(x)                        x is None 
self.assertIsNotNone(x)                     x is not None 
self.assertIn(a, b)                         a in b
self.assertNotIn(a, b)                      a not in b
self.assertIsInstance(a, b)                 isinstance(a, b)  
self.assertNotIsInstance(a, b)              not isinstance(a, b)  
self.assertAlmostEqual(a, b, places=5)      a within 5 decimal places of b
self.assertNotAlmostEqual(a, b, delta=0.1)  a is not within 0.1 of b
self.assertGreater(a, b)                    a is > b
self.assertGreaterEqual(a, b)               a is >= b
self.assertLess(a, b)                       a is < b
self.assertLessEqual(a, b)                  a is <= b

for expected exceptions, use:

with self.assertRaises(Exception):
    blah...blah...blah

with self.assertRaises(KeyError):
    blah...blah...blah

Test if __name__ == "__main__":
    def test__main__(self):
        # loads and runs the bottom section: if __name__ == "__main__"
        runpy = imp.load_source('__main__', os.path.join(up_one, 'filename.py') )

    # for python >= 3.7
    def test__main__(self):
        # loads and runs the bottom section: if __name__ == "__main__"
        from importlib.machinery import SourceFileLoader

        script_path = os.path.abspath( os.path.join(up_one, 'filename.py') )
        SourceFileLoader("__main__", script_path).load_module()


See:
      https://docs.python.org/2/library/unittest.html
         or
      https://docs.python.org/dev/library/unittest.html
for more assert options
"""

import sys, os

here = os.path.abspath(os.path.dirname(__file__)) # Needed for py.test
up_one = os.path.split( here )[0]  # Needed to find models development version
if here not in sys.path[:2]:
    sys.path.insert(0, here)
if up_one not in sys.path[:2]:
    sys.path.insert(0, up_one)

from rocketprops.rocket_prop import get_prop; 

class MyTest(unittest.TestCase):

    def test_A50_ref_pts(self):
        """Test A50 reference points with interpolator calls"""
        prop = get_prop( "A50" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 2.3611, places=None, delta=0.00023611)
        self.assertAlmostEqual(prop.Pc, 1731, places=None, delta=0.1731)
        self.assertAlmostEqual(prop.Tc, 1092.67, places=None, delta=0.109267)
        self.assertAlmostEqual(prop.SG, 0.903547, places=None, delta=9.03547e-05)
        self.assertAlmostEqual(prop.visc, 0.00920868, places=None, delta=9.20868e-07)
        self.assertAlmostEqual(prop.cond, 0.166107, places=None, delta=1.66107e-05)
        self.assertAlmostEqual(prop.Tnbp, 617.67, places=None, delta=0.061767)
        self.assertAlmostEqual(prop.Tfreeze, 481.67, places=None, delta=0.048167)
        self.assertAlmostEqual(prop.Cp, 0.728232, places=None, delta=7.28232e-05)
        self.assertAlmostEqual(prop.MolWt, 41.802, places=None, delta=0.0041802)
        self.assertAlmostEqual(prop.Hvap, 346.5, places=None, delta=0.03465)
        self.assertAlmostEqual(prop.surf, 0.000169873, places=None, delta=1.69873e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.82918e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00047222)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.84174e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=3.32213e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000145646)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0693)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.39746e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000180709)
        SGvap = 2.823412e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.82341e-08)
        Z = 3.090671e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.09067e-08)
        Z = 9.890754e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.89075e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00047222)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.84174e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=3.32213e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000145646)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0693)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.39746e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000180709)
        SGvap = 2.823412e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.82341e-08)
        Z = 3.090671e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.09067e-08)
        Z = 9.890754e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.89075e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=9.03547e-05)

    def test_CLF5_ref_pts(self):
        """Test CLF5 reference points with interpolator calls"""
        prop = get_prop( "CLF5" )
        self.assertAlmostEqual(prop.T, 468.208, places=None, delta=0.0468208)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pc, 771, places=None, delta=0.0771)
        self.assertAlmostEqual(prop.Tc, 749.07, places=None, delta=0.074907)
        self.assertAlmostEqual(prop.SG, 1.90998, places=None, delta=0.000190998)
        self.assertAlmostEqual(prop.visc, 0.00464742, places=None, delta=4.64742e-07)
        self.assertAlmostEqual(prop.cond, 0.0587355, places=None, delta=5.87355e-06)
        self.assertAlmostEqual(prop.Tnbp, 466.97, places=None, delta=0.046697)
        self.assertAlmostEqual(prop.Tfreeze, 306.27, places=None, delta=0.030627)
        self.assertAlmostEqual(prop.Cp, 0.282844, places=None, delta=2.82844e-05)
        self.assertAlmostEqual(prop.MolWt, 130.445, places=None, delta=0.0130445)
        self.assertAlmostEqual(prop.Hvap, 76.0399, places=None, delta=0.00760399)
        self.assertAlmostEqual(prop.surf, 0.000120409, places=None, delta=1.20409e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0468208)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.25053e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.936416)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=4.40877)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=9.29484e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.17471e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=5.65687e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.015208)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.40817e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000381996)
        SGvap = 6.428538e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=6.42854e-07)
        Z = 3.148642e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.14864e-07)
        Z = 9.354910e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.35491e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=4.40877)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=9.29484e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.17471e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=5.65687e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.015208)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.40817e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000381996)
        SGvap = 6.428538e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=6.42854e-07)
        Z = 3.148642e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.14864e-07)
        Z = 9.354910e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.35491e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000190998)

    def test_Ethane_ref_pts(self):
        """Test Ethane reference points with interpolator calls"""
        prop = get_prop( "Ethane" )
        self.assertAlmostEqual(prop.T, 332.224, places=None, delta=0.0332224)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6963, places=None, delta=0.00146963)
        self.assertAlmostEqual(prop.Pc, 706.653, places=None, delta=0.0706653)
        self.assertAlmostEqual(prop.Tc, 549.58, places=None, delta=0.054958)
        self.assertAlmostEqual(prop.SG, 0.543829, places=None, delta=5.43829e-05)
        self.assertAlmostEqual(prop.visc, 0.0016637, places=None, delta=1.6637e-07)
        self.assertAlmostEqual(prop.cond, 0.0965368, places=None, delta=9.65368e-06)
        self.assertAlmostEqual(prop.Tnbp, 332.224, places=None, delta=0.0332224)
        self.assertAlmostEqual(prop.Tfreeze, 162.662, places=None, delta=0.0162662)
        self.assertAlmostEqual(prop.Cp, 0.582661, places=None, delta=5.82661e-05)
        self.assertAlmostEqual(prop.MolWt, 30.069, places=None, delta=0.0030069)
        self.assertAlmostEqual(prop.Hvap, 210.547, places=None, delta=0.0210547)
        self.assertAlmostEqual(prop.surf, 9.15615e-05, places=None, delta=9.15615e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0332224)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.04506e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0332224)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293925)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=3.32741e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.93074e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.00116532)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0421093)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.83123e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000108766)
        SGvap = 2.054518e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.05452e-07)
        Z = 3.651684e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.65168e-07)
        Z = 9.665956e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.66596e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293925)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=3.32741e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.93074e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.00116532)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0421093)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.83123e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000108766)
        SGvap = 2.054518e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.05452e-07)
        Z = 3.651684e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.65168e-07)
        Z = 9.665956e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.66596e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=5.43829e-05)

    def test_Ethanol_ref_pts(self):
        """Test Ethanol reference points with interpolator calls"""
        prop = get_prop( "Ethanol" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 0.85928, places=None, delta=8.5928e-05)
        self.assertAlmostEqual(prop.Pvap, 0.85928, places=None, delta=8.5928e-05)
        self.assertAlmostEqual(prop.Pc, 891.692, places=None, delta=0.0891692)
        self.assertAlmostEqual(prop.Tc, 925.02, places=None, delta=0.092502)
        self.assertAlmostEqual(prop.SG, 0.78959, places=None, delta=7.8959e-05)
        self.assertAlmostEqual(prop.visc, 0.0119519, places=None, delta=1.19519e-06)
        self.assertAlmostEqual(prop.cond, 0.096156, places=None, delta=9.6156e-06)
        self.assertAlmostEqual(prop.Tnbp, 632.502, places=None, delta=0.0632502)
        self.assertAlmostEqual(prop.Tfreeze, 286.29, places=None, delta=0.028629)
        self.assertAlmostEqual(prop.Cp, 0.600415, places=None, delta=6.00415e-05)
        self.assertAlmostEqual(prop.MolWt, 46.0684, places=None, delta=0.00460684)
        self.assertAlmostEqual(prop.Hvap, 398.636, places=None, delta=0.0398636)
        self.assertAlmostEqual(prop.surf, 0.000127988, places=None, delta=1.27988e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.70442e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000171856)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.39037e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.92312e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000120083)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0797271)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.55976e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000157918)
        SGvap = 1.124039e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.12404e-08)
        Z = 1.418469e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.41847e-08)
        Z = 9.964120e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.96412e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000171856)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.39037e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.92312e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000120083)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0797271)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.55976e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000157918)
        SGvap = 1.124039e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.12404e-08)
        Z = 1.418469e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.41847e-08)
        Z = 9.964120e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.96412e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=7.8959e-05)

    def test_F2_ref_pts(self):
        """Test F2 reference points with interpolator calls"""
        prop = get_prop( "F2" )
        self.assertAlmostEqual(prop.T, 153.066, places=None, delta=0.0153066)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.696, places=None, delta=0.0014696)
        self.assertAlmostEqual(prop.Pc, 750.193, places=None, delta=0.0750193)
        self.assertAlmostEqual(prop.Tc, 259.945, places=None, delta=0.0259945)
        self.assertAlmostEqual(prop.SG, 1.5018, places=None, delta=0.00015018)
        self.assertAlmostEqual(prop.visc, 0.00242217, places=None, delta=2.42217e-07)
        self.assertAlmostEqual(prop.cond, 0.0777162, places=None, delta=7.77162e-06)
        self.assertAlmostEqual(prop.Tnbp, 153.066, places=None, delta=0.0153066)
        self.assertAlmostEqual(prop.Tfreeze, 96.266, places=None, delta=0.0096266)
        self.assertAlmostEqual(prop.Cp, 0.360896, places=None, delta=3.60896e-05)
        self.assertAlmostEqual(prop.MolWt, 37.9968, places=None, delta=0.00379968)
        self.assertAlmostEqual(prop.Hvap, 75.0142, places=None, delta=0.00750142)
        self.assertAlmostEqual(prop.surf, 7.62121e-05, places=None, delta=7.62121e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0153066)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.8884e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0153066)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293919)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=4.84433e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=0.000155432)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000721792)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0150028)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.52424e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000300361)
        SGvap = 5.641246e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=5.64125e-07)
        Z = 3.626676e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.62668e-07)
        Z = 9.654881e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.65488e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293919)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=4.84433e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=0.000155432)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000721792)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0150028)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.52424e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000300361)
        SGvap = 5.641246e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=5.64125e-07)
        Z = 3.626676e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.62668e-07)
        Z = 9.654881e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.65488e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.00015018)

    def test_IRFNA_ref_pts(self):
        """Test IRFNA reference points with interpolator calls"""
        prop = get_prop( "IRFNA" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 2.13588, places=None, delta=0.000213588)
        self.assertAlmostEqual(prop.Pc, 1286, places=None, delta=0.1286)
        self.assertAlmostEqual(prop.Tc, 979.67, places=None, delta=0.097967)
        self.assertAlmostEqual(prop.SG, 1.57624, places=None, delta=0.000157624)
        self.assertAlmostEqual(prop.visc, 0.0131885, places=None, delta=1.31885e-06)
        self.assertAlmostEqual(prop.cond, 0.169211, places=None, delta=1.69211e-05)
        self.assertAlmostEqual(prop.Tnbp, 607.67, places=None, delta=0.060767)
        self.assertAlmostEqual(prop.Tfreeze, 403.67, places=None, delta=0.040367)
        self.assertAlmostEqual(prop.Cp, 0.419083, places=None, delta=4.19083e-05)
        self.assertAlmostEqual(prop.MolWt, 59.7, places=None, delta=0.00597)
        self.assertAlmostEqual(prop.Hvap, 247, places=None, delta=0.0247)
        self.assertAlmostEqual(prop.surf, 0.000266522, places=None, delta=2.66522e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.3862e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000427175)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.6377e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=3.38423e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=8.38166e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0494)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=5.33045e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000315248)
        SGvap = 3.653676e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=3.65368e-08)
        Z = 2.288868e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.28887e-08)
        Z = 9.874447e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.87445e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000427175)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.6377e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=3.38423e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=8.38166e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0494)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=5.33045e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000315248)
        SGvap = 3.653676e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=3.65368e-08)
        Z = 2.288868e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.28887e-08)
        Z = 9.874447e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.87445e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000157624)

    def test_LOX_ref_pts(self):
        """Test LOX reference points with interpolator calls"""
        prop = get_prop( "LOX" )
        self.assertAlmostEqual(prop.T, 162.338, places=None, delta=0.0162338)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pc, 731.425, places=None, delta=0.0731425)
        self.assertAlmostEqual(prop.Tc, 278.246, places=None, delta=0.0278246)
        self.assertAlmostEqual(prop.SG, 1.14117, places=None, delta=0.000114117)
        self.assertAlmostEqual(prop.visc, 0.00194672, places=None, delta=1.94672e-07)
        self.assertAlmostEqual(prop.cond, 0.0871745, places=None, delta=8.71745e-06)
        self.assertAlmostEqual(prop.Tnbp, 162.338, places=None, delta=0.0162338)
        self.assertAlmostEqual(prop.Tfreeze, 97.8498, places=None, delta=0.00978498)
        self.assertAlmostEqual(prop.Cp, 0.405886, places=None, delta=4.05886e-05)
        self.assertAlmostEqual(prop.MolWt, 31.9988, places=None, delta=0.00319988)
        self.assertAlmostEqual(prop.Hvap, 91.6588, places=None, delta=0.00916588)
        self.assertAlmostEqual(prop.surf, 7.52227e-05, places=None, delta=7.52227e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0162338)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.83434e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0162338)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293919)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=3.89344e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.74349e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000811773)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0183318)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.50445e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000228235)
        SGvap = 4.466968e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=4.46697e-07)
        Z = 3.789750e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.78975e-07)
        Z = 9.681673e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.68167e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293919)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=3.89344e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.74349e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000811773)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0183318)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.50445e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000228235)
        SGvap = 4.466968e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=4.46697e-07)
        Z = 3.789750e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.78975e-07)
        Z = 9.681673e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.68167e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000114117)

    def test_Methane_ref_pts(self):
        """Test Methane reference points with interpolator calls"""
        prop = get_prop( "Methane" )
        self.assertAlmostEqual(prop.T, 201.001, places=None, delta=0.0201001)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6957, places=None, delta=0.00146957)
        self.assertAlmostEqual(prop.Pc, 667.057, places=None, delta=0.0667057)
        self.assertAlmostEqual(prop.Tc, 343.015, places=None, delta=0.0343015)
        self.assertAlmostEqual(prop.SG, 0.422357, places=None, delta=4.22357e-05)
        self.assertAlmostEqual(prop.visc, 0.00116808, places=None, delta=1.16808e-07)
        self.assertAlmostEqual(prop.cond, 0.106233, places=None, delta=1.06233e-05)
        self.assertAlmostEqual(prop.Tnbp, 201.001, places=None, delta=0.0201001)
        self.assertAlmostEqual(prop.Tfreeze, 163.35, places=None, delta=0.016335)
        self.assertAlmostEqual(prop.Cp, 0.831998, places=None, delta=8.31998e-05)
        self.assertAlmostEqual(prop.MolWt, 16.0428, places=None, delta=0.00160428)
        self.assertAlmostEqual(prop.Hvap, 219.764, places=None, delta=0.0219764)
        self.assertAlmostEqual(prop.surf, 7.59241e-05, places=None, delta=7.59241e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0201001)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.85982e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0201001)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293914)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.33617e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.12466e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.0001664)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0439527)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.51848e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=8.44714e-05)
        SGvap = 1.816384e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.81638e-07)
        Z = 4.146179e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=4.14618e-07)
        Z = 9.640953e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.64095e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293914)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.33617e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.12466e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.0001664)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0439527)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.51848e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=8.44714e-05)
        SGvap = 1.816384e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.81638e-07)
        Z = 4.146179e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=4.14618e-07)
        Z = 9.640953e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.64095e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=4.22357e-05)

    def test_Methanol_ref_pts(self):
        """Test Methanol reference points with interpolator calls"""
        prop = get_prop( "Methanol" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 1.89009, places=None, delta=0.000189009)
        self.assertAlmostEqual(prop.Pvap, 1.89009, places=None, delta=0.000189009)
        self.assertAlmostEqual(prop.Pc, 1175.31, places=None, delta=0.117531)
        self.assertAlmostEqual(prop.Tc, 922.68, places=None, delta=0.092268)
        self.assertAlmostEqual(prop.SG, 0.790928, places=None, delta=7.90928e-05)
        self.assertAlmostEqual(prop.visc, 0.00584984, places=None, delta=5.84984e-07)
        self.assertAlmostEqual(prop.cond, 0.116984, places=None, delta=1.16984e-05)
        self.assertAlmostEqual(prop.Tnbp, 607.738, places=None, delta=0.0607738)
        self.assertAlmostEqual(prop.Tfreeze, 316.098, places=None, delta=0.0316098)
        self.assertAlmostEqual(prop.Cp, 0.598637, places=None, delta=5.98637e-05)
        self.assertAlmostEqual(prop.MolWt, 32.0422, places=None, delta=0.00320422)
        self.assertAlmostEqual(prop.Hvap, 506.175, places=None, delta=0.0506175)
        self.assertAlmostEqual(prop.surf, 0.000129471, places=None, delta=1.29471e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.71888e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000378018)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.16997e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.33968e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000119727)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.101235)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.58942e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000158186)
        SGvap = 1.751364e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.75136e-08)
        Z = 2.166539e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.16654e-08)
        Z = 9.784287e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.78429e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000378018)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.16997e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.33968e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000119727)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.101235)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.58942e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000158186)
        SGvap = 1.751364e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.75136e-08)
        Z = 2.166539e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.16654e-08)
        Z = 9.784287e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.78429e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=7.90928e-05)

    def test_MHF3_ref_pts(self):
        """Test MHF3 reference points with interpolator calls"""
        prop = get_prop( "MHF3" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.749349, places=None, delta=7.49349e-05)
        self.assertAlmostEqual(prop.Pc, 1373, places=None, delta=0.1373)
        self.assertAlmostEqual(prop.Tc, 1076.67, places=None, delta=0.107667)
        self.assertAlmostEqual(prop.SG, 0.894813, places=None, delta=8.94813e-05)
        self.assertAlmostEqual(prop.visc, 0.00941389, places=None, delta=9.41389e-07)
        self.assertAlmostEqual(prop.cond, 0.16074, places=None, delta=1.6074e-05)
        self.assertAlmostEqual(prop.Tnbp, 653.07, places=None, delta=0.065307)
        self.assertAlmostEqual(prop.Tfreeze, 394.67, places=None, delta=0.039467)
        self.assertAlmostEqual(prop.Cp, 0.717663, places=None, delta=7.17663e-05)
        self.assertAlmostEqual(prop.MolWt, 43.412, places=None, delta=0.0043412)
        self.assertAlmostEqual(prop.Hvap, 370, places=None, delta=0.037)
        self.assertAlmostEqual(prop.surf, 0.000203865, places=None, delta=2.03865e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.90094e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00014987)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.88278e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=3.2148e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000143533)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.074)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.0773e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000178963)
        SGvap = 9.251346e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=9.25135e-09)
        Z = 1.028617e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.02862e-08)
        Z = 9.949042e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.94904e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00014987)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.88278e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=3.2148e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000143533)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.074)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.0773e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000178963)
        SGvap = 9.251346e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=9.25135e-09)
        Z = 1.028617e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.02862e-08)
        Z = 9.949042e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.94904e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=8.94813e-05)

    def test_MMH_ref_pts(self):
        """Test MMH reference points with interpolator calls"""
        prop = get_prop( "MMH" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.727413, places=None, delta=7.27413e-05)
        self.assertAlmostEqual(prop.Pc, 1195, places=None, delta=0.1195)
        self.assertAlmostEqual(prop.Tc, 1053.67, places=None, delta=0.105367)
        self.assertAlmostEqual(prop.SG, 0.879839, places=None, delta=8.79839e-05)
        self.assertAlmostEqual(prop.visc, 0.00844866, places=None, delta=8.44866e-07)
        self.assertAlmostEqual(prop.cond, 0.144158, places=None, delta=1.44158e-05)
        self.assertAlmostEqual(prop.Tnbp, 649.47, places=None, delta=0.064947)
        self.assertAlmostEqual(prop.Tfreeze, 397.37, places=None, delta=0.039737)
        self.assertAlmostEqual(prop.Cp, 0.69986, places=None, delta=6.9986e-05)
        self.assertAlmostEqual(prop.MolWt, 46.0724, places=None, delta=0.00460724)
        self.assertAlmostEqual(prop.Hvap, 377, places=None, delta=0.0377)
        self.assertAlmostEqual(prop.surf, 0.000195877, places=None, delta=1.95877e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.00792e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000145483)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.68973e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.88315e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000139972)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0754)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.91754e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000175968)
        SGvap = 9.534957e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=9.53496e-09)
        Z = 1.077733e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.07773e-08)
        Z = 9.944794e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.94479e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000145483)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.68973e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.88315e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000139972)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0754)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.91754e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000175968)
        SGvap = 9.534957e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=9.53496e-09)
        Z = 1.077733e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.07773e-08)
        Z = 9.944794e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.94479e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=8.79839e-05)


    def test_MON10_ref_pts(self):
        """Test MON10 reference points with interpolator calls"""
        prop = get_prop( "MON10" )
        self.assertAlmostEqual(prop.T, 527.7, places=None, delta=0.05277)
        self.assertAlmostEqual(prop.P, 24.2732, places=None, delta=0.00242732)
        self.assertAlmostEqual(prop.Pvap, 24.2732, places=None, delta=0.00242732)
        self.assertAlmostEqual(prop.Pc, 1303.33, places=None, delta=0.130333)
        self.assertAlmostEqual(prop.Tc, 755.877, places=None, delta=0.0755877)
        self.assertAlmostEqual(prop.SG, 1.41848, places=None, delta=0.000141848)
        self.assertAlmostEqual(prop.visc, 0.00379652, places=None, delta=3.79652e-07)
        self.assertAlmostEqual(prop.cond, 0.102461, places=None, delta=1.02461e-05)
        self.assertAlmostEqual(prop.Tnbp, 509.07, places=None, delta=0.050907)
        self.assertAlmostEqual(prop.Tfreeze, 450, places=None, delta=0.045)
        self.assertAlmostEqual(prop.Cp, 0.463742, places=None, delta=4.63742e-05)
        self.assertAlmostEqual(prop.MolWt, 87.3528, places=None, delta=0.00873528)
        self.assertAlmostEqual(prop.Hvap, 157.438, places=None, delta=0.0157438)
        self.assertAlmostEqual(prop.surf, 0.000199149, places=None, delta=1.99149e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.05277)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.98129e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.05277)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00485464)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=7.59304e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.04922e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.27484e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0314876)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.98297e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000283696)
        SGvap = 6.289853e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=6.28985e-07)
        Z = 4.229100e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=4.2291e-07)
        Z = 9.537426e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.53743e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00485464)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=7.59304e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.04922e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.27484e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0314876)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.98297e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000283696)
        SGvap = 6.289853e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=6.28985e-07)
        Z = 4.229100e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=4.2291e-07)
        Z = 9.537426e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.53743e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000141848)

    def test_MON25_ref_pts(self):
        """Test MON25 reference points with interpolator calls"""
        prop = get_prop( "MON25" )
        self.assertAlmostEqual(prop.T, 527.7, places=None, delta=0.05277)
        self.assertAlmostEqual(prop.P, 61.7133, places=None, delta=0.00617133)
        self.assertAlmostEqual(prop.Pvap, 61.7133, places=None, delta=0.00617133)
        self.assertAlmostEqual(prop.Pc, 1733.61, places=None, delta=0.173361)
        self.assertAlmostEqual(prop.Tc, 725, places=None, delta=0.0725)
        self.assertAlmostEqual(prop.SG, 1.38991, places=None, delta=0.000138991)
        self.assertAlmostEqual(prop.visc, 0.00442678, places=None, delta=4.42678e-07)
        self.assertAlmostEqual(prop.cond, 0.114932, places=None, delta=1.14932e-05)
        self.assertAlmostEqual(prop.Tnbp, 474.751, places=None, delta=0.0474751)
        self.assertAlmostEqual(prop.Tfreeze, 389.126, places=None, delta=0.0389126)
        self.assertAlmostEqual(prop.Cp, 0.468618, places=None, delta=4.68618e-05)
        self.assertAlmostEqual(prop.MolWt, 81.1875, places=None, delta=0.00811875)
        self.assertAlmostEqual(prop.Hvap, 150.97, places=None, delta=0.015097)
        self.assertAlmostEqual(prop.surf, 0.000201805, places=None, delta=2.01805e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.05277)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=7.27862e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.05277)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.0123427)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=8.85355e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.29865e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.37236e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0301941)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.03609e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000277982)
        SGvap = 1.527152e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.52715e-06)
        Z = 1.019881e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.01988e-06)
        Z = 9.282252e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.28225e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.0123427)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=8.85355e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.29865e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.37236e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0301941)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.03609e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000277982)
        SGvap = 1.527152e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.52715e-06)
        Z = 1.019881e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.01988e-06)
        Z = 9.282252e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.28225e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000138991)

    def test_MON30_ref_pts(self):
        """Test MON30 reference points with interpolator calls"""
        prop = get_prop( "MON30" )
        self.assertAlmostEqual(prop.T, 527.7, places=None, delta=0.05277)
        self.assertAlmostEqual(prop.P, 86.3444, places=None, delta=0.00863444)
        self.assertAlmostEqual(prop.Pvap, 86.3444, places=None, delta=0.00863444)
        self.assertAlmostEqual(prop.Pc, 2142.52, places=None, delta=0.214252)
        self.assertAlmostEqual(prop.Tc, 721, places=None, delta=0.0721)
        self.assertAlmostEqual(prop.SG, 1.38132, places=None, delta=0.000138132)
        self.assertAlmostEqual(prop.visc, 0.00485107, places=None, delta=4.85107e-07)
        self.assertAlmostEqual(prop.cond, 0.128195, places=None, delta=1.28195e-05)
        self.assertAlmostEqual(prop.Tnbp, 462.67, places=None, delta=0.046267)
        self.assertAlmostEqual(prop.Tfreeze, 345.87, places=None, delta=0.034587)
        self.assertAlmostEqual(prop.Cp, 0.470751, places=None, delta=4.70751e-05)
        self.assertAlmostEqual(prop.MolWt, 79.3213, places=None, delta=0.00793213)
        self.assertAlmostEqual(prop.Hvap, 149.728, places=None, delta=0.0149728)
        self.assertAlmostEqual(prop.surf, 0.000222687, places=None, delta=2.22687e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.05277)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=7.319e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.05277)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.0172689)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=9.70213e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.56389e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.41502e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0299456)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.45374e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000276264)
        SGvap = 2.074979e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.07498e-06)
        Z = 1.402806e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.40281e-06)
        Z = 9.338526e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.33853e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.0172689)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=9.70213e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.56389e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.41502e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0299456)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.45374e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000276264)
        SGvap = 2.074979e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.07498e-06)
        Z = 1.402806e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.40281e-06)
        Z = 9.338526e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.33853e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000138132)

    def test_N2H4_ref_pts(self):
        """Test N2H4 reference points with interpolator calls"""
        prop = get_prop( "N2H4" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.199916, places=None, delta=1.99916e-05)
        self.assertAlmostEqual(prop.Pc, 2131, places=None, delta=0.2131)
        self.assertAlmostEqual(prop.Tc, 1175.67, places=None, delta=0.117567)
        self.assertAlmostEqual(prop.SG, 1.01007, places=None, delta=0.000101007)
        self.assertAlmostEqual(prop.visc, 0.0102795, places=None, delta=1.02795e-06)
        self.assertAlmostEqual(prop.cond, 0.283117, places=None, delta=2.83117e-05)
        self.assertAlmostEqual(prop.Tnbp, 697.27, places=None, delta=0.069727)
        self.assertAlmostEqual(prop.Tfreeze, 494.42, places=None, delta=0.049442)
        self.assertAlmostEqual(prop.Cp, 0.737769, places=None, delta=7.37769e-05)
        self.assertAlmostEqual(prop.MolWt, 32.0453, places=None, delta=0.00320453)
        self.assertAlmostEqual(prop.Hvap, 583, places=None, delta=0.0583)
        self.assertAlmostEqual(prop.surf, 0.000386381, places=None, delta=3.86381e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.48825e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=3.99833e-05)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.0559e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=5.66234e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000147554)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.1166)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=7.72762e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000202014)
        SGvap = 1.815425e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.81543e-09)
        Z = 1.794541e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.79454e-09)
        Z = 9.984514e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.98451e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=3.99833e-05)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.0559e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=5.66234e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000147554)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.1166)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=7.72762e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000202014)
        SGvap = 1.815425e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.81543e-09)
        Z = 1.794541e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.79454e-09)
        Z = 9.984514e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.98451e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000101007)

    def test_N2O4_ref_pts(self):
        """Test N2O4 reference points with interpolator calls"""
        prop = get_prop( "N2O4" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 13.7843, places=None, delta=0.00137843)
        self.assertAlmostEqual(prop.Pc, 1441.3, places=None, delta=0.14413)
        self.assertAlmostEqual(prop.Tc, 776.47, places=None, delta=0.077647)
        self.assertAlmostEqual(prop.SG, 1.44144, places=None, delta=0.000144144)
        self.assertAlmostEqual(prop.visc, 0.00420093, places=None, delta=4.20093e-07)
        self.assertAlmostEqual(prop.cond, 0.0766961, places=None, delta=7.66961e-06)
        self.assertAlmostEqual(prop.Tnbp, 530.07, places=None, delta=0.053007)
        self.assertAlmostEqual(prop.Tfreeze, 471.42, places=None, delta=0.047142)
        self.assertAlmostEqual(prop.Cp, 0.374677, places=None, delta=3.74677e-05)
        self.assertAlmostEqual(prop.MolWt, 92.011, places=None, delta=0.0092011)
        self.assertAlmostEqual(prop.Hvap, 178.2, places=None, delta=0.01782)
        self.assertAlmostEqual(prop.surf, 0.000149673, places=None, delta=1.49673e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.79576e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00275686)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=8.40186e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.53392e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=7.49354e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.03564)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.99346e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000288288)
        SGvap = 3.674388e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=3.67439e-07)
        Z = 2.489448e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.48945e-07)
        Z = 9.766336e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.76634e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00275686)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=8.40186e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.53392e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=7.49354e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.03564)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.99346e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000288288)
        SGvap = 3.674388e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=3.67439e-07)
        Z = 2.489448e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.48945e-07)
        Z = 9.766336e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.76634e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000144144)

    def test_N2O_ref_pts(self):
        """Test N2O reference points with interpolator calls"""
        prop = get_prop( "N2O" )
        self.assertAlmostEqual(prop.T, 332.424, places=None, delta=0.0332424)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6925, places=None, delta=0.00146925)
        self.assertAlmostEqual(prop.Pc, 1050.8, places=None, delta=0.10508)
        self.assertAlmostEqual(prop.Tc, 557.136, places=None, delta=0.0557136)
        self.assertAlmostEqual(prop.SG, 1.23046, places=None, delta=0.000123046)
        self.assertAlmostEqual(prop.visc, 0.00323728, places=None, delta=3.23728e-07)
        self.assertAlmostEqual(prop.cond, 0.116128, places=None, delta=1.16128e-05)
        self.assertAlmostEqual(prop.Tnbp, 332.424, places=None, delta=0.0332424)
        self.assertAlmostEqual(prop.Tfreeze, 328.221, places=None, delta=0.0328221)
        self.assertAlmostEqual(prop.Cp, 0.41086, places=None, delta=4.1086e-05)
        self.assertAlmostEqual(prop.MolWt, 44.0128, places=None, delta=0.00440128)
        self.assertAlmostEqual(prop.Hvap, 161.022, places=None, delta=0.0161022)
        self.assertAlmostEqual(prop.surf, 0.000135501, places=None, delta=1.35501e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0332424)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.96666e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0332424)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.0029385)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=6.47456e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.32257e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=8.21721e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0322043)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.71001e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000246092)
        SGvap = 2.980780e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.98078e-07)
        Z = 2.359845e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.35984e-07)
        Z = 9.741419e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.74142e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.0029385)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=6.47456e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.32257e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=8.21721e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0322043)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.71001e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000246092)
        SGvap = 2.980780e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.98078e-07)
        Z = 2.359845e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.35984e-07)
        Z = 9.741419e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.74142e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000123046)

    def test_NH3_ref_pts(self):
        """Test NH3 reference points with interpolator calls"""
        prop = get_prop( "NH3" )
        self.assertAlmostEqual(prop.T, 431.681, places=None, delta=0.0431681)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6955, places=None, delta=0.00146955)
        self.assertAlmostEqual(prop.Pc, 1643.71, places=None, delta=0.164371)
        self.assertAlmostEqual(prop.Tc, 729.72, places=None, delta=0.072972)
        self.assertAlmostEqual(prop.SG, 0.681973, places=None, delta=6.81973e-05)
        self.assertAlmostEqual(prop.visc, 0.00255484, places=None, delta=2.55484e-07)
        self.assertAlmostEqual(prop.cond, 0.384883, places=None, delta=3.84883e-05)
        self.assertAlmostEqual(prop.Tnbp, 431.681, places=None, delta=0.0431681)
        self.assertAlmostEqual(prop.Tfreeze, 351.891, places=None, delta=0.0351891)
        self.assertAlmostEqual(prop.Cp, 1.06307, places=None, delta=0.000106307)
        self.assertAlmostEqual(prop.MolWt, 17.0303, places=None, delta=0.00170303)
        self.assertAlmostEqual(prop.Hvap, 589.173, places=None, delta=0.0589173)
        self.assertAlmostEqual(prop.surf, 0.000255547, places=None, delta=2.55547e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0431681)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.91571e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0431681)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293911)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=5.10968e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=7.69765e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000212613)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.117835)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=5.11094e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000136395)
        SGvap = 8.895284e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=8.89528e-08)
        Z = 1.269203e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.2692e-07)
        Z = 9.730570e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.73057e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293911)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=5.10968e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=7.69765e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000212613)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.117835)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=5.11094e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000136395)
        SGvap = 8.895284e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=8.89528e-08)
        Z = 1.269203e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.2692e-07)
        Z = 9.730570e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.73057e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=6.81973e-05)

    def test_PH2_ref_pts(self):
        """Test PH2 reference points with interpolator calls"""
        prop = get_prop( "PH2" )
        self.assertAlmostEqual(prop.T, 36.4878, places=None, delta=0.00364878)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6949, places=None, delta=0.00146949)
        self.assertAlmostEqual(prop.Pc, 186.489, places=None, delta=0.0186489)
        self.assertAlmostEqual(prop.Tc, 59.2884, places=None, delta=0.00592884)
        self.assertAlmostEqual(prop.SG, 0.0708306, places=None, delta=7.08306e-06)
        self.assertAlmostEqual(prop.visc, 0.000133306, places=None, delta=1.33306e-08)
        self.assertAlmostEqual(prop.cond, 0.0598114, places=None, delta=5.98114e-06)
        self.assertAlmostEqual(prop.Tnbp, 36.4878, places=None, delta=0.00364878)
        self.assertAlmostEqual(prop.Tfreeze, 24.912, places=None, delta=0.0024912)
        self.assertAlmostEqual(prop.Cp, 2.32517, places=None, delta=0.000232517)
        self.assertAlmostEqual(prop.MolWt, 2.01594, places=None, delta=0.000201594)
        self.assertAlmostEqual(prop.Hvap, 191.897, places=None, delta=0.0191897)
        self.assertAlmostEqual(prop.surf, 1.09954e-05, places=None, delta=1.09954e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.00364878)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.15429e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.00364878)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293897)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.66611e-08)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.19623e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000465035)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0383794)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.19908e-09)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=1.41661e-05)
        SGvap = 1.338573e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.33857e-07)
        Z = 1.711324e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.71132e-06)
        Z = 9.055476e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.05548e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293897)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.66611e-08)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.19623e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000465035)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0383794)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.19908e-09)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=1.41661e-05)
        SGvap = 1.338573e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.33857e-07)
        Z = 1.711324e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.71132e-06)
        Z = 9.055476e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.05548e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=1.41661e-05)

    def test_Propane_ref_pts(self):
        """Test Propane reference points with interpolator calls"""
        prop = get_prop( "Propane" )
        self.assertAlmostEqual(prop.T, 415.865, places=None, delta=0.0415865)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 14.6958, places=None, delta=0.00146958)
        self.assertAlmostEqual(prop.Pc, 616.584, places=None, delta=0.0616584)
        self.assertAlmostEqual(prop.Tc, 665.802, places=None, delta=0.0665802)
        self.assertAlmostEqual(prop.SG, 0.580884, places=None, delta=5.80884e-05)
        self.assertAlmostEqual(prop.visc, 0.00197219, places=None, delta=1.97219e-07)
        self.assertAlmostEqual(prop.cond, 0.07469, places=None, delta=7.469e-06)
        self.assertAlmostEqual(prop.Tnbp, 415.865, places=None, delta=0.0415865)
        self.assertAlmostEqual(prop.Tfreeze, 153.954, places=None, delta=0.0153954)
        self.assertAlmostEqual(prop.Cp, 0.536817, places=None, delta=5.36817e-05)
        self.assertAlmostEqual(prop.MolWt, 44.0956, places=None, delta=0.00440956)
        self.assertAlmostEqual(prop.Hvap, 183.094, places=None, delta=0.0183094)
        self.assertAlmostEqual(prop.surf, 9.03964e-05, places=None, delta=9.03964e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0415865)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.24607e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0415865)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00293916)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=3.94438e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.4938e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000107363)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0366188)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.80793e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000116177)
        SGvap = 2.415974e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.41597e-07)
        Z = 4.004965e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=4.00496e-07)
        Z = 9.629367e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.62937e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00293916)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=3.94438e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.4938e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000107363)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0366188)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.80793e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000116177)
        SGvap = 2.415974e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.41597e-07)
        Z = 4.004965e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=4.00496e-07)
        Z = 9.629367e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.62937e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=5.80884e-05)

    def test_RP1_ref_pts(self):
        """Test RP1 reference points with interpolator calls"""
        prop = get_prop( "RP1" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.00427928, places=None, delta=4.27928e-07)
        self.assertAlmostEqual(prop.Pc, 315, places=None, delta=0.0315)
        self.assertAlmostEqual(prop.Tc, 1217.67, places=None, delta=0.121767)
        self.assertAlmostEqual(prop.SG, 0.809954, places=None, delta=8.09954e-05)
        self.assertAlmostEqual(prop.visc, 0.0166858, places=None, delta=1.66858e-06)
        self.assertAlmostEqual(prop.cond, 0.0786879, places=None, delta=7.86879e-06)
        self.assertAlmostEqual(prop.Tnbp, 881.67, places=None, delta=0.088167)
        self.assertAlmostEqual(prop.Tfreeze, 409.67, places=None, delta=0.040967)
        self.assertAlmostEqual(prop.Cp, 0.475379, places=None, delta=4.75379e-05)
        self.assertAlmostEqual(prop.MolWt, 172, places=None, delta=0.0172)
        self.assertAlmostEqual(prop.Hvap, 125, places=None, delta=0.0125)
        self.assertAlmostEqual(prop.surf, 0.000165813, places=None, delta=1.65813e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.33344e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=8.55856e-06)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=3.33716e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.57376e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.50759e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.025)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.31626e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000161991)
        SGvap = 2.084669e-06
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=2.08467e-10)
        Z = 2.572863e-06
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.57286e-10)
        Z = 9.996320e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.99632e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=8.55856e-06)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=3.33716e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.57376e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.50759e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.025)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.31626e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000161991)
        SGvap = 2.084669e-06
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=2.08467e-10)
        Z = 2.572863e-06
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.57286e-10)
        Z = 9.996320e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.99632e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=8.09954e-05)

    def test_UDMH_ref_pts(self):
        """Test UDMH reference points with interpolator calls"""
        prop = get_prop( "UDMH" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 2.57496, places=None, delta=0.000257496)
        self.assertAlmostEqual(prop.Pc, 867, places=None, delta=0.0867)
        self.assertAlmostEqual(prop.Tc, 941.67, places=None, delta=0.094167)
        self.assertAlmostEqual(prop.SG, 0.790444, places=None, delta=7.90444e-05)
        self.assertAlmostEqual(prop.visc, 0.00553308, places=None, delta=5.53308e-07)
        self.assertAlmostEqual(prop.cond, 0.0918907, places=None, delta=9.18907e-06)
        self.assertAlmostEqual(prop.Tnbp, 603.85, places=None, delta=0.060385)
        self.assertAlmostEqual(prop.Tfreeze, 388.73, places=None, delta=0.038873)
        self.assertAlmostEqual(prop.Cp, 0.665112, places=None, delta=6.65112e-05)
        self.assertAlmostEqual(prop.MolWt, 60.0995, places=None, delta=0.00600995)
        self.assertAlmostEqual(prop.Hvap, 250.55, places=None, delta=0.025055)
        self.assertAlmostEqual(prop.surf, 0.000140655, places=None, delta=1.40655e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.60356e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000514991)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.10662e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.83781e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000133022)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.05011)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=2.8131e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000158089)
        SGvap = 4.454497e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=4.4545e-08)
        Z = 5.539390e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=5.53939e-08)
        Z = 9.829565e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.82956e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000514991)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.10662e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.83781e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000133022)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.05011)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=2.8131e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000158089)
        SGvap = 4.454497e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=4.4545e-08)
        Z = 5.539390e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=5.53939e-08)
        Z = 9.829565e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.82956e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=7.90444e-05)

    def test_Water_ref_pts(self):
        """Test Water reference points with interpolator calls"""
        prop = get_prop( "Water" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 0.339289, places=None, delta=3.39289e-05)
        self.assertAlmostEqual(prop.Pvap, 0.339289, places=None, delta=3.39289e-05)
        self.assertAlmostEqual(prop.Pc, 3200.11, places=None, delta=0.320011)
        self.assertAlmostEqual(prop.Tc, 1164.77, places=None, delta=0.116477)
        self.assertAlmostEqual(prop.SG, 0.998163, places=None, delta=9.98163e-05)
        self.assertAlmostEqual(prop.visc, 0.0100165, places=None, delta=1.00165e-06)
        self.assertAlmostEqual(prop.cond, 0.34599, places=None, delta=3.4599e-05)
        self.assertAlmostEqual(prop.Tnbp, 671.624, places=None, delta=0.0671624)
        self.assertAlmostEqual(prop.Tfreeze, 491.688, places=None, delta=0.0491688)
        self.assertAlmostEqual(prop.Cp, 1.00009, places=None, delta=0.000100009)
        self.assertAlmostEqual(prop.MolWt, 18.0153, places=None, delta=0.00180153)
        self.assertAlmostEqual(prop.Hvap, 1055.53, places=None, delta=0.105553)
        self.assertAlmostEqual(prop.surf, 0.000415334, places=None, delta=4.15334e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.53024e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=6.78579e-05)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.00329e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=6.9198e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000200017)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.211106)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=8.30668e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000199633)
        SGvap = 1.731390e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.73139e-09)
        Z = 1.732562e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.73256e-09)
        Z = 9.988617e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.98862e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=6.78579e-05)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.00329e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=6.9198e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000200017)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.211106)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=8.30668e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000199633)
        SGvap = 1.731390e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.73139e-09)
        Z = 1.732562e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.73256e-09)
        Z = 9.988617e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.98862e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=9.98163e-05)


        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

