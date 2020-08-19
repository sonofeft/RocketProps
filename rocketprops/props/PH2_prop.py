
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Ph2
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Ph2')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Ph2"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 36.4878 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6948534802 # psia
        self.Pc      = 186.48947466 # psia
        self.Tc      = 59.2884 # degR
        self.Zc      = 0.30223885382 # Z at critical pt
        self.omega   = -0.21860648262979798 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.0708306167316 # SG
        self.visc    = 0.000133305601003 # poise
        self.cond    = 0.0598114067754 # BTU/hr/ft/delF
        self.Tnbp    = 36.4878 # degR
        self.Tfreeze = 24.912 # degR
        self.Ttriple = 24.84594 # degR
        self.Cp      = 2.32517319167 # BTU/lbm/delF
        self.MolWt   = 2.01594 # g/gmole
        self.Hvap    = 191.896930123 # BTU/lbm
        self.surf    = 1.09954126588e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.42018337482542956, 0.45070003930830166, 0.4812167037911738, 0.5117333682740459, 0.5422500327569181, 0.5727666972397902, 0.6032833617226623, 0.6338000262055344, 0.6643166906884066, 0.6948333551712788, 0.7253500196541508, 0.7558666841370231, 0.7863833486198951, 0.8169000131027673, 0.8474166775856393, 0.8779333420685115, 0.9084500065513835, 0.9389666710342557, 0.9694833355171278, 1.0]
        self.tL = [24.912, 26.721284210526314, 28.53056842105263, 30.339852631578946, 32.149136842105264, 33.95842105263158, 35.76770526315789, 37.57698947368421, 39.38627368421053, 41.195557894736844, 43.00484210526316, 44.81412631578948, 46.623410526315794, 48.43269473684211, 50.24197894736842, 52.05126315789474, 53.86054736842105, 55.66983157894737, 57.47911578947369, 59.2884]
        
        self.log10pL  = [0.0183795497220368, 0.25569436866676204, 0.4656541687171755, 0.6531452670037352, 0.8219540250761733, 0.9750550455539113, 1.1148153434864272, 1.243141546191338, 1.3615873382443904, 1.4714328052800911, 1.573743747077011, 1.6694166229378438, 1.7592131710742813, 1.843787687182169, 1.9237093538591126, 1.9994819434039228, 2.071564151476475, 2.1403979185813897, 2.206471856872957, 2.2706555340071013]
        self.log10viscL = [-3.5888827820744003, -3.645414381849989, -3.696002455084552, -3.74202724756111, -3.7844231337031977, -3.8238825069149733, -3.860955778596873, -3.8961039443247816, -3.9297298343547413, -3.962200101087265, -3.9938639915869523, -4.025072843243994, -4.056204386369084, -4.087698373019526, -4.120116935110548, -4.154262257094689, -4.191445870396326, -4.234258026202778, -4.289814278226119, -4.454468207572155]
        self.condL = [0.043693720648754285, 0.04802968647275226, 0.0515823631974751, 0.054420964048780114, 0.056626600521574116, 0.05828105193718628, 0.05945972599660808, 0.06022802905111303, 0.060639989332109144, 0.06073812473678162, 0.06055382367832501, 0.0601077300746213, 0.05940973041437389, 0.058458091383299854, 0.05723697139627078, 0.05571049502213279, 0.0538080861183722, 0.05138075573773148, 0.048006670673522225, 0.03969983725256325]
        self.cpL = [1.6573229555362967, 1.7320059827742387, 1.8168950518256641, 1.912192955537009, 2.01892405954122, 2.1376691836940407, 2.269085192410681, 2.414490823536498, 2.576327142670081, 2.758627473000995, 2.9677005268526893, 3.213321221005406, 3.510981521371542, 3.8864528424502365, 4.385920909525083, 5.101588754163036, 6.249690688710174, 8.490944062260024, 15.297244339997382, 579.4510577037208]
        self.hvapL = [193.64818249198999, 194.4999490390988, 195.01922721114093, 195.15060596614228, 194.8352500902924, 194.01272150787955, 192.62214887648298, 190.60149874636494, 187.88525304049583, 184.40075668958573, 180.06310274010244, 174.76787964172198, 168.38025664540868, 160.71722155331418, 151.515945678003, 140.3710039705816, 126.59066267979279, 108.78969616047893, 83.19176915527927, 0.0]
        self.surfL = [1.702613486998123e-05, 1.607343514385187e-05, 1.5124171226164977e-05, 1.4178531937119732e-05, 1.3236728928522377e-05, 1.2299001153786636e-05, 1.1365620596216198e-05, 1.0436899734495198e-05, 9.51320146214372e-06, 8.594952566348148e-06, 7.682662531705947e-06, 6.776950607821466e-06, 5.8785862820211825e-06, 4.988552715693025e-06, 4.1081523303704155e-06, 3.2391971005554998e-06, 2.38439180506815e-06, 1.5482476505196292e-06, 7.400200459948761e-07, 0.0]    
        self.SG_liqL = [0.07694999921813274, 0.07612795793928442, 0.07526708894965375, 0.07435717336714241, 0.07339251965424617, 0.07236888656493591, 0.07128194403896836, 0.07012645202508123, 0.06889570405743818, 0.06758098197545347, 0.06617084523428647, 0.06465006667848221, 0.06299792075224173, 0.06118525812806352, 0.05916913046557844, 0.05688190925088075, 0.05420602272469311, 0.050901512766566404, 0.04630032685471787, 0.03132371304644032]
        self.log10SG_vapL = [-3.892962704627715, -3.6828981758871127, -3.4973470515506637, -3.331602656753448, -3.1820268194683905, -3.0457662051643224, -2.920548827016541, -2.8045350615954012, -2.696206479578923, -2.5942805956282053, -2.497642432276209, -2.4052850871683815, -2.3162510848498066, -2.2295630309703873, -2.1441223717979834, -2.0585272431264334, -1.9706702356958115, -1.8766062334551399, -1.765819722024995, -1.504126763216845]
        
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
        RefProp calculations for PH2  (H2(L), Hydrogen, ParaHydrogen). 
        
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
        
        trL = [0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (743.7242590074275 + psat))  # Fit Standard Deviation = 2.461980515021304e-05
        dsg_o_sgL.append(  0.1389949270885777*log10x + 0.08827915233091083*log10x**2 + -0.0232010061734211*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (682.100357574733 + psat))  # Fit Standard Deviation = 1.9714700249336247e-05
        dsg_o_sgL.append(  0.14648859861837418*log10x + 0.08125199456822575*log10x**2 + -0.020308797617120317*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (615.0314831994513 + psat))  # Fit Standard Deviation = 1.6339532969061507e-05
        dsg_o_sgL.append(  0.1543833160963508*log10x + 0.07406606565948373*log10x**2 + -0.017835332070525508*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (688.2772065821217 + psat))  # Fit Standard Deviation = 9.886514092538638e-06
        dsg_o_sgL.append(  0.20579567526534367*log10x + 0.04090400541334042*log10x**2 + -0.00998872240943502*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (499.03873077839035 + psat))  # Fit Standard Deviation = 1.129922852510562e-05
        dsg_o_sgL.append(  0.18433172135031553*log10x + 0.05017865631778303*log10x**2 + -0.011407984482752978*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (354.1827568734911 + psat))  # Fit Standard Deviation = 1.4207328775577287e-05
        dsg_o_sgL.append(  0.170194616230476*log10x + 0.053737838732422036*log10x**2 + -0.011506415721801572*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (234.5329803253944 + psat))  # Fit Standard Deviation = 1.831674778694238e-05
        dsg_o_sgL.append(  0.1601601366509197*log10x + 0.05423136009448475*log10x**2 + -0.01105300472835858*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (129.8217972853021 + psat))  # Fit Standard Deviation = 2.4065632480753247e-05
        dsg_o_sgL.append(  0.1517623707908696*log10x + 0.053057957989809924*log10x**2 + -0.01033426908283744*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (36.141723451535164 + psat))  # Fit Standard Deviation = 3.310285592515163e-05
        dsg_o_sgL.append(  0.1438146504157458*log10x + 0.05052910781146872*log10x**2 + -0.009372391930922425*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.3129657197463574e-08 + psat))  # Fit Standard Deviation = 0.0002785766610145244
        dsg_o_sgL.append(  0.21998931357139223*log10x + -0.0008032008105722168*log10x**2 + 0.001188759569309543*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3.416419371125169e-08 + psat))  # Fit Standard Deviation = 0.002530396350661312
        dsg_o_sgL.append(  0.45733458833360624*log10x + -0.19942349709805463*log10x**2 + 0.052837918204109165*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.728910777494507e-08 + psat))  # Fit Standard Deviation = 0.024084857641403196
        dsg_o_sgL.append(  1.5247611676133936*log10x + -1.3519631789435367*log10x**2 + 0.4119847628502448*log10x**3  )

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

    
