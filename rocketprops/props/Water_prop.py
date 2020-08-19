
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Water
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Water')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Water"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 527.67 # degR
        self.P       = 0.339289327159 # psia
        self.Pvap    = 0.339289327159 # psia
        self.Pc      = 3200.1118128 # psia
        self.Tc      = 1164.7728 # degR
        self.Zc      = 0.229493084738 # Z at critical pt
        self.omega   = 0.3442895966367192 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.998163451361 # SG
        self.visc    = 0.0100164691014 # poise
        self.cond    = 0.345990142049 # BTU/hr/ft/delF
        self.Tnbp    = 671.62374 # degR
        self.Tfreeze = 491.688 # degR
        self.Ttriple = 491.688 # degR
        self.Cp      = 1.00008592509 # BTU/lbm/delF
        self.MolWt   = 18.015268 # g/gmole
        self.Hvap    = 1055.52906578 # BTU/lbm
        self.surf    = 0.000415334061149 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.4221321102278488, 0.4525462096895409, 0.4829603091512331, 0.5133744086129253, 0.5437885080746174, 0.5742026075363096, 0.6046167069980017, 0.635030806459694, 0.6654449059213862, 0.6958590053830783, 0.7262731048447705, 0.7566872043064626, 0.7871013037681548, 0.8175154032298471, 0.8479295026915391, 0.8783436021532313, 0.9087577016149235, 0.9391718010766156, 0.969585900538308, 1.0]
        self.tL = [491.68800000000005, 527.1135157894737, 562.5390315789474, 597.9645473684211, 633.3900631578947, 668.8155789473684, 704.2410947368421, 739.6666105263158, 775.0921263157895, 810.5176421052631, 845.9431578947368, 881.3686736842105, 916.7941894736841, 952.219705263158, 987.6452210526315, 1023.0707368421051, 1058.496252631579, 1093.9217684210525, 1129.3472842105264, 1164.7728]
        
        self.log10pL  = [-1.0520125323045935, -0.47775698271278944, 0.015246344393391634, 0.442240524717325, 0.815026039076302, 1.142897899682636, 1.4332747820608858, 1.6921391921407676, 1.9243554861589713, 2.1339068623200097, 2.3240770352197004, 2.4975924611454294, 2.6567353700103604, 2.803435164492838, 2.939344603752641, 3.0659071628583465, 3.1844238214560616, 3.2961361991406024, 3.4023744425067033, 3.505165152944341]
        self.log10viscL = [-1.746864677792142, -1.9959894575403203, -2.179963819218995, -2.3250154990447927, -2.4436740513915174, -2.5428604511809647, -2.6269545170715687, -2.6990443985018917, -2.761475859953106, -2.8161213364045414, -2.864532900810337, -2.9080458210220854, -2.947862517104878, -2.9851350847825313, -3.021066976127431, -3.0570739310814132, -3.095108258665219, -3.13851199848112, -3.1959548700925824, -3.4041683405208913]
        self.condL = [0.3243791227412857, 0.3456707647346066, 0.36407539688445484, 0.377788703697484, 0.3869206140618188, 0.3923330130812562, 0.3948835691460576, 0.39516262120545903, 0.3934858094629224, 0.3899644408642576, 0.3845688744066583, 0.37715911502994715, 0.36748747382405833, 0.35520170505904103, 0.339914229543648, 0.3214417920017921, 0.30021793419118326, 0.2773513130772703, 0.25332092612160606, 0.3524925917304185]
        self.cpL = [1.0085828151338445, 1.0001386435988233, 0.9989468513487699, 1.000174096181458, 1.002852679129289, 1.007141475259904, 1.0134824045589228, 1.0223726552249355, 1.0343646975260634, 1.0501485670174502, 1.0706801238105141, 1.0973766843213486, 1.1324563228010904, 1.1796043401324912, 1.2454360291065152, 1.3431185754080999, 1.5029427770298898, 1.8141941201564458, 2.765067965250912, 91.30908450294936]
        self.hvapL = [1075.9190169889478, 1055.8438950444552, 1035.7224593361427, 1015.2829007730164, 994.3013042590591, 972.5257939225368, 949.6561744308299, 925.346157268879, 899.2145463412205, 870.8502802702967, 839.800089426642, 805.5369265664588, 767.4101160395346, 724.5689776695984, 675.831495401475, 619.426791319745, 552.4201278382121, 469.17209406799236, 355.07875385889247, 0.0]
        self.surfL = [0.00043195133541828226, 0.00041560111537718034, 0.00039798770119008514, 0.0003791658360482522, 0.00035919444905048296, 0.0003381373304632192, 0.00031606397594299764, 0.00029305065885266497, 0.00026918181730403295, 0.0002445518865784888, 0.0002192677807198375, 0.0001934523540997156, 0.00016724940621192638, 0.00014083124662607414, 0.00011441079651054992, 8.826245470222988e-05, 6.276204158635995e-05, 3.847636527455826e-05, 1.6428516761260782e-05, 0.0]    
        self.SG_liqL = [0.9997941728219975, 0.9982266990200434, 0.9924154635527068, 0.9836462652067586, 0.972552203348282, 0.9594829638903821, 0.9446353813451042, 0.9281076828622988, 0.909923249233034, 0.8900395089073463, 0.8683473514389392, 0.8446618551755486, 0.818701653299522, 0.7900492341617161, 0.7580738695265281, 0.7217724921627227, 0.6794081765532912, 0.6275312700850599, 0.5565191314574603, 0.32200038370684136]
        self.log10SG_vapL = [-5.313848002174229, -4.7694777223629545, -4.304106282640733, -3.902572111119477, -3.5530786003172397, -3.2462748581530545, -2.9746421947603365, -2.7320680742082812, -2.513537821583698, -2.3148966455697852, -2.1326522345409344, -1.963801920944148, -1.805672600240915, -1.655755477499836, -1.5115009928865064, -1.3699978663296972, -1.2273357524142423, -1.076961628558139, -0.903318389389039, -0.49214361078347163]
        
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
        RefProp calculations for Water  (H2O). 
        
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
        log10x = log10(1 + dp / (5917.775463812979 + psat))  # Fit Standard Deviation = 9.971025449443777e-08
        dsg_o_sgL.append(  0.043426333401859474*log10x + 0.04346226677029711*log10x**2 + 0.027196094289756337*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6684.205890052857 + psat))  # Fit Standard Deviation = 5.5242460981846956e-08
        dsg_o_sgL.append(  0.04691301179146745*log10x + 0.04599392154975231*log10x**2 + 0.026781244802483065*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (6265.375801085998 + psat))  # Fit Standard Deviation = 5.7901274692214546e-08
        dsg_o_sgL.append(  0.04629775480338429*log10x + 0.04487639178497619*log10x**2 + 0.025550446131436057*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5202.2130403129995 + psat))  # Fit Standard Deviation = 9.28937403453633e-08
        dsg_o_sgL.append(  0.04316244754107831*log10x + 0.04177656813458316*log10x**2 + 0.024181180940274306*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3900.008505622403 + psat))  # Fit Standard Deviation = 1.9997167153648701e-07
        dsg_o_sgL.append(  0.038500329502806734*log10x + 0.037459918469434826*log10x**2 + 0.022864349699535075*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (15776.372111883877 + psat))  # Fit Standard Deviation = 4.462632748746753e-08
        dsg_o_sgL.append(  0.19063731815214296*log10x + 0.05231812289008245*log10x**2 + -0.0029788640971406943*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (11352.590115303881 + psat))  # Fit Standard Deviation = 9.95712739422933e-08
        dsg_o_sgL.append(  0.1815735004421759*log10x + 0.04999126627830176*log10x**2 + -0.003274184163409955*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (7443.751062090155 + psat))  # Fit Standard Deviation = 2.7470598752655364e-07
        dsg_o_sgL.append(  0.1735737581982258*log10x + 0.04778778785614774*log10x**2 + -0.003942114542881836*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4006.4645313438577 + psat))  # Fit Standard Deviation = 9.203386421442475e-07
        dsg_o_sgL.append(  0.16472609394027288*log10x + 0.0460472253310367*log10x**2 + -0.004707559769388753*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1050.4983216420685 + psat))  # Fit Standard Deviation = 3.557391757491166e-06
        dsg_o_sgL.append(  0.15273261028060375*log10x + 0.044893966608037336*log10x**2 + -0.005618816893574429*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.7669279591408333e-07 + psat))  # Fit Standard Deviation = 0.000226318480066038
        dsg_o_sgL.append(  0.3491970789033811*log10x + -0.20267054596833087*log10x**2 + 0.12512745103693515*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.2527190583912108e-05 + psat))  # Fit Standard Deviation = 0.05415499137146242
        dsg_o_sgL.append(  5.034273410613715*log10x + -15.885313712915094*log10x**2 + 15.849049784108315*log10x**3  )

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

    
