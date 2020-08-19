
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of MON10
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MON10')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MON10"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.7 # degR
        self.P       = 24.273196754531593 # psia
        self.Pvap    = 24.273196754531593 # psia
        self.Pc      = 1303.3289113335716 # psia
        self.Tc      = 755.8773644841885 # degR
        self.Zc      = 0.4184962226439506 # Z at critical pt
        self.omega   = 0.7140807387408901 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.4184815270595454 # SG
        self.visc    = 0.003796518763223495 # poise
        self.cond    = 0.10246119321643679 # BTU/hr/ft/delF
        self.Tnbp    = 509.07000000000016 # degR
        self.Tfreeze = 450.00000000000006 # degR
        self.Ttriple = 450.00000000000006 # degR
        self.Cp      = 0.46374207490334696 # BTU/lbm/delF
        self.MolWt   = 87.35282322083394 # g/gmole
        self.Hvap    = 157.43805102336165 # BTU/lbm
        self.surf    = 0.00019914871142760719 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.5953346682197324, 0.6155679348087457, 0.6358012013977591, 0.6560344679867725, 0.6762677345757859, 0.6965010011647993, 0.7167342677538127, 0.736967534342826, 0.7572008009318394, 0.7774340675208529, 0.7976673341098661, 0.8179006006988796, 0.838133867287893, 0.8583671338769063, 0.8786004004659197, 0.8988336670549331, 0.9190669336439465, 0.9393002002329598, 0.9595334668219733, 0.9797667334109866, 1.0]
        self.tL = [450.0000000000001, 465.2938682242095, 480.5877364484189, 495.8816046726283, 511.17547289683785, 526.4693411210473, 541.7632093452567, 557.0570775694661, 572.3509457936755, 587.644814017885, 602.9386822420943, 618.2325504663038, 633.5264186905132, 648.8202869147226, 664.114155138932, 679.4080233631414, 694.7018915873509, 709.9957598115602, 725.2896280357697, 740.5834962599791, 755.8773644841885]
        
        self.log10pL  = [0.34140450941574196, 0.5777917601795362, 0.7973739045626129, 1.0018529687017614, 1.1927145314778071, 1.3712598937865432, 1.538632800557757, 1.695841762291005, 1.843778798918352, 1.9832352571495495, 2.1149152197092924, 2.2394469211678527, 2.35739250288937, 2.4692563728430645, 2.5754923786790838, 2.6765099464240287, 2.772679265381085, 2.8643354615935803, 2.9517812938310626, 3.0352860223669142, 3.115054029182583]
        self.log10viscL = [-2.168420592307172, -2.221236602860439, -2.272396822473324, -2.32200202205986, -2.370698152509533, -2.416951219610978, -2.461892140948615, -2.5058523947389038, -2.549176308290579, -2.592226146071913, -2.63539577427544, -2.6791207471745553, -2.7239138841667714, -2.770397138822858, -2.8193836163458594, -2.871992304589238, -2.924600992832617, -2.977209681075995, -3.029818369319374, -3.0824270575627524, -3.135035745806131]
        self.condL = [0.11021676499264027, 0.10869021811041821, 0.10716367122819614, 0.10563712434597411, 0.10411057746375206, 0.10258403058152998, 0.10105748369930793, 0.09953093681708589, 0.09800438993486384, 0.09647784305264177, 0.09495129617041972, 0.09342474928819768, 0.09189820240597563, 0.09037165552375358, 0.08884510864153151, 0.08731856175930945, 0.0857920148770874, 0.08426546799486535, 0.0827389211126433, 0.08121237423042124, 0.07968582734819919]
        self.cpL = [0.4553021457892832, 0.45600412493922704, 0.4571673815921648, 0.458793650078016, 0.4608977125667173, 0.46350958259835173, 0.46667794465506734, 0.47047541838989293, 0.47500659240517895, 0.480420435085175, 0.4869299097822466, 0.49484398006423386, 0.5046220164841343, 0.5169711807138635, 0.5330324860670456, 0.5547675780991798, 0.5858594714570411, 0.6341814467214075, 0.7205803590110105, 0.9315958456427831, 6.167825518035357]
        self.hvapL = [177.26806775396327, 173.62252387395324, 169.86222057241423, 165.9768222343589, 161.95438540897874, 157.78098989366381, 153.4402541695377, 148.9126877807929, 144.17480851357908, 139.1979113387536, 133.94630596063553, 128.3747143261841, 122.42428330331994, 116.01619575932007, 109.04084780154513, 101.33816323999224, 92.65823500256842, 82.57143824756422, 70.21659240327581, 53.27593807230212, 0.0]
        self.surfL = [0.0002849280238659792, 0.0002676137731989653, 0.0002505009309668683, 0.00023359815513175283, 0.00021691500469354786, 0.00020046209542979077, 0.0001842512947059314, 0.00016829596864659086, 0.00015261130085078824, 0.0001372147110505396, 0.00012212641700266373, 0.00010737020788522037, 9.297454128204495e-05, 7.897415685977396e-05, 6.541255968485913e-05, 5.234606806146934e-05, 3.9850933036278725e-05, 2.8037261596431518e-05, 1.7080986278215364e-05, 7.321286354098012e-06, 0.0]    
        self.SG_liqL = [1.5139392814018182, 1.4962340651184913, 1.478035659417441, 1.4593091863889884, 1.4400156758531715, 1.420111377007949, 1.3995469159117218, 1.3782662548108824, 1.3562053937848946, 1.3332907329814574, 1.3094369814337838, 1.2845444505920798, 1.258495498193154, 1.2311497755550238, 1.2023377519010074, 1.1718516940850123, 1.1394327769612982, 1.1047521063439802, 1.0673817723298589, 1.0267487676911589, 0.9820576626361933]
        self.log10SG_vapL = [-3.192917482074309, -2.9692941869601985, -2.761376971969198, -2.5673501317061476, -2.3856001244708946, -2.2146856222277798, -2.0533126113738254, -1.9003132641063893, -1.7546275695502052, -1.6152869206778437, -1.4813989985817255, -1.3521333799561042, -1.2267073148524281, -1.1043710736597814, -0.9843921309894463, -0.8660372150837791, -0.7485508717936872, -0.6311286722187975, -0.5128828484995491, -0.3928008690213321, -0.2697570466376868]
        
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

    
