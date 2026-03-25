# from scipy.optimize import curve_fit
from rocketprops.InterpProp_scipy import InterpProp
import numpy as np
from rocketprops.unit_conv_data import get_value

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, 
                                                          perox_freeze_pt_degC_terp,
                                                          get_molWt_mix)
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

# 2D Grid Data
T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]
#  Hvap (kJ/kg) given pcent_H2O2
# htp_hvap_dataD = {
#     0:   [2501, 2454, 2406, 2358, 2309, 2257, 2202, 2145],
#     3:   [2485, 2438, 2390, 2342, 2293, 2242, 2187, 2130],
#     10:  [2445, 2400, 2352, 2305, 2256, 2205, 2150, 2095],
#     35:  [2325, 2280, 2232, 2185, 2136, 2085, 2030, 1970],
#     50:  [2270, 2225, 2178, 2131, 2082, 2028, 1970, 1905],
#     70:  [2210, 2160, 2115, 2060, 2010, 1955, 1895, 1830],
#     85:  [1995, 1952, 1915, 1868, 1820, 1785, 1732, 1680],
#     90:  [1935, 1890, 1855, 1812, 1765, 1731, 1685, 1635],
#     98:  [1830, 1782, 1750, 1712, 1670, 1640, 1600, 1555],
#     100: [1810, 1765, 1730, 1690, 1650, 1618, 1580, 1535]
# }

# Updated 2D Grid Data (Corrected with Schumb Equation for 100% H2O2)
# hvapEqn BTU/lbm = 1.798797832 * ((0.021066 * TdegK**2) - (25.817 * TdegK) + 18412) / 34.0147
# T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
# pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

htp_hvap_dataD = {
  0: [2501.0, 2454.0, 2406.0, 2358.0, 2309.0, 2257.0, 2202.0, 2145.0],
  3: [2473.7, 2427.1, 2379.6, 2332.1, 2283.7, 2232.5, 2178.4, 2122.5],
  10: [2410.0, 2364.3, 2317.8, 2271.6, 2224.7, 2175.4, 2123.5, 2070.0],
  35: [2182.4, 2139.9, 2097.5, 2055.7, 2014.1, 1971.3, 1927.2, 1882.5],
  50: [2045.8, 2005.3, 1965.2, 1926.2, 1887.7, 1848.8, 1809.4, 1770.0],
  70: [1863.8, 1825.8, 1788.9, 1753.5, 1719.2, 1685.5, 1652.4, 1620.0],
  85: [1727.2, 1691.1, 1656.7, 1624.0, 1592.8, 1563.1, 1534.6, 1507.6],
  90: [1681.7, 1646.3, 1612.6, 1580.8, 1550.7, 1522.2, 1495.3, 1470.1],
  98: [1608.9, 1574.5, 1542.1, 1511.7, 1483.3, 1456.9, 1432.5, 1410.1],
  100: [1590.7, 1556.5, 1524.4, 1494.4, 1466.5, 1440.6, 1416.8, 1395.1],
}

# Using 80 C in order to get n values of about 0.35 (more physically consistent)
WATSON_START_T_C = 80 # start watson model at this temperature degC

hvap_at_tD = {} # key=temperature (degC), value=list of hvap at temperature

for i,T in enumerate(T_C_common):
    hvapL = []
    for pcent_H2O2 in htp_hvap_dataD.keys():
        hvapL.append( htp_hvap_dataD[ pcent_H2O2 ][i] )
    hvap_at_tD[ T ] = hvapL


hvap_at_t_terpD = {} # key=temperature (degC), value=interpolator for hvap at temperature
for T in T_C_common:
    hvap_at_t_terpD[T] = InterpProp( pcent_h2o2L, hvap_at_tD[T], extrapOK=True )

# use this to get interpolated hvap data for any given concentration
def get_hvap_0_to_140T_data_at_conc( pcent_H2O2 ):
    hvap_at_tL = [ round(hvap_at_t_terpD[T](pcent_H2O2), 8) for T in T_C_common ]
    return hvap_at_tL


# ============ Get full range Hvap interpolator ==============

pcent_propD = {} # key=pcent_H2O2, value=Hvap_Peroxide_Liquid at pcent_H2O2

def get_eng_hvap_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = Hvap_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_hvap_at_TdegR( TdegR )



