from rocketprops.InterpProp_scipy import InterpProp
from rocketprops.unit_conv_data import get_value
# from rocketprops.rocket_prop import get_prop

from rocketprops.peroxidexx.peroxidexx_main_data import (perox_Tcrit_degC_terp, perox_boil_pt_degC_terp,
                                                          perox_freeze_pt_degC_terp, 
                                                          perox_Tcrit_degC_terp, perox_Cp_at_freeze_pt_terp)
from rocketprops.peroxidexx.peroxidexx_main_data import set_ax2_degC

# use Water data from RocketProp
water_Tc = 1164.7728 # degR

water_tL = [491.68800000000005, 527.1135157894737, 562.5390315789474, 597.9645473684211, 633.3900631578947, 668.8155789473684, 704.2410947368421, 739.6666105263158, 775.0921263157895, 810.5176421052631, 845.9431578947368, 881.3686736842105, 916.7941894736841, 952.219705263158, 987.6452210526315, 1023.0707368421051, 1058.496252631579, 1093.9217684210525, 1129.3472842105264, 1164.7728]
water_cpL = [1.0085828151338445, 1.0001386435988233, 0.9989468513487699, 1.000174096181458, 1.002852679129289, 1.007141475259904, 1.0134824045589228, 1.0223726552249355, 1.0343646975260634, 1.0501485670174502, 1.0706801238105141, 1.0973766843213486, 1.1324563228010904, 1.1796043401324912, 1.2454360291065152, 1.3431185754080999, 1.5029427770298898, 1.8141941201564458, 2.765067965250912, 91.30908450294936]
water_CpAtTdegR = InterpProp( water_tL, water_cpL)

# Standard temperature grid for most 2D properties (°C)
T_C_common = [0, 20, 40, 60, 80, 100, 120, 140]
pcent_h2o2L = [0, 3, 10, 35, 50, 70, 85, 90, 98, 100]


# High-Temp Pure Components
h2o2_cp_kJL   = [3.22, 3.29, 3.58, 4.02, 4.75, 6.20, 11.40, 85.0] # High T H2O2
water_cp_kJL  = [4.28, 4.31, 4.50, 4.86, 5.72, 10.10, 8.0, 5.0] # High T water approx

# convert to BTU/lbm/delF
water_btuL = [get_value( float(cp), 'kJ/kg/delK', 'BTU/lbm/delF' ) for cp in water_cp_kJL]

# -------------- data for very high temperature 100% H2O2 ----------
# Temperature in degrees Celsius
temp_degC_H2O2_hiT = [140, 150, 200, 250, 300, 350, 400, 450]
temp_degR_H2O2_hiT = [get_value(t, 'degC', 'degR') for t in temp_degC_H2O2_hiT]

for t_R, cp in zip(temp_degR_H2O2_hiT, water_btuL):
    if t_R < water_Tc:
        print( 'TdegR=%g water cp=%g, cp_ref=%g'%(t_R, water_CpAtTdegR( t_R ), cp))

# Specific Heat Capacity in kJ/(kg·K)
# Note: 450C is an approximation of the asymptotic spike; 
# the value at the critical point (457C) is mathematically infinite.
cp_kj_kgK_H2O2_hiT = [3.22, 3.29, 3.58, 4.02, 4.75, 6.20, 11.40, 85.0]

hiT_H2O2_degR_terp = InterpProp(temp_degR_H2O2_hiT, cp_kj_kgK_H2O2_hiT, extrapOK=True)


# 2D Grid Data
htp_cp_dataD = {
    0:   [4.21, 4.18, 4.18, 4.18, 4.20, 4.22, 4.24, 4.28],
    3:   [4.16, 4.14, 4.14, 4.15, 4.17, 4.19, 4.21, 4.25],
    10:  [4.04, 4.05, 4.07, 4.10, 4.13, 4.16, 4.19, 4.23],
    35:  [3.66, 3.70, 3.76, 3.82, 3.87, 3.93, 3.99, 4.04],
    50:  [3.47, 3.52, 3.58, 3.65, 3.71, 3.78, 3.84, 3.90],
    70:  [3.22, 3.28, 3.34, 3.41, 3.47, 3.53, 3.59, 3.66],
    85:  [2.96, 3.03, 3.09, 3.16, 3.23, 3.30, 3.37, 3.44],
    90:  [2.87, 2.94, 3.01, 3.08, 3.15, 3.22, 3.29, 3.36],
    98:  [2.73, 2.80, 2.88, 2.95, 3.03, 3.11, 3.18, 3.25],
    100: [2.688333, 2.771429, 2.852143, 2.930476, 3.006429, 3.08, 3.151191, 3.22],
    #100: [2.69, 2.77, 2.85, 2.93, 3.01, 3.08, 3.15, 3.22]
}


