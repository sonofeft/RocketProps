
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

    def test_M20_ref_pts(self):
        """Test M20 reference points with interpolator calls"""
        prop = get_prop( "M20" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.300351, places=None, delta=3.00351e-05)
        self.assertAlmostEqual(prop.Pc, 1931.86, places=None, delta=0.193186)
        self.assertAlmostEqual(prop.Tc, 1150.96, places=None, delta=0.115096)
        self.assertAlmostEqual(prop.SG, 0.980694, places=None, delta=9.80694e-05)
        self.assertAlmostEqual(prop.visc, 0.0100714, places=None, delta=1.00714e-06)
        self.assertAlmostEqual(prop.cond, 0.270383, places=None, delta=2.70383e-05)
        self.assertAlmostEqual(prop.Tnbp, 686.45, places=None, delta=0.068645)
        self.assertAlmostEqual(prop.Tfreeze, 483.55, places=None, delta=0.048355)
        self.assertAlmostEqual(prop.Cp, 0.733093, places=None, delta=7.33093e-05)
        self.assertAlmostEqual(prop.MolWt, 34.1231, places=None, delta=0.00341231)
        self.assertAlmostEqual(prop.Hvap, 533.465, places=None, delta=0.0533465)
        self.assertAlmostEqual(prop.surf, 0.000359821, places=None, delta=3.59821e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.5846e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00150176)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=2.01427e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=0.000540766)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000146619)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.106693)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=7.19641e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000196139)
        SGvap = 3.166434e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=3.16643e-09)
        Z = 2.951988e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=2.95199e-09)
        Z = 9.142739e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.14274e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.0901054)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=2.01427e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=0.000540766)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000146619)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.106693)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=7.19641e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000196139)
        SGvap = 3.166434e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=3.16643e-09)
        Z = 2.951988e-05
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=2.95199e-09)
        Z = 9.142739e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.14274e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=9.80694e-05)

    def test_M90_ref_pts(self):
        """Test M90 reference points with interpolator calls"""
        prop = get_prop( "M90" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 0.743344, places=None, delta=7.43344e-05)
        self.assertAlmostEqual(prop.Pc, 1320.77, places=None, delta=0.132077)
        self.assertAlmostEqual(prop.Tc, 1070.01, places=None, delta=0.107001)
        self.assertAlmostEqual(prop.SG, 0.890483, places=None, delta=8.90483e-05)
        self.assertAlmostEqual(prop.visc, 0.00912737, places=None, delta=9.12737e-07)
        self.assertAlmostEqual(prop.cond, 0.158439, places=None, delta=1.58439e-05)
        self.assertAlmostEqual(prop.Tnbp, 651.97, places=None, delta=0.065197)
        self.assertAlmostEqual(prop.Tfreeze, 395.44122857142855, places=None, delta=0.0394733)
        self.assertAlmostEqual(prop.Cp, 0.712576, places=None, delta=7.12576e-05)
        self.assertAlmostEqual(prop.MolWt, 44.1402, places=None, delta=0.00441402)
        self.assertAlmostEqual(prop.Hvap, 372, places=None, delta=0.0372)
        self.assertAlmostEqual(prop.surf, 0.000201782, places=None, delta=2.01782e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.93146e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000148669)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.82547e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=3.16878e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000142515)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0744)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.03564e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000178097)
        SGvap = 9.329066e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=9.32907e-09)
        Z = 1.042550e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.04255e-08)
        Z = 9.951411e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.95141e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000148669)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.82547e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=3.16878e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000142515)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0744)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.03564e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000178097)
        SGvap = 9.329066e-05
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=9.32907e-09)
        Z = 1.042550e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.04255e-08)
        Z = 9.951411e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.95141e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=8.90483e-05)

    def test_MON5_ref_pts(self):
        """Test MON5 reference points with interpolator calls"""
        prop = get_prop( "MON5" )
        self.assertAlmostEqual(prop.T, 527.685, places=None, delta=0.0527685)
        self.assertAlmostEqual(prop.P, 19.6089, places=None, delta=0.00196089)
        self.assertAlmostEqual(prop.Pvap, 19.163, places=None, delta=0.0019163)
        self.assertAlmostEqual(prop.Pc, 1374.38, places=None, delta=0.137438)
        self.assertAlmostEqual(prop.Tc, 766.583, places=None, delta=0.0766583)
        self.assertAlmostEqual(prop.SG, 1.4299, places=None, delta=0.00014299)
        self.assertAlmostEqual(prop.visc, 0.00399359, places=None, delta=3.99359e-07)
        self.assertAlmostEqual(prop.cond, 0.0849398, places=None, delta=8.49398e-06)
        self.assertAlmostEqual(prop.Tnbp, 517.699, places=None, delta=0.0517699)
        self.assertAlmostEqual(prop.Tfreeze, 461.225, places=None, delta=0.0461225)
        self.assertAlmostEqual(prop.Cp, 0.419211, places=None, delta=4.19211e-05)
        self.assertAlmostEqual(prop.MolWt, 89.6214, places=None, delta=0.00896214)
        self.assertAlmostEqual(prop.Hvap, 167.819, places=None, delta=0.0167819)
        self.assertAlmostEqual(prop.surf, 0.00017462, places=None, delta=1.7462e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0527685)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=6.8836e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=1.05537)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.038326)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=7.98718e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=0.00016988)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=8.38422e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0335638)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.49239e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000285979)
        SGvap = 4.991319e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=4.99132e-07)
        Z = 3.392188e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.39219e-07)
        Z = 9.718135e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.71814e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=5.7489)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=7.98718e-06)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=0.00016988)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=8.38422e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0335638)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.49239e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000285979)
        SGvap = 4.991319e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=4.99132e-07)
        Z = 3.392188e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.39219e-07)
        Z = 9.718135e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.71814e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.00014299)

    def test_MON20_ref_pts(self):
        """Test MON20 reference points with interpolator calls"""
        prop = get_prop( "MON20" )
        self.assertAlmostEqual(prop.T, 527.7, places=None, delta=0.05277)
        self.assertAlmostEqual(prop.P, 49.8346, places=None, delta=0.00498346)
        self.assertAlmostEqual(prop.Pvap, 48.7868, places=None, delta=0.00487868)
        self.assertAlmostEqual(prop.Pc, 1573.16, places=None, delta=0.157316)
        self.assertAlmostEqual(prop.Tc, 736.864, places=None, delta=0.0736864)
        self.assertAlmostEqual(prop.SG, 1.40021, places=None, delta=0.000140021)
        self.assertAlmostEqual(prop.visc, 0.00422654, places=None, delta=4.22654e-07)
        self.assertAlmostEqual(prop.cond, 0.108835, places=None, delta=1.08835e-05)
        self.assertAlmostEqual(prop.Tnbp, 482.328, places=None, delta=0.0482328)
        self.assertAlmostEqual(prop.Tfreeze, 418.659, places=None, delta=0.0418659)
        self.assertAlmostEqual(prop.Cp, 0.466785, places=None, delta=4.66785e-05)
        self.assertAlmostEqual(prop.MolWt, 83.1436, places=None, delta=0.00831436)
        self.assertAlmostEqual(prop.Hvap, 153.341, places=None, delta=0.0153341)
        self.assertAlmostEqual(prop.surf, 0.000201896, places=None, delta=2.01896e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.05277)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=7.16143e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.05277)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00975736)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=8.45307e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.1767e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.33571e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0306681)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.03792e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000280041)
        SGvap = 1.210156e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.21016e-06)
        Z = 8.196725e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=8.19673e-07)
        Z = 9.483973e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.48397e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00975736)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=8.45307e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.1767e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.33571e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0306681)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.03792e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000280041)
        SGvap = 1.210156e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.21016e-06)
        Z = 8.196725e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=8.19673e-07)
        Z = 9.483973e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.48397e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000140021)

    def test_MON27_ref_pts(self):
        """Test MON27 reference points with interpolator calls"""
        prop = get_prop( "MON27" )
        self.assertAlmostEqual(prop.T, 527.7, places=None, delta=0.05277)
        self.assertAlmostEqual(prop.P, 71.7035, places=None, delta=0.00717035)
        self.assertAlmostEqual(prop.Pvap, 71.628, places=None, delta=0.0071628)
        self.assertAlmostEqual(prop.Pc, 1897.21, places=None, delta=0.189721)
        self.assertAlmostEqual(prop.Tc, 723.405, places=None, delta=0.0723405)
        self.assertAlmostEqual(prop.SG, 1.38647, places=None, delta=0.000138647)
        self.assertAlmostEqual(prop.visc, 0.00459224, places=None, delta=4.59224e-07)
        self.assertAlmostEqual(prop.cond, 0.117939, places=None, delta=1.17939e-05)
        self.assertAlmostEqual(prop.Tnbp, 469.3, places=None, delta=0.04693)
        self.assertAlmostEqual(prop.Tfreeze, 376.838, places=None, delta=0.0376838)
        self.assertAlmostEqual(prop.Cp, 0.469463, places=None, delta=4.69463e-05)
        self.assertAlmostEqual(prop.MolWt, 80.4306, places=None, delta=0.00804306)
        self.assertAlmostEqual(prop.Hvap, 150.477, places=None, delta=0.0150477)
        self.assertAlmostEqual(prop.surf, 0.000210267, places=None, delta=2.10267e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.05277)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=7.29467e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.05277)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.0143256)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=9.18449e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=2.35879e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=9.38926e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0300955)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=4.20535e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000277294)
        SGvap = 1.748330e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.74833e-06)
        Z = 1.175605e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.1756e-06)
        Z = 9.322846e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.32285e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.0143256)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=9.18449e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=2.35879e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=9.38926e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0300955)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=4.20535e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000277294)
        SGvap = 1.748330e-02
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.74833e-06)
        Z = 1.175605e-02
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.1756e-06)
        Z = 9.322846e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.32285e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.000138647)

    def test_A25_ref_pts(self):
        """Test A25 reference points with interpolator calls"""
        prop = get_prop( "A25" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 2.44883, places=None, delta=0.000244883)
        self.assertAlmostEqual(prop.Pc, 1250.48, places=None, delta=0.125048)
        self.assertAlmostEqual(prop.Tc, 1013.05, places=None, delta=0.101305)
        self.assertAlmostEqual(prop.SG, 0.84322, places=None, delta=8.4322e-05)
        self.assertAlmostEqual(prop.visc, 0.0071381, places=None, delta=7.1381e-07)
        self.assertAlmostEqual(prop.cond, 0.11564, places=None, delta=1.1564e-05)
        self.assertAlmostEqual(prop.Tnbp, 611.25, places=None, delta=0.061125)
        self.assertAlmostEqual(prop.Tfreeze, 454.041, places=None, delta=0.0454041)
        self.assertAlmostEqual(prop.Cp, 0.696672, places=None, delta=6.96672e-05)
        self.assertAlmostEqual(prop.MolWt, 49.308, places=None, delta=0.0049308)
        self.assertAlmostEqual(prop.Hvap, 298.525, places=None, delta=0.0298525)
        self.assertAlmostEqual(prop.surf, 0.000161019, places=None, delta=1.61019e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.2087e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000489766)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.42762e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=0.00023128)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.000139334)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.059705)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=3.22038e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000168644)
        SGvap = 3.489964e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=3.48996e-08)
        Z = 4.051582e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=4.05158e-08)
        Z = 9.789142e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.78914e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000489766)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.42762e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=0.00023128)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.000139334)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.059705)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=3.22038e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000168644)
        SGvap = 3.489964e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=3.48996e-08)
        Z = 4.051582e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=4.05158e-08)
        Z = 9.789142e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.78914e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=8.4322e-05)

    def test_A75_ref_pts(self):
        """Test A75 reference points with interpolator calls"""
        prop = get_prop( "A75" )
        self.assertAlmostEqual(prop.T, 527.67, places=None, delta=0.052767)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 1.13774, places=None, delta=0.000113774)
        self.assertAlmostEqual(prop.Pc, 1919.16, places=None, delta=0.191916)
        self.assertAlmostEqual(prop.Tc, 1132.69, places=None, delta=0.113269)
        self.assertAlmostEqual(prop.SG, 0.953844, places=None, delta=9.53844e-05)
        self.assertAlmostEqual(prop.visc, 0.00972937, places=None, delta=9.72937e-07)
        self.assertAlmostEqual(prop.cond, 0.20355, places=None, delta=2.0355e-05)
        self.assertAlmostEqual(prop.Tnbp, 652.31, places=None, delta=0.065231)
        self.assertAlmostEqual(prop.Tfreeze, 490.578, places=None, delta=0.0490578)
        self.assertAlmostEqual(prop.Cp, 0.733001, places=None, delta=7.33001e-05)
        self.assertAlmostEqual(prop.MolWt, 36.2791, places=None, delta=0.00362791)
        self.assertAlmostEqual(prop.Hvap, 464.75, places=None, delta=0.046475)
        self.assertAlmostEqual(prop.surf, 0.000301923, places=None, delta=3.01923e-08)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.052767)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=4.65854e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.052767)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.000227548)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=1.94587e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=0.0004071)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=0.0001466)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.09295)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=6.03846e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000190769)
        SGvap = 1.321838e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=1.32184e-08)
        Z = 1.224337e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=1.22434e-08)
        Z = 8.834862e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=8.83486e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.000227548)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=1.94587e-05)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=0.0004071)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=0.0001466)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.09295)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=6.03846e-07)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000190769)
        SGvap = 1.321838e-04
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=1.32184e-08)
        Z = 1.224337e-04
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=1.22434e-08)
        Z = 8.834862e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=8.83486e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=9.53844e-05)

    def test_FLOX70_ref_pts(self):
        """Test FLOX70 reference points with interpolator calls"""
        prop = get_prop( "FLOX70" )
        self.assertAlmostEqual(prop.T, 156.193, places=None, delta=0.0156193)
        self.assertAlmostEqual(prop.P, 14.6959, places=None, delta=0.00146959)
        self.assertAlmostEqual(prop.Pvap, 15.2499, places=None, delta=0.00152499)
        self.assertAlmostEqual(prop.Pc, 744.379, places=None, delta=0.0744379)
        self.assertAlmostEqual(prop.Tc, 266.682, places=None, delta=0.0266682)
        self.assertAlmostEqual(prop.SG, 1.3717, places=None, delta=0.00013717)
        self.assertAlmostEqual(prop.visc, 0.00224928, places=None, delta=2.24928e-07)
        self.assertAlmostEqual(prop.cond, 0.0782234, places=None, delta=7.82234e-06)
        self.assertAlmostEqual(prop.Tnbp, 155.582, places=None, delta=0.0155582)
        self.assertAlmostEqual(prop.Tfreeze, 96.7411, places=None, delta=0.00967411)
        self.assertAlmostEqual(prop.Cp, 0.375008, places=None, delta=3.75008e-05)
        self.assertAlmostEqual(prop.MolWt, 35.9739, places=None, delta=0.00359739)
        self.assertAlmostEqual(prop.Hvap, 79.9297, places=None, delta=0.00799297)
        self.assertAlmostEqual(prop.surf, 7.5534e-05, places=None, delta=7.5534e-09)
        T = prop.T
        Tr = T / prop.Tc
        self.assertAlmostEqual(prop.T, prop.TAtTr( Tr ), places=None, delta=0.0156193)
        self.assertAlmostEqual(Tr, prop.TrAtT( T ), places=None, delta=5.85691e-05)
        self.assertAlmostEqual(prop.T, prop.TdegRAtPsat( prop.Pvap ), places=None, delta=0.0156193)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTdegR( T ), places=None, delta=0.00304997)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTdegR( T ), places=None, delta=4.49855e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTdegR( T ), places=None, delta=1.56447e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTdegR( T ), places=None, delta=7.50016e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTdegR( T ), places=None, delta=0.0159859)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTdegR( T ), places=None, delta=1.51068e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTdegR( T ), places=None, delta=0.000274341)
        SGvap = 5.532682e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTdegR( T ), places=None, delta=5.53268e-07)
        Z = 3.822828e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTdegR( T ), places=None, delta=3.82283e-07)
        Z = 9.477847e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTdegR( T ), places=None, delta=9.47785e-05)
        self.assertAlmostEqual(prop.Pvap, prop.PvapAtTr( Tr ), places=None, delta=0.00304997)
        self.assertAlmostEqual(prop.visc, prop.ViscAtTr( Tr ), places=None, delta=4.49855e-07)
        self.assertAlmostEqual(prop.cond, prop.CondAtTr( Tr ), places=None, delta=1.56447e-05)
        self.assertAlmostEqual(prop.Cp, prop.CpAtTr( Tr ), places=None, delta=7.50016e-05)
        self.assertAlmostEqual(prop.Hvap, prop.HvapAtTr( Tr ), places=None, delta=0.0159859)
        self.assertAlmostEqual(prop.surf, prop.SurfAtTr( Tr ), places=None, delta=1.51068e-08)
        self.assertAlmostEqual(prop.SG, prop.SGLiqAtTr( Tr ), places=None, delta=0.000274341)
        SGvap = 5.532682e-03
        self.assertAlmostEqual(SGvap, prop.SGVapAtTr( Tr ), places=None, delta=5.53268e-07)
        Z = 3.822828e-03
        self.assertAlmostEqual(Z, prop.ZLiqAtTr( Tr ), places=None, delta=3.82283e-07)
        Z = 9.477847e-01
        self.assertAlmostEqual(Z, prop.ZVapAtTr( Tr ), places=None, delta=9.47785e-05)
        self.assertAlmostEqual(prop.SG_compressed(prop.T, prop.P), prop.SG, places=None, delta=0.00013717)
        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

