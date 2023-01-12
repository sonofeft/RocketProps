
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='XXX')

    def set_std_state(self):
        """Set properties and standard state of Propellant, XXX"""
        
        self.dataSrc = 'Scaled Reference Point'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 2.016502173151945 # psia
        self.Pc      = 1731 # psia
        self.Tc      = 1092.67 # degR
        self.Zc      = 0.3074013086987 # Z at critical pt
        self.omega   = 0.14167100548382533 # omega  = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.9035471601513377 # SG
        self.visc    = 0.009208681003236614 # poise
        self.cond    = 0.1661065246970707 # BTU/hr/ft/delF
        self.Tnbp    = 617.6700000000001 # degR
        self.Tfreeze = 481.67 # degR
        self.Ttriple = 481.67 # degR
        self.Cp      = 0.7282323251759043 # BTU/lbm/delF
        self.MolWt   = 41.802 # g/gmole
        self.Hvap    = 346.5000380753298 # BTU/lbm
        self.surf    = 0.00016987300288460853 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.44081927754948885, 0.4687783136720144, 0.49673734979453993, 0.5246963859170656, 0.5526554220395911, 0.5806144581621167, 0.6085734942846421, 0.6365325304071677, 0.6644915665296933, 0.6924506026522188, 0.7204096387747444, 0.74836867489727, 0.7763277110197955, 0.8042867471423211, 0.8322457832648467, 0.8602048193873723, 0.8881638555098977, 0.9161228916324232, 0.9440819277549488, 0.9720409638774745, 1.0]
        self.tL = [481.67, 512.22, 542.77, 573.32, 603.87, 634.4200000000001, 664.97, 695.52, 726.07, 756.62, 787.1700000000001, 817.72, 848.27, 878.82, 909.37, 939.9200000000001, 970.47, 1001.02, 1031.57, 1062.1200000000001, 1092.67]
        
        self.log10pL  = [-0.2804383245863168, 0.12143381760334529, 0.47217657389676365, 0.7806584942556513, 1.0538978240047174, 1.2975116550632282, 1.5160413651933298, 1.7131924104203837, 1.8920137334236435, 2.0550339059118117, 2.2043658315374026, 2.3417883376535005, 2.4688106442485687, 2.5867241354372075, 2.6966448570133403, 2.7995496444843635, 2.8963088666746306, 2.9877200764227267, 3.0745520564828444, 3.157632964155744, 3.238297067875394]
        self.log10viscL = [-1.8505534915413386, -1.9758982259757776, -2.0922991742886863, -2.200948111429712, -2.3028134103382882, -2.398692609851381, -2.48925037596593, -2.575046471468895, -2.656556732565421, -2.7341890510425846, -2.8082957243360998, -2.879183121098888, -2.9471193334210253, -3.012340298897088, -3.075054745631731, -3.135448221727163, -3.193686405409529, -3.2499178446042296, -3.304276240049917, -3.3568823602809577, -3.4078456574881617]
        self.condL = [0.1702508206263199, 0.16749846756895986, 0.1647461145115998, 0.1619937614542397, 0.1592414083968796, 0.15648905533951954, 0.15373670228215947, 0.15098434922479942, 0.14823199616743932, 0.14547964311007924, 0.14272729005271917, 0.1399749369953591, 0.13722258393799902, 0.13447023088063895, 0.13171787782327887, 0.1289655247659188, 0.1262131717085587, 0.12346081865119864, 0.12070846559383855, 0.11795611253647849, 0.11520375947911839]
        self.cpL = [0.7282325643661325, 0.7282323943175616, 0.728232267991947, 0.7282321826661224, 0.7282321371962763, 0.7282321319665747, 0.72823216898708, 0.7282322521648426, 0.7282323878086845, 0.7282325854866329, 0.7282328594605672, 0.7282332311301466, 0.7282337333565523, 0.728234418537321, 0.7282353748053685, 0.7282367617332832, 0.7282388997122591, 0.7282425383807662, 0.7282499314051673, 0.7282723673377746, 0.7294916728371137]
        self.hvapL = [356.7206076152664, 349.9889264309463, 343.03211218471114, 335.82942947476613, 328.35687199215613, 320.586404280129, 312.4849638367322, 304.0131246332462, 295.12327118691445, 285.75704628830374, 275.84168759733933, 265.2846030025412, 253.96503398070269, 241.7206525206534, 228.32477049342037, 213.44470712798062, 196.5581327409308, 176.7608591548975, 152.22415142987074, 117.96089683229545, 0.0]
        self.surfL = [0.0001869265857638773, 0.00017556759861220563, 0.00016434074515020154, 0.0001532517054203767, 0.00014230675058972923, 0.00013151284512255912, 0.00012087777458546465, 0.00011041030780366149, 0.00010012040595361015, 9.001949722333686e-05, 8.012084544067633e-05, 7.044005745880026e-05, 6.0995802831209235e-05, 5.181087246202983e-05, 4.291380778226965e-05, 3.434155632756044e-05, 2.6144142478173257e-05, 1.839380175133203e-05, 1.1205954413133762e-05, 4.803118496392389e-06, 0.0]    
        self.SG_liqL = [0.9254663278842504, 0.9109877446729612, 0.8961937936289038, 0.8810555353439385, 0.8655394976884035, 0.849606629123638, 0.83321092185612, 0.8162975686697305, 0.7988004458014394, 0.7806385958031482, 0.7617111807328697, 0.7418900106140692, 0.721008062237657, 0.6988410194467022, 0.675075875672377, 0.649253545767155, 0.6206534303554444, 0.5880277158249064, 0.5488488309532146, 0.4961920195778265, 0.3130752170731534]
        self.log10SG_vapL = [-4.167615106624848, -3.791953440387698, -3.4654952115877085, -3.1793845496671134, -2.926576495741253, -2.7014019857650204, -2.4992522254794274, -2.3163437705887846, -2.149539207054044, -1.9962067254059632, -1.8541069117981883, -1.7212978430536001, -1.596050602820784, -1.4767665365856038, -1.3618838110848601, -1.2497505007945227, -1.138412895726497, -1.025178185238739, -0.9054561837747247, -0.7682452447307377, -0.5043513096247483]
        
        # ========== save dataSrc for each value ===========
        data_srcD = dict() # index=parameter, value=data source
        data_srcD["main"]    = "Scaled Reference Point"
        data_srcD["T"]       = "Scaled Reference Point" # degR
        data_srcD["P"]       = "Scaled Reference Point" # psia
        data_srcD["Pvap"]    = "Scaled Reference Point" # psia
        data_srcD["Pc"]      = "Scaled Reference Point" # psia
        data_srcD["Tc"]      = "Scaled Reference Point" # degR
        data_srcD["Zc"]      = "Scaled Reference Point" # Z at critical pt
        data_srcD["omega"]   = "Scaled Reference Point" # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        data_srcD["SG"]      = "Scaled Reference Point" # SG
        data_srcD["visc"]    = "Scaled Reference Point" # poise
        data_srcD["cond"]    = "Scaled Reference Point" # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = "Scaled Reference Point" # degR
        data_srcD["Tfreeze"] = "Scaled Reference Point" # degR
        data_srcD["Ttriple"] = "Scaled Reference Point" # degR
        data_srcD["Cp"]      = "Scaled Reference Point" # BTU/lbm/delF
        data_srcD["MolWt"]   = "Scaled Reference Point" # g/gmole
        data_srcD["Hvap"]    = "Scaled Reference Point" # BTU/lbm
        data_srcD["surf"]    = "Scaled Reference Point" # lbf/in

        data_srcD["trL"]     = "Scaled Reference Point"
        data_srcD["tL"]      = "Scaled Reference Point"

        data_srcD["log10pL"]      = "Scaled Reference Point"
        data_srcD["log10viscL"]   = "Scaled Reference Point"
        data_srcD["condL"]        = "Scaled Reference Point"
        data_srcD["cpL"]          = "Scaled Reference Point"
        data_srcD["hvapL"]        = "Scaled Reference Point"
        data_srcD["surfL"]        = "Scaled Reference Point"    
        data_srcD["SG_liqL"]      = "Scaled Reference Point"
        data_srcD["log10SG_vapL"] = "Scaled Reference Point"
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
    
        # calculate omega from definition (make self-consistent with Pvap.)
        self.omega = -1.0 - log10( self.PvapAtTr(0.7) / self.Pc )
    

if __name__ == '__main__':
    from rocketprops.unit_conv_data import get_value
    C = Prop()
    print('T = %g R = %g K'%( C.T, C.T/1.8 ))
    print('SurfaceTension = %g lbf/in'%C.surf, ' = ', get_value(C.surf, 'lbf/in', 'mN/m'), 'mN/m' )
    
    print()
    print('Tr_data_range =', C.Tr_data_range())
    print('  T_data_range=',C.T_data_range())
    print('  P_data_range=', C.P_data_range())
    
    C.plot_sat_props()

    
