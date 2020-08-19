
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of N2H4
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='N2H4')

    def set_std_state(self):
        """Set properties and standard state of Propellant, N2H4"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.19991643568769324 # psia
        self.Pc      = 2131 # psia
        self.Tc      = 1175.67 # degR
        self.Zc      = 0.26166359464536776 # Z at critical pt
        self.omega   = 0.31775551706632665 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.010071055786346 # SG
        self.visc    = 0.010279506276771388 # poise
        self.cond    = 0.2831171236931418 # BTU/hr/ft/delF
        self.Tnbp    = 697.27 # degR
        self.Tfreeze = 494.42 # degR
        self.Ttriple = 494.42 # degR
        self.Cp      = 0.7377690794489066 # BTU/lbm/delF
        self.MolWt   = 32.0453 # g/gmole
        self.Hvap    = 583.0000586288642 # BTU/lbm
        self.surf    = 0.00038638119778515017 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.42054317963374077, 0.44951602065205376, 0.4784888616703667, 0.5074617026886796, 0.5364345437069926, 0.5654073847253056, 0.5943802257436186, 0.6233530667619315, 0.6523259077802445, 0.6812987487985575, 0.7102715898168703, 0.7392444308351833, 0.7682172718534963, 0.7971901128718093, 0.8261629538901223, 0.8551357949084352, 0.8841086359267482, 0.9130814769450611, 0.9420543179633741, 0.971027158981687, 1.0]
        self.tL = [494.42, 528.4825000000001, 562.5450000000001, 596.6075, 630.6700000000001, 664.7325000000001, 698.7950000000001, 732.8575000000001, 766.9200000000001, 800.9825000000001, 835.045, 869.1075000000001, 903.1700000000001, 937.2325000000001, 971.2950000000001, 1005.3575000000001, 1039.42, 1073.4825, 1107.545, 1141.6075, 1175.67]
        
        self.log10pL  = [-1.2314546262849444, -0.6870526172921168, -0.2139499418305812, 0.20040363703920824, 0.565825303933674, 0.8901009305290604, 1.1794816127034902, 1.4390417764694865, 1.6729419013311788, 1.8846242677154554, 2.076960870127152, 2.252366643257035, 2.412887192627981, 2.5602675666056043, 2.6960068025236628, 2.8214017507892275, 2.937582868505014, 3.0455442264787216, 3.146170040478342, 3.2402616402475526, 3.328583449714202]
        self.log10viscL = [-1.852186783706388, -1.9912117399441023, -2.1193174403022073, -2.23809645953801, -2.3488133719006385, -2.4524951187787987, -2.5499810515893864, -2.6419713600908916, -2.7290517690299243, -2.811720608928529, -2.890403031391739, -2.9654659785388393, -3.0372279868440444, -3.105966910413839, -3.171927545453749, -3.2353253991192297, -3.296352554153907, -3.355179614458102, -3.411959969807745, -3.466831070465056, -3.519917261585504]
        self.condL = [0.2828153415820077, 0.2831171695534954, 0.28236207703771077, 0.2796471989340911, 0.27464301694420074, 0.2679375546928656, 0.25888650287107307, 0.24859900155772166, 0.2384389308984527, 0.2281178018135722, 0.21760333165407605, 0.20685699628106602, 0.1958285067878105, 0.1844503038118041, 0.17262841701790296, 0.16022544713858247, 0.1470261571941133, 0.13265968313125598, 0.1157965982678647, 0.12309914971960496, 0.1392353209971407]
        self.cpL = [0.7275870263198156, 0.7380319960419878, 0.7497288811952735, 0.7614842198468846, 0.7727064663823543, 0.7843649421402379, 0.796022349426081, 0.8080332885859892, 0.8209430854682619, 0.8355474905841779, 0.851347251996815, 0.8685797842279572, 0.888417494010466, 0.9121266559553796, 0.9418332646394101, 0.9813800962620732, 1.038475163895752, 1.1311508869977709, 1.3136503161443327, 1.8579724143962213, 32.3911199783706]
        self.hvapL = [594.3174723816354, 582.7190587953419, 570.741884174138, 558.351362067837, 545.5074789542455, 532.1635410197607, 518.2645260530653, 503.74487786903353, 488.5254955213249, 472.5095285952297, 455.5763477810456, 437.5726260018143, 418.2986473792892, 397.48632330700974, 374.7618631871127, 349.5776918004625, 321.0758961437182, 287.77517299423175, 246.68943825562647, 189.71461405666585, 0.0]
        self.surfL = [0.0004083433651861924, 0.0003857408094586473, 0.0003591288807741431, 0.0003329892117327349, 0.0003073404321093103, 0.00028220314330201925, 0.0002576003325923004, 0.00023355745858356347, 0.00021010366930733872, 0.0001872715159753113, 0.00016509931788011116, 0.00014363063813422724, 0.00012291848048696523, 0.0001030250440687974, 8.402946732149928e-05, 6.60298932306035e-05, 4.916054172722002e-05, 3.360635348783639e-05, 1.9661873367825438e-05, 7.858228384534371e-06, -1.7205356741102976e-22]    
        self.SG_liqL = [1.0259049485949754, 1.0096797602757333, 0.993076988773433, 0.9760633048404315, 0.9586001851762277, 0.9406427164747956, 0.9221380229507018, 0.903023162278914, 0.8832222535816837, 0.8626424664349276, 0.841168268437897, 0.8186529137079849, 0.7949053711548292, 0.7696693203087508, 0.7425874493822776, 0.7131362454457024, 0.6804949275223782, 0.6432440331370165, 0.5985126145376435, 0.5384503594208263, 0.33141633683602434]
        self.log10SG_vapL = [-5.245444612942634, -4.72957741572193, -4.2828118956477725, -3.892564743565788, -3.548875560178817, -3.24372271791348, -2.970550707996566, -2.7239375233473617, -2.4993539032136134, -2.2929821676625646, -2.1015734601099396, -1.922329626707633, -1.7528004124705103, -1.5907887176531672, -1.4342566548272593, -1.2812228682160949, -1.129635733426494, -0.9771938636057891, -0.8210541360526549, -0.6572842886884478, -0.4796260872779861]
        
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
        RefProp calculations for N2H4  (Hydrazine). 
        
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
        log10x = log10(1 + dp / (8181.896689786365 + psat))  # Fit Standard Deviation = 1.4599035737477177e-08
        dsg_o_sgL.append(  0.03596905386776402*log10x + 0.03422481406799366*log10x**2 + 0.018145043285356762*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6607.514842625012 + psat))  # Fit Standard Deviation = 3.1433495619389054e-08
        dsg_o_sgL.append(  0.03437703084358101*log10x + 0.03299822756277037*log10x**2 + 0.0181965020224925*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5279.604261167696 + psat))  # Fit Standard Deviation = 6.760225695068379e-08
        dsg_o_sgL.append(  0.03272644737039378*log10x + 0.031690217687700514*log10x**2 + 0.018313362913823957*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4136.3415644247825 + psat))  # Fit Standard Deviation = 1.4700650514058681e-07
        dsg_o_sgL.append(  0.030891497541985467*log10x + 0.030153880468657034*log10x**2 + 0.01844613469521949*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3126.1480995468896 + psat))  # Fit Standard Deviation = 3.296154819246511e-07
        dsg_o_sgL.append(  0.028689751180799503*log10x + 0.02817271484776563*log10x**2 + 0.018527726453631897*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2214.445872131976 + psat))  # Fit Standard Deviation = 7.801830942730602e-07
        dsg_o_sgL.append(  0.02589796085872186*log10x + 0.025452075384908113*log10x**2 + 0.018473547000763958*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (11431.54122850591 + psat))  # Fit Standard Deviation = 1.1515271283872017e-07
        dsg_o_sgL.append(  0.16870593148164548*log10x + 0.04255520755424098*log10x**2 + -0.0052824769955791455*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (7984.986840949949 + psat))  # Fit Standard Deviation = 2.591867733349267e-07
        dsg_o_sgL.append(  0.16207224342366308*log10x + 0.043354666526977254*log10x**2 + -0.0043665640101013545*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4875.595046225594 + psat))  # Fit Standard Deviation = 6.056574182999508e-07
        dsg_o_sgL.append(  0.15204774064362592*log10x + 0.043330697093828995*log10x**2 + -0.0036021468562124994*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2164.111453664107 + psat))  # Fit Standard Deviation = 1.466119713153005e-06
        dsg_o_sgL.append(  0.1377965307867554*log10x + 0.04216208023869644*log10x**2 + -0.003325937895888776*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (0.00022108777662191456 + psat))  # Fit Standard Deviation = 3.908764250469068e-06
        dsg_o_sgL.append(  0.12663981792607898*log10x + 0.03386707348486395*log10x**2 + -0.0021506009690383126*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (7.675709569359322e-08 + psat))  # Fit Standard Deviation = 0.050001476377369306
        dsg_o_sgL.append(  3.504026320642934*log10x + -7.994261024646266*log10x**2 + 5.766505717449902*log10x**3  )

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

    
