
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MMH_scaled')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MMH_scaled"""
        
        self.dataSrc = 'Scaled Reference Point'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.8054904541220975 # psia
        self.Pc      = 1195 # psia
        self.Tc      = 1053.67 # degR
        self.Zc      = 0.3074013086987 # Z at critical pt
        self.omega   = 0.297025896650245 # omega  = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.8798394613717013 # SG
        self.visc    = 0.008448662042797346 # poise
        self.cond    = 0.1441577322485178 # BTU/hr/ft/delF
        self.Tnbp    = 649.47 # degR
        self.Tfreeze = 397.37 # degR
        self.Ttriple = 397.37 # degR
        self.Cp      = 0.6998597443550909 # BTU/lbm/delF
        self.MolWt   = 46.0724 # g/gmole
        self.Hvap    = 377.0000676611555 # BTU/lbm
        self.surf    = 0.0001958767819978368 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.37712946178594814, 0.40827298869665074, 0.43941651560735334, 0.47056004251805594, 0.5017035694287585, 0.5328470963394611, 0.5639906232501637, 0.5951341501608663, 0.6262776770715689, 0.6574212039822714, 0.688564730892974, 0.7197082578036766, 0.7508517847143793, 0.781995311625082, 0.8131388385357845, 0.844282365446487, 0.8754258923571896, 0.9065694192678923, 0.9377129461785948, 0.9688564730892975, 1.0]
        self.tL = [397.37, 430.185, 463.0, 495.81500000000005, 528.63, 561.445, 594.26, 627.075, 659.8900000000001, 692.705, 725.52, 758.335, 791.1500000000001, 823.9650000000001, 856.7800000000001, 889.595, 922.4100000000001, 955.2250000000001, 988.0400000000001, 1020.8550000000001, 1053.67]
        
        self.log10pL  = [-2.5157344759717524, -1.7419325652032898, -1.0951802232537136, -0.5483625745277984, -0.0812534012139702, 0.32150749357666314, 0.6717669573275371, 0.9787866583629007, 1.249894585280499, 1.490951707234823, 1.7066924368941572, 1.900977296419942, 2.0769835402488903, 2.2373514455350154, 2.3842988485678367, 2.5197133696224023, 2.6452303285468175, 2.762305246442619, 2.8722968023500375, 2.9766112405261334, 3.0773679052841563]
        self.log10viscL = [-1.4979488066588296, -1.6630055880652197, -1.8128921219919552, -1.9501637636881863, -2.076780068924169, -2.1942767308476188, -2.303879646456162, -2.4065830192399966, -2.5032043013607517, -2.594423757527169, -2.680813543141109, -2.762859464381848, -2.8409775247914792, -2.9155266889908726, -2.98681885611038, -3.0551267443576875, -3.1206901906798175, -3.183721233094431, -3.244408247498841, -3.3029193424932246, -3.3594051664036915]
        self.condL = [0.15622941054537537, 0.15318925610706852, 0.1501491016687617, 0.14710894723045487, 0.14406879279214804, 0.1410286383538412, 0.1379884839155344, 0.1349483294772275, 0.13190817503892072, 0.12886802060061386, 0.12582786616230707, 0.1227877117240002, 0.11974755728569336, 0.11670740284738655, 0.11366724840907974, 0.1106270939707729, 0.10758693953246606, 0.10454678509415923, 0.1015066306558524, 0.09846647621754556, 0.09542632177923874]
        self.cpL = [0.6998617980026451, 0.6998611235970428, 0.6998605668446518, 0.6998601083574476, 0.69985973452562, 0.6998594361369914, 0.6998592075799, 0.6998590464805987, 0.6998589537267038, 0.6998589339181356, 0.6998589964019828, 0.6998591572426652, 0.6998594428703224, 0.6998598970305229, 0.699860594850163, 0.6998616739705716, 0.6998634126596639, 0.6998664647529111, 0.6998728014848088, 0.6998923183342777, 0.7010898225961727]
        self.hvapL = [410.5142488488308, 402.4870053011064, 394.1979872178034, 385.623302965234, 376.73531318476336, 367.50176556964874, 357.8846570625791, 347.8387112651689, 337.30930008537405, 326.2295413767625, 314.51613728102734, 302.06321859367466, 288.7328961282125, 274.3400900376364, 258.62677181546803, 241.21499036052046, 221.51266708576873, 198.49765751972205, 170.10988786030998, 130.76007980832418, 0.0]
        self.surfL = [0.0002567195119275447, 0.0002411194108201939, 0.00022570077826201694, 0.00021047141505746027, 0.00019543993384407046, 0.00018061589941365363, 0.00016601000423592494, 0.00015163429115925897, 0.0001375024405723961, 0.0001236301476149031, 0.00011003562844043272, 9.674031704518474e-05, 8.376985364851597e-05, 7.115553861232985e-05, 5.893656990414936e-05, 4.7163690190008684e-05, 3.5905601492336444e-05, 2.526150996016573e-05, 1.5389930415012864e-05, 6.59646262239862e-06, 0.0]    
        self.SG_liqL = [0.9447514552074996, 0.9289188645971231, 0.912760067729865, 0.896245016489418, 0.879338961750561, 0.8620013690732669, 0.8441844927173996, 0.8258314671879232, 0.806873701679215, 0.787227240472187, 0.7667875421104666, 0.7454217530063428, 0.7229568392937068, 0.6991605132969899, 0.6737088079247789, 0.6461268422521937, 0.6156697491064693, 0.5810488160070182, 0.5396565885260198, 0.4843612811853376, 0.29567054461868014]
        self.log10SG_vapL = [-6.277528244747494, -5.538163529202444, -4.923258980697789, -4.405969643017284, -3.9662181658820153, -3.5886846900547162, -3.2614738490969586, -2.9752106703702927, -2.7224115050063347, -2.497032681144128, -2.2941351295686636, -2.109625387337648, -1.9400462327172878, -1.7823961513492714, -1.6339564961777873, -1.4920957581042915, -1.3539894970289124, -1.2160942855194476, -1.0728145708101535, -0.9113872025312577, -0.5291919387364732]
        
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

    