cp_at_tD = {} # key=temperature (degC), value=list of cp at temperature

for i,T in enumerate(T_C_common):
    cpL = []
    for pcent_H2O2 in htp_cp_dataD.keys():
        cpL.append( htp_cp_dataD[ pcent_H2O2 ][i] )
    cp_at_tD[ T ] = cpL


cp_at_t_terpD = {} # key=temperature (degC), value=interpolator for cp at temperature
for T in T_C_common:
    cp_at_t_terpD[T] = InterpProp( pcent_h2o2L, cp_at_tD[T], extrapOK=True )

# use this to get interpolated cp data for any given concentration
def get_cp_0_to_140T_data_at_conc( pcent_H2O2 ):
    cp_at_tL = [ round(cp_at_t_terpD[T](pcent_H2O2), 8) for T in T_C_common ]
    return cp_at_tL


cp_water_low_temp_terp = InterpProp( T_C_common, [4.21, 4.18, 4.18, 4.18, 4.20, 4.22, 4.24, 4.28], extrapOK=True)
cp_h2o2_low_temp_terp = InterpProp( T_C_common, [2.688333, 2.771429, 2.852143, 2.930476, 3.006429, 3.08, 3.151191, 3.22], extrapOK=True)

# tr_water_140C = (140 + 273.15) / 647.096
# tr_h2o2_140C  = (140 + 273.15) / 730.2

cp_water_140  = 4.28 # kJ/kg/delK
cp_h2o2_140   = 3.22 # kJ/kg/delK


pcent_propD = {} # key=pcent_H2O2, value=CP_Peroxide_Liquid at pcent_H2O2

def get_eng_cp_at_TdegR( pcent_H2O2, TdegR ):
    if pcent_H2O2 not in pcent_propD:
        pcent_propD[pcent_H2O2] = CP_Peroxide_Liquid( pcent_H2O2=pcent_H2O2 )

    return pcent_propD[pcent_H2O2].get_eng_cp_at_TdegR( TdegR )

pcent_propD = {} # key=pcent_H2O2, value=XX_Peroxide_Liquid at pcent_H2O2

