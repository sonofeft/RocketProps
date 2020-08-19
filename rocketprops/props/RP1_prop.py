
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of RP1
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='RP1')

    def set_std_state(self):
        """Set properties and standard state of Propellant, RP1"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.004279280146851448 # psia
        self.Pc      = 315 # psia
        self.Tc      = 1217.67 # degR
        self.Zc      = 0.26813849913567744 # Z at critical pt
        self.omega   = 0.51236299976203 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.8099539515237648 # SG
        self.visc    = 0.01668577972950885 # poise
        self.cond    = 0.07868785664751778 # BTU/hr/ft/delF
        self.Tnbp    = 881.6700000000001 # degR
        self.Tfreeze = 409.67 # degR
        self.Ttriple = 409.67 # degR
        self.Cp      = 0.4753793651963285 # BTU/lbm/delF
        self.MolWt   = 172 # g/gmole
        self.Hvap    = 125.00004441257069 # BTU/lbm
        self.surf    = 0.00016581323657279998 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.3364376226728095, 0.36961574153916904, 0.40279386040552856, 0.43597197927188813, 0.4691500981382476, 0.5023282170046072, 0.5355063358709666, 0.5686844547373262, 0.6018625736036858, 0.6350406924700452, 0.6682188113364047, 0.7013969302027643, 0.7345750490691239, 0.7677531679354834, 0.8009312868018429, 0.8341094056682024, 0.8672875245345619, 0.9004656434009215, 0.933643762267281, 0.9668218811336405, 1.0]
        self.tL = [409.67, 450.07, 490.46999999999997, 530.87, 571.27, 611.6700000000001, 652.0699999999999, 692.47, 732.8700000000001, 773.27, 813.67, 854.07, 894.4700000000001, 934.8700000000001, 975.2700000000001, 1015.6700000000001, 1056.0700000000002, 1096.4700000000003, 1136.8700000000001, 1177.2700000000002, 1217.67]
        
        self.log10pL  = [-3.8191587960516133, -3.3225368265305457, -2.8259148570094776, -2.3292928874884096, -1.8411018814022009, -1.2130584988978197, -0.7732849129812904, -0.27576950018994867, 0.1037811210695065, 0.4469100583703726, 0.7351337865638281, 0.9966276624556696, 1.2262628685253598, 1.4297176458424494, 1.6401736027487401, 1.827034135739729, 1.9887694448269433, 2.13263600543867, 2.2643919564795194, 2.3957434562722364, 2.513580856971416]
        self.log10viscL = [-1.1424228114761967, -1.3887489815649405, -1.6027228803159297, -1.7918717237386284, -1.9613545913972101, -2.1252206334492563, -2.2360531659177614, -2.3097420348120123, -2.3908522398115113, -2.4719624448110094, -2.553072649810508, -2.6299900518840094, -2.70338546051721, -2.774906709393103, -2.8497669328700734, -2.927997778759886, -3.0125278258408352, -3.111239991480777, -3.224616513922001, -3.3690178958022203, -3.5134192776824387]
        self.condL = [0.08349006882680204, 0.08160399625944413, 0.08001030258502714, 0.07858069110569041, 0.07730926708154136, 0.07621189502793109, 0.07521308853013495, 0.07424130678932928, 0.07329994377183013, 0.07233090246535252, 0.07134545590153588, 0.07040160749985067, 0.06949649115766095, 0.06863055908025066, 0.0678474895969638, 0.06699809112369924, 0.06597645159206679, 0.06469067259440817, 0.06282796578185583, 0.0600809758218047, 0.05187900051469137]
        self.cpL = [0.4164142447899971, 0.43861354551474946, 0.45876870289835275, 0.47686703168398253, 0.49683700405544373, 0.5184361430580887, 0.5402811803952589, 0.5620942069575713, 0.5833715985917645, 0.6059759424926876, 0.6293050887332605, 0.6501224471566046, 0.6707053329230177, 0.6924594037626055, 0.7174728670561324, 0.7445913408206658, 0.7744633192417497, 0.8115982907843312, 0.8674271516342682, 1.0007353089027595, 1.3547476245393404]
        self.hvapL = [133.10274665849755, 130.41318075623656, 127.63790498780898, 124.76916378647532, 121.79799153616997, 118.71393431647842, 115.50468426479684, 112.1555906808037, 108.64899325457056, 104.96329179989674, 101.07161368771445, 96.93984494086138, 92.52361163043017, 87.76343957114538, 82.57654811374348, 76.84190975757538, 70.37034588298076, 62.836140314169334, 53.58511034314562, 40.8514497525342, 0.0]
        self.surfL = [0.00020110265350770237, 0.00018888222778267163, 0.0001768039564521123, 0.0001648739503194531, 0.00015309895614208394, 0.00014148646655271548, 0.0001300448575568025, 0.00011878356298641223, 0.00010771329944993967, 9.684636182201449e-05, 8.619701982763213e-05, 7.578206390659496e-05, 6.562157946694393e-05, 5.5740085820776916e-05, 4.616828891335602e-05, 3.694593829355231e-05, 2.8126852071676205e-05, 1.978874393479827e-05, 1.2055787347521442e-05, 5.1673755811094605e-06, 0.0]    
        self.SG_liqL = [0.8544704463688385, 0.8395386131907443, 0.8242931939583938, 0.8087061504030922, 0.7927450749225593, 0.7763721854105912, 0.7595430039383082, 0.7422045892080958, 0.7242931245604547, 0.7057305504881043, 0.686419736777801, 0.666237341797623, 0.6450228507497502, 0.6225609705288174, 0.5985517220475092, 0.5725558490767494, 0.5438851780693585, 0.5113507146267136, 0.4725507736105898, 0.4209312142476964, 0.2477451042650749]
        self.log10SG_vapL = [-7.021975480474308, -6.566181556875634, -6.106855371439201, -5.644531217806308, -5.188026624820028, -4.589007681132568, -4.176008894085855, -3.701811252834113, -3.342627152531675, -3.0156948114810422, -2.7397703809969207, -2.4852719800853498, -2.2574950305062447, -2.050548631510393, -1.8226042896875132, -1.6079404584659955, -1.410035136127062, -1.2199316394145614, -1.0274590712935217, -0.7975982872858599, -0.5460868287594169]
        
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
        RefProp calculations for RP1  (RP-1). 
        
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
        log10x = log10(1 + dp / (2711.561322115711 + psat))  # Fit Standard Deviation = 4.763132787032469e-07
        dsg_o_sgL.append(  0.02724310615509977*log10x + 0.026740483033153184*log10x**2 + 0.018216812890644998*log10x**3  )

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2040.4902325716507 + psat))  # Fit Standard Deviation = 9.876899467924745e-07
        dsg_o_sgL.append(  0.02448686368383292*log10x + 0.024013865790125228*log10x**2 + 0.018025544938689964*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1493.3108199595347 + psat))  # Fit Standard Deviation = 2.030085736877373e-06
        dsg_o_sgL.append(  0.021576139097461217*log10x + 0.02089595217529488*log10x**2 + 0.017742951239720528*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1052.002751558613 + psat))  # Fit Standard Deviation = 4.16518926583506e-06
        dsg_o_sgL.append(  0.018539119978294515*log10x + 0.01732334486056667*log10x**2 + 0.017357093895877092*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (704.5101941350781 + psat))  # Fit Standard Deviation = 8.55342648584307e-06
        dsg_o_sgL.append(  0.01545924891133973*log10x + 0.013244685906653656*log10x**2 + 0.016852695354192166*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (440.42384110209616 + psat))  # Fit Standard Deviation = 1.7565956990829967e-05
        dsg_o_sgL.append(  0.012484179284333494*log10x + 0.008617201580771127*log10x**2 + 0.016207201328548866*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (248.24024707271462 + psat))  # Fit Standard Deviation = 3.5953200282572224e-05
        dsg_o_sgL.append(  0.009839984483811064*log10x + 0.0033756171888542127*log10x**2 + 0.015385963319585133*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (113.9807968641889 + psat))  # Fit Standard Deviation = 7.285264143428316e-05
        dsg_o_sgL.append(  0.007912860028858817*log10x + -0.0027460160763761008*log10x**2 + 0.014333100559937542*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2480.0946335890626 + psat))  # Fit Standard Deviation = 2.7488269257734393e-06
        dsg_o_sgL.append(  0.15149782766607758*log10x + 0.041430385932726105*log10x**2 + -0.007721122866799761*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1646.1257667871091 + psat))  # Fit Standard Deviation = 5.032507036728612e-06
        dsg_o_sgL.append(  0.14654215864813608*log10x + 0.04215689369860926*log10x**2 + -0.008196475263517985*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (958.8833015394819 + psat))  # Fit Standard Deviation = 9.042830900362289e-06
        dsg_o_sgL.append(  0.1394777433784282*log10x + 0.04332135672400373*log10x**2 + -0.008652045904215156*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (410.2119738004101 + psat))  # Fit Standard Deviation = 1.4622099515519596e-05
        dsg_o_sgL.append(  0.1286973801384083*log10x + 0.04506957932197583*log10x**2 + -0.009012163458480745*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (0.7015761950563051 + psat))  # Fit Standard Deviation = 1.1575269799302454e-05
        dsg_o_sgL.append(  0.11153616968974724*log10x + 0.046950279459703155*log10x**2 + -0.008957280109793223*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.93642660132482e-07 + psat))  # Fit Standard Deviation = 0.004117348166031686
        dsg_o_sgL.append(  0.579798365485937*log10x + -0.3952399797002273*log10x**2 + 0.12696172184192014*log10x**3  )

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

    
