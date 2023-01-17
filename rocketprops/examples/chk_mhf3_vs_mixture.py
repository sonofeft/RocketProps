
from rocketprops.plot_multi_props import make_plots
from rocketprops.rocket_prop import get_prop

C = get_prop( 'M86' )
# tmpD = build_mixture( prop_name='MON15' )
# tmpD = build_mixture( prop_name='FLOX70' )

# C = Prop( valueD=tmpD )
print('T = %g R = %g K'%( C.T, C.T/1.8 ))

print()
print('Tr_data_range =', C.Tr_data_range())
print('  T_data_range=',C.T_data_range())
print('  P_data_range=', C.P_data_range())

# C.plot_sat_props()
make_plots( prop_nameL=['MHF3', 'MMH', 'N2H4'], prop_objL=[C], 
            abs_T=1, ref_scaled=False, show_gas_dens=False)

