from math import log10, exp, log
from numpy.polynomial import Polynomial

from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, perox_Pcrit_psia_terp,
                                                          perox_freeze_pt_degC_terp, perox_boil_pt_degC_terp,
                                                          perox_Tcrit_degC_terp, perox_visc_at_tfreeze_terp,
                                                          perox_visc_at_tboil_terp, get_molWt_mix)
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC


pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

# 2D Grid Data (mPa·s / cP)
T_C_visc = [0, 20, 40, 60, 80, 100, 120, 140]

# Corrected Viscosity Table (cP / mPa·s)
# Anchored to Schumb-MIT (100% = 1.245 cP @ 20C)
# Includes the characteristic HTP-Water "Viscosity Hump"

htp_visc_data_cp = {
    # Conc: [0C,     20C,    40C,    60C,    80C,    100C,   120C,   140C]
    0:   [1.792, 1.002, 0.653, 0.467, 0.355, 0.282, 0.232, 0.196],
    3:   [1.805, 1.020, 0.670, 0.485, 0.370, 0.295, 0.245, 0.205],
    10:  [1.850, 1.100, 0.745, 0.540, 0.415, 0.330, 0.275, 0.230],
    35:  [2.100, 1.450, 0.980, 0.720, 0.550, 0.435, 0.355, 0.295],
    50:  [2.250, 1.620, 1.120, 0.810, 0.620, 0.485, 0.395, 0.325], # < Peak region
    70:  [2.320, 1.700, 1.180, 0.860, 0.655, 0.510, 0.415, 0.340], # < Peak region
    85:  [2.180, 1.580, 1.110, 0.810, 0.620, 0.485, 0.395, 0.325],
    90:  [2.080, 1.480, 1.050, 0.770, 0.595, 0.465, 0.380, 0.315],
    98:  [1.880, 1.290, 0.925, 0.685, 0.530, 0.420, 0.345, 0.285],
    100: [1.820, 1.246, 0.895, 0.669, 0.517, 0.410, 0.334, 0.277]
}

# Make dict of visc lists
visc_at_tD = {} # key=temperature (degC), value=list of visc at temperature

for i,T in enumerate(T_C_visc):
    viscL = []
    for pcent_H2O2 in htp_visc_data_cp.keys():
        viscL.append( htp_visc_data_cp[ pcent_H2O2 ][i] )
    visc_at_tD[ T ] = viscL

# Make dict of log10(visc) lists
log10_visc_at_tD = {} # key=temperature (degC), value=list of log10(visc) at temperature
for T in T_C_visc:
    log10_visc_at_tD[T] = [ log10(visc) for visc in visc_at_tD[T]]

# Make dict of interpolators for log10(visc)
log10_visc_at_t_terpD = {} # key=temperature (degC), value=interpolator for visc at temperature
for T in T_C_visc:
    log10_visc_at_t_terpD[T] = InterpProp( pcent_h2o2L, log10_visc_at_tD[T], extrapOK=True )

# use this to get interpolated visc data for any given concentration
def get_visc_0_to_140T_data_at_conc( pcent_H2O2 ):
    visc_at_tL = [ round( 10**log10_visc_at_t_terpD[T](pcent_H2O2), 8 ) for T in T_C_visc ]
    return visc_at_tL


pcent_propD = {} # key=pcent_H2O2, value=Visc_Peroxide_Liquid at pcent_H2O2

def get_eng_visc_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = Visc_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_visc_at_TdegR( TdegR )


