
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of N2O4
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='N2O4')

    def set_std_state(self):
        """Set properties and standard state of Propellant, N2O4"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 13.784291729592374 # psia
        self.Pc      = 1441.3 # psia
        self.Tc      = 776.47 # degR
        self.Zc      = 0.5138641859568427 # Z at critical pt
        self.omega   = 0.8390566067888894 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.4414376322641351 # SG
        self.visc    = 0.004200928509133176 # poise
        self.cond    = 0.07669610806555478 # BTU/hr/ft/delF
        self.Tnbp    = 530.07 # degR
        self.Tfreeze = 471.42 # degR
        self.Ttriple = 471.42 # degR
        self.Cp      = 0.37467696872777195 # BTU/lbm/delF
        self.MolWt   = 92.011 # g/gmole
        self.Hvap    = 178.20011535308134 # BTU/lbm
        self.surf    = 0.00014967279946090646 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.6071322781305137, 0.626775664223988, 0.6464190503174624, 0.6660624364109367, 0.685705822504411, 0.7053492085978853, 0.7249925946913596, 0.744635980784834, 0.7642793668783082, 0.7839227529717826, 0.8035661390652569, 0.8232095251587312, 0.8428529112522055, 0.8624962973456798, 0.8821396834391542, 0.9017830695326284, 0.9214264556261027, 0.9410698417195771, 0.9607132278130515, 0.9803566139065256, 1.0]
        self.tL = [471.42, 486.67249999999996, 501.925, 517.1775, 532.4300000000001, 547.6825, 562.935, 578.1875, 593.44, 608.6925000000001, 623.945, 639.1975000000001, 654.45, 669.7025, 684.955, 700.2075, 715.46, 730.7125000000001, 745.9650000000001, 761.2175, 776.47]
        
        self.log10pL  = [0.4311982984306286, 0.6341021595967953, 0.8288238472031348, 1.015517523990038, 1.194365461998596, 1.3655709179375544, 1.5293520585583056, 1.6859367101331486, 1.8355577399221379, 1.97844889721388, 2.1148409463920377, 2.2449579105669932, 2.3690132019357986, 2.4872053226430757, 2.5997126286177465, 2.7066862397521474, 2.8082392313496856, 2.904427744976741, 2.9952116766135104, 3.0803471188591582, 3.158754386632288]
        self.log10viscL = [-2.205256925927789, -2.251922015290393, -2.298366217619037, -2.3446637354299718, -2.3911180727587764, -2.437042328208599, -2.4816791915170073, -2.527372289599403, -2.5738044469695396, -2.619869524368844, -2.6660073977973004, -2.712556460927556, -2.7603843218732917, -2.8083360967917006, -2.8569025328012794, -2.907126227775091, -2.9637543749209065, -3.0239384631060213, -3.084122551291136, -3.14430663947625, -3.204490727661365]
        self.condL = [0.08394510206507247, 0.08205961836127508, 0.08018000854681112, 0.0782421290640433, 0.07594127641121842, 0.07329727457688043, 0.07028770408216876, 0.06674359796542383, 0.06342117755673418, 0.059306572234309074, 0.055237821002587326, 0.05131175618277579, 0.047462970574765485, 0.04368092582930899, 0.03995165034172043, 0.036255490502615166, 0.032562619525186395, 0.02882282099748917, 0.028521917315192137, 0.03118119076619747, 0.03384046421720284]
        self.cpL = [0.3548803358484525, 0.35803414299369274, 0.36440472374779603, 0.3705169123055864, 0.37663781918043054, 0.383480725936322, 0.39110352345821975, 0.3996943087050558, 0.4100402853386684, 0.4232347640963599, 0.44103766615933204, 0.4636002157130129, 0.49318210872245155, 0.525091214211172, 0.5468378524847136, 0.5744527924158493, 0.6179317888291739, 0.6909879624202404, 0.8384414432819515, 1.2853041256405318, 18.12391312205086]
        self.hvapL = [193.66167137548388, 189.64682930352083, 185.50630629123813, 181.22880753150645, 176.80128357515548, 172.20852814212373, 167.4326499580973, 162.45236701243866, 157.24204472380717, 151.7703550264685, 145.9983571439808, 139.87666440529577, 133.34110482876397, 126.30577044218796, 118.65124748677871, 110.20321781770063, 100.6896975080888, 89.6434401584559, 76.12872017708192, 57.63062486331801, 0.0]
        self.surfL = [0.00017996726665707916, 0.0001732732049269209, 0.00016450971235460238, 0.00015572672721514774, 0.00014692304712101998, 0.00013809733275022722, 0.00012924804133706522, 0.00012037342965432124, 0.00011147144941747863, 0.00010253973901158816, 9.35754525767247e-05, 8.457521287285729e-05, 7.553480720915126e-05, 6.64490172049598e-05, 5.731098811417506e-05, 4.8111623861384394e-05, 3.8837873402715725e-05, 2.9470058215701798e-05, 1.997403160129142e-05, 1.0277984514502076e-05, 2.1491295921389273e-08]    
        self.SG_liqL = [1.5131561871811643, 1.494624413048305, 1.4745679300566505, 1.4546641877973483, 1.4355276855394645, 1.4160943656616498, 1.3957949917725823, 1.3739349269224228, 1.352243912301831, 1.3311034784774136, 1.3085492139433255, 1.2845015763555099, 1.2584665238008963, 1.2284871554505115, 1.1932794908633853, 1.154088388766835, 1.101222114343528, 1.0345133411881715, 0.9526411360034355, 0.8418974354960151, 0.4962219455028899]
        self.log10SG_vapL = [-3.10107038453399, -2.9107371705790905, -2.7277401047385084, -2.5518425301244787, -2.3827604092211208, -2.220169729978429, -2.063713332241588, -1.9130073390294997, -1.767647319493553, -1.6272142966413343, -1.4912807568589266, -1.3594169411088948, -1.2311979379145026, -1.1062125328737933, -0.9840755616613281, -0.8644470312313262, -0.747064429001113, -0.6318020470194365, -0.5187922035727425, -0.40872706696612576, -0.30432403288917514]
        
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

    
