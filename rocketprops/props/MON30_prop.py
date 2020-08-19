
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of MON30
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MON30')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MON30"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.7 # degR
        self.P       = 86.34441183625188 # psia
        self.Pvap    = 86.34441183625188 # psia
        self.Pc      = 2142.5245822424185 # psia
        self.Tc      = 721.0 # degR
        self.Zc      = 0.5220141197964717 # Z at critical pt
        self.omega   = 0.6411706852345824 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.3813202531514739 # SG
        self.visc    = 0.004851065341953962 # poise
        self.cond    = 0.12819468114844268 # BTU/hr/ft/delF
        self.Tnbp    = 462.6700000000002 # degR
        self.Tfreeze = 345.87000000000023 # degR
        self.Ttriple = 345.87000000000023 # degR
        self.Cp      = 0.47075109219072686 # BTU/lbm/delF
        self.MolWt   = 79.32133165547617 # g/gmole
        self.Hvap    = 149.72811268063035 # BTU/lbm
        self.surf    = 0.00022268698896467574 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.47970873786407797, 0.505723300970874, 0.5317378640776702, 0.5577524271844663, 0.5837669902912623, 0.6097815533980585, 0.6357961165048546, 0.6618106796116507, 0.6878252427184468, 0.7138398058252429, 0.7398543689320389, 0.7658689320388351, 0.7918834951456312, 0.8178980582524273, 0.8439126213592234, 0.8699271844660195, 0.8959417475728155, 0.9219563106796117, 0.9479708737864078, 0.9739854368932039, 1.0]
        self.tL = [345.87000000000023, 364.6265000000002, 383.3830000000002, 402.13950000000017, 420.89600000000013, 439.6525000000002, 458.40900000000016, 477.1655000000002, 495.92200000000014, 514.6785000000001, 533.4350000000001, 552.1915000000001, 570.9480000000001, 589.7045000000002, 608.4610000000001, 627.2175000000001, 645.974, 664.7305, 683.487, 702.2435, 721.0]
        
        self.log10pL  = [-1.0740267015837957, -0.6019099362464798, -0.18256826020299288, 0.19209039057074156, 0.5286488521695581, 0.832506278224053, 1.1081237631224548, 1.3592120327017876, 1.5888765377775134, 1.7997308135286876, 1.993985909757506, 2.173521572217568, 2.3399433555088898, 2.4946287715737374, 2.638764787335171, 2.773378378526653, 2.8993613262130062, 3.017489842773828, 3.1284384031691648, 3.2327823646622704, 3.3309258134988484]
        self.log10viscL = [-1.5916350547649434, -1.6827826809035984, -1.7691078473695405, -1.8510957867585587, -1.9291609555361358, -2.003662273207911, -2.074910391748643, -2.143178081266847, -2.2087043082032656, -2.2731836885416916, -2.331820947492808, -2.389245327879379, -2.4460825856690223, -2.5030220068408093, -2.560863090780951, -2.62059532722868, -2.6835431093462017, -2.7516431911948604, -2.8197432730435184, -2.887843354892177, -2.9559434367408355]
        self.condL = [0.14722186071778695, 0.14525913018051365, 0.14329639964324034, 0.141333669105967, 0.13937093856869368, 0.13740820803142037, 0.13544547749414707, 0.1334827469568738, 0.13152001641960046, 0.12955728588232712, 0.12759455534505384, 0.12563182480778048, 0.12366909427050722, 0.12170636373323386, 0.11974363319596056, 0.11778090265868725, 0.11581817212141393, 0.11385544158414065, 0.11189271104686732, 0.10992998050959399, 0.10796724997232068]
        self.cpL = [0.44947337608768384, 0.4479490485280091, 0.44743705505363185, 0.4478190011467268, 0.44901188546215276, 0.45096489134549067, 0.453658746392956, 0.4571078591588523, 0.46136596219108145, 0.46653679674878507, 0.47279280398241547, 0.48040756510053706, 0.48981356105799717, 0.5017100536264966, 0.5172788155876517, 0.5386572822845754, 0.5701162140150757, 0.621575792088477, 0.72260910769644, 1.0201840998726743, 15.69790988106092]
        self.hvapL = [195.48949985020565, 191.48977299388986, 187.3636877267264, 183.09984818129342, 178.68508418034173, 174.10404386061543, 169.3386585249141, 164.36742732170867, 159.16444199911464, 153.6980267578219, 147.92879066713, 141.80675128655932, 135.26692685098752, 128.22227205242416, 120.55170841350748, 112.07834663964141, 102.52593094380711, 91.41932757630343, 77.80557969360716, 59.117703717723735, 0.0]
        self.surfL = [0.0005007669324131924, 0.0004703367764885092, 0.00044026060008029117, 0.0004105536197370731, 0.0003812326356001904, 0.000352316305119621, 0.0003238254854371492, 0.00029578366779499826, 0.0002682175376844743, 0.00024115771064716875, 0.00021463971981150042, 0.00018870537515305633, 0.0001634046914677408, 0.0001387987244427357, 0.00011496393513784139, 9.199930414483907e-05, 7.003884426534181e-05, 4.9276070821012826e-05, 3.002018890622394e-05, 1.2867313151986454e-05, 0.0]    
        self.SG_liqL = [1.569288214554281, 1.5522601717340458, 1.5347827136081926, 1.5168259255969663, 1.4983566018802357, 1.4793377280531748, 1.4597278558838422, 1.439480341608653, 1.4185424098782948, 1.3968539924657555, 1.374346272441854, 1.350939838026982, 1.3265423114778376, 1.301045260235205, 1.2743201085787959, 1.2462126283332593, 1.2165353614423775, 1.1850569503711326, 1.1514866989759769, 1.1154515031290357, 1.076460033129462]
        self.log10SG_vapL = [-4.539306501912008, -4.089893807775316, -3.6919013528636837, -3.337227485715143, -3.0192284422910087, -2.732397171551507, -2.472124795123362, -2.2345217770139945, -2.0162821826859356, -1.8145789338062417, -1.6269813504245376, -1.4513888251372629, -1.2859763652247251, -1.1291491009555203, -0.9795038230242835, -0.8357963259399962, -0.696913991556343, -0.5618540326523406, -0.42971038455255683, -0.29968308392814375, -0.17124684400807227]
        
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

    
