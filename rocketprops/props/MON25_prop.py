
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of MON25
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MON25')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MON25"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.7 # degR
        self.P       = 61.7132926063791 # psia
        self.Pvap    = 61.7132926063791 # psia
        self.Pc      = 1733.6097044931748 # psia
        self.Tc      = 725.0 # degR
        self.Zc      = 0.43222849888080184 # Z at critical pt
        self.omega   = 0.6690226514442315 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.389908384165817 # SG
        self.visc    = 0.004426776053891213 # poise
        self.cond    = 0.11493225244740853 # BTU/hr/ft/delF
        self.Tnbp    = 474.7505320208363 # degR
        self.Tfreeze = 389.12566220844053 # degR
        self.Ttriple = 389.12566220844053 # degR
        self.Cp      = 0.4686178740723048 # BTU/lbm/delF
        self.MolWt   = 81.18748953501195 # g/gmole
        self.Hvap    = 150.97046711243692 # BTU/lbm
        self.surf    = 0.00020180458912914698 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.5367250513219869, 0.5598887987558876, 0.5830525461897882, 0.6062162936236889, 0.6293800410575895, 0.6525437884914902, 0.6757075359253908, 0.6988712833592915, 0.7220350307931922, 0.7451987782270928, 0.7683625256609934, 0.7915262730948941, 0.8146900205287948, 0.8378537679626954, 0.8610175153965961, 0.8841812628304968, 0.9073450102643974, 0.930508757698298, 0.9536725051321987, 0.9768362525660994, 1.0]
        self.tL = [389.1256622084405, 405.9193790980185, 422.71309598759643, 439.50681287717447, 456.3005297667524, 473.09424665633037, 489.88796354590835, 506.6816804354863, 523.4753973250644, 540.2691142146423, 557.0628311042202, 573.8565479937982, 590.6502648833763, 607.4439817729542, 624.2376986625321, 641.0314155521102, 657.8251324416881, 674.618849331266, 691.412566220844, 708.2062831104221, 725.0]
        
        self.log10pL  = [-0.25822842543920205, 0.07573624542051406, 0.3795408619895562, 0.6569854155862659, 0.9112792617067554, 1.1451476876990558, 1.3609165632531854, 1.5605801585119239, 1.7458559092696675, 1.9182289683143816, 2.078988696262789, 2.229258739313052, 2.3700219632971864, 2.502141226252008, 2.6263767472501804, 2.7434006417579333, 2.8538090082448018, 2.958131684265883, 3.056839132554731, 3.150343060664652, 3.2389513294354573]
        self.log10viscL = [-1.849197543523761, -1.9193462719714602, -1.9866036659330484, -2.0511988925192517, -2.1133344011224127, -2.173190985017066, -2.230929604952335, -2.288518895917737, -2.340950309315269, -2.3920086586601528, -2.4421249470600297, -2.4917542232322756, -2.5413904219915318, -2.5915909903807446, -2.6430184213363357, -2.696505313431577, -2.7531721794932, -2.8146493034600137, -2.876126427426828, -2.937603551393642, -2.9990806753604557]
        self.condL = [0.12935303898117506, 0.12760539500731466, 0.12585775103345426, 0.12411010705959388, 0.12236246308573348, 0.12061481911187309, 0.11886717513801269, 0.1171195311641523, 0.1153718871902919, 0.11362424321643148, 0.11187659924257112, 0.11012895526871071, 0.10838131129485032, 0.10663366732098992, 0.10488602334712953, 0.10313837937326913, 0.10139073539940874, 0.09964309142554834, 0.09789544745168796, 0.09614780347782752, 0.09440015950396716]
        self.cpL = [0.4506849920005477, 0.45057277139907426, 0.451117010764024, 0.45227781751200014, 0.4540347360248375, 0.45638747853989997, 0.459358208038919, 0.46299588352159704, 0.4673835989495494, 0.4726505807518655, 0.47899187232672075, 0.48670142479241696, 0.49622997468670504, 0.508291919073993, 0.5240772176205236, 0.5457127757158595, 0.5774031573719441, 0.6288152281817374, 0.7284837830828523, 1.016975954872821, 13.390308361186909]
        self.hvapL = [187.0883356592434, 183.25314974615483, 179.29696516160442, 175.20887500744058, 170.97627475733483, 166.58447258045413, 162.0161774686792, 157.25081506149124, 152.2635949118305, 147.02420970306028, 141.49497278228324, 135.62806767503784, 129.36133350007407, 122.61151098032325, 115.2627995119183, 107.14603995618943, 97.9970849225087, 87.36170153102209, 74.32905052943605, 56.446391884506404, 0.0]
        self.surfL = [0.0003866553849402083, 0.0003631594572116165, 0.00033993684642418193, 0.0003169993016772364, 0.0002943597948039718, 0.00027203273171467536, 0.00025003421675982087, 0.00022838238814845672, 0.0002070978504537794, 0.00018620424274469092, 0.00016572900108886612, 0.00014570440807358943, 0.000126169081444785, 0.00010717016391236863, 8.876669308165404e-05, 7.103509448384033e-05, 5.407884294532061e-05, 3.80473567610067e-05, 2.3179381357266217e-05, 9.93519259738649e-06, 0.0]    
        self.SG_liqL = [1.5471591949987307, 1.5299055238836263, 1.5122209246787797, 1.494077880137773, 1.4754459612757926, 1.4562913870109118, 1.4365764954846014, 1.4162591045985529, 1.3952917322702552, 1.3736206372172444, 1.3511846275356787, 1.3279135651179854, 1.3037264662118477, 1.2785290576257158, 1.2522105868354307, 1.2246395901381333, 1.1956581746044137, 1.1650741286065889, 1.1326497710496837, 1.0980857431321263, 1.0609966567322016]
        self.log10SG_vapL = [-3.7637454715099548, -3.4473435110841764, -3.1599186695470602, -2.897569962606605, -2.6569554434509217, -2.4351904554928088, -2.229768265484417, -2.038497240121441, -1.8594501264272298, -1.6909221021123784, -1.5313951196026345, -1.379506700205616, -1.2340217641286815, -1.0938063295923688, -0.9578019993956349, -0.8250000905602759, -0.6944140743834564, -0.5650487917316201, -0.4358653540040997, -0.305746360607683, -0.17355610240093053]
        
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

    
