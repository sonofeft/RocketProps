from scipy.optimize import brentq
from math import log10
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, perox_Pcrit_psia_terp,
                                                          perox_freeze_pt_degC_terp, perox_boil_pt_degC_terp,
                                                          perox_Tcrit_degC_terp, perox_pvap_at_tfreeze_terp,
                                                          find_omega, edalat_p_sat, terp_transition)


# Vapor Pressure - Note: Uses a different T_C grid than the others
T_C_pvap = [0, 20, 50, 80, 100, 120, 140]
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

# # High-Precision Vapor Pressure Data for H2O2-H2O System (psia)
# # Based on experimental correlations for aerospace-grade HTP
# # Will correctly be lower than the AFRPL-TR-67-144 values
# htp_pvap_data_psia = {
#     # Conc: [0C,     20C,    50C,    80C,    100C,   120C,   140C]
#     0:   [0.0886, 0.3391, 1.7850, 6.8748, 14.696, 28.790, 52.417],
#     3:   [0.0858, 0.3283, 1.7310, 6.6782, 14.288, 28.024, 51.092],
#     10:  [0.0792, 0.3031, 1.6034, 6.2163, 13.336, 26.251, 48.067],
#     35:  [0.0535, 0.2048, 1.1075, 4.4173, 9.6800, 19.497, 36.529],
#     50:  [0.0381, 0.1458, 0.8122, 3.3275, 7.4250, 15.318, 29.351],
#     70:  [0.0210, 0.0804, 0.4683, 2.0315, 4.7180, 10.158, 20.214],
#     85:  [0.0104, 0.0398, 0.2452, 1.1355, 2.7540, 6.2110, 12.871],
#     90:  [0.0080, 0.0306, 0.1931, 0.9168, 2.2640, 5.2040, 10.953],
#     98:  [0.0059, 0.0226, 0.1472, 0.7226, 1.8150, 4.3010, 9.2550],
#     100: [0.0055, 0.0211, 0.1384, 0.6865, 1.7330, 4.1290, 8.9280]
# }

# Fully Re-Blended Vapor Pressure Data (psia)
# Anchored to Schumb-MIT Correlation (100%) and Steam Tables (0%)
# use mole-averaged properties
# T_C_pvap = [0, 20, 50, 80, 100, 120, 140]
htp_pvap_data_psia = {
    # Conc: [0C,      20C,     50C,     80C,     100C,    120C,    140C]
    0: [ 0.08860, 0.33910, 1.78500, 6.87480,14.69600,28.79000,52.41700],
    3: [ 0.08730, 0.33410, 1.75930, 6.77930,14.49690,28.40970,51.74230],
   10: [ 0.08400, 0.32170, 1.69640, 6.54550,14.00930,27.47860,50.09010],
   35: [ 0.07010, 0.26970, 1.43140, 5.55980,11.95440,23.55420,43.12660],
   50: [ 0.05970, 0.23080, 1.23320, 4.82300,10.41810,20.62020,37.92070],
   70: [ 0.04250, 0.16620, 0.90420, 3.59940, 7.86690,15.74810,29.27580],
   85: [ 0.02610, 0.10440, 0.58970, 2.43000, 5.42870,11.09180,21.01360],
   90: [ 0.01970, 0.08050, 0.46780, 1.97660, 4.48340, 9.28650,17.81030],
   98: [ 0.00830, 0.03780, 0.25050, 1.16890, 2.79930, 6.07030,12.10360],
  100: [ 0.00530, 0.02620, 0.19140, 0.94900, 2.34090, 5.19480,10.55020],
}
# Make dict of pvap lists
pvap_at_tD = {} # key=temperature (degC), value=list of pvap at temperature

for i,T in enumerate(T_C_pvap):
    pvapL = []
    for pcent_H2O2 in htp_pvap_data_psia.keys():
        pvapL.append( htp_pvap_data_psia[ pcent_H2O2 ][i] )
    pvap_at_tD[ T ] = pvapL

# Make dict of log10(pvap) lists
log10_pvap_at_tD = {} # key=temperature (degC), value=list of log10(pvap) at temperature
for T in T_C_pvap:
    log10_pvap_at_tD[T] = [ log10(pvap) for pvap in pvap_at_tD[T]]

# Make dict of interpolators for log10(pvap)
log10_pvap_at_t_terpD = {} # key=temperature (degC), value=interpolator for pvap at temperature
for T in T_C_pvap:
    log10_pvap_at_t_terpD[T] = InterpProp( pcent_h2o2L, log10_pvap_at_tD[T], extrapOK=True )

# use this to get interpolated pvap data for any given concentration
def get_pvap_0_to_140T_data_at_conc( pcent_H2O2 ):
    pvap_at_tL = [ round( 10**log10_pvap_at_t_terpD[T](pcent_H2O2), 8 ) for T in T_C_pvap ]
    return pvap_at_tL

