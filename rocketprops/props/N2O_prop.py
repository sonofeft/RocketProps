
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of N2O
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='N2O')

    def set_std_state(self):
        """Set properties and standard state of Propellant, N2O"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 332.424 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6925017421 # psia
        self.Pc      = 1050.7981365 # psia
        self.Tc      = 557.136 # degR
        self.Zc      = 0.274188000182 # Z at critical pt
        self.omega   = 0.16218603413317356 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.2304601946 # SG
        self.visc    = 0.00323727790595 # poise
        self.cond    = 0.116128310697 # BTU/hr/ft/delF
        self.Tnbp    = 332.424 # degR
        self.Tfreeze = 328.221 # degR
        self.Ttriple = 328.194 # degR
        self.Cp      = 0.410860422425 # BTU/lbm/delF
        self.MolWt   = 44.0128 # g/gmole
        self.Hvap    = 161.021690437 # BTU/lbm
        self.surf    = 0.000135500695213 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.5891218661152753, 0.6107470310565766, 0.632372195997878, 0.6539973609391793, 0.6756225258804806, 0.6972476908217818, 0.7188728557630831, 0.7404980207043844, 0.7621231856456857, 0.783748350586987, 0.8053735155282883, 0.8269986804695896, 0.848623845410891, 0.8702490103521923, 0.8918741752934934, 0.9134993402347947, 0.935124505176096, 0.9567496701173974, 0.9783748350586987, 1.0]
        self.tL = [328.221, 340.26915789473685, 352.3173157894737, 364.36547368421054, 376.4136315789474, 388.46178947368423, 400.5099473684211, 412.55810526315787, 424.6062631578947, 436.65442105263156, 448.7025789473684, 460.75073684210525, 472.7988947368421, 484.84705263157895, 496.89521052631574, 508.9433684210526, 520.9915263157894, 533.0396842105263, 545.0878421052631, 557.136]
        
        self.log10pL  = [1.1055617728053555, 1.2772627166199342, 1.4354993203726558, 1.581820525022235, 1.7175617632099185, 1.8438789314706459, 1.9617764642399431, 2.0721306830680937, 2.1757093516478965, 2.2731881947181307, 2.3651650199353615, 2.452172011245149, 2.5346867478599027, 2.613142574579265, 2.6879391894679636, 2.759454957622761, 2.828064256221659, 2.8941690925751584, 2.95828134715178, 3.0215018033490857]
        self.log10viscL = [-2.469378901168471, -2.5266707804392223, -2.580187616680808, -2.6303448537352656, -2.6775499185116303, -2.7221990207981874, -2.764676424590731, -2.80535640618209, -2.844608108973316, -2.8828037126029566, -2.920330755846914, -2.9576103789470407, -2.99512494795571, -3.033462149677622, -3.0733906658482524, -3.1160047836584632, -3.163046629019083, -3.2178168480527902, -3.2890398353054153, -3.5177657820038726]
        self.condL = [0.1176274767777161, 0.11334060669578942, 0.1090847019612952, 0.10485638329158685, 0.10065220143376816, 0.09646890861980931, 0.09230352430084679, 0.08815336996519559, 0.0840161076116382, 0.07988979232006349, 0.07577294956774687, 0.0716646844519229, 0.06756484266757318, 0.0634742789809473, 0.05939549888644501, 0.0553347066174086, 0.05131039083394111, 0.047401438822246886, 0.04418736376136558, 0.060762154355989424]
        self.cpL = [0.41055395495841834, 0.41174236919273516, 0.41361170809678954, 0.41621861847654185, 0.41969090948397514, 0.42412282007062135, 0.4295708029309488, 0.4362029642747142, 0.4442664788652352, 0.4540620515608059, 0.46609837524387077, 0.4810876760472674, 0.5001619236532778, 0.5251991469938965, 0.5595594393061558, 0.6099192469209959, 0.6917717040204273, 0.8515538162079614, 1.3251126797567891, 21.674017499877642]
        self.hvapL = [162.1488477565455, 158.88849403536685, 155.52655520107623, 152.04173915012655, 148.412045641346, 144.61419027287843, 140.6228875811086, 136.40995063521447, 131.94311914501765, 127.18445983557964, 122.08806896184164, 116.59659850816007, 110.63571478752512, 104.1047111204797, 96.85939952909166, 88.6778019303769, 79.18142631468568, 67.61267905205142, 51.90901261834861, 0.0]
        self.surfL = [0.0001387017645627886, 0.00012956741833735437, 0.00012056412260002751, 0.00011169754481533377, 0.00010297396497371615, 9.440038683387941e-05, 8.598467872708244e-05, 7.77357546531408e-05, 6.966381151163546e-05, 6.178064655124907e-05, 5.410009290252319e-05, 4.663863515254706e-05, 3.941631131716878e-05, 3.2458094809242786e-05, 2.579613579471104e-05, 1.947368039725965e-05, 1.3552681431429672e-05, 8.131117623280291e-06, 3.3950990493262645e-06, 0.0]    
        self.SG_liqL = [1.2373090418178718, 1.2175626606002659, 1.1974361778358975, 1.176870087290887, 1.1557991099406735, 1.1341504190074, 1.1118413413726134, 1.0887762823994724, 1.0648424720343677, 1.0399038685670798, 1.0137920806269958, 0.9862922616501358, 0.957120103414421, 0.9258820941046867, 0.8920017824092707, 0.8545694240817845, 0.8119914507558137, 0.7609832684324795, 0.6923029702592032, 0.45201199463342173]
        self.log10SG_vapL = [-2.582729349681181, -2.4231902460355648, -2.275844397065695, -2.139117953783139, -2.0116462512701188, -1.8922371765110262, -1.7798397282738094, -1.6735163883800828, -1.5724179324101608, -1.4757591380805433, -1.3827933982316913, -1.2927832672101989, -1.2049618941812508, -1.1184757109956818, -1.0322877729492868, -0.9449916753024952, -0.8543924702843402, -0.7563299451028725, -0.6397978877820018, -0.3448500405558946]
        
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
        RefProp calculations for N2O  (Dinitrogen Oxide, NitrousOxide). 
        
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
        
        trL = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (880.2154163609767 + psat))  # Fit Standard Deviation = 5.585070150619566e-06
        dsg_o_sgL.append(  0.016655284302163644*log10x + 0.015113129814281591*log10x**2 + 0.01671363509253497*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6940.958368522281 + psat))  # Fit Standard Deviation = 2.7892920848102335e-07
        dsg_o_sgL.append(  0.1642041392386537*log10x + 0.038655502210612584*log10x**2 + -0.008018867529841921*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5212.923491702651 + psat))  # Fit Standard Deviation = 5.231662167617468e-07
        dsg_o_sgL.append(  0.16444796778586074*log10x + 0.03906723346032002*log10x**2 + -0.008770652312788351*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3704.1348206583607 + psat))  # Fit Standard Deviation = 1.053132696313498e-06
        dsg_o_sgL.append(  0.16365551800678563*log10x + 0.039815711748955714*log10x**2 + -0.009477462938988712*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2392.4044731311988 + psat))  # Fit Standard Deviation = 2.38619320968346e-06
        dsg_o_sgL.append(  0.1611222070272661*log10x + 0.04104304688934062*log10x**2 + -0.010063321760446912*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1259.5435595038346 + psat))  # Fit Standard Deviation = 6.362161653844991e-06
        dsg_o_sgL.append(  0.15538667515291557*log10x + 0.04290389050001555*log10x**2 + -0.010366368069385791*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (294.87664066389266 + psat))  # Fit Standard Deviation = 1.986169922356495e-05
        dsg_o_sgL.append(  0.1432675331853062*log10x + 0.045439901911218154*log10x**2 + -0.010107116905703392*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (7.513626163952091e-08 + psat))  # Fit Standard Deviation = 0.0004890188457035044
        dsg_o_sgL.append(  0.3128749390446353*log10x + -0.12251729690202048*log10x**2 + 0.05085358866170666*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4.077241698382011e-07 + psat))  # Fit Standard Deviation = 0.04105812781926922
        dsg_o_sgL.append(  2.6971637860324242*log10x + -4.67932236532584*log10x**2 + 2.640471639851386*log10x**3  )

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

    
