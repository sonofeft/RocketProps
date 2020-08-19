
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Methane
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Methane')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Methane"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 201.0006 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6956962557 # psia
        self.Pc      = 667.05738984 # psia
        self.Tc      = 343.0152 # degR
        self.Zc      = 0.286362092267 # Z at critical pt
        self.omega   = 0.011416206377049987 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.422356770643 # SG
        self.visc    = 0.0011680847877 # poise
        self.cond    = 0.106232850218 # BTU/hr/ft/delF
        self.Tnbp    = 201.0006 # degR
        self.Tfreeze = 163.35 # degR
        self.Ttriple = 163.24938 # degR
        self.Cp      = 0.831998009854 # BTU/lbm/delF
        self.MolWt   = 16.0428 # g/gmole
        self.Hvap    = 219.763721789 # BTU/lbm
        self.surf    = 7.5924137276e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.47621796351881784, 0.5037854391230906, 0.5313529147273632, 0.5589203903316361, 0.5864878659359088, 0.6140553415401816, 0.6416228171444543, 0.669190292748727, 0.6967577683529997, 0.7243252439572725, 0.7518927195615452, 0.779460195165818, 0.8070276707700907, 0.8345951463743636, 0.8621626219786364, 0.8897300975829091, 0.9172975731871817, 0.9448650487914545, 0.9724325243957272, 1.0]
        self.tL = [163.35, 172.80606315789473, 182.26212631578946, 191.71818947368422, 201.17425263157895, 210.63031578947368, 220.08637894736842, 229.54244210526315, 238.99850526315788, 248.4545684210526, 257.91063157894735, 267.3666947368421, 276.8227578947368, 286.2788210526316, 295.73488421052633, 305.19094736842106, 314.6470105263158, 324.10307368421053, 333.55913684210526, 343.0152]
        
        self.log10pL  = [0.23264361884422727, 0.508643871455029, 0.7538796474427377, 0.9732290893858793, 1.1706377688833973, 1.3493260155641436, 1.5119433223002885, 1.660685509637575, 1.797384989835147, 1.923581205831105, 2.040576253726238, 2.1494793537145878, 2.251242957730435, 2.3466927445285597, 2.436553522714567, 2.521473246557463, 2.6020484894460054, 2.678859284659806, 2.7525424786690236, 2.8241632081991317]
        self.log10viscL = [-2.7143039035314005, -2.777866528574153, -2.833707311285279, -2.884977080572727, -2.933395640405683, -2.9799349007719687, -3.0251579062379226, -3.0693990288229447, -3.1128755807453423, -3.155746747827189, -3.198150751046426, -3.240236217940331, -3.282201134757716, -3.3243298035978257, -3.367070733141434, -3.411181195394227, -3.4580219563091616, -3.5103967381437586, -3.5761441449647813, -3.7983273756349654]
        self.condL = [0.12205211780372892, 0.11835303675989571, 0.11443072589919448, 0.11034838206236075, 0.106155083409364, 0.10188876750784562, 0.0975784118879158, 0.09324561133569795, 0.08890568345123256, 0.08456838843009054, 0.08023831424362575, 0.07591494997290513, 0.07159244553244039, 0.06725903890140657, 0.06289618014503802, 0.05847786797458671, 0.05397391035360283, 0.04938248744818109, 0.04504646876129546, 0.0769893823480152]
        self.cpL = [0.8049658188280815, 0.8099437197663291, 0.8162409828124303, 0.8236382935976175, 0.8321657225683061, 0.8420110848460762, 0.8534847181490937, 0.8670199653070148, 0.8832026849564582, 0.9028335200487732, 0.9270387005324866, 0.9574659719752661, 0.9966475024991474, 1.0487245001794516, 1.1210448619226376, 1.228164252977412, 1.4037993572637455, 1.748460267047304, 2.7693357808248136, 76.67089213101649]
        self.hvapL = [234.11344907873342, 230.83782364192797, 227.3696148446361, 223.6669591962957, 219.68790247075395, 215.38858758456487, 210.72172861711135, 205.63499046766213, 200.0689779553033, 193.9544986209251, 187.20860930101702, 179.72862964121634, 171.38263298094245, 161.9934572553039, 151.30978605704843, 138.94857224723017, 124.26433472699077, 105.98677032078734, 80.75792400813302, 0.0]
        self.surfL = [0.00010703820597217893, 9.886662859893939e-05, 9.093085672639039e-05, 8.323659821799798e-05, 7.578964429254111e-05, 6.859590851812005e-05, 6.166147826532992e-05, 5.499268353745525e-05, 4.8596190557058326e-05, 4.247913150422387e-05, 3.664928860265767e-05, 3.1115362784908433e-05, 2.588737961625848e-05, 2.0977329806541583e-05, 1.640023788731197e-05, 1.2176082896930724e-05, 8.333629681075217e-06, 4.919383919170624e-06, 2.0252969278220894e-06, 0.0]    
        self.SG_liqL = [0.4514015328198097, 0.4443491212840538, 0.43714890424442787, 0.42977911538588787, 0.4222159816256076, 0.4144325967265641, 0.40639770571049383, 0.39807421623697975, 0.38941722800621453, 0.3803712890140364, 0.3708664192841981, 0.3608121116783594, 0.3500878352706865, 0.3385270355099366, 0.32588787336180747, 0.3117938159690598, 0.29559606462064275, 0.27598828902321826, 0.2494392216103673, 0.1626581430291753]
        self.log10SG_vapL = [-3.5978956103989272, -3.3443443653137943, -3.11953212120435, -2.9186040485316647, -2.7376273106026368, -2.573384382485981, -2.4232166755429803, -2.2849033678471673, -2.15656517321364, -2.0365854769746616, -1.9235426021069195, -1.8161471538685647, -1.7131770904583832, -1.6133990927310544, -1.5154541656813767, -1.4176562188883488, -1.317559842920401, -1.210779847427005, -1.0862205389775554, -0.7887241900881622]
        
        # ========== save dataSrc for each value ===========
        data_srcD = {} # index=parameter, value=data source
        data_srcD["main"]    = "RefProp"
        data_srcD["T"]       = "RefProp" # degR
        data_srcD["P"]       = "RefProp" # psia
        data_srcD["Pvap"]    = "RefProp" # psia
        data_srcD["Pc"]      = "RefProp" # psia
        data_srcD["Tc"]      = "RefProp" # degR
        data_srcD["Zc"]      = "RefProp" # Z at critical pt
        data_srcD["omega"]   = "RefProp" # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        data_srcD["SG"]      = "RefProp" # SG
        data_srcD["visc"]    = "RefProp" # poise
        data_srcD["cond"]    = "RefProp" # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = "RefProp" # degR
        data_srcD["Tfreeze"] = "RefProp" # degR
        data_srcD["Ttriple"] = "RefProp" # degR
        data_srcD["Cp"]      = "RefProp" # BTU/lbm/delF
        data_srcD["MolWt"]   = "RefProp" # g/gmole
        data_srcD["Hvap"]    = "RefProp" # BTU/lbm
        data_srcD["surf"]    = "RefProp" # lbf/in

        data_srcD["trL"]     = "RefProp"
        data_srcD["tL"]      = "RefProp"

        data_srcD["log10pL"]      = "RefProp"
        data_srcD["log10viscL"]   = "RefProp"
        data_srcD["condL"]        = "RefProp"
        data_srcD["cpL"]          = "RefProp"
        data_srcD["hvapL"]        = "RefProp"
        data_srcD["surfL"]        = "RefProp"    
        data_srcD["SG_liqL"]      = "RefProp"
        data_srcD["log10SG_vapL"] = "RefProp"
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

    def SG_compressed(self, TdegR, Ppsia):
        '''Calculates compressed-liquid specific gravity from curve fit of 
        RefProp calculations for Methane  (CH4). 
        
        The fitted equation is a modified, polynomial version of the Tait equation
        see: equation 4-12.2 in the 5th Ed. of Gases and Liquids.
        or: https://en.wikipedia.org/wiki/Tait_equation

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml
        '''
        
        Tr = TdegR / self.Tc
        Psat = self.PvapAtTr( Tr )
        dP = max(0.0, Ppsia - Psat) # don't let dP fall below zero
        
        trL = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (642.8300880368608 + psat))  # Fit Standard Deviation = 1.0431457273911057e-05
        dsg_o_sgL.append(  0.016731927978062618*log10x + 0.01406162241000191*log10x**2 + 0.018536635429924807*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (402.5444900434918 + psat))  # Fit Standard Deviation = 2.0523848534424355e-05
        dsg_o_sgL.append(  0.013347517078576645*log10x + 0.008889198993672217*log10x**2 + 0.01757528372584917*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (225.33964090905388 + psat))  # Fit Standard Deviation = 3.952579538147984e-05
        dsg_o_sgL.append(  0.010565623648638058*log10x + 0.0034661392306444805*log10x**2 + 0.01656428201172605*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3379.234403367386 + psat))  # Fit Standard Deviation = 1.6089577688060532e-06
        dsg_o_sgL.append(  0.1631682148295521*log10x + 0.04476371272509037*log10x**2 + -0.006577099813849565*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2491.5205839527553 + psat))  # Fit Standard Deviation = 3.0322427891496145e-06
        dsg_o_sgL.append(  0.15915557207905132*log10x + 0.044612160920540725*log10x**2 + -0.0071531259114979645*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1715.6890386005036 + psat))  # Fit Standard Deviation = 5.656846077421953e-06
        dsg_o_sgL.append(  0.15410683139033435*log10x + 0.04479162003568072*log10x**2 + -0.007677795524310365*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1044.0401983314557 + psat))  # Fit Standard Deviation = 1.0288985181922773e-05
        dsg_o_sgL.append(  0.14750108942219073*log10x + 0.04533331075413714*log10x**2 + -0.008166904625588901*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (471.3805075969267 + psat))  # Fit Standard Deviation = 1.797920570626269e-05
        dsg_o_sgL.append(  0.13844366943551326*log10x + 0.046313450429621525*log10x**2 + -0.008604666577912383*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (0.0010161682988999521 + psat))  # Fit Standard Deviation = 3.0778351517173445e-05
        dsg_o_sgL.append(  0.1271044003229242*log10x + 0.04667006286229852*log10x**2 + -0.0086368866144908*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.1008801654267633e-05 + psat))  # Fit Standard Deviation = 0.0011568060929140654
        dsg_o_sgL.append(  0.3829243336248461*log10x + -0.1940680963015701*log10x**2 + 0.07150521691662466*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3.573967670366063e-09 + psat))  # Fit Standard Deviation = 0.036662642942756195
        dsg_o_sgL.append(  2.267371554275571*log10x + -3.2204824105127243*log10x**2 + 1.5051337648894572*log10x**3  )

        sgratio_terp = InterpProp( trL, dsg_o_sgL, extrapOK=True )
        
        SGratio = sgratio_terp( Tr )
        SGsat = self.SGLiqAtTr( Tr )
        SG = SGsat / ( 1.0 - SGratio )
        
        return SG

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

    
