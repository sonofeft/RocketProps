
from rocketprops.plot_multi_props import make_plots

make_plots( ['LF2', 'FLOX70', 'LOX'], abs_T=1,
             Tmin=130, Tmax=170, save_figures=True)
