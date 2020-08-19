
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Ammonia
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Ammonia')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Ammonia"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 431.6814 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6955372969 # psia
        self.Pc      = 1643.7122541 # psia
        self.Tc      = 729.72 # degR
        self.Zc      = 0.254547225787 # Z at critical pt
        self.omega   = 0.25601362767424973 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.681972543378 # SG
        self.visc    = 0.00255483891753 # poise
        self.cond    = 0.38488260463 # BTU/hr/ft/delF
        self.Tnbp    = 431.6814 # degR
        self.Tfreeze = 351.891 # degR
        self.Ttriple = 351.891 # degR
        self.Cp      = 1.06306557784 # BTU/lbm/delF
        self.MolWt   = 17.03026 # g/gmole
        self.Hvap    = 589.172863882 # BTU/lbm
        self.surf    = 0.000255547117299 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.4822274296990627, 0.5094786176096383, 0.536729805520214, 0.5639809934307897, 0.5912321813413652, 0.6184833692519409, 0.6457345571625166, 0.6729857450730922, 0.7002369329836678, 0.7274881208942436, 0.7547393088048191, 0.7819904967153949, 0.8092416846259706, 0.8364928725365461, 0.8637440604471216, 0.8909952483576975, 0.9182464362682731, 0.9454976241788486, 0.9727488120894244, 1.0]
        self.tL = [351.891, 371.77673684210527, 391.66247368421057, 411.5482105263158, 431.43394736842106, 451.31968421052636, 471.2054210526316, 491.09115789473685, 510.97689473684215, 530.8626315789475, 550.7483684210526, 570.634105263158, 590.5198421052633, 610.4055789473684, 630.2913157894736, 650.177052631579, 670.0627894736842, 689.9485263157894, 709.8342631578948, 729.72]
        
        self.log10pL  = [-0.05381458886880206, 0.3064605763259402, 0.6255074271296022, 0.909682763236478, 1.1641864493415108, 1.3933100206406897, 1.600619894073728, 1.7890968205631343, 1.961244970981564, 2.1191790176711374, 2.264694638747961, 2.399326209576734, 2.5243945284816443, 2.6410469739290354, 2.7502924491538785, 2.8530340689456057, 2.9501046701255738, 3.042316830945455, 3.1305624151410907, 3.2160687707730786]
        self.log10viscL = [-2.2521475542297074, -2.352908529169169, -2.442021401291909, -2.521121054826769, -2.59180342403545, -2.655585094028812, -2.7138471709886955, -2.7677988113778165, -2.818469104914135, -2.8667226511423602, -2.913290938081187, -2.9588136876996294, -3.0038885276222813, -3.049132902448691, -3.0952710732631754, -3.1432797638038394, -3.194693273736083, -3.2524708112409275, -3.324940672011833, -3.5680697451747507]
        self.condL = [0.47352165425056825, 0.4510574752026766, 0.4287334497475356, 0.40671690662191917, 0.38514773059849766, 0.36412254299592084, 0.3436954155095086, 0.32388460108278766, 0.3046802829159328, 0.28605129744209135, 0.26795014270852757, 0.250316057468931, 0.23307598498602128, 0.21614310695203626, 0.19941262902620865, 0.1827550985320198, 0.16601029183305838, 0.14900262852756446, 0.1318849463073428, 0.17091071907731123]
        self.cpL = [1.0043608293091513, 1.0192687448873325, 1.0345621890929355, 1.0491887817115357, 1.0628999082834947, 1.0759867626832256, 1.089065303797449, 1.1029535425181, 1.1186336198290927, 1.1372864919569932, 1.1604010037798371, 1.1899852786366532, 1.2289572401527582, 1.2819016903304377, 1.3566811129511132, 1.468365966386273, 1.6509884875843546, 2.005924484173869, 3.0641573632380874, 81.85567348239823]
        self.hvapL = [638.5948034012747, 627.3191863460634, 615.404216679329, 602.7702798939755, 589.3452159124756, 575.0538487434458, 559.8114065878315, 543.5187065296889, 526.0569461124499, 507.28039261185484, 487.00542718200575, 464.9939262809358, 440.9274781143907, 414.3655538485129, 384.6729489909846, 350.8815112393444, 311.38762410140083, 263.12646317525713, 198.19083145960178, 0.0]
        self.surfL = [0.00035550987396459167, 0.0003295508872986226, 0.0003042817013189555, 0.0002797087812682051, 0.00025583966866075903, 0.00023268319528594697, 0.0002102497563779353, 0.00018855166491079896, 0.00016760361959325688, 0.0001474233363076754, 0.00012803242156848296, 0.0001094576171665837, 9.17326387487608e-05, 7.49010156822168e-05, 5.9020734203588606e-05, 4.4172422145395724e-05, 3.0475372485965522e-05, 1.812430968682644e-05, 7.500968674669963e-06, 0.0]    
        self.SG_liqL = [0.7329042288061083, 0.7210032741531567, 0.7085505182084572, 0.6955855037892353, 0.6821427339566717, 0.6682397997704058, 0.65387264391951, 0.6390135970331171, 0.6236096770380921, 0.6075795988419361, 0.590808213235135, 0.573136793293114, 0.554346596926947, 0.5341309186184889, 0.5120457900037902, 0.48741628228342665, 0.459132126911124, 0.4250732542859667, 0.3795509075914059, 0.2250006571867121]
        self.log10SG_vapL = [-4.19318538788404, -3.855409696062982, -3.5569642605423155, -3.2914589044181977, -3.0536449236553183, -2.8391729535260146, -2.6444116942671134, -2.4663056868275954, -2.30225885744369, -2.1500354088240985, -2.0076718189386558, -1.8733938700965964, -1.7455307669919646, -1.6224132803320472, -1.5022302948142061, -1.3827848000499834, -1.2609868841308849, -1.1315099616822726, -0.9814851457177797, -0.6478162133902116]
        
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
        RefProp calculations for NH3  (Ammonia). 
        
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
        log10x = log10(1 + dp / (5252.722609769466 + psat))  # Fit Standard Deviation = 1.0060591140468756e-07
        dsg_o_sgL.append(  0.03955024781090233*log10x + 0.03841900363177283*log10x**2 + 0.022733169326533433*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3699.338649125036 + psat))  # Fit Standard Deviation = 2.575464755722122e-07
        dsg_o_sgL.append(  0.035417470267759404*log10x + 0.03451853242582196*log10x**2 + 0.021696457571681073*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2568.34452368028 + psat))  # Fit Standard Deviation = 6.381842229711579e-07
        dsg_o_sgL.append(  0.03126974890307171*log10x + 0.030548098142950127*log10x**2 + 0.020943063472069215*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (11023.427975836727 + psat))  # Fit Standard Deviation = 3.223070789814432e-07
        dsg_o_sgL.append(  0.17083847023929066*log10x + 0.05234552332521625*log10x**2 + -0.00016140267657862908*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (8013.20108871707 + psat))  # Fit Standard Deviation = 5.80537351011035e-07
        dsg_o_sgL.append(  0.16404692571669116*log10x + 0.05112375912269118*log10x**2 + -0.0001510833371681649*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5529.756820835035 + psat))  # Fit Standard Deviation = 1.1015989006083535e-06
        dsg_o_sgL.append(  0.15757930003880885*log10x + 0.04944912274596679*log10x**2 + -0.0007002548242401284*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3458.1587714116017 + psat))  # Fit Standard Deviation = 2.207970494977422e-06
        dsg_o_sgL.append(  0.15096615932535035*log10x + 0.04751238124431654*log10x**2 + -0.0017379888803756194*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1734.2647126892991 + psat))  # Fit Standard Deviation = 4.610654751817515e-06
        dsg_o_sgL.append(  0.14363909991873663*log10x + 0.045697164705484815*log10x**2 + -0.0032817099721452426*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (321.9813487004404 + psat))  # Fit Standard Deviation = 9.59383673184999e-06
        dsg_o_sgL.append(  0.13427847151966282*log10x + 0.04476939260186801*log10x**2 + -0.005318843288404176*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.3492304727740898e-05 + psat))  # Fit Standard Deviation = 0.0004980169388843503
        dsg_o_sgL.append(  0.35746238120735674*log10x + -0.19730558987435537*log10x**2 + 0.09686252402959622*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3.167366164032964e-07 + psat))  # Fit Standard Deviation = 0.050554171087399576
        dsg_o_sgL.append(  3.6330583412824033*log10x + -7.926411876008353*log10x**2 + 5.518271069017113*log10x**3  )

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

    
