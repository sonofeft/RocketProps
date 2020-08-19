
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of F2
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='F2')

    def set_std_state(self):
        """Set properties and standard state of Propellant, F2"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 153.06624 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6959564081 # psia
        self.Pc      = 750.19299948 # psia
        self.Tc      = 259.9452 # degR
        self.Zc      = 0.276149277781 # Z at critical pt
        self.omega   = 0.04490196517384115 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.50180315728 # SG
        self.visc    = 0.0024221672235591515 # poise
        self.cond    = 0.07771621359483595 # BTU/hr/ft/delF
        self.Tnbp    = 153.06624 # degR
        self.Tfreeze = 96.26598 # degR
        self.Ttriple = 96.26598 # degR
        self.Cp      = 0.3608961498041464 # BTU/lbm/delF
        self.MolWt   = 37.99681 # g/gmole
        self.Hvap    = 75.014218379 # BTU/lbm
        self.surf    = 7.62120650231e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.3703318237843976, 0.4034722541115346, 0.43661268443867157, 0.46975311476580855, 0.5028935450929455, 0.5360339754200825, 0.5691744057472194, 0.6023148360743563, 0.6354552664014933, 0.6685956967286304, 0.7017361270557673, 0.7348765573829042, 0.7680169877100411, 0.8011574180371782, 0.8342978483643152, 0.8674382786914521, 0.900578709018589, 0.9337191393457259, 0.9668595696728631, 1.0]
        self.tL = [96.26598, 104.88067578947368, 113.49537157894737, 122.11006736842106, 130.72476315789473, 139.33945894736843, 147.9541547368421, 156.56885052631577, 165.18354631578947, 173.79824210526317, 182.41293789473684, 191.0276336842105, 199.64232947368419, 208.25702526315789, 216.87172105263159, 225.48641684210526, 234.10111263157893, 242.7158084210526, 251.33050421052633, 259.9452]
        
        self.log10pL  = [-1.4604660304097383, -0.8583287864783504, -0.35577114247637487, 0.06910283591423606, 0.43246886607908347, 0.7465070907287945, 1.020514880529067, 1.261681391399096, 1.4756342995774405, 1.6668332584096415, 1.838857793872948, 1.9946202149118624, 2.136523834545689, 2.2665805822874154, 2.3864981414004216, 2.4977440876740564, 2.60159331111275, 2.6991700736446207, 2.791544427981517, 2.8807638992182114]
        self.log10viscL = [-2.13564240251722, -2.2159494187393713, -2.293584870749284, -2.3684422394822686, -2.4405317073425508, -2.5099276315874515, -2.576738203106682, -2.6410876897019606, -2.703105999473821, -2.76292258697098, -2.8206629737018245, -2.876446857441699, -2.930387190689021, -2.982589848386362, -3.0331536494127156, -3.082170584761253, -3.129726160209766, -3.1758997957674997, -3.220765246030797, -3.26326311709974]
        self.condL = [0.10681634207727052, 0.10240554572986045, 0.09799503742852632, 0.09358517888973358, 0.08917657404253934, 0.08477010264846592, 0.08036690730661028, 0.075968328998042, 0.07157579694389757, 0.06719068485326071, 0.06281414712617403, 0.05844694646961266, 0.05408928038399545, 0.049740609524967866, 0.04539948695174454, 0.04106338415655981, 0.03672850760164304, 0.032397179559587166, 0.028053276011098346, 0.023691047155914934]
        self.cpL = [0.36459737890108845, 0.3486777998834476, 0.3521774510500328, 0.3535243696087388, 0.3546145853392889, 0.35634558663294985, 0.3589948111481616, 0.36267344854754446, 0.3674803619299637, 0.3735804124577506, 0.38127718743317224, 0.3911100304600162, 0.4040136694777233, 0.4216210709860632, 0.44691317755536725, 0.48581573441933595, 0.5519050596856385, 0.6849011829618873, 1.0804256534656396, 35.597386537269706]
        self.hvapL = [85.64128640530868, 84.18250850451334, 82.7059888052049, 81.17611855671396, 79.58565138823734, 77.91306129703065, 76.13250434164264, 74.21806429912954, 72.14475643081236, 69.88765922648115, 67.41951719089491, 64.70685670427957, 61.70436887699809, 58.34670798423953, 54.53548203669018, 50.11577036518757, 44.82604174211143, 38.1631424312865, 28.833733183856268, 0.0]
        self.surfL = [0.00013039213670906755, 0.00012180502950441762, 0.0001133411215482773, 0.00010500574076716256, 9.680479091705639e-05, 8.874485616121995e-05, 8.083333343889495e-05, 7.307860271183767e-05, 6.549024998299748e-05, 5.8079365727451346e-05, 5.085895433237764e-05, 4.3844512792642234e-05, 3.7054878645821534e-05, 3.051352914668045e-05, 2.4250688343528322e-05, 1.830701148317906e-05, 1.274073978475915e-05, 7.643982065219644e-06, 3.1916985394959943e-06, 0.0]    
        self.SG_liqL = [1.706717314427076, 1.6761849461965255, 1.646292385019033, 1.6160866106674576, 1.5853434880760195, 1.5538834089235964, 1.521516091632366, 1.4880542851781369, 1.453313953398395, 1.4171002348529353, 1.3791837617655696, 1.3392667420008184, 1.2969324276435654, 1.2515638725936058, 1.2022017832659113, 1.147269398022797, 1.0839654365345912, 1.006644071926707, 0.9006734348694395, 0.5928649329087468]
        self.log10SG_vapL = [-4.690076965110834, -4.124843621358218, -3.6558724307271238, -3.2614793058540696, -2.9256007600455574, -2.636120322947133, -2.383787460193754, -2.161454300057172, -1.9635229561389334, -1.7855336464402034, -1.623850016124423, -1.4754132175589834, -1.337543163226651, -1.207765595513143, -1.0836353822186084, -0.9624982221307135, -0.8410335982901163, -0.7139849487678319, -0.5685761590263064, -0.22704423677701036]
        
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
        data_srcD["visc"]    = "thermo" # poise
        data_srcD["cond"]    = "thermo" # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = "RefProp" # degR
        data_srcD["Tfreeze"] = "RefProp" # degR
        data_srcD["Ttriple"] = "RefProp" # degR
        data_srcD["Cp"]      = "thermo" # BTU/lbm/delF
        data_srcD["MolWt"]   = "RefProp" # g/gmole
        data_srcD["Hvap"]    = "RefProp" # BTU/lbm
        data_srcD["surf"]    = "RefProp" # lbf/in

        data_srcD["trL"]     = "RefProp"
        data_srcD["tL"]      = "RefProp"

        data_srcD["log10pL"]      = "RefProp"
        data_srcD["log10viscL"]   = "thermo"
        data_srcD["condL"]        = "thermo"
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
        RefProp calculations for F2  (Fluorine). 
        
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
        log10x = log10(1 + dp / (4074.8818151923874 + psat))  # Fit Standard Deviation = 2.0521622020578788e-07
        dsg_o_sgL.append(  0.0565279040938761*log10x + 0.018896978922127022*log10x**2 + 0.03378149312746902*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2508.028818646614 + psat))  # Fit Standard Deviation = 1.426078917747848e-06
        dsg_o_sgL.append(  0.039507805997920996*log10x + 0.03131932108726925*log10x**2 + 0.02026704618516518*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (808.7392335774572 + psat))  # Fit Standard Deviation = 1.0124870340883487e-05
        dsg_o_sgL.append(  0.015961735865797202*log10x + 0.01342251424354341*log10x**2 + 0.017030661463301233*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (357.74088307027955 + psat))  # Fit Standard Deviation = 3.249878267111269e-05
        dsg_o_sgL.append(  0.009760851504483166*log10x + 0.004186407362717191*log10x**2 + 0.015100116223993244*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (158.1278954111362 + psat))  # Fit Standard Deviation = 7.320817190185947e-05
        dsg_o_sgL.append(  0.00729124480965539*log10x + -0.0021727627968333493*log10x**2 + 0.013640819986155683*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5800.866819771327 + psat))  # Fit Standard Deviation = 5.220697117028062e-06
        dsg_o_sgL.append(  0.22529095736235033*log10x + -0.004449560891564454*log10x**2 + -0.04667262645527269*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4235.043394889023 + psat))  # Fit Standard Deviation = 8.03281977354538e-06
        dsg_o_sgL.append(  0.21728628893306*log10x + 0.005251523537582371*log10x**2 + -0.04186449948044654*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2903.8327297063124 + psat))  # Fit Standard Deviation = 1.692953619803671e-05
        dsg_o_sgL.append(  0.20635954029374265*log10x + 0.016726303592368985*log10x**2 + -0.035822790225732*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1779.3236758744283 + psat))  # Fit Standard Deviation = 3.871192872031938e-05
        dsg_o_sgL.append(  0.1917246079908458*log10x + 0.028170658859916282*log10x**2 + -0.0292500972609483*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (848.231065500521 + psat))  # Fit Standard Deviation = 8.530247563811843e-05
        dsg_o_sgL.append(  0.17226102937594362*log10x + 0.03825845615789056*log10x**2 + -0.02276351871524869*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (112.78561796474095 + psat))  # Fit Standard Deviation = 0.00017488377329919762
        dsg_o_sgL.append(  0.1465883709392945*log10x + 0.046118510674935595*log10x**2 + -0.01702641277899482*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.8421589652799907e-06 + psat))  # Fit Standard Deviation = 0.0012322697935482226
        dsg_o_sgL.append(  0.37792616550654434*log10x + -0.18978361574128644*log10x**2 + 0.06590092494306225*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5.01456935698613e-10 + psat))  # Fit Standard Deviation = 0.03401186694264974
        dsg_o_sgL.append(  2.225686420341324*log10x + -3.2719534724189114*log10x**2 + 1.5892402149170106*log10x**3  )

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

    
