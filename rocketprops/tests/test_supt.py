
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
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'filename.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'filename.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)


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

from rocketprops.tank_supt import calc_tank_volume
from rocketprops.rocket_prop import get_prop
from rocketprops.line_supt import calc_line_id_dp, calc_line_vel_dp
from rocketprops.valve_supt import cv_valve_dp, kv_valve_dp
from rocketprops.injector_supt import calc_inj_velocity, calc_orifice_flow_rate

class MyTest(unittest.TestCase):


    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass


    def test_tank_vol(self):
        """test tank_vol"""
        pObj = get_prop('N2H4')

        cc_Total, kg_loaded, kg_residual = calc_tank_volume( pObj, kg_expelled=50.0,
                                                            TmaxC=50.0, expPcent=98.0, ullPcent=3.0 )        
        self.assertAlmostEqual(cc_Total, 53510.4, places=1)
        self.assertAlmostEqual(kg_loaded, 51.0526, places=4)
        self.assertAlmostEqual(kg_residual, 1.05263, places=4)

    def test_line(self):
        """test line"""
        pObj = get_prop('hydrazine')

        ID, deltaP = calc_line_id_dp( pObj, TdegR=530.0, Ppsia=240.0,
                                    wdotPPS=0.5, velFPS=13,
                                    roughness=5.0E-6,  Kfactors=5.0, len_inches=50.0)
        print( 'Inside Diam=%g inches, Pressure Drop =%g psid'%(ID, deltaP) )

        vel, dp = calc_line_vel_dp( pObj, TdegR=530.0, Ppsia=240.0,
                        wdotPPS=0.5, IDinches=ID,
                        roughness=5.0E-6,  Kfactors=5.0, len_inches=50.0)        

        self.assertAlmostEqual(vel, 13.0, places=1)
        self.assertAlmostEqual(dp, 9.66264, places=4)

    def test_valve(self):
        """test valve"""
        pObj = get_prop( 'MMH' )

        # Imperial valve flow coefficient, Cv
        dp = cv_valve_dp( pObj, Cv=1.0, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)
        self.assertAlmostEqual(dp, 14.6749, places=4)

        # Metric valve flow coefficient, Kv
        Kv = 1.0 / 1.1560992283526375  # Conversion factor for Cv to Kv
        dp = kv_valve_dp( pObj, Kv=Kv, wdotPPS=0.5, TdegR=530.0, Ppsia=1000.0)        

        self.assertAlmostEqual(dp, 14.6749, places=4)

    def test_injector(self):
        """test injector"""
        pObj = get_prop( 'N2O4' )
        ft_per_sec = calc_inj_velocity( pObj, dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)

        wdot = calc_orifice_flow_rate(pObj, CdOrf=0.75, DiamInches=0.01,
                            dPpsia=50.0, TdegR=530.0, Ppsia=1000.0)        

        self.assertAlmostEqual(ft_per_sec, 71.7716993053127, places=5)
        self.assertAlmostEqual(wdot, 0.00264060215451235, places=7)

    def test_tank_vol__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'tank_supt.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'tank_supt.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_line_vol__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'line_supt.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'line_supt.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_valve_vol__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'valve_supt.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'valve_supt.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_injector_vol__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'injector_supt.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'injector_supt.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_colbrook__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'colebrook.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'colebrook.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_InterpProp_scipy__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'InterpProp_scipy.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'InterpProp_scipy.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)

    def test_mixing_functions__main__(self):
        """Test the __main__ section at the bottom of the file"""
        if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # loads and runs the bottom section: if __name__ == "__main__"
            import imp
            runpy = imp.load_source('__main__', os.path.join(up_one, 'mixing_functions.py') )

        elif sys.version_info.major == 3 and sys.version_info.minor > 6:
            # for python >= 3.7
            # loads and runs the bottom section: if __name__ == "__main__"
            import types
            from importlib.machinery import SourceFileLoader

            script_path = os.path.abspath( os.path.join(up_one, 'mixing_functions.py') )
            loader = SourceFileLoader("__main__", script_path)
            mod = types.ModuleType(loader.name)
            loader.exec_module(mod)



if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

