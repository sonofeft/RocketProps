from scipy.optimize import curve_fit
import numpy as np
from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, 
                                                          perox_freeze_pt_degC_terp, perox_SG_at_freeze_pt_terp,
                                                          perox_Dcrit_SG_terp, perox_Tcrit_degC_terp, get_molWt_mix)

# Standard temperature grid for most 2D properties (°C)
T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

# Density (Specific Gravity) - Source: Schumb (1955)
htp_density_dataD = {
    0:   [1.000, 0.998, 0.992, 0.983, 0.972, 0.958, 0.943, 0.926],
    3:   [1.011, 1.009, 1.003, 0.994, 0.983, 0.969, 0.954, 0.937],
    10:  [1.039, 1.035, 1.028, 1.018, 1.006, 0.992, 0.976, 0.959],
    35:  [1.141, 1.133, 1.121, 1.108, 1.093, 1.077, 1.059, 1.040],
    50:  [1.205, 1.194, 1.181, 1.166, 1.150, 1.132, 1.113, 1.093],
    70:  [1.308, 1.290, 1.272, 1.253, 1.234, 1.214, 1.193, 1.171],
    85:  [1.380, 1.359, 1.338, 1.317, 1.295, 1.273, 1.251, 1.228],
    90:  [1.405, 1.383, 1.361, 1.339, 1.316, 1.293, 1.270, 1.247],
    98:  [1.446, 1.422, 1.398, 1.374, 1.350, 1.325, 1.300, 1.275],
    100: [1.470, 1.443, 1.417, 1.392, 1.367, 1.341, 1.315, 1.289]
}

sg_at_tD = {} # key=temperature (degC), value=list of sg at temperature

for i,T in enumerate(T_C_common):
    sgL = []
    for pcent_H2O2 in htp_density_dataD.keys():
        sgL.append( htp_density_dataD[ pcent_H2O2 ][i] )
    sg_at_tD[ T ] = sgL


sg_at_t_terpD = {} # key=temperature (degC), value=interpolator for sg at temperature
for T in T_C_common:
    sg_at_t_terpD[T] = InterpProp( pcent_h2o2L, sg_at_tD[T], extrapOK=True )

# use this to get interpolated sg data for any given concentration
def get_sg_0_to_140T_data_at_conc( pcent_H2O2 ):
    sg_at_tL = [ round(sg_at_t_terpD[T](pcent_H2O2), 8) for T in T_C_common ]
    return sg_at_tL

# ============ Get full range SG interpolator ==============

pcent_propD = {} # key=pcent_H2O2, value=SG_Peroxide_Liquid at pcent_H2O2

def get_eng_sg_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = SG_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_sg_at_TdegR( TdegR )

def poly2(t, c0, c1, c2):
    return c0 + c1*t + c2*t**2

class SG_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.SGfreeze = perox_SG_at_freeze_pt_terp( pcent_H2O2 )

        if self.Tfreeze_C < 0:
            self.t_CL = [ self.Tfreeze_C ] + T_C_common.copy()
            self.sgL  = [ self.SGfreeze ]  + get_sg_0_to_140T_data_at_conc( pcent_H2O2 )
        else:
            self.t_CL =  T_C_common.copy()
            self.sgL  =  get_sg_0_to_140T_data_at_conc( pcent_H2O2 )

        # fit t_CL, sgL to a quadratic polynomial
        popt, _ = curve_fit(poly2, self.t_CL, self.sgL)
        self.c0, self.c1, self.c2 = popt

        self.T_handover_C = self.t_CL[-1]
        self.molWt = get_molWt_mix( pcent_H2O2 )
        self.SGc = perox_Dcrit_SG_terp( pcent_H2O2 )
        self.Vc = self.molWt / self.SGc
        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )
        self.Tc_K = self.Tc_C + 273.15

        # Rackett Handshake: Solve for Zra at 140C
        tr_handover = (self.T_handover_C + 273.15) / self.Tc_K
        sg_handover = poly2(self.T_handover_C, self.c0, self.c1, self.c2)
        v_handover = self.molWt / sg_handover

        self.Zra = (v_handover / self.Vc) ** (1.0 / (1 - tr_handover)**(2/7))

    def get_SG_at_TdegC(self, TdegC):

            
        if TdegC <= self.T_handover_C:
            # Fitted Quadratic Polynomial
            rho = poly2( TdegC, self.c0, self.c1, self.c2)
            return rho
        
        else:
            # Rackett Equation optimized for Thandover and Tc critical point
            TdegK = TdegC +  273.15            
            Tr = np.clip(TdegK / self.Tc_K, 0, 1.0)
            
            V = self.Vc * (self.Zra**((1 - Tr)**(2/7)))
            return self.molWt / V
    
    def get_eng_sg_at_TdegR( self, TdegR ):
        """Return SG in units g/cc"""
        TdegC = get_value( TdegR, 'degR', 'degC' )
        sg = self.get_SG_at_TdegC( TdegC )
        return sg


        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Density', xlabel='Temperature (degR)', ylabel='Density (SG)'):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.figure(figsize=(9, 6))
        
        xL = []
        yL = []
        dx = ( self.Tc_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_sg_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL + [self.Tc_C]
        t_RL = [get_value(t,'degC','degR') for t in t_CL]
        sgL  = self.sgL  + [self.SGc]
        _line, = plt.plot( t_RL, sgL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='SG Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

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


    def summ_print(self):
        print( '=== Summary for SG_Peroxide_Liquid( %g ) ==='%self.pcent_H2O2 )
        print( 'T data (degC)', " ".join(['%6g'%t for t in self.t_CL]))
        print( 'SG data  at T'," ".join( ['%6g'%d for d in self.sgL]))
        print()
        print( ' ... Polynomial Constants ...')
        print( "c0=%g, c1=%g, c2=%g"%(self.c0, self.c1, self.c2) )
        print( "Tc_C = %g degC"%self.Tc_C, '    Tc_R = %g degR'%(self.Tc_K*1.8,) )
        print( "T_handover_C = %g degC"%self.T_handover_C )
        print( "molWt=%g"%self.molWt )
        print( "SGc = %g SG"%self.SGc)
        print( "Vc = %g cc/gmole"%self.Vc)
        print( "Zra = %g "%self.Zra)

        print( 'Show SG errors in quadratic polynomial')
        for SG,TdegC in zip(self.sgL,self.t_CL):
            sg_calc = self.get_SG_at_TdegC( TdegC )
            print( 'at T=%6g degC'%TdegC, 'SG=%6g'%SG, 'SGcalc=%6g'%sg_calc, '%%diff=%8g%%'%((sg_calc-SG)*100/SG,) )



if __name__ == "__main__":

    print( 'list of sg data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    for t in T_C_common:
        print( t, sg_at_tD[t])


    print()
    print( 'Results of calling "get_sg_0_to_140T_data_at_conc" with any concentration.')
    print( 'Should match original data for sg at pcent_H2O2 for each temperature')
    print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    for c in pcent_h2o2L:
        print( c, get_sg_0_to_140T_data_at_conc(c))

    print( 'Try some intermediate concentrations.')
    for c in [2,5,77.5]:
        print( c, get_sg_0_to_140T_data_at_conc(c))

    print( '========== Test SG_Peroxide_Liquid =============\n')

    for conc in pcent_h2o2L:
        sg_liq = SG_Peroxide_Liquid( pcent_H2O2=conc )
        sg_liq.summ_print()

        if conc == pcent_h2o2L[-1]:
            sg_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            sg_liq.plot( do_show=False, new_fig=True )
        else:
            sg_liq.plot( do_show=False, new_fig=False )

        
