
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of H2O2
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='H2O2')

    def set_std_state(self):
        """Set properties and standard state of Propellant, H2O2"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 518.67 # degR
        self.P       = 14.7 # psia
        self.Pvap    = 0.018011480310070306 # psia
        self.Pc      = 3144.418153990189 # psia
        self.Tc      = 1314.3600000000001 # degR
        self.Zc      = 0.2595981624582702 # Z at critical pt
        self.omega   = 0.33721326122742146 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.4500213026088176 # SG
        self.visc    = 0.01363059463754792 # poise
        self.cond    = 0.25435984611807494 # BTU/hr/ft/delF
        self.Tnbp    = 762.0299999999999 # degR
        self.Tfreeze = 490.8959999999999 # degR
        self.Ttriple = 490.8959999999999 # degR
        self.Cp      = 0.6568527068398862 # BTU/lbm/delF
        self.MolWt   = 34.0147 # g/gmole
        self.Hvap    = 672.7637352128993 # BTU/lbm
        self.surf    = 0.0004645984856406036 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.37348671596822774, 0.40481238016981635, 0.43613804437140496, 0.4674637085729936, 0.4987893727745822, 0.5301150369761708, 0.5614407011777593, 0.592766365379348, 0.6240920295809367, 0.6554176937825252, 0.6867433579841138, 0.7180690221857025, 0.7493946863872911, 0.7807203505888797, 0.8120460147904682, 0.8433716789920569, 0.8746973431936456, 0.9060230073952342, 0.9373486715968227, 0.9686743357984113, 1.0]
        self.tL = [490.89599999999984, 532.0691999999999, 573.2423999999999, 614.4155999999999, 655.5887999999999, 696.762, 737.9351999999999, 779.1084, 820.2816, 861.4548, 902.6279999999999, 943.8012, 984.9744000000001, 1026.1476, 1067.3208, 1108.494, 1149.6672, 1190.8404000000003, 1232.0136, 1273.1868, 1314.3600000000001]
        
        self.log10pL  = [-2.275724130399211, -1.504838151070994, -0.8407043715414616, -0.28044890940664713, 0.20091481766514604, 0.6150525901327548, 0.9767988391108672, 1.30149008874308, 1.588886837181701, 1.8437609276605418, 2.0712527952463575, 2.2755578653139086, 2.4601345840944733, 2.6278621952233783, 2.7811620989499577, 2.922093064480465, 3.052428259245091, 3.1737217074686535, 3.2873749809215993, 3.3947380838433374, 3.4975402949675636]
        self.log10viscL = [-1.7362641125724994, -1.9230844000530387, -2.0833354761119987, -2.2220088217114298, -2.3435973279008295, -2.4502467933887866, -2.5451054228507233, -2.630183883953269, -2.70672149332533, -2.7759428795169723, -2.8388492264729037, -2.896267012180683, -2.9488845233090615, -2.9972795791663684, -3.041940838752937, -3.083284359323581, -3.121666596867247, -3.1573947096457515, -3.190734795702789, -3.2219185320318346, -3.2511853391043397]
        self.condL = [0.24293874050715555, 0.25919830561293244, 0.2710898048555301, 0.279199613312928, 0.2840458436818196, 0.2845354175415366, 0.28249486924119, 0.27359694554744407, 0.2563617340639294, 0.23871043580305307, 0.22092972970015584, 0.2020006966827546, 0.182795101805341, 0.16418471012240649, 0.14664749832156065, 0.12965691748202998, 0.11278474937056618, 0.09560834358046394, 0.07774526941222407, 0.05925717936133964, 0.04052036476919289]
        self.cpL = [0.6417789242380816, 0.664330419973155, 0.6862526272917834, 0.707431327371711, 0.7278663047656492, 0.7475574000201745, 0.7665037252526088, 0.799813922309229, 0.8294482013451827, 0.8643545228770187, 0.9086481340039033, 0.9632822828254821, 1.031539485902784, 1.1205535526585588, 1.2366763981769782, 1.4072170062412415, 1.6919280635704759, 2.259180163198248, 4.307307584594864, 12.486041396496892, 22.780548390178712]
        self.hvapL = [684.1940240756664, 667.4408493497249, 651.8577619607537, 637.45698557116, 624.0290853481641, 610.2749981712038, 595.9067113255761, 580.8497822556765, 565.0141378960863, 548.2891644017735, 530.5366453848856, 511.58028290355037, 491.18955587679045, 469.053702387447, 444.7373527508652, 417.59921987862344, 386.62810030373606, 350.06436063414736, 304.32505364990215, 239.54218073197015, 0.0]
        self.surfL = [0.0004833514150659162, 0.00045558699558114683, 0.0004280458047928396, 0.00040073830881752275, 0.00037367610747736065, 0.00034687213554113547, 0.00032034091548643797, 0.0002940988796035895, 0.0002681647872773778, 0.00024256027587775847, 0.0002173106041416678, 0.00019244568142446237, 0.00016800153705588715, 0.00014402249730904255, 0.00012056456258604658, 9.770096290289468e-05, 7.553203399511073e-05, 5.4204781690929133e-05, 3.395854740031771e-05, 1.526746839115004e-05, 0.0]    
        self.SG_liqL = [1.4699350522955354, 1.4404204212180591, 1.4109441665377476, 1.3815062882546005, 1.3521067863686183, 1.3227456608798, 1.2934229117881466, 1.2658427028056172, 1.2376825597548646, 1.2084775704759874, 1.1780692015126581, 1.1462559548085713, 1.1127753462966548, 1.0772749375400514, 1.0392630775387324, 0.9980188958665579, 0.9524113179972414, 0.900482663626705, 0.8382698889854712, 0.7549251872128433, 0.46799999999999997]
        self.log10SG_vapL = [-6.260969155705786, -5.524988824775669, -4.892996879692536, -4.362301395337222, -3.907915144196679, -3.518045606553121, -3.1775949850132834, -2.870697170945925, -2.5972351621969216, -2.352081164367227, -2.1297308122009837, -1.9256363033900121, -1.7359698494075615, -1.5574188176284405, -1.3869944697725043, -1.2218311683699026, -1.0589383500868241, -0.8948293201560957, -0.7248440866742951, -0.5416076162627375, -0.3297541469258757]
        
        # ========== save dataSrc for each value ===========
        data_srcD = {} # index=parameter, value=data source
        data_srcD["main"]    = "RocketProps"
        data_srcD["T"]       = "RocketProps" # degR
        data_srcD["P"]       = "RocketProps" # psia
        data_srcD["Pvap"]    = "RocketProps" # psia
        data_srcD["Pc"]      = "RocketProps" # psia
        data_srcD["Tc"]      = "RocketProps" # degR
        data_srcD["Zc"]      = "RocketProps" # Z at critical pt
        data_srcD["omega"]   = "RocketProps" # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        data_srcD["SG"]      = "RocketProps" # SG
        data_srcD["visc"]    = "RocketProps" # poise
        data_srcD["cond"]    = "RocketProps" # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = "RocketProps" # degR
        data_srcD["Tfreeze"] = "RocketProps" # degR
        data_srcD["Ttriple"] = "RocketProps" # degR
        data_srcD["Cp"]      = "RocketProps" # BTU/lbm/delF
        data_srcD["MolWt"]   = "RocketProps" # g/gmole
        data_srcD["Hvap"]    = "RocketProps" # BTU/lbm
        data_srcD["surf"]    = "RocketProps" # lbf/in

        data_srcD["trL"]     = "RocketProps"
        data_srcD["tL"]      = "RocketProps"

        data_srcD["log10pL"]      = "RocketProps"
        data_srcD["log10viscL"]   = "RocketProps"
        data_srcD["condL"]        = "RocketProps"
        data_srcD["cpL"]          = "RocketProps"
        data_srcD["hvapL"]        = "RocketProps"
        data_srcD["surfL"]        = "RocketProps"    
        data_srcD["SG_liqL"]      = "RocketProps"
        data_srcD["log10SG_vapL"] = "RocketProps"
        self.data_srcD = data_srcD
        
        
        # ========== initialize saturation interpolators ===========
        self.log10p_terp = InterpProp(self.trL, self.log10pL, extrapOK=False)
        try:
            self.log10visc_terp = InterpProp(self.trL, self.log10viscL, extrapOK=False)
        except:
            pass
        try:
            self.cond_terp = InterpProp(self.trL, self.condL, extrapOK=False)
        except:
            pass
        self.cp_terp = InterpProp(self.trL, self.cpL, extrapOK=False)
        self.hvap_terp = InterpProp(self.trL, self.hvapL, extrapOK=False)
        self.surf_terp = InterpProp(self.trL, self.surfL, extrapOK=False)
        self.SG_liq_terp = InterpProp(self.trL, self.SG_liqL, extrapOK=False)
        self.log10SG_vap_terp = InterpProp(self.trL, self.log10SG_vapL, extrapOK=False)

if __name__ == '__main__':
    from rocketprops.unit_conv_data import get_value
    C = Prop()
    print('T = %g R = %g K'%( C.T, C.T/1.8 ))
    print('SurfaceTension = %g lbf/in'%C.surf, ' = ', get_value(C.surf, 'lbf/in', 'mN/m'), 'mN/m' )
    
    print()
    print(' Tr_data_range =', C.Tr_data_range())
    print('  T_data_range=',C.T_data_range())
    print('  P_data_range=', C.P_data_range())
    
    print( 'omega =%s'%C.omega )
    
    C.plot_sat_props()

    
