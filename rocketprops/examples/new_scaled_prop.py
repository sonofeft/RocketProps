from rocketprops.make_scaled_propellant import add_propellant
from rocketprops.unit_conv_data import get_value

# M20 data from PRISM
PC = 1943.8000000000002 # psia
TC = 1150.6 # degR
PREF = 14.7 # psia
TREF = 530.0 # degR
DREF = 0.03519628990509059 # lbm/cuin
VREF = 4.9744000000000003e-05 # lbm/in/sec
CREF = 5.903400000000001e-06  # BTU/in/sec/degR
TBOIL = 687.84 # degR
CPREF = 0.7280800000000001  # BTU/lbm-degR
WTMOL = 34.8524 # lbm/lbmole
DHVAP = 541.78 # BTU/lbm
SURF = 0.00034216000000000004 # lbf/in

add_propellant( prop_name='M20',
                Tref        = 527.67, # degR
                Pref        = 14.6959, # psia
                SG_ref       = get_value(DREF, 'lbm/in**3', 'SG'), # SG
                Cp_ref       = CPREF, # BTU/lbm/delF
                Hvap_ref     = DHVAP, # BTU/lbm
                cond_ref     = get_value(CREF, 'BTU/s/inch/delF', 'BTU/hr/ft/delF'), # BTU/hr/ft/delF
                surf_ref     = SURF, # lbf/in
                visc_ref     = get_value(VREF, 'lbm/s/inch', 'poise'), # poise (P)
                Pc_psia       = PC, # psia
                Tc_degR       = TC, # degR
                Tnbp_degR     = TBOIL, # degR
                Tfreeze_degR  = 483.55, # degR
                Ttriple_degR  = 483.55, # degR
                MolWt    = WTMOL) # g/gmole



# add_propellant( prop_name='MMH',
#                 Tref        = 527.67, # degR
#                 Pref        = 14.6959, # psia
#                 SG_ref       = 0.8798394613717013, # SG
#                 Cp_ref       = 0.6998597443550909, # BTU/lbm/delF
#                 Hvap_ref     = 377.0000676611555, # BTU/lbm
#                 cond_ref     = 0.1441577322485178, # BTU/hr/ft/delF
#                 surf_ref     = 0.0001958767819978368, # lbf/in
#                 visc_ref     = 0.008448662042797346, # poise (P)
#                 Pc_psia       = 1195, # psia
#                 Tc_degR       = 1053.67, # degR
#                 Tnbp_degR     = 649.47, # degR
#                 Tfreeze_degR  = 397.37, # degR
#                 Ttriple_degR  = 397.37, # degR
#                 MolWt    = 46.0724) # g/gmole
