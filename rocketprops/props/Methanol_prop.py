
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Methanol
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Methanol')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Methanol"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 527.67 # degR
        self.P       = 1.89009076582 # psia
        self.Pvap    = 1.89009076582 # psia
        self.Pc      = 1175.31300195 # psia
        self.Tc      = 922.68 # degR
        self.Zc      = 0.221138723259 # Z at critical pt
        self.omega   = 0.5646279527412872 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.790928353374 # SG
        self.visc    = 0.00584983624524 # poise
        self.cond    = 0.116984204459 # BTU/hr/ft/delF
        self.Tnbp    = 607.7376 # degR
        self.Tfreeze = 316.098 # degR
        self.Ttriple = 316.098 # degR
        self.Cp      = 0.598637435914 # BTU/lbm/delF
        self.MolWt   = 32.04216 # g/gmole
        self.Hvap    = 506.174659683 # BTU/lbm
        self.surf    = 0.000129470848379 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.3425868123293016, 0.3771875064172331, 0.41178820050516457, 0.4463888945930961, 0.4809895886810276, 0.515590282768959, 0.5501909768568906, 0.5847916709448221, 0.6193923650327535, 0.6539930591206852, 0.6885937532086166, 0.723194447296548, 0.7577951413844797, 0.7923958354724111, 0.8269965295603426, 0.8615972236482741, 0.8961979177362055, 0.9307986118241371, 0.9653993059120686, 1.0]
        self.tL = [316.098, 348.0233684210526, 379.9487368421053, 411.87410526315796, 443.79947368421057, 475.7248421052632, 507.65021052631585, 539.5755789473685, 571.5009473684211, 603.4263157894738, 635.3516842105264, 667.277052631579, 699.2024210526317, 731.1277894736843, 763.053157894737, 794.9785263157896, 826.9038947368422, 858.829263157895, 890.7546315789475, 922.6800000000001]
        
        self.log10pL  = [-4.568041343682912, -3.426175897726996, -2.4886007425044743, -1.7067916935171517, -1.0463244796949103, -0.4821436269850317, 0.0044388689379552025, 0.4276610322792718, 0.7985799444957368, 1.1259270216407529, 1.4166946097649735, 1.6765515283455275, 1.9101521698251016, 2.1213763832381582, 2.3135053212096905, 2.4892644786941323, 2.6505645444723083, 2.798615708211274, 2.937097307506557, 3.070179795161525]
        self.log10viscL = [-0.892334045998053, -1.2374710079487936, -1.5019928180992934, -1.706457636945853, -1.8773785341227793, -2.0262432083025232, -2.1578660315256606, -2.274978081386827, -2.3798085429073748, -2.47447834411857, -2.561043617552284, -2.641478112047254, -2.717672806978498, -2.791464535821466, -2.864687985482856, -2.9392443693957877, -3.0172428589914166, -3.1018066773170285, -3.2030113883441436, -3.3938604777976664]
        self.condL = [0.1565409232664758, 0.14773755562297144, 0.14001223289161926, 0.13342170384734103, 0.12785099577070835, 0.12314300446136274, 0.11916702931222166, 0.11578204263256975, 0.11285015702965055, 0.11024582121465633, 0.10786030636292335, 0.10560203518074639, 0.1033946313450882, 0.10117482013979259, 0.09889288767781239, 0.09652078956620103, 0.09408230788341888, 0.09179174317977327, 0.09117448091810589, 0.11335571013162729]
        self.cpL = [0.5250477724988539, 0.5287886497383155, 0.5315210557396867, 0.5390165492502057, 0.5500459735512088, 0.5648385414173157, 0.5840998269083668, 0.6081885158808865, 0.6370587597060676, 0.67050819119183, 0.7084446856734308, 0.7511064790261485, 0.7992912170701368, 0.8547197625638148, 0.9207741368340593, 1.004224349682646, 1.1204017834671147, 1.3182653766204302, 1.9087965760148562, 20.234833703308066]
        self.hvapL = [565.5046945735913, 557.8678338537848, 550.058366345057, 541.8463784156847, 533.0302872159612, 523.4902424167067, 513.1340335913362, 501.8473304237992, 489.4519644051585, 475.6765769467351, 460.1420815247999, 442.35551125464315, 421.7005519847231, 397.4240204315621, 368.6931250094674, 335.1213219896233, 298.13759767845477, 257.112976376965, 193.96908177644775, 0.0]
        self.surfL = [0.0001956482012498527, 0.00018320677515381415, 0.00017197599406819353, 0.0001617289855512758, 0.0001522470548827114, 0.00014332044619874907, 0.00013474925749869116, 0.00012634455753746218, 0.0001179297733919466, 0.00010934245012341793, 0.00010043653717080256, 9.108544675369582e-05, 8.11862922534576e-05, 7.066602573059902e-05, 5.9490838242498865e-05, 4.76816658439141e-05, 3.534254576502414e-05, 2.2721173144693202e-05, 1.0378256741858536e-05, 2.095199165621674e-07]    
        self.SG_liqL = [0.9045643806392595, 0.8869386863222748, 0.8692773155700391, 0.8519013099045403, 0.8348083798865514, 0.8179759957120225, 0.8013318944961002, 0.7847295913199116, 0.7679537522507351, 0.7507358104144812, 0.7327647105971267, 0.7136852451488889, 0.6930798133718477, 0.670428406022531, 0.6450362857477969, 0.6159042195149915, 0.5814498027320545, 0.5385766465588984, 0.4774099103577368, 0.2755629043704677]
        self.log10SG_vapL = [-8.38828522270717, -7.287911920798633, -6.3880697781312445, -5.640525902322043, -5.011170701769704, -4.475190649642974, -4.014065738358517, -3.613626978710237, -3.2627637370935356, -2.952555546542785, -2.675674746597, -2.4259429374108614, -2.197958172744626, -1.986762973065808, -1.787705903832734, -1.5974069584948187, -1.4169243549658836, -1.243164823259537, -1.0328945835647714, -0.5597792465304997]
        
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
        RefProp calculations for Methanol  (CH4O). 
        
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
        
        trL = [0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.35 ) # saturation pressure at Tr=0.35
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3191.715186959335 + psat))  # Fit Standard Deviation = 2.837118788145182e-07
        dsg_o_sgL.append(  0.027616043627984255*log10x + 0.02683968541176404*log10x**2 + 0.01713538185956224*log10x**3  )

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2655.177365208165 + psat))  # Fit Standard Deviation = 4.801888610778139e-07
        dsg_o_sgL.append(  0.028768071331671797*log10x + 0.027856084140237214*log10x**2 + 0.018342824335801866*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2066.375197975173 + psat))  # Fit Standard Deviation = 8.865877559244185e-07
        dsg_o_sgL.append(  0.026659034866233455*log10x + 0.02579633769674572*log10x**2 + 0.01821968148866191*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1553.1170152935774 + psat))  # Fit Standard Deviation = 1.6877012414566917e-06
        dsg_o_sgL.append(  0.02375494146637885*log10x + 0.022859601269758296*log10x**2 + 0.017858556461887103*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1144.2862358209711 + psat))  # Fit Standard Deviation = 3.1713324845605746e-06
        dsg_o_sgL.append(  0.02080985258260405*log10x + 0.019662827028871052*log10x**2 + 0.017496964450814452*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (817.5051334225126 + psat))  # Fit Standard Deviation = 5.913015205876159e-06
        dsg_o_sgL.append(  0.017889720622633287*log10x + 0.0161750381111185*log10x**2 + 0.017114948902916167*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (547.1596400613786 + psat))  # Fit Standard Deviation = 1.1192232128330875e-05
        dsg_o_sgL.append(  0.014931831953339296*log10x + 0.012179120440580516*log10x**2 + 0.016630805565163175*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4323.04250312209 + psat))  # Fit Standard Deviation = 2.039917054866528e-06
        dsg_o_sgL.append(  0.13909272168886705*log10x + 0.04603766491887147*log10x**2 + 0.0002697145150835314*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3303.4863597105946 + psat))  # Fit Standard Deviation = 2.9086310844193335e-06
        dsg_o_sgL.append(  0.13910040778242827*log10x + 0.04480386602562593*log10x**2 + -0.0012443476675556976*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2294.5283064564173 + psat))  # Fit Standard Deviation = 4.204301217656713e-06
        dsg_o_sgL.append(  0.1384849799280445*log10x + 0.0435828031756756*log10x**2 + -0.003110219235934577*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1319.899549691 + psat))  # Fit Standard Deviation = 6.096221294895582e-06
        dsg_o_sgL.append(  0.1374994841324965*log10x + 0.04280551274187621*log10x**2 + -0.005477611223877531*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (402.27147840383395 + psat))  # Fit Standard Deviation = 1.1786722710970603e-05
        dsg_o_sgL.append(  0.13528880666408333*log10x + 0.04340147786947483*log10x**2 + -0.00815935338979355*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4.969200897313042e-06 + psat))  # Fit Standard Deviation = 0.00043297760566535107
        dsg_o_sgL.append(  0.293573462248885*log10x + -0.10455194328330915*log10x**2 + 0.04316028134505978*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.4350024341074379e-08 + psat))  # Fit Standard Deviation = 0.028212264902254692
        dsg_o_sgL.append(  2.258018439174332*log10x + -3.9109948315804117*log10x**2 + 2.2807107666077533*log10x**3  )

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

    
