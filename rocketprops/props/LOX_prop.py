
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Oxygen
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Oxygen')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Oxygen"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 162.33804 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6959328435 # psia
        self.Pc      = 731.4251211 # psia
        self.Tc      = 278.2458 # degR
        self.Zc      = 0.287942793955 # Z at critical pt
        self.omega   = 0.022172611915116436 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.14117404803 # SG
        self.visc    = 0.00194672186444 # poise
        self.cond    = 0.0871744939303 # BTU/hr/ft/delF
        self.Tnbp    = 162.33804 # degR
        self.Tfreeze = 97.8498 # degR
        self.Ttriple = 97.8498 # degR
        self.Cp      = 0.4058864967465755 # BTU/lbm/delF
        self.MolWt   = 31.9988 # g/gmole
        self.Hvap    = 91.6588458138 # BTU/lbm
        self.surf    = 7.52226710455e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.35166676370317185, 0.3857895656135312, 0.4199123675238906, 0.45403516943425, 0.48815797134460936, 0.5222807732549688, 0.5564035751653281, 0.5905263770756876, 0.6246491789860469, 0.6587719808964062, 0.6928947828067656, 0.727017584717125, 0.7611403866274844, 0.7952631885378437, 0.8293859904482032, 0.8635087923585625, 0.8976315942689219, 0.9317543961792812, 0.9658771980896407, 1.0]
        self.tL = [97.8498, 107.34432631578947, 116.83885263157894, 126.33337894736842, 135.8279052631579, 145.32243157894737, 154.81695789473684, 164.31148421052632, 173.8060105263158, 183.30053684210526, 192.79506315789473, 202.2895894736842, 211.78411578947367, 221.27864210526315, 230.77316842105262, 240.2676947368421, 249.76222105263156, 259.25674736842103, 268.7512736842105, 278.2458]
        
        self.log10pL  = [-1.673341131133972, -1.018305651048643, -0.4785759383792178, -0.027202888953684393, 0.35527132408368406, 0.6832307481166809, 0.9674989884468345, 1.216340083470871, 1.4361458036374772, 1.6319197765311875, 1.8076246141897894, 1.9664343888761047, 2.110920781127441, 2.2431924714835683, 2.365001794575694, 2.4778293749114297, 2.5829564100327183, 2.6815383175272447, 2.7747245638133577, 2.8641514270323496]
        self.log10viscL = [-2.111469665354645, -2.230222749139041, -2.337479354409211, -2.4328625043228658, -2.5175141489859465, -2.5930299104892574, -2.661068467611863, -2.723193897212939, -2.7808142956888893, -2.835167337781597, -2.8873317487794776, -2.938254810250441, -2.988792583909965, -3.0397663339402614, -3.092050367647488, -3.1467353143912673, -3.205498261068823, -3.271635245868653, -3.3541490057145755, -3.6047667207303604]
        self.condL = [0.11674653428718658, 0.11243148901053093, 0.10808932250912168, 0.10374739446667904, 0.09940289378680718, 0.09504527233238817, 0.09066484784655873, 0.08625544072606327, 0.08184407460772634, 0.0774056850449846, 0.0729420730588843, 0.06846471300412509, 0.06398470816028613, 0.05951408092384452, 0.05506459912530319, 0.050644851651085, 0.04625472010482058, 0.04188281266216134, 0.03762096550870005, 0.047440227244870924]
        self.cpL = [0.3999080995028288, 0.39986470953448705, 0.4008502574944795, 0.4010769482749897, 0.40127055281667323, 0.40207033298933803, 0.40386353148751775, 0.40690269800942785, 0.41141351700179396, 0.4176753044727583, 0.42609497603705204, 0.43730236638460057, 0.4523091587286386, 0.472817812896814, 0.5018983203782212, 0.5456821927836282, 0.6184084972761777, 0.7620401329843498, 1.1805659609626207, 39.9744418582123]
        self.hvapL = [104.42143519895221, 102.67348214855879, 100.90149896055726, 99.10428047868746, 97.2701105764984, 95.36860837467255, 93.35827761148636, 91.19416524853438, 88.83171550394385, 86.22701718799784, 83.33457575145738, 80.10337550638823, 76.47124152467183, 72.35646703406533, 67.64383632237869, 62.15780440952316, 55.602425219431055, 47.39682473308241, 36.02892069023571, 0.0]
        self.surfL = [0.00012949864440348668, 0.0001211798572405094, 0.0001129658243110163, 0.00010486127620720714, 9.68714647103584e-05, 8.900225865081874e-05, 8.126026548862478e-05, 7.365298802437037e-05, 6.61890301652283e-05, 5.887837296304487e-05, 5.1732754369674534e-05, 4.4766207589693324e-05, 3.799585252845024e-05, 3.1443112946526816e-05, 2.513569891519111e-05, 1.9111090523097977e-05, 1.3423343414674658e-05, 8.158693814977866e-06, 3.4830186527611792e-06, 0.0]    
        self.SG_liqL = [1.3060789653692286, 1.2836038721174605, 1.260092771706973, 1.2361076760176366, 1.211755580407437, 1.1869849976411773, 1.1616841989357605, 1.1357131691613582, 1.108910637103779, 1.0810900819646374, 1.0520288217425533, 1.0214498465584976, 0.9889926238523316, 0.9541639296526844, 0.9162483316524143, 0.8741273278080032, 0.8258609834492318, 0.7675315006141954, 0.6888052251690647, 0.43614416372475523]
        self.log10SG_vapL = [-4.984718637591657, -4.369661407295961, -3.8662145910164427, -3.447786009065347, -3.0950973177466357, -2.7938286286079363, -2.533166226208821, -2.30483838965894, -2.1024387978938464, -1.920935197773639, -1.7563040880617609, -1.605251759001329, -1.4649911337785313, -1.333045882860113, -1.2070460553642963, -1.084450902099389, -0.9620367755386742, -0.834587658343251, -0.6897356663169578, -0.36036993467294526]
        
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
        data_srcD["Cp"]      = "CoolProp" # BTU/lbm/delF
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
        RefProp calculations for LOX  (O2(L), Oxygen). 
        
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
        log10x = log10(1 + dp / (1565.4989622746668 + psat))  # Fit Standard Deviation = 2.5421176827074696e-06
        dsg_o_sgL.append(  0.024504159303010187*log10x + 0.023741862618903847*log10x**2 + 0.020817741894599135*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1142.1300319742031 + psat))  # Fit Standard Deviation = 4.613549831506936e-06
        dsg_o_sgL.append(  0.021321693699385746*log10x + 0.020002061700427617*log10x**2 + 0.020043152801078424*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (796.5687033622493 + psat))  # Fit Standard Deviation = 8.541961101318089e-06
        dsg_o_sgL.append(  0.01811359731714677*log10x + 0.015875840682873083*log10x**2 + 0.019250979505716838*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (522.9800210245902 + psat))  # Fit Standard Deviation = 1.599677382531878e-05
        dsg_o_sgL.append(  0.014990784899862174*log10x + 0.011327287371128309*log10x**2 + 0.018413377773129975*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (310.29181302084805 + psat))  # Fit Standard Deviation = 3.0169599984360245e-05
        dsg_o_sgL.append(  0.012096012292934225*log10x + 0.006284575360468623*log10x**2 + 0.017474976759937387*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4004.6669573193412 + psat))  # Fit Standard Deviation = 3.4708600730533275e-06
        dsg_o_sgL.append(  0.1713660039223299*log10x + 0.0450593359607568*log10x**2 + -0.00749484493950303*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2911.3976340013637 + psat))  # Fit Standard Deviation = 5.620466770884779e-06
        dsg_o_sgL.append(  0.16484689527618201*log10x + 0.04533974289559379*log10x**2 + -0.007300765306905699*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1984.744853689273 + psat))  # Fit Standard Deviation = 9.191497687438977e-06
        dsg_o_sgL.append(  0.1578349378171348*log10x + 0.04562013483534058*log10x**2 + -0.0073238565261411715*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1200.5214990673778 + psat))  # Fit Standard Deviation = 1.5077659151545371e-05
        dsg_o_sgL.append(  0.14963859606514818*log10x + 0.046024143574883505*log10x**2 + -0.007506374630562695*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (542.1018884237864 + psat))  # Fit Standard Deviation = 2.450039511581722e-05
        dsg_o_sgL.append(  0.1391153704301389*log10x + 0.04670003611350748*log10x**2 + -0.007774992503905318*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (0.022818172715366222 + psat))  # Fit Standard Deviation = 3.8208321246162495e-05
        dsg_o_sgL.append(  0.12413335126920151*log10x + 0.047660180616607734*log10x**2 + -0.007950389489123157*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.42084172191136e-06 + psat))  # Fit Standard Deviation = 0.0011154051331061098
        dsg_o_sgL.append(  0.3827636571040357*log10x + -0.19946283054948838*log10x**2 + 0.07661525362239033*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.8615834935979536e-06 + psat))  # Fit Standard Deviation = 0.037367390648883274
        dsg_o_sgL.append(  2.340023173056651*log10x + -3.4531382789431726*log10x**2 + 1.6738282493779768*log10x**3  )

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

    