class CP_Peroxide_Liquid:
    def __init__(self, pcent_H2O2=70):

        self.pcent_H2O2 = pcent_H2O2

        self.Tfreeze_C = perox_freeze_pt_degC_terp( pcent_H2O2 )
        self.CPfreeze = perox_Cp_at_freeze_pt_terp( pcent_H2O2 )

        if self.Tfreeze_C < 0:
            self.t_CL = [ self.Tfreeze_C ] + T_C_common.copy()
            self.cpL  = [ self.CPfreeze ]  + get_cp_0_to_140T_data_at_conc( pcent_H2O2 )
        else:
            self.t_CL =  T_C_common.copy()
            self.cpL  =  get_cp_0_to_140T_data_at_conc( pcent_H2O2 )

        self.cp_low_temp_terp = InterpProp( self.t_CL, self.cpL, extrapOK=True)

        # fit t_CL, cpL to a quadratic polynomial
        self.T_handover_C = 140
        self.Tc_C = perox_Tcrit_degC_terp( pcent_H2O2 )
        self.Tc_K = self.Tc_C + 273.15

        self.Tboil_C = perox_boil_pt_degC_terp( pcent_H2O2 )

        # get Cp at 140C for H2O2 and water

        self.wt_frac = self.pcent_H2O2 / 100.0
        self.cp_mix_140_weighted = (self.wt_frac * cp_h2o2_140) + ((1 - self.wt_frac) * cp_water_140)

        # get the interpolation of the pcent_H2O2 Cp at 140
        self.cp_calc_140 = self.cp_low_temp_terp( 140 )

        # use interpolated value to correct weighted mix value
        self.corr_factor = self.cp_calc_140 / self.cp_mix_140_weighted 

    def get_Cp_at_TdegC(self, TdegC):            
        if TdegC <= self.T_handover_C:
            cp = self.cp_low_temp_terp( TdegC )
            return get_value( float(cp), 'kJ/kg/delK', 'BTU/lbm/delF' )
        
        else:
            TdegR = get_value( TdegC, 'degC', 'degR')

            cp_water_at_TdegR = get_value( water_CpAtTdegR( TdegR ), 'BTU/lbm/delF', 'kJ/kg/delK')
            
            cp_h2o2_at_TdegR  = hiT_H2O2_degR_terp( TdegR ) # 'kJ/kg/delK'
            
            cp_at_TdegR_weighted = (self.wt_frac * cp_h2o2_at_TdegR) + ((1 - self.wt_frac) * cp_water_at_TdegR)            

            cp = self.corr_factor * cp_at_TdegR_weighted
            return get_value( float(cp), 'kJ/kg/delK', 'BTU/lbm/delF' )

    def get_eng_cp_at_TdegR(self, TdegR):
        return self.get_Cp_at_TdegC( get_value( TdegR, 'degR', 'degC') )


    def summ_print(self):
        print( '=== Summary for CP_Peroxide_Liquid( %g ) ==='%self.pcent_H2O2 )
        print( 'T data (degC)', " ".join(['%6g'%t for t in self.t_CL]))
        print( 'Cp data  at T'," ".join( ['%6g'%d for d in self.cpL]))
        print()
        print( "Tboil_C = %g degC"%self.Tboil_C )
        print( "Tc_C = %g degC"%self.Tc_C )
        print( "T_handover_C = %g degC"%self.T_handover_C )

        
    def plot(self, Npts=100, do_show=True, new_fig=True,
              title='Peroxide Density', xlabel='Temperature (degR)', ylabel='Cp (BTU/lbm-degF)'):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.figure(figsize=(12, 9))
        
        xL = []
        yL = []
        Tmax_C = 350
        dx = ( Tmax_C - self.Tfreeze_C ) / Npts
        for i in range(Npts+1):
            TdegC = self.Tfreeze_C + i * dx
            xL.append( get_value(TdegC,'degC','degR') )
            yL.append( self.get_eng_cp_at_TdegR( xL[-1] ) )
        
        t_CL = self.t_CL #+ [self.Tc_C]
        t_RL = [get_value(t,'degC','degR') for t in t_CL]
        cpL  = self.cpL  #+ [self.SGc]
        cpL = [get_value( float(cp), 'kJ/kg/delK', 'BTU/lbm/delF' ) for cp in cpL]
        _line, = plt.plot( t_RL, cpL, 'o', label='%g%% Data'%self.pcent_H2O2, markersize=8 )
        plt.plot(xL, yL, '-', label='Cp Peroxide_%g'%self.pcent_H2O2, color=_line.get_color() )

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
            # plt.gca().set_ylim(top=4.0)
            # plt.ylim(0.4, 4.0)
            plt.tight_layout()
            plt.show()


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # print( 'list of cp data for each temperature (degC)[0, 20, 40, 60, 80, 100, 120, 140]' )
    # for t in T_C_common:
    #     print( t, cp_at_tD[t])


    print()
    # print( 'Results of calling "get_cp_0_to_140T_data_at_conc" with any concentration.')
    # print( 'Should match original data for cp at pcent_H2O2 for each temperature')
    # print( '  [0,   20,    40,    60,    80,    100,   120,   140]    (degC)' )
    # for c in pcent_h2o2L:
    #     print( c, get_cp_0_to_140T_data_at_conc(c))

    print( 'Try some intermediate concentrations.')
    for c in [2,5,77.5]:
        print( c, get_cp_0_to_140T_data_at_conc(c))


    for conc in pcent_h2o2L:
        cp_liq = CP_Peroxide_Liquid( pcent_H2O2=conc )
        # cp_liq.summ_print()

        if conc == pcent_h2o2L[-1]:
            cp_liq.plot( do_show=True, new_fig=False )
        elif conc == pcent_h2o2L[0]:
            cp_liq.plot( do_show=False, new_fig=True )
        else:
            cp_liq.plot( do_show=False, new_fig=False )

    