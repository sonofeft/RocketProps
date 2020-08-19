
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of A50
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='A50')

    def set_std_state(self):
        """Set properties and standard state of Propellant, A50"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 2.361098929901482 # psia
        self.Pc      = 1731 # psia
        self.Tc      = 1092.67 # degR
        self.Zc      = 0.32031589706927566 # Z at critical pt
        self.omega   = 0.16664587517590368 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.9035471601513377 # SG
        self.visc    = 0.009208681003236614 # poise
        self.cond    = 0.1661065246970707 # BTU/hr/ft/delF
        self.Tnbp    = 617.6700000000001 # degR
        self.Tfreeze = 481.67 # degR
        self.Ttriple = 481.67 # degR
        self.Cp      = 0.7282323251759043 # BTU/lbm/delF
        self.MolWt   = 41.802 # g/gmole
        self.Hvap    = 346.5000380753298 # BTU/lbm
        self.surf    = 0.00016987300288460853 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.44081927754948885, 0.4687783136720144, 0.49673734979454, 0.5246963859170655, 0.5526554220395911, 0.5806144581621167, 0.6085734942846421, 0.6365325304071677, 0.6644915665296933, 0.6924506026522188, 0.7204096387747445, 0.74836867489727, 0.7763277110197955, 0.8042867471423212, 0.8322457832648467, 0.8602048193873723, 0.8881638555098978, 0.9161228916324233, 0.9440819277549488, 0.9720409638774745, 1.0]
        self.tL = [481.67, 512.22, 542.7700000000001, 573.3199999999999, 603.87, 634.4200000000001, 664.9699999999999, 695.52, 726.07, 756.62, 787.1700000000002, 817.72, 848.27, 878.8200000000002, 909.3700000000001, 939.9200000000001, 970.4700000000001, 1001.0200000000001, 1031.57, 1062.1200000000001, 1092.67]
        
        self.log10pL  = [-0.13936053627984823, 0.2104741995458726, 0.5237113613567, 0.8055260869937526, 1.0601417974740044, 1.291055770640097, 1.5012027394702494, 1.69307562885486, 1.8688161332520403, 2.030283767284262, 2.179109390566876, 2.316737491508662, 2.4444604063075426, 2.5634469828167346, 2.6747679215460654, 2.7794202320557786, 2.878354350994216, 2.9725109205430322, 3.0628857599571435, 3.150693389705462, 3.238297067875394]
        self.log10viscL = [-1.8505514848582325, -1.9758965221402502, -2.092297232960033, -2.2009466911111657, -2.3028117044817367, -2.3986913491738258, -2.489248909825648, -2.5750452987447905, -2.656555467693018, -2.7341879232976045, -2.8082946166889124, -2.879182022525781, -2.9471183439954203, -3.012339265836891, -3.0750538426268728, -3.1354472690507675, -3.1936855637636556, -3.2499169710593594, -3.3042754403101045, -3.3568815577444107, -3.407844884659563]
        self.condL = [0.16689140260811203, 0.16689140260811203, 0.164772136083728, 0.16221555992280765, 0.15930790129527833, 0.15611764366474407, 0.15273299602810228, 0.1488924388539687, 0.14499406521331887, 0.14073103854768365, 0.13641114492295298, 0.13174502711744204, 0.12693248636795226, 0.12180740991041751, 0.11630096342398727, 0.11030400663574506, 0.10364484683414335, 0.09602589072243459, 0.0867995819859769, 0.0936587480872445, 0.10546414790597335]
        self.cpL = [0.7089840779528899, 0.7220694817767477, 0.7341809473901714, 0.7466147714133649, 0.758620167303049, 0.7700007220482723, 0.7810430121996752, 0.7933752419203103, 0.8065049458302264, 0.8203734768367642, 0.8351667661394867, 0.8511703003411789, 0.8688191254623021, 0.8887886612887123, 0.9121699146241768, 0.9408380977827613, 0.9783287030948075, 1.0323276987897585, 1.1241136576431514, 1.3516703964095127, 11.355473674888856]
        self.hvapL = [356.8516873228355, 350.0331517926422, 342.98859064386244, 335.69725203176864, 328.1351169484372, 320.27414291832645, 312.08126891728574, 303.51708304382225, 294.5340028192894, 285.07373244770594, 275.06361437165396, 264.4112288305934, 252.9960978409908, 240.65635350140008, 227.16608025440385, 212.19394895178223, 195.22015175372547, 175.34570362904103, 150.75456852331848, 116.50290510298234, 0.0]
        self.surfL = [0.000181200637087032, 0.00017451886317468318, 0.00016533247651142854, 0.00015614645546635785, 0.00014696082171866337, 0.00013777559926756138, 0.00012859081576425737, 0.00011940650230138387, 0.00011022269535030747, 0.00010103943679873503, 9.18567769441448e-05, 8.267477527868846e-05, 7.349350561147624e-05, 6.431305907420268e-05, 5.513355448683764e-05, 4.5955148884998734e-05, 3.677806529344205e-05, 2.7602637816209825e-05, 1.842943714316914e-05, 9.25964540259305e-06, 9.884052722230236e-08]    
        self.SG_liqL = [0.9261776483243327, 0.9112237449393337, 0.8959660402826182, 0.8803759497275117, 0.8644204004985917, 0.8480607941390989, 0.8312516415151575, 0.8139387352566474, 0.7960566536048348, 0.7775252721040483, 0.7582447574921487, 0.7380881554408519, 0.7168899989912246, 0.6944279906663193, 0.6703918424748478, 0.6443263151959874, 0.6155166300163627, 0.5827246921446813, 0.5434419297134679, 0.49079395805545484, 0.3086607999066754]
        self.log10SG_vapL = [-4.024640514697925, -3.6999988056471653, -3.4096440279319773, -3.148333188631153, -2.9117338502454007, -2.696217253277966, -2.49871041785381, -2.3165864999097057, -2.1475797710541578, -1.9897162359973593, -1.8412538006099173, -1.7006274837586959, -1.566395653091467, -1.4371826437115953, -1.3116109616507392, -1.1882112649254961, -1.0652868321741138, -0.9406805330770236, -0.8113085514609752, -0.6720044021486639, -0.5105185226566424]
        
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

    