class Hvap_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        # self.Hvap_at_freeze = perox_hvap_at_tfreeze_terp( pcent_H2O2 )

        # if self.Tfreeze_C < 0:
        #     self.t_CL = [ self.Tfreeze_C ] + T_C_common.copy()
        #     self.hvapL  = [ self.Hvap_at_freeze ]  + get_hvap_0_to_140T_data_at_conc( pcent_H2O2 )
        # else:
        self.t_CL =  T_C_common.copy()
        self.hvapL  =  get_hvap_0_to_140T_data_at_conc( pcent_H2O2 )

        self.lo_temp_terp = InterpProp( self.t_CL, self.hvapL, extrapOK=True)

        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )
        self.Tc_K = self.Tc_C + 273.15

        # popt, _ = curve_fit( self.watson_model, self.t_CL, self.hvapL, p0=[2100, 0.38])
        # self.A_opt, self.n_opt = popt

        # extend data with Watson equation 
        val_watson = self.lo_temp_terp( WATSON_START_T_C )
        slope_watson = self.lo_temp_terp.deriv( WATSON_START_T_C )

        T_K = WATSON_START_T_C + 273.15
        Tr = T_K / self.Tc_K
        # 1. Calculate n
        # n = -S* * (Tc - T*) / H*
        self.n_opt = (-slope_watson * (self.Tc_K - T_K)) / val_watson

        # 2. Calculate A
        # A = H* / (1 - Tr)^n
        self.A_opt = val_watson / (1 - Tr)**self.n_opt


    def watson_model(self, t_c, A, n):
        """
        Standard Watson Equation: Hv = A * (1 - Tr)^n
        t_c: Input temperature in Celsius
        A: Anchor coefficient (H_vap at T=0K, theoretically)
        n: Power law exponent
        """
        tk = t_c + 273.15
        tr = tk / self.Tc_K
        # We use (1-tr) because Hv must be 0 when tr=1
        
        # We use (1-tr) because Hv must be 0 when tr=1
        if isinstance(tr, np.ndarray):
            # 2. Clip values: anything > 1 becomes 1.0
            # None for the first argument means "no lower bound"
            tr = np.clip(tr, None, 1.0)
        else:
            tr = min( tr, 1.0)

        val = A * (1 - tr)**n
        return val

    def get_hvap_at_TdegC(self, TdegC):
        """Return Hvap in units of kJ/kg for input temperature in degC"""
        if TdegC <= WATSON_START_T_C:
            return self.lo_temp_terp( TdegC )
        else:
            return self.watson_model( TdegC, self.A_opt, self.n_opt)

    
    def get_eng_hvap_at_TdegR( self, TdegR ):
        """Return Hvap in units of BTU/lbm  for input temperature in degR"""
        TdegC = get_value( TdegR, 'degR', 'degC' )
        hvap_kJ_kg = self.get_hvap_at_TdegC( TdegC )

        return get_value( float(hvap_kJ_kg), 'kJ/kg', 'BTU/lbm' )


    def summ_print(self):
        print( '=== Summary for Hvap_Peroxide_Liquid( %g ) ==='%self.pcent_H2O2 )
        print( 'T data (degC)', " ".join(['%6g'%t for t in self.t_CL]))
        print( 'Hvap data  at T'," ".join( ['%6g'%d for d in self.hvapL]))
        print()
        print( "Tc_C = %g degC"%self.Tc_C )
        print()
        print( '   ... Watson Coefficients ...')
        print( 'A=%g,  n=%g'%(self.A_opt, self.n_opt))
        print( '.............\n')

        print( 'Show Hvap errors in Watson Equation')
        for hvap,TdegC in zip(self.hvapL,self.t_CL):
            hvap_calc = self.get_hvap_at_TdegC( TdegC )
            print( 'at T=%6g degC'%TdegC, 'hvap=%6g'%hvap, 'hvapcalc=%6g'%hvap_calc, 
                  '%%diff=%8g%%'%((hvap_calc-hvap)*100/hvap,) )

        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Heat of Vaporization\n(Follow Watson Equation: Hv = A * (1 - Tr)^n)', 
              xlabel='Temperature (degR)', ylabel='Hvap (BTU/lbm)'):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.figure(figsize=(9, 6))
        
        xL = []
        yL = []
        dx = ( self.Tc_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_hvap_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL + [self.Tc_C]
        t_RL = [get_value(t,'degC','degR') for t in t_CL]
        hvapL  = self.hvapL  + [0]
        hvap_btuL = [ get_value( h, 'kJ/kg', 'BTU/lbm') for h in hvapL]
        _line, = plt.plot( t_RL, hvap_btuL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='Hvap Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

        plt.title(title , fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
                
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        plt.tight_layout()
        
        if do_show:
            set_ax2_degC( plt.gca() )
            plt.tight_layout()
            plt.show()




if __name__ == "__main__":

    print( 'list of hvap data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    for t in T_C_common:
        print( t, hvap_at_tD[t])


    print()
    print( 'Results of calling "get_hvap_0_to_140T_data_at_conc" with any concentration.')
    print( 'Should match original data for hvap at pcent_H2O2 for each temperature')
    print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    for c in pcent_h2o2L:
        print( c, get_hvap_0_to_140T_data_at_conc(c))

    print( 'Try some intermediate concentrations.')
    for c in [2,5,77.5]:
        print( c, get_hvap_0_to_140T_data_at_conc(c))


    hvap_obj = Hvap_Peroxide_Liquid( pcent_H2O2=85 )
    hvap_obj.summ_print()


    for conc in pcent_h2o2L:
        hvap_liq = Hvap_Peroxide_Liquid( pcent_H2O2=conc )
        hvap_liq.summ_print()


        if conc == pcent_h2o2L[-1]:
            hvap_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            hvap_liq.plot( do_show=False, new_fig=True )
        else:
            hvap_liq.plot( do_show=False, new_fig=False )


