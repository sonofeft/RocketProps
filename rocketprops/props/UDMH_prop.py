
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of UDMH
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='UDMH')

    def set_std_state(self):
        """Set properties and standard state of Propellant, UDMH"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 2.5749567850999577 # psia
        self.Pc      = 867 # psia
        self.Tc      = 941.6700000000001 # degR
        self.Zc      = 0.29851217871530905 # Z at critical pt
        self.omega   = 0.3499236187886665 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.7904440144318352 # SG
        self.visc    = 0.0055330849434126715 # poise
        self.cond    = 0.0918906797422783 # BTU/hr/ft/delF
        self.Tnbp    = 603.85 # degR
        self.Tfreeze = 388.73 # degR
        self.Ttriple = 388.73 # degR
        self.Cp      = 0.6651120126449406 # BTU/lbm/delF
        self.MolWt   = 60.09946 # g/gmole
        self.Hvap    = 250.54995212763518 # BTU/lbm
        self.surf    = 0.0001406549239868261 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.4128091581976701, 0.4421687002877866, 0.4715282423779031, 0.5008877844680196, 0.5302473265581361, 0.5596068686482526, 0.5889664107383691, 0.6183259528284856, 0.6476854949186021, 0.6770450370087187, 0.7064045790988351, 0.7357641211889516, 0.7651236632790681, 0.7944832053691846, 0.8238427474593011, 0.8532022895494176, 0.8825618316395341, 0.9119213737296505, 0.941280915819767, 0.9706404579098835, 1.0]
        self.tL = [388.73, 416.377, 444.02400000000006, 471.67100000000005, 499.3180000000001, 526.965, 554.6120000000001, 582.259, 609.9060000000001, 637.5530000000001, 665.2000000000002, 692.8470000000001, 720.4940000000001, 748.1410000000001, 775.7880000000001, 803.4350000000001, 831.0820000000001, 858.729, 886.3760000000001, 914.023, 941.6700000000001]
        
        self.log10pL  = [-2.0322822887443923, -1.3723693243810342, -0.8187480588073967, -0.34909152396327636, 0.053613890249281704, 0.4024814143706068, 0.7077142389393332, 0.9773136846969005, 1.217594731299083, 1.4335673713461905, 1.629222812865501, 1.8077510905556542, 1.971708484039811, 2.1231476881776468, 2.2637199656205884, 2.3947559258171043, 2.5173297146791933, 2.632309954545235, 2.7403993498057018, 2.8421621713166347, 2.9380190974762104]
        self.log10viscL = [-1.2526344512487293, -1.5659200080942153, -1.7986194181571824, -1.9838868134810053, -2.133891995833604, -2.2543453307794854, -2.3486771670679616, -2.4310401352148907, -2.5097647192694916, -2.58664967543945, -2.660074938576418, -2.7303385924767976, -2.797701811611523, -2.8623943580117777, -2.9246202397723096, -2.9845603507875147, -3.0423769950661086, -3.098215216933693, -3.152206172807487, -3.204468017370492, -3.255108173130664]
        self.condL = [0.11013502982148698, 0.10698577708738044, 0.10335845838910211, 0.09968781014699712, 0.09576007865198413, 0.09198422544277202, 0.08839727508104021, 0.08430237892234284, 0.08018234371974098, 0.07713285252920075, 0.07340030549168984, 0.06970896154765932, 0.06586241700161026, 0.0619331585027207, 0.05785679615482195, 0.053587574811767215, 0.04904823693008731, 0.04411265025960606, 0.03849170183944253, 0.04056789420306039, 0.04590814144475609]
        self.cpL = [0.596682416565721, 0.6103155460138874, 0.6241743876327678, 0.6384156848223458, 0.651245467475526, 0.6647605782293551, 0.6787767741950571, 0.6921808942554468, 0.7057171657329365, 0.7204759113106828, 0.7372229903603524, 0.755368507379479, 0.7756231456327168, 0.7988747781829404, 0.826638095579527, 0.8616786076988383, 0.909577916901148, 0.9834418828461458, 1.1227772651027683, 1.5259308047187978, 24.124474686887325]
        self.hvapL = [280.4029919470376, 274.85963655993044, 269.1368963538311, 263.21844576868864, 257.0854028853986, 250.71574001587535, 244.08350879920948, 237.15780351152554, 229.90134637257043, 222.2685125645629, 214.20249925645928, 205.63113970399294, 196.4604805594875, 186.5644740445938, 175.7674848608997, 163.81240601953147, 150.29675650109337, 134.52631462489472, 115.10349942322331, 88.24278170008648, 0.0]
        self.surfL = [0.00018891404585190917, 0.00017929093492706028, 0.00016967733303595796, 0.00016007376306388782, 0.00015048080338199616, 0.00014089910408160149, 0.00013132940756255593, 0.00012177254925933399, 0.0001122295079829853, 0.00010270140948461738, 9.3189592246569e-05, 8.369566514727349e-05, 7.422157189527021e-05, 6.476977918371853e-05, 5.5343407023631096e-05, 4.59466693081835e-05, 3.658545713849554e-05, 2.7268606384324793e-05, 1.8011276180111286e-05, 8.844408722859965e-06, 0.0]    
        self.SG_liqL = [0.861758079678825, 0.8482932839217563, 0.8344990221000811, 0.8203468430742434, 0.8058038724216394, 0.7908317952485838, 0.7753855190124295, 0.7594113846424005, 0.7428447252190753, 0.7256064571540607, 0.7075981923698685, 0.6886950076133296, 0.6687343421649681, 0.6474981622160516, 0.6246826517477513, 0.5998428663155424, 0.5722815204607544, 0.5407933064404191, 0.5029417191139957, 0.4520686510242297, 0.2767475209543379]
        self.log10SG_vapL = [-5.668878776377086, -5.03854793632041, -4.512262171083802, -4.067688454518944, -3.687704092426336, -3.359013807808756, -3.071189602477149, -2.8159849794898553, -2.5868298642625307, -2.3784477797764425, -2.1865586086191184, -2.00764295088866, -1.8387510172431065, -1.6773424457445258, -1.5211445602034095, -1.3680155397324938, -1.2157947522652914, -1.0621122046121503, -0.9041053944255878, -0.7379370970738628, -0.5579162607497765]
        
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

    
