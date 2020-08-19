
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of CLF5
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='CLF5')

    def set_std_state(self):
        """Set properties and standard state of Propellant, CLF5"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 468.20824117597454 # degR
        self.P       = 14.695900000005908 # psia
        self.Pvap    = 14.695900000005908 # psia
        self.Pc      = 771 # psia
        self.Tc      = 749.0699999999999 # degR
        self.Zc      = 0.28125762405570104 # Z at critical pt
        self.omega   = 0.22425053808315965 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.9099796506185258 # SG
        self.visc    = 0.004647417632611833 # poise
        self.cond    = 0.058735542785699764 # BTU/hr/ft/delF
        self.Tnbp    = 466.97 # degR
        self.Tfreeze = 306.27 # degR
        self.Ttriple = 306.27 # degR
        self.Cp      = 0.28284373300151516 # BTU/lbm/delF
        self.MolWt   = 130.445 # g/gmole
        self.Hvap    = 76.03994509997979 # BTU/lbm
        self.surf    = 0.00012040859346238442 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.4088669950738916, 0.43842364532019706, 0.46798029556650245, 0.4975369458128079, 0.5270935960591133, 0.5566502463054187, 0.5862068965517242, 0.6157635467980296, 0.645320197044335, 0.6748768472906403, 0.7044334975369457, 0.7339901477832512, 0.7635467980295567, 0.7931034482758621, 0.8226600985221675, 0.8522167487684729, 0.8817733990147782, 0.9113300492610836, 0.9408866995073892, 0.9704433497536946, 1.0]
        self.tL = [306.27, 328.40999999999997, 350.54999999999995, 372.69, 394.83, 416.96999999999997, 439.11, 461.25, 483.38999999999993, 505.5299999999999, 527.6699999999998, 549.81, 571.95, 594.0899999999999, 616.2299999999999, 638.3699999999999, 660.5099999999999, 682.6499999999999, 704.79, 726.93, 749.0699999999999]
        
        self.log10pL  = [-0.9527302966638411, -0.6323405705111577, -0.31195084435847437, 0.00847282937737443, 0.3166800600366749, 0.585342931968776, 0.8556330043231708, 1.0890231863795712, 1.3100255016481859, 1.510270847743631, 1.6891881040396126, 1.8630442220101817, 2.0171478734381783, 2.1602358994316844, 2.294836662126627, 2.41839865536697, 2.533438043671308, 2.6399619714896727, 2.7290745710222195, 2.8085317886262495, 2.884455663804013]
        self.log10viscL = [-1.719058452778134, -1.8132931703304112, -1.9075278878826882, -2.0017626054349655, -2.088993149286505, -2.1690357636785755, -2.2426119393761748, -2.311607866713249, -2.3780932132113026, -2.441602202039906, -2.501418924090836, -2.557227959268781, -2.6101667661912784, -2.6608707640761002, -2.710106698672409, -2.758533122222819, -2.8065282624110672, -2.8549699688827217, -2.904000699878612, -2.9530314308745016, -3.0020621618703913]
        self.condL = [0.0750461885894282, 0.07281621687013475, 0.07058624515084128, 0.0683562734315478, 0.06612630171225434, 0.06389632999296087, 0.06166635827366741, 0.05943638655437395, 0.057206414835080495, 0.054976443115787026, 0.05274647139649358, 0.05051649967720009, 0.048286527957906604, 0.04605655623861316, 0.0438265845193197, 0.041596612800026224, 0.03936664108073277, 0.037136669361439306, 0.03490669764214582, 0.03267672592285237, 0.030446754203558895]
        self.cpL = [0.25598091203135653, 0.25931285676017213, 0.2626448014889877, 0.2659767462178033, 0.2693086909466189, 0.2725264225818321, 0.2762554514867955, 0.2810977587694013, 0.2869117166849509, 0.29281245884035134, 0.29803479800619276, 0.30197239083754923, 0.3060083362219219, 0.3107696526035751, 0.3177613729964591, 0.32942565807189256, 0.3477283814977893, 0.37874746060891273, 0.4412563346411675, 0.6294374933519366, 11.419372730927384]
        self.hvapL = [90.35161903058628, 88.61129219940915, 86.81360398446348, 84.95329874919959, 83.02429445770603, 81.01949155104705, 78.9305215274404, 76.74741037561144, 74.45811898252151, 72.04790106370838, 69.49838210315123, 66.78619633591491, 63.88089348526563, 60.741575899973405, 57.31118514987563, 53.506075098587914, 49.195083278613644, 44.15150897281414, 37.9177564540135, 29.249538651769203, 0.0]
        self.surfL = [0.0002100431143421424, 0.00019727940270979446, 0.00018466416525822642, 0.00017220378446007535, 0.00015990530701467216, 0.00014777655865619643, 0.00013582628776385042, 0.00012406434757145793, 0.0001125019311178139, 0.00010115187987324484, 9.002909795476085e-05, 7.915112225810002e-05, 6.853893113230043e-05, 5.82181339494154e-05, 4.82208017550484e-05, 3.8588451251704295e-05, 2.9377293152172886e-05, 2.0668496076433098e-05, 1.2591753893605465e-05, 5.3971026294300425e-06, 0.0]    
        self.SG_liqL = [2.1892669747118028, 2.1539402478573155, 2.1178556486567897, 2.0809438618197205, 2.0431247276251305, 2.004304739872869, 1.9643737551365341, 1.9232005882237877, 1.8806269981911734, 1.8364592867043636, 1.7904562448321912, 1.7423113128275083, 1.6916251723706461, 1.637861691299692, 1.5802730132143865, 1.5177626808330171, 1.4486104120467505, 1.369838889027787, 1.2754212832604956, 1.1488614979989529, 0.712705266924602]
        self.log10SG_vapL = [-4.147943971754535, -3.8572756414324942, -3.564200806610678, -3.2686098089156643, -2.9825930343485694, -2.733763938074105, -2.4796408918993165, -2.259631924576451, -2.0478672515504717, -1.852901460145374, -1.6755723853836184, -1.4966732084179792, -1.333392113075166, -1.1750223108666622, -1.0173792261420107, -0.8635903233656822, -0.7090645293940606, -0.5527209043501118, -0.41696986359325766, -0.29001476531054665, -0.15625986094361854]
        
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

    
