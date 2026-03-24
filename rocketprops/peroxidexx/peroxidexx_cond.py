from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp,
                                                          perox_freeze_pt_degC_terp,
                                                          perox_Tcrit_degC_terp, get_molWt_mix)
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

pcent_propD = {} # key=pcent_H2O2, value=Cond_Peroxide_Liquid at pcent_H2O2

def get_eng_cond_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = Cond_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_cond_at_TdegR( TdegR )


class Cond_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):
        """
        Calculates Thermal Conductivity using Dual-Master Blending.
        Handles the shift in hump and critical point accurately for all mixtures.
        """

        self.pcent_H2O2 = pcent_H2O2
        self.frac_H2O2 = pcent_H2O2 / 100.0

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )
        self.Tc_K = self.Tc_C + 273.15

        # 1. Master Curves (Extended to Supercritical Range)
        # degC
        self.t_ref = [0, 20, 40, 60, 80, 100, 120, 140, 200, 300, 370, 400, 450]
        # Pure Water (0%) (W/m·K)
        self.k_water = [0.561, 0.598, 0.631, 0.654, 0.670, 0.679, 0.683, 0.684, 0.660, 0.540, 0.120, 0.040, 0.030]
        # Pure H2O2 (100%)  (W/m·K)
        self.k_h2o2 = [0.421, 0.446, 0.465, 0.479, 0.488, 0.493, 0.492, 0.488, 0.420, 0.280, 0.210, 0.150, 0.080]

        self.water_k_terp = InterpProp( self.t_ref, self.k_water, extrapOK=True)
        self.h2o2_k_terp = InterpProp( self.t_ref, self.k_h2o2, extrapOK=True)

        if self.Tfreeze_C < 0:
            self.t_CL = [ self.Tfreeze_C ] # list of temperatures (degC)
        else:
            self.t_CL = [] # list of temperatures (degC)

        for tc in self.t_ref:
            if tc < self.Tc_C:
                if tc!=370 :
                    self.t_CL.append( tc )
                elif pcent_H2O2 < 14:
                    self.t_CL.append( tc )

        self.condL = [] # list of cond (W/m·K)
        for tc in self.t_CL:
            k_water = self.water_k_terp( tc )
            k_h2o2 = self.h2o2_k_terp( tc )
            self.condL.append( self.frac_H2O2 * k_h2o2 + (1 - self.frac_H2O2) * k_water )

        self.k_terp = InterpProp( self.t_CL, self.condL, extrapOK=True) # (W/m·K)


    def get_cond_at_TdegC(self, TdegC):
        """Return cond in units of W/m/K for input temperature in degC"""
        k_mix = self.k_terp( TdegC )
        
        return k_mix

    def get_eng_cond_at_TdegR(self, TdegR):
        """Return cond in units of BTU/hr/ft/delF  for input temperature in degR"""
        k = self.get_cond_at_TdegC( get_value( TdegR, 'degR', 'degC') )
        return  get_value( k, 'W/m/K', 'BTU/hr/ft/delF')



    def summ_print(self):
        print( '\n=== Summary for Cond_Peroxide_Liquid( %g ) ==='%self.pcent_H2O2 )
        print( 'T data (degC)', " ".join(['%6g'%t for t in self.t_CL]))
        print( 'Cond data (W/m·K)'," ".join( ['%6g'%d for d in self.condL]))
        print()
        print( "Tc_C = %g degC"%self.Tc_C )

        print( 'Show Cond errors in mixture calc')
        for cond,TdegC in zip(self.condL,self.t_CL):
            cond_calc = self.get_cond_at_TdegC( TdegC )
            if TdegC in T_C_common:
                cond_data =  get_k_data(TdegC, self.pcent_H2O2)
            else:
                cond_data = 1
            print( 'at T=%6g degC'%TdegC, 'cond=%6g'%cond_data, 'cond_calc=%6g'%cond_calc, 
                  '%%diff=%8g%%'%((cond_calc-cond_data)*100/cond_data,) )
        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Thermal Conductivity', xlabel='Temperature (degR)', ylabel='Cond (BTU/hr/ft/delF)'):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.figure(figsize=(9, 6))
        
        xL = []
        yL = []
        dx = ( self.Tc_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_cond_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL + [self.Tc_C]
        t_RL = [get_value(t,'degC','degR') for t in t_CL]
        condL  = self.condL  + [self.get_cond_at_TdegC( self.Tc_C )]
        condL = [get_value( k, 'W/m/K', 'BTU/hr/ft/delF') for k in condL]

        _line, = plt.plot( t_RL, condL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='Cond Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

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

# earlier data grid for cond
T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]

def get_k_data(TdegC, pcent_h2o2):
    # Example Usage:
    # val = get_k_data(140, 90)
    # print(f"K at 140C, 90%: {val} W/m·K")

    # 1. Grid Definition
    
    htp_k_data = {
        0:   [0.561, 0.598, 0.631, 0.654, 0.670, 0.679, 0.683, 0.684],
        3:   [0.558, 0.594, 0.627, 0.650, 0.665, 0.674, 0.678, 0.679],
        10:  [0.551, 0.585, 0.617, 0.638, 0.652, 0.660, 0.664, 0.665],
        35:  [0.528, 0.556, 0.581, 0.598, 0.609, 0.615, 0.617, 0.616],
        50:  [0.515, 0.540, 0.561, 0.575, 0.585, 0.589, 0.590, 0.588],
        70:  [0.495, 0.518, 0.536, 0.548, 0.555, 0.556, 0.554, 0.549],
        85:  [0.458, 0.482, 0.501, 0.514, 0.522, 0.525, 0.523, 0.519],
        90:  [0.446, 0.470, 0.489, 0.503, 0.511, 0.514, 0.512, 0.508],
        98:  [0.426, 0.451, 0.470, 0.484, 0.493, 0.497, 0.496, 0.492],
        100: [0.421, 0.446, 0.465, 0.479, 0.488, 0.493, 0.492, 0.488]
    }

    # 2. Extract specific list for the concentration
    # Using .get() to avoid KeyError
    k_list = htp_k_data.get(pcent_h2o2)
    if k_list is None:
        raise ValueError(f"Concentration {pcent_h2o2}% not found in grid.")

    # 3. Find index of the temperature
    try:
        t_idx = T_C_common.index(TdegC)
    except ValueError:
        raise ValueError(f"Temperature {TdegC}°C not found in common temperature list.")

    # 4. Return the specific thermal conductivity value
    return k_list[t_idx]


if __name__ == "__main__":

    

    print( '========== Test Cond_Peroxide_Liquid =============\n')

    for conc in pcent_h2o2L:
        cond_liq = Cond_Peroxide_Liquid( pcent_H2O2=conc )
        cond_liq.summ_print()


        if conc == pcent_h2o2L[-1]:
            cond_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            cond_liq.plot( do_show=False, new_fig=True )
        else:
            cond_liq.plot( do_show=False, new_fig=False )