pcent_propD = {} # key=pcent_H2O2, value=Pvap_Peroxide_Liquid at pcent_H2O2

def get_eng_pvap_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = Pvap_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_pvap_at_TdegR( TdegR )

class Pvap_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.Tboil_C = perox_boil_pt_degC_terp( pcent_H2O2 ) # Pvap = 14.6959 psia (1 atm)
        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )

        self.Tfreeze_K = get_value( self.Tfreeze_C, 'degC', 'degK')
        self.Tboil_K = get_value( self.Tboil_C, 'degC', 'degK')
        self.Tc_K = get_value( self.Tc_C, 'degC', 'degK')

        self.Pc_psia = perox_Pcrit_psia_terp( pcent_H2O2 )

        # get vapor pressures for pcent_H2O2 from 0 to 140 C
        self.pvap_psiaL = get_pvap_0_to_140T_data_at_conc( pcent_H2O2 )
        t_KL = [get_value(t, 'degC', 'degK') for t in T_C_pvap]

        if self.Tfreeze_K < t_KL[0] - 1: # use -1 degC to prevent wiggle of polynomial fit
            Pvap_freeze = perox_pvap_at_tfreeze_terp( pcent_H2O2 )
            self.pvap_psiaL = [Pvap_freeze] + self.pvap_psiaL
            t_KL = [self.Tfreeze_K] + t_KL

        self.t_KL = t_KL
        self.trL = [t/self.Tc_K for t in t_KL ]

        # make Edalat curve from 140C on
        Pvap_at_140C = 10**log10_pvap_at_t_terpD[T](pcent_H2O2)
        Tref_K = get_value( 140, 'degC', 'degK')

        self.omega = find_omega( Tref_K, Pvap_at_140C, self.Tc_K, self.Pc_psia)
        # self.omega = find_omega( self.Tboil_K, 14.6959, self.Tc_K, self.Pc_psia)
        # self.omega = find_omega( t_KL[-1], self.pvap_psiaL[-1], self.Tc_K, self.Pc_psia)


        Tc_R = get_value( self.Tc_K, 'degK', 'degR')
        self.psat_obj = Psat( self.trL, self.pvap_psiaL, Tc_R, self.Pc_psia, self.omega )
        # self.psat_obj = Psat( self.trL + [1.0], self.pvap_psiaL + [self.Pc_psia], Tc_R, self.Pc_psia, self.omega )

        # make interpolator up to 140C
        self.log10p_tr_140_terp = InterpProp(self.trL, [log10(p) for p in self.pvap_psiaL], extrapOK=False)

        self.tr_140 = (140 + 273.15) / self.Tc_K

        # check omega calc
        # omega_chk =  -1.0 - log10( self( 0.7 ) / self.Pc_psia )  
        # print( 'omega_chk = %g'%omega_chk, '   self.omega=%g'%self.omega )


    def __call__(self, Tr):
        if Tr <= self.tr_140:
            return 10**self.log10p_tr_140_terp( Tr )
        else:
            return 10.0**self.psat_obj.log10p_tr_terp( Tr )
    
    def get_pvap_at_TdegC(self, TdegC):
        """Return pvap in units psia when called with degC"""
        Tr = (TdegC + 273.15) / self.Tc_K 
        if TdegC <= 140:
            return 10**self.log10p_tr_140_terp( Tr )
        else:
            return 10.0**self.psat_obj.log10p_tr_terp(  Tr ) #  (psia)


    def get_eng_pvap_at_TdegR( self, TdegR ):
        """Return pvap in units psia when called with degR"""
        TdegC = get_value( TdegR, 'degR', 'degC' )
        
        return self.get_pvap_at_TdegC( TdegC )




    def summ_print(self):
        print( '=== Summary for Pvap_Peroxide_Liquid( %g%% ) ==='%self.pcent_H2O2 )
        print( 'Tfreeze = %8g (degC)'%self.Tfreeze_C, '  %8g (degK)'%self.Tfreeze_K)
        print( 'Tboil   = %8g (degC)'%self.Tboil_C, '  %8g (degK)'%self.Tboil_K)
        print( 'Tc      = %8g (degC)'%self.Tc_C, '  %8g (degK)'%self.Tc_K)

        print( 'Pc        = %g (psia)'%self.Pc_psia)
        print( 'omega(est)= %g '%self.omega)

        print( 'T data (degC)', " ".join(['%8g'%t for t in T_C_pvap]))
        print( 'Tr           ', " ".join(['%6g'%t for t in self.trL]))
        print( 'Pvap data (psia)', " ".join(['%6g'%p for p in self.pvap_psiaL]))
        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Vapor Pressure', 
              xlabel='Temperature (degR)', ylabel='Vapor Pressure (psia)'):
        import matplotlib.pyplot as plt
        from matplotlib.ticker import StrMethodFormatter
        import matplotlib.ticker as ticker

        if new_fig:
            plt.subplots( figsize=(12,8))
            
        
        xL = []
        yL = []
        dx = ( self.Tc_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_pvap_at_TdegR( xL[-1] ) )
        
        t_KL = self.t_KL + [self.Tc_K]
        pvapL  = self.pvap_psiaL  + [ self.Pc_psia ]

        t_RL = [ get_value(t,'degK','degR') for t in t_KL]
        pvapL = [self.get_eng_pvap_at_TdegR(t) for t in t_RL]

        _line, = plt.plot( t_RL, pvapL, 'o', markersize=8  , label='%g%% Data'%self.pcent_H2O2 )
        plt.plot(xL, yL, '-', label='Pvap Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

        plt.title(title , fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)

        
        plt.yscale('log')
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        plt.gca().yaxis.set_major_formatter(StrMethodFormatter('{x:,g}')) # 2 decimal places
        plt.gca().yaxis.set_minor_formatter(StrMethodFormatter('{x:,g}')) # 2 decimal places
        plt.gca().tick_params(axis='y', which='minor', labelsize=8)

        
        if do_show:
            set_ax2_degC( plt.gca() )
            plt.tight_layout()
            plt.show()




class Psat:
    MINVALUE = 1.0E-8
    
    def __init__(self, trL, pL, Tc_R, Pc_psia, omega):
        """
        Given a list of reduced temperatures and absolute pressures, 
        scale the Edalat eqn to fill in missing data.
        """
        self.trL = trL[:] # save copy
        self.pL = pL[:]   # save copy, may need to fix any None values.

        tr_inc = 0.01
        while self.trL[-1] < 1.0:
            try:
                tr = self.trL[-1] + tr_inc
                p = edalat_p_sat( tr*Tc_R, Tc_R, Pc_psia, omega)
                self.pL.append( p )
                self.trL.append( tr )
                
            except:
                break

        self.trL.append( 1.0 )
        self.pL.append( Pc_psia )
        
        self.log10p_tr_terp = InterpProp(self.trL, [log10(p) for p in self.pL], extrapOK=False)
                

    def __call__(self, Tr):
        
        return 10.0**self.log10p_tr_terp( Tr )
        



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt

    # print( 'list of pvap data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    # for t in T_C_pvap:
    #     print( t, pvap_at_tD[t])

    # print()
    # print( 'show lists of log10(pvap)') # log10_pvap_at_tD
    # for t in T_C_pvap:
    #     print( t, log10_pvap_at_tD[t])



    # print()
    # print( 'Results of calling "get_pvap_0_to_140T_data_at_conc" with any concentration.')
    # print( 'Should match original data for pvap at pcent_H2O2 for each temperature')
    # print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    # for c in pcent_h2o2L:
    #     print( c, get_pvap_0_to_140T_data_at_conc(c))

    # print( 'Try some intermediate concentrations.')
    # for c in [2,5,77.5]:
    #     print( c, get_pvap_0_to_140T_data_at_conc(c))

    print()
    pvap_obj = Pvap_Peroxide_Liquid( pcent_H2O2=70 )
    pvap_obj.summ_print()


    # check if can reproduce data
    print()
    print( '=========== check if can reproduce Pvap data ==============')

    for i,T_C in enumerate(T_C_pvap):
        T_K = get_value( T_C, 'degC', 'degK')
        tr = T_K / pvap_obj.Tc_K
        pvap = pvap_obj( tr )
        print( 'pcent_H2O2=%g, T_C=%g, Pvap=%g'%( pvap_obj.pcent_H2O2, T_C, pvap ),
              htp_pvap_data_psia[pvap_obj.pcent_H2O2][i])


    for conc in pcent_h2o2L:
        visc_liq = Pvap_Peroxide_Liquid( pcent_H2O2=conc )
        visc_liq.summ_print()

        if conc == pcent_h2o2L[-1]:
            visc_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            visc_liq.plot( do_show=False, new_fig=True )
        else:
            visc_liq.plot( do_show=False, new_fig=False )



    # # --- Create Plot ---
    # plt.figure(figsize=(10, 6))

    # for pcent_H2O2 in [60, 70, 80, 90]: # pcent_h2o2L:
    #     PO = Pvap_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    #     # Generate temperatures for plotting
    #     T_plot = np.linspace(PO.Tfreeze_K, PO.Tc_K, 100)
    #     trL = [T/PO.Tc_K for T in T_plot]
    #     pvL = [PO(tr) for tr in trL]

    #     TdegCL = [get_value(T,'degK','degC') for T in T_plot]
    #     plt.semilogy(TdegCL, pvL, label='%g%%'%pcent_H2O2) #, linestyle='--', alpha=0.7)


    # plt.xlabel('Temperature (degC)')
    # plt.ylabel('Pvap (psia)')
    # plt.title('Edalat scaled Pvap')
    # plt.legend()
    # plt.grid(True, linestyle='--', alpha=0.6)
    # #plt.savefig('h2o2_density_comparison.png')
    # plt.show()
