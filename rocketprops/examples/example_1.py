"""
This example demonstrates the proper use of project: rocketprops
"""
import sys
import os
from rocketprops.rocket_prop import get_prop

p = get_prop('c3h8')
p.summ_print()
p.plot_sat_props(save_figures=True)
