
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of MMH
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MMH')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MMH"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.7274133154081348 # psia
        self.Pc      = 1195 # psia
        self.Tc      = 1053.67 # degR
        self.Zc      = 0.26338938217655683 # Z at critical pt
        self.omega   = 0.28680344162000093 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
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
        self.trL = [0.37712946178594814, 0.40827298869665074, 0.43941651560735334, 0.47056004251805594, 0.5017035694287585, 0.5328470963394611, 0.5639906232501637, 0.5951341501608662, 0.6262776770715689, 0.6574212039822714, 0.6885647308929741, 0.7197082578036766, 0.7508517847143792, 0.7819953116250818, 0.8131388385357844, 0.844282365446487, 0.8754258923571896, 0.9065694192678921, 0.9377129461785947, 0.9688564730892975, 1.0]
        self.tL = [397.37, 430.185, 463.0, 495.81500000000005, 528.63, 561.445, 594.26, 627.0749999999999, 659.89, 692.705, 725.5200000000001, 758.335, 791.15, 823.965, 856.78, 889.595, 922.41, 955.225, 988.04, 1020.8550000000001, 1053.67]
        
        self.log10pL  = [-2.7414245983651573, -1.8969622355445945, -1.1998753409681648, -0.6173095335605722, -0.12491607939372697, 0.2956521263307987, 0.6584149592273555, 0.9742137488433035, 1.2515172475935756, 1.4969985348874384, 1.7159553841688089, 1.9126215141023268, 2.0904004111403727, 2.2520433164695888, 2.399786355376714, 2.5354573662946125, 2.660559973463536, 2.7763403336152015, 2.88384036144323, 2.983939199343523, 3.0773679052841563]
        self.log10viscL = [-0.9391471874522483, -1.3584368889154772, -1.698012257181378, -1.9069846696138069, -2.077788493504421, -2.2214664725059734, -2.3361283238028787, -2.428034709227801, -2.5112618913128895, -2.594391687406626, -2.6806220552644864, -2.7626773049148983, -2.8408039779944603, -2.915360767989803, -2.986660161069911, -3.0549744352014288, -3.1205439894712383, -3.183580485966125, -3.2442727004626097, -3.3027885305315534, -3.35927881111061]
        self.condL = [0.14622268231888433, 0.14622268231888433, 0.14621874233903867, 0.1454637065008603, 0.14410789679121955, 0.14178169514978442, 0.13872690550770228, 0.1349148630626086, 0.13045559210661903, 0.12491120911388866, 0.11872028820705269, 0.112358422713997, 0.10631977887082497, 0.10044419622388734, 0.09477759908731866, 0.08828987439874897, 0.08019576075457142, 0.0704944520480966, 0.06139900945140393, 0.0631658424722527, 0.07195174501123086]
        self.cpL = [0.679002254699395, 0.6822173051394047, 0.6878912076082673, 0.6939645966695106, 0.7000312721473902, 0.7056811552554715, 0.7119511993160879, 0.7188815287189327, 0.7258411031080202, 0.7335411672856395, 0.7437820469108334, 0.7580463337994104, 0.7763467437540109, 0.8000295795944691, 0.831734626373075, 0.8737636062796494, 0.9346515231172009, 1.0193397482246895, 1.1740925844929717, 1.6244001121861613, 28.51320767547775]
        self.hvapL = [410.4289109307158, 402.42277728498755, 394.15511010507146, 385.6020247568183, 376.73588852068605, 367.5244550381481, 357.9297260123787, 347.90642786430845, 337.39993222270573, 326.3433517544488, 314.6533756152855, 302.2241090604686, 288.91761670844727, 274.54873743516646, 258.8592991821347, 241.47108983967755, 221.79152865212245, 198.79740828481428, 170.42600255711332, 131.07880318952033, 0.0]
        self.surfL = [0.00023546774034859848, 0.0002262240672637695, 0.00021609637894753154, 0.00020588161003298982, 0.0001955738493356034, 0.00018516629922811593, 0.0001746512649107268, 0.00016401977237298084, 0.0001532614183445943, 0.0001423638625945411, 0.0001313123238447862, 0.00012008884722193538, 0.00010867097096871818, 9.703032081257124e-05, 8.512917954268118e-05, 7.291654182991242e-05, 6.0317595919164714e-05, 4.721681912390367e-05, 3.3405811951332886e-05, 1.8424845754659776e-05, 0.0]    
        self.SG_liqL = [0.9448242110819741, 0.9289699636107457, 0.9127916978570874, 0.8962594490421218, 0.879338562404805, 0.8619886111919051, 0.8441619736432548, 0.8258019284460081, 0.8068400544230196, 0.7871925981223978, 0.7667552631151755, 0.7453954982816801, 0.7229406517394681, 0.699158931994362, 0.6737270398759856, 0.6461710364871962, 0.6157474706139564, 0.5811699641425555, 0.5398355238453286, 0.4846236916789145, 0.2961834064047918]
        self.log10SG_vapL = [-6.5030943572871704, -5.692997994813139, -5.027559061120656, -4.474060476490519, -4.008110366284448, -3.611161747842198, -3.2688808897348394, -2.97004899050083, -2.705799229354191, -2.4690655073176893, -2.254167803795137, -2.0564893444234964, -1.872217900517997, -1.698132063081089, -1.5314165526085628, -1.3694901013589051, -1.2098247386394294, -1.0497230782508136, -0.8859908381277022, -0.7143690092507525, -0.528439276364106]
        
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

    def SG_compressed(self, TdegR, Ppsia):
        '''Calculates compressed-liquid specific gravity from curve fit of 
        RefProp calculations for MMH  (MonoMethylHydrazine). 
        
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
        
        trL = [0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (10589.569810046796 + psat))  # Fit Standard Deviation = 5.412853307430722e-09
        dsg_o_sgL.append(  0.03637202072794378*log10x + 0.03433360832953265*log10x**2 + 0.01755389602818833*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (8209.80212388197 + psat))  # Fit Standard Deviation = 1.3732567299692015e-08
        dsg_o_sgL.append(  0.03424745204142822*log10x + 0.0326132859006542*log10x**2 + 0.017305252406757534*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6177.069852339128 + psat))  # Fit Standard Deviation = 3.649801671155937e-08
        dsg_o_sgL.append(  0.031731611035634225*log10x + 0.030522365461474306*log10x**2 + 0.017017316090043155*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4463.447278953207 + psat))  # Fit Standard Deviation = 1.0250653986950578e-07
        dsg_o_sgL.append(  0.028755239731389402*log10x + 0.027958102774981296*log10x**2 + 0.01668944740664264*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3051.3681793762908 + psat))  # Fit Standard Deviation = 3.0549534026969583e-07
        dsg_o_sgL.append(  0.02526304170957798*log10x + 0.024783327342416634*log10x**2 + 0.01631462420624741*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1924.4267211664935 + psat))  # Fit Standard Deviation = 9.661687227198927e-07
        dsg_o_sgL.append(  0.021233944430324954*log10x + 0.0208076386225839*log10x**2 + 0.015868935317814522*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (9663.41884523568 + psat))  # Fit Standard Deviation = 7.925895276324919e-08
        dsg_o_sgL.append(  0.14427357034611538*log10x + 0.03617415930108113*log10x**2 + -0.00496049708979845*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6561.907880284143 + psat))  # Fit Standard Deviation = 2.1772650245162727e-07
        dsg_o_sgL.append(  0.14187820777474008*log10x + 0.03594946846548841*log10x**2 + -0.005501754517593817*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4085.12881682702 + psat))  # Fit Standard Deviation = 6.299833364242372e-07
        dsg_o_sgL.append(  0.13926949995690333*log10x + 0.03608588889026804*log10x**2 + -0.006229042313223188*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2149.871388014923 + psat))  # Fit Standard Deviation = 1.9123738833081077e-06
        dsg_o_sgL.append(  0.13561384760517012*log10x + 0.036899881106801515*log10x**2 + -0.0071107633320449636*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (682.8908382720118 + psat))  # Fit Standard Deviation = 5.984463062913862e-06
        dsg_o_sgL.append(  0.12877682269857624*log10x + 0.03887229569815003*log10x**2 + -0.0080205562404789*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5.920969290175338e-07 + psat))  # Fit Standard Deviation = 0.00017512560120193173
        dsg_o_sgL.append(  0.2245552477733884*log10x + -0.045290544198862547*log10x**2 + 0.0192201152457745*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (9.225720702300927e-09 + psat))  # Fit Standard Deviation = 0.04316871431359113
        dsg_o_sgL.append(  2.778463860710788*log10x + -4.862787854598258*log10x**2 + 2.7425312824163206*log10x**3  )

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

    
