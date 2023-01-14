
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='M20_scaled')

    def set_std_state(self):
        """Set properties and standard state of Propellant, M20_scaled"""
        
        self.dataSrc = 'Scaled Reference Point'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.23088651044536063 # psia
        self.Pc      = 1943.8000000000002 # psia
        self.Tc      = 1150.6 # degR
        self.Zc      = 0.3074013086987 # Z at critical pt
        self.omega   = 0.32414790270621824 # omega  = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.9742299507254817 # SG
        self.visc    = 0.008883267265064347 # poise
        self.cond    = 0.2550268800005305 # BTU/hr/ft/delF
        self.Tnbp    = 687.84 # degR
        self.Tfreeze = 483.55 # degR
        self.Ttriple = 483.55 # degR
        self.Cp      = 0.7280800000000001 # BTU/lbm/delF
        self.MolWt   = 34.8524 # g/gmole
        self.Hvap    = 541.78 # BTU/lbm
        self.surf    = 0.00034216000000000004 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.4202589953067965, 0.4492460455414567, 0.47823309577611683, 0.5072201460107771, 0.5362071962454372, 0.5651942464800974, 0.5941812967147575, 0.6231683469494178, 0.6521553971840779, 0.6811424474187382, 0.7101294976533983, 0.7391165478880585, 0.7681035981227187, 0.7970906483573788, 0.8260776985920391, 0.8550647488266991, 0.8840517990613594, 0.9130388492960195, 0.9420258995306797, 0.9710129497653398, 1.0]
        self.tL = [483.55, 516.9025, 550.255, 583.6075000000001, 616.96, 650.3125, 683.665, 717.0175, 750.37, 783.7225000000001, 817.075, 850.4275, 883.78, 917.1324999999999, 950.485, 983.8375, 1017.19, 1050.5425, 1083.895, 1117.2475, 1150.6]
        
        self.log10pL  = [-1.3921710139223757, -0.8068930557075197, -0.30508384138366634, 0.12888831304132337, 0.507169409927572, 0.8393203579033921, 1.1329541019219822, 1.3941951220332385, 1.6280166247108798, 1.8384919384465466, 2.02898473662058, 2.2022950386175406, 2.3607729090920553, 2.506408455280652, 2.64090457686322, 2.7657377006129473, 2.8822115071358447, 2.991510239454689, 3.0947652054373216, 3.1931812417708567, 3.288651577789465]
        self.log10viscL = [-1.8759589883266137, -2.010312303350965, -2.1344418565448096, -2.2497941954971465, -2.357529042350242, -2.4585904453179115, -2.5537571498957683, -2.6436790724135526, -2.7289042376044934, -2.8098990239156834, -2.8870636175895217, -2.9607439749072646, -3.0312411985740573, -3.0988189713156404, -3.163709510581612, -3.2261183839518814, -3.2862284372085715, -3.344203024329959, -3.400188683181682, -3.454317367276835, -3.5067083191582236]
        self.condL = [0.2599408591462891, 0.256226138170339, 0.2525114171943891, 0.24879669621843897, 0.2450819752424889, 0.24136725426653885, 0.23765253329058877, 0.23393781231463873, 0.23022309133868865, 0.2265083703627386, 0.22279364938678856, 0.21907892841083848, 0.21536420743488843, 0.2116494864589384, 0.20793476548298834, 0.20422004450703826, 0.20050532353108821, 0.19679060255513814, 0.19307588157918815, 0.18936116060323807, 0.18564643962728802]
        self.cpL = [0.7280809498491292, 0.7280802117896646, 0.7280795938805167, 0.7280790810856221, 0.7280786629807657, 0.7280783330086829, 0.7280780881325105, 0.7280779288510788, 0.7280778596121793, 0.728077889751656, 0.7280780352342624, 0.7280783217510141, 0.7280787903084622, 0.7280795077653002, 0.7280805880689952, 0.7280822391837318, 0.7280848807591226, 0.728089497965975, 0.7280990598164339, 0.7281284679351179, 0.7298024867767402]
        self.hvapL = [556.3093258332684, 545.3821149043945, 534.0996886393924, 522.4296651045506, 510.3345865044839, 497.77074796106973, 484.6866574690317, 471.0209752547038, 456.6997013036745, 441.6322483092234, 425.7058114757409, 408.77704192952564, 390.65926778355, 371.1019799352889, 349.756008211832, 326.11002847158977, 299.36326231490955, 268.1337675456294, 229.63760654079596, 176.32668716360305, 0.0]
        self.surfL = [0.0003720083025753777, 0.0003494024356142882, 0.0003270595319411941, 0.0003049908955820303, 0.0002832090069776103, 0.00026172772632086484, 0.00024056254790546546, 0.00021973092283806292, 0.00019925267515990636, 0.00017915054845672916, 0.0001594509394770638, 0.0001401849078956655, 0.00012138960856067515, 0.00010311039834588218, 8.540407842410386e-05, 6.834417921349117e-05, 5.203025575976425e-05, 3.66060661700874e-05, 2.230131183818217e-05, 9.558832691505809e-06, 0.0]    
        self.SG_liqL = [0.9960852074292438, 0.9796180534745443, 0.9628076720040554, 0.9456224764709997, 0.9280259376140549, 0.9099754431505599, 0.8914207980728354, 0.8723022174311296, 0.8525475857906791, 0.8320686288430971, 0.8107554214245737, 0.7884682592559521, 0.7650251725368326, 0.740181857063159, 0.7135975531775024, 0.6847727072500245, 0.652923643297839, 0.6166942711021377, 0.5733401920869743, 0.5153525750545762, 0.31671298191154246]
        self.log10SG_vapL = [-5.360387339014369, -4.803991246724244, -4.329126385983539, -3.9202632648776286, -3.5652778135584726, -3.254563836600721, -2.980412279401646, -2.7365676842290796, -2.517902843955144, -2.3201727733780335, -2.139822267358011, -1.9738294194294972, -1.819571730316492, -1.6747023507178223, -1.5370208523225624, -1.404312054394069, -1.2740952850573468, -1.1431279389849252, -1.006116602343283, -0.8507309664640992, -0.49933413474303284]
        
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

    
