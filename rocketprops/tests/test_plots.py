
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

import matplotlib.pyplot as plt
from rocketprops.rocket_prop import get_prop; 
from rocketprops.plot_multi_props import make_plots

class MyTest(unittest.TestCase):


    def test_should_always_pass_cleanly(self):
        """Should always pass cleanly."""
        pass


    def test_plot_sat_props(self):
        """test plot_sat_props"""
        prop = get_prop( "MMH" )

        num_figures_before = plt.gcf().number
        prop.plot_sat_props( show_plot=False )
        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after        


    def test_multiplot_Tr(self):
        """test multiplot"""

        num_figures_before = plt.gcf().number
        make_plots( ['MMH', 'N2H4'], abs_T=0, ref_scaled=True, show_plots=False)
        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after        

    def test_multiplot_T(self):
        """test multiplot"""
        prop = get_prop( "MHF3" )

        num_figures_before = plt.gcf().number
        make_plots( ['MMH', 'N2H4'], prop_objL=[prop], abs_T=1, 
                    ref_scaled=False, show_plots=False, show_gas_dens=True)
        num_figures_after = plt.gcf().number
        assert num_figures_before < num_figures_after        

if __name__ == '__main__':
    # Can test just this file from command prompt
    #  or it can be part of test discovery from nose, unittest, pytest, etc.
    unittest.main()

