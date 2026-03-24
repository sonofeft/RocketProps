from scipy.optimize import curve_fit
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp,
                                                          perox_freeze_pt_degC_terp, perox_surf_at_tfreeze_terp,
                                                          get_molWt_mix, perox_surf_at_tboil_terp)
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC


# 2D Grid Data
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

# 2D Grid Data  Surface Tension  (mN/m)
T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
# htp_surf_dataD = {
#     0:   [75.6, 72.8, 69.6, 66.2, 62.7, 58.9, 55.0, 50.9],
#     3:   [75.8, 73.0, 69.8, 66.5, 63.0, 59.2, 55.3, 51.2],
#     10:  [76.3, 73.5, 70.4, 67.1, 63.6, 59.9, 56.1, 52.1],
#     35:  [77.8, 75.1, 72.1, 69.0, 65.6, 62.1, 58.5, 54.8],
#     50:  [78.6, 75.9, 73.0, 70.0, 66.8, 63.4, 59.9, 56.4],
#     70:  [79.5, 76.8, 74.0, 71.3, 68.5, 65.8, 62.5, 59.2],
#     85:  [81.2, 78.4, 75.6, 72.8, 70.0, 67.2, 64.1, 61.0],
#     90:  [81.8, 79.0, 76.2, 73.4, 70.6, 67.8, 64.7, 61.6],
#     98:  [82.7, 79.9, 77.0, 74.2, 71.4, 68.6, 65.6, 62.6],
#     100: [83.0, 80.1, 77.3, 74.5, 71.7, 68.9, 65.9, 62.9]
# }

# Fully Corrected Surface Tension Data (mN/m or dynes/cm)
# Anchored to Schumb-MIT Correlation (100% H2O2) and Steam Tables (0%)
# Non-linear mixture rule: Meissner & Michaels (z^1.35)
htp_surf_dataD = {
    0: [75.60000,72.80000,69.60000,66.20000,62.70000,58.90000,55.00000,50.90000],
    3: [75.63363,72.82846,69.62482,66.22193,62.71942,58.91805,55.01706,50.91684],
   10: [75.77888,72.95139,69.73199,66.31662,62.80328,58.99601,55.09075,50.98954],
   35: [76.75948,73.78130,70.45553,66.95596,63.36949,59.52232,55.58826,51.48040],
   50: [77.71406,74.58918,71.15986,67.57832,63.92066,60.03466,56.07256,51.95822],
   70: [79.57503,76.16418,72.53299,68.79163,64.99519,61.03349,57.01671,52.88976],
   85: [81.60257,77.88014,74.02901,70.11354,66.16589,62.12172,58.04537,53.90468],
   90: [82.44361,78.59194,74.64958,70.66188,66.65151,62.57312,58.47207,54.32567],
   98: [84.00961,79.91729,75.80506,71.68288,67.55572,63.41363,59.26657,55.10956],
  100: [84.45000,80.29000,76.13000,71.97000,67.81000,63.65000,59.49000,55.33000],
}

surf_at_tD = {} # key=temperature (degC), value=list of surf at temperature

for i,T in enumerate(T_C_common):
    surfL = []
    for pcent_H2O2 in htp_surf_dataD.keys():
        surfL.append( htp_surf_dataD[ pcent_H2O2 ][i] )
    surf_at_tD[ T ] = surfL


surf_at_t_terpD = {} # key=temperature (degC), value=interpolator for surf at temperature
for T in T_C_common:
    surf_at_t_terpD[T] = InterpProp( pcent_h2o2L, surf_at_tD[T], extrapOK=True )

# use this to get interpolated surf data for any given concentration
def get_surf_0_to_140T_data_at_conc( pcent_H2O2 ):
    surf_at_tL = [ round(surf_at_t_terpD[T](pcent_H2O2), 8) for T in T_C_common ]
    return surf_at_tL


# ============ Get full range surf interpolator ==============

pcent_propD = {} # key=pcent_H2O2, value=Surf_Peroxide_Liquid at pcent_H2O2

def get_eng_surf_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = Surf_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_surf_at_TdegR( TdegR )

