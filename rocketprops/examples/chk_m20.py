from rocketprops.rocket_prop import get_prop
Pm20 = get_prop( 'M20' )
Pm20.summ_print()

from rocketprops.plot_multi_props import make_plots
# make_plots( prop_nameL=['MMH', 'M20', 'N2H4'] )#, prop_objL=None, abs_T=True, Tmin=480, Tmax=600)

# make_plots( ['MMH', 'M20', 'N2H4'], abs_T=1, ref_scaled=False, 
#             Tmin=480, Tmax=600, save_figures=True)

make_plots( ['MON30', 'MON25', 'MON10', 'MON3', 'N2O4'], abs_T=True, 
            Tmin=430, Tmax=600, save_figures=True)

# make_plots( ['UDMH','A25', 'A50', 'N2H4'], abs_T=1,
#             Tmin=430, Tmax=560, save_figures=True)