class Visc_Peroxide_Liquid:


    def calc_local_andrade_constants(self, TK1, V1, TK2, V2):
        """Calculates Andrade fit constants A and B between (TK1, V1) and (TK2, V2) for local interpolation"""
        
        B = (log(V1) - log(V2)) / (1/TK1 - 1/TK2)
        A = log(V1) - B/TK1
        return A, B

    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.Tboil_C = perox_boil_pt_degC_terp( pcent_H2O2 )
        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )

        self.Tfreeze_K = get_value( self.Tfreeze_C, 'degC', 'degK')
        self.Tboil_K = get_value( self.Tboil_C, 'degC', 'degK')
        self.Tc_K = get_value( self.Tc_C, 'degC', 'degK')

        # self.Pc_psia = perox_Pcrit_psia_terp( pcent_H2O2 )

        # get vapor pressures for pcent_H2O2 from 0 to 140 C
        self.visc_cpL = get_visc_0_to_140T_data_at_conc( pcent_H2O2 )

        self.t_CL = T_C_visc.copy()
        self.t_KL = [get_value(t, 'degC', 'degK') for t in self.t_CL]

        self.Visc_freeze = perox_visc_at_tfreeze_terp( pcent_H2O2 )
        if self.Tfreeze_K < self.t_KL[0] - 1:

            
            # self.visc_cpL = [self.Visc_freeze] + self.visc_cpL
            # self.t_KL = [self.Tfreeze_K] + self.t_KL
            # self.t_CL = [self.Tfreeze_C] + self.t_CL

            # use polynomial to fit log10(visc) and fill in from freeze pt to 0C
            degree = 3
            log10_viscL = [log10(v) for v in [self.Visc_freeze] + self.visc_cpL[:degree]]
            cubic_terp = Polynomial.fit( [self.Tfreeze_K] + self.t_KL[:degree], 
                                     log10_viscL,
                                     deg=degree)

            t_KL = []
            viscL = []
            T_K = self.Tfreeze_K
            while T_K < 273.15 - 4:
                t_KL.append( T_K )
                viscL.append( 10**cubic_terp( T_K ) )
                T_K += 5

            self.visc_cpL = viscL + self.visc_cpL
            self.t_KL = t_KL + self.t_KL
            self.t_CL = [T_K-273.15 for T_K in t_KL] + self.t_CL


        # if self.Tboil_K > self.t_KL[-1]:
        #     Visc_boil = perox_visc_at_tboil_terp( pcent_H2O2 )
        #     self.t_KL.append( self.Tboil_K )
        #     self.t_CL.append( self.Tboil_C )
        #     self.visc_cpL.append( Visc_boil )

        self.trL = [t/self.Tc_K for t in self.t_KL ]

        # ================================================================================
        # Make a long list of Andrade interpolated values for InterpProp interpolator
        # make list 100 points lone (about 10 points in between each data point)

        # run calculation to largest data value (Tboil or 140C)
        T_finalK = self.Tc_K # 160 + 273.15 # max( self.Tboil_K, self.t_KL[-1])

        # dt = (self.Tboil_K - self.t_KL[0] ) / 100
        dt = (T_finalK - self.t_KL[0] ) / 200

        tr_bigKL = [] # big list of reduced temperatures
        v_bigcpL = [] # big list of viscosity
        tK = self.t_KL[0] # start with lowest temperature in Kelvin (either 273.15(0C) or Tfreeze_K)

        nT = 0 # point at first temperature
        A, B = self.calc_local_andrade_constants( self.t_KL[nT], self.visc_cpL[nT], self.t_KL[nT+1], self.visc_cpL[nT+1] )
        while tK <= T_finalK:
            visc = exp(A + B/tK)

            tr_bigKL.append( tK / self.Tc_K )
            v_bigcpL.append( visc )

            # if tK < self.t_KL[nT] or tK > self.t_KL[nT+1]:
            #     print( '  OOPS: t_KL[nT], tK, t_KL[nT+1]', self.t_KL[nT], tK, self.t_KL[nT+1])

            tK += dt
            if tK > self.t_KL[nT+1] and nT < len(self.t_KL)-2:
                nT += 1
                A, B = self.calc_local_andrade_constants( self.t_KL[nT], self.visc_cpL[nT], self.t_KL[nT+1], self.visc_cpL[nT+1] )

        
        # self.log10p_terp = InterpProp(tr_bigKL, [log10(v) for v in v_bigcpL], extrapOK=False)

        # interpolator uses reduced Temperature (T/Tc) returns cP
        self.cp_tr_terp = InterpProp( tr_bigKL, v_bigcpL, extrapOK=True ) # returns  (mPa·s / cP)
                

    # def __call__(self, Tr):    
    #     return self.cp_tr_terp( Tr ) #  (mPa·s / cP)
    
    def get_visc_at_TdegC(self, TdegC):
        """Return visc in units cP when called with degC"""
        return self.cp_tr_terp( (TdegC + 273.15) / self.Tc_K ) #  (mPa·s / cP)


    def get_eng_visc_at_TdegR( self, TdegR ):
        """Return visc in units poise when called with degR"""
        TdegC = get_value( TdegR, 'degR', 'degC' )
        visc_cP = self.get_visc_at_TdegC( TdegC )
        return get_value( visc_cP, 'cp', 'poise')


    def summ_print(self):
        print( '=== Summary for Visc_Peroxide_Liquid( %g%% ) ==='%self.pcent_H2O2 )
        print( 'Tfreeze = %8g (degC)'%self.Tfreeze_C, '  %8g (degK)'%self.Tfreeze_K)
        print( 'Tboil   = %8g (degC)'%self.Tboil_C, '  %8g (degK)'%self.Tboil_K)
        print( 'Tc      = %8g (degC)'%self.Tc_C, '  %8g (degK)'%self.Tc_K)

        print( 'Visc_freeze = %8g cP'%self.Visc_freeze)

        # print( 'Pc        = %g (psia)'%self.Pc_psia)
        # print( 'omega(est)= %g '%self.omega)

        print( 'T data (degC)', " ".join(['%8g'%t for t in self.t_CL]))
        print( 'Tr           ', " ".join(['%6g'%t for t in self.trL]))
        print( 'Visc data (cP)', " ".join(['%6g'%p for p in self.visc_cpL]))
        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Viscosity', 
              xlabel='Temperature (degR)', ylabel='Viscosity (poise)'):
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
            yL.append( self.get_eng_visc_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL + [self.Tc_C]
        viscL  = self.visc_cpL  + [0]

        t_RL = [ get_value(t,'degC','degR') for t in t_CL]
        viscL = [self.get_eng_visc_at_TdegR(t) for t in t_RL]

        _line, = plt.plot( t_RL, viscL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='visc Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

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



if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

    # print( 'list of visc data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    # print( '       at each concentraion:\n   [0,   3,   10,   35,   50,   70,   85,   90,   98,   100]')
    # for t in T_C_visc:
    #     print( t, visc_at_tD[t])

    # print()
    # print( 'show lists of log10(visc)') # log10_visc_at_tD
    # for t in T_C_visc:
    #     print( t, log10_visc_at_tD[t])



    # print()
    # print( 'Results of calling "get_visc_0_to_140T_data_at_conc" with any concentration.')
    # print( 'Should match original data for visc at pcent_H2O2 for each temperature')
    # print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    # for c in pcent_h2o2L:
    #     print( c, get_visc_0_to_140T_data_at_conc(c))

    # print( 'Try some intermediate concentrations.')
    # print( '  [0,           20,         40,         60,         80,         100,        120,        140] (degC)' )
    # for c in [2,5,77.5]:
    #     print( c, get_visc_0_to_140T_data_at_conc(c))

    visc_obj = Visc_Peroxide_Liquid( 90 )

    visc_obj.summ_print()


    # check if can reproduce data
    print()
    print( '=========== check if can reproduce Visc data ==============')

    for T_C in visc_obj.t_CL:
        T_K = get_value( T_C, 'degC', 'degK')
        tr = T_K / visc_obj.Tc_K
        visc = visc_obj.get_visc_at_TdegC( T_C )
        print( 'pcent_H2O2=%g, T_C=%g, Visc=%g'%( visc_obj.pcent_H2O2, T_C, visc ), end='' )

        try:
            i = T_C_visc.index( T_C )
        except:
            i = -1
        
        if visc_obj.pcent_H2O2 in htp_visc_data_cp and i >= 0:
            print( '  data=%g'%htp_visc_data_cp[visc_obj.pcent_H2O2][i] )
        else:
            print()

            #   htp_visc_data_cp[visc_obj.pcent_H2O2][i]

    for conc in pcent_h2o2L:
        visc_liq = Visc_Peroxide_Liquid( pcent_H2O2=conc )
        visc_liq.summ_print()

        if conc == pcent_h2o2L[-1]:
            visc_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            visc_liq.plot( do_show=False, new_fig=True )
        else:
            visc_liq.plot( do_show=False, new_fig=False )

