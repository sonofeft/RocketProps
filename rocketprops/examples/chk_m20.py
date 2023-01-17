# from rocketprops.rocket_prop import get_prop
# Pm20 = get_prop( 'M20' )
# Pm20.summ_print()

from rocketprops.plot_multi_props import make_plots
# make_plots( ['MMH', 'M20', 'N2H4'], abs_T=True, Tmin=480, Tmax=600)

make_plots( ['MMH', 'M20', 'N2H4'], abs_T=1, ref_scaled=False, 
            Tmin=480, Tmax=600, save_figures=True)