class Surf_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.surf_at_freeze = perox_surf_at_tfreeze_terp( pcent_H2O2 )

        # if self.Tfreeze_C < 0:
        #     self.t_CL = [ self.Tfreeze_C ] + T_C_common.copy()
        #     self.surfL  = [ self.surf_at_freeze ]  + get_surf_0_to_140T_data_at_conc( pcent_H2O2 )
        # else:
        self.t_CL =  T_C_common.copy()
        self.surfL  =  get_surf_0_to_140T_data_at_conc( pcent_H2O2 )

        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )
        self.Tc_K = self.Tc_C + 273.15

        popt, _ = curve_fit( self.watson_model, self.t_CL, self.surfL, p0=[100, 0.7])
        # popt, pcov = curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, 
        # check_finite=True, bounds=(-inf, inf), method=None, jac=None, **kwargs)

        self.A_opt, self.n_opt = popt



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
        return A * (1 - tr)**n

    def get_surf_at_TdegC(self, TdegC):
        """Return surf in units mN/m"""
        return self.watson_model( TdegC, self.A_opt, self.n_opt)
    
    def get_eng_surf_at_TdegR( self, TdegR ):
        """Return surf in units lbf/in"""
        TdegC = get_value( TdegR, 'degR', 'degC' )
        surf_mN_m = self.get_surf_at_TdegC( TdegC )
        return get_value( surf_mN_m, 'mN/m', 'lbf/in')

    def summ_print(self):
        print( '\n=== Summary for Surf_Peroxide_Liquid( %g ) ==='%self.pcent_H2O2 )
        print( 'T data (degC)', " ".join(['%6g'%t for t in self.t_CL]))
        print( 'Surf data (mN/m)'," ".join( ['%6g'%d for d in self.surfL]))
        print()
        print( "Tc_C = %g degC"%self.Tc_C )
        print()
        print( '   ... Watson Coefficients ...')
        print( 'A=%g,  n=%g'%(self.A_opt, self.n_opt))
        print( '.............\n')

        print( 'Show surf errors in Watson Equation')
        for surf,TdegC in zip(self.surfL,self.t_CL):
            surf_calc = self.get_surf_at_TdegC( TdegC )
            print( 'at T=%6g degC'%TdegC, 'surf=%6g'%surf, 'surfcalc=%6g'%surf_calc, 
                  '%%diff=%8g%%'%((surf_calc-surf)*100/surf,) )

        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Surface Tension\n(Follow Watson Equation: Hv = A * (1 - Tr)^n)', 
              xlabel='Temperature (degR)', ylabel='Surf (lbf/in)'):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.subplots( figsize=(12,8))
            
        
        xL = []
        yL = []
        dx = ( self.Tc_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_surf_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL + [self.Tc_C]
        surfL  = self.surfL  + [0]

        t_RL = [ get_value(t,'degC','degR') for t in t_CL]
        surfL = [self.get_eng_surf_at_TdegR(t) for t in t_RL]

        _line, = plt.plot( t_RL, surfL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='Surf Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

        plt.title(title , fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
                
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        
        if do_show:
            set_ax2_degC( plt.gca() )
            plt.tight_layout()
            plt.show()





if __name__ == "__main__":

    print( 'list of surf data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    for t in T_C_common:
        print( t, surf_at_tD[t])


    print()
    print( 'Results of calling "get_surf_0_to_140T_data_at_conc" with any concentration.')
    print( 'Should match original data for surf at pcent_H2O2 for each temperature')
    print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    for c in pcent_h2o2L:
        print( c, get_surf_0_to_140T_data_at_conc(c))

    print( 'Try some intermediate concentrations.')
    for c in [2,5,77.5]:
        print( c, get_surf_0_to_140T_data_at_conc(c))


    surf_obj = Surf_Peroxide_Liquid( pcent_H2O2=85 )
    surf_obj.summ_print()


    A_list = []
    n_list = []

    for conc in pcent_h2o2L:
        surf_liq = Surf_Peroxide_Liquid( pcent_H2O2=conc )
        surf_liq.summ_print()

        A_list.append( float(surf_liq.A_opt) )
        n_list.append( float(surf_liq.n_opt) )


        if conc == pcent_h2o2L[-1]:
            surf_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            surf_liq.plot( do_show=False, new_fig=True )
        else:
            surf_liq.plot( do_show=False, new_fig=False )

    print()
    print( 'A_list =', A_list)
    print( 'n_list =', n_list)


