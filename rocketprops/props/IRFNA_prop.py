
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of IRFNA
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='IRFNA')

    def set_std_state(self):
        """Set properties and standard state of Propellant, IRFNA"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 2.135876033460818 # psia
        self.Pc      = 1286 # psia
        self.Tc      = 979.6700000000001 # degR
        self.Zc      = 0.21794013781106664 # Z at critical pt
        self.omega   = 0.3487947899218191 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 1.5762395859334883 # SG
        self.visc    = 0.013188519928579041 # poise
        self.cond    = 0.169211417143103 # BTU/hr/ft/delF
        self.Tnbp    = 607.6700000000001 # degR
        self.Tfreeze = 403.67 # degR
        self.Ttriple = 403.67 # degR
        self.Cp      = 0.41908324128930385 # BTU/lbm/delF
        self.MolWt   = 59.7 # g/gmole
        self.Hvap    = 246.99988957766823 # BTU/lbm
        self.surf    = 0.00026652226048496204 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.4120469137566731, 0.44144456806883947, 0.4708422223810058, 0.5002398766931722, 0.5296375310053385, 0.5590351853175048, 0.5884328396296712, 0.6178304939418375, 0.6472281482540039, 0.6766258025661702, 0.7060234568783366, 0.7354211111905029, 0.7648187655026693, 0.7942164198148356, 0.8236140741270019, 0.8530117284391683, 0.8824093827513346, 0.911807037063501, 0.9412046913756673, 0.9706023456878337, 1.0]
        self.tL = [403.67, 432.46999999999997, 461.27, 490.07, 518.87, 547.67, 576.47, 605.27, 634.07, 662.87, 691.6700000000001, 720.47, 749.2700000000001, 778.07, 806.87, 835.6700000000001, 864.47, 893.2700000000001, 922.07, 950.8700000000001, 979.6700000000001]
        
        self.log10pL  = [-1.9491772092665605, -1.2535308118611288, -0.6773364304193603, -0.19407995562105335, 0.21627731304522116, 0.5690301427852897, 0.875941554588764, 1.1461086094517872, 1.3865918319330495, 1.6028800221313153, 1.799238246546263, 1.9789714225659154, 2.1446257936772173, 2.2981437340065467, 2.4409824478559, 2.5742033056616447, 2.6985347851010695, 2.8144063148037675, 2.9219361653270592, 3.020798300313294, 3.109240968588203]
        self.log10viscL = [-1.0222700795115027, -1.2178047267868573, -1.482415155676226, -1.6755547504763648, -1.8374562332005946, -1.9653028974770101, -2.0639344982704477, -2.156629746786851, -2.2580830020486697, -2.3661784053688426, -2.453357503984333, -2.536114996145905, -2.614878006567161, -2.690014081984719, -2.761843062327194, -2.8306433477016326, -2.896660512413923, -2.9601105888931154, -3.02118609775103, -3.08005814146961, -3.136880329407713]
        self.condL = [0.1817447761833147, 0.18010908700543976, 0.17711652309604056, 0.17377365038811743, 0.17038449924015608, 0.1663730475841573, 0.16227004981294962, 0.15636053376157266, 0.1523425605094831, 0.14967419183431024, 0.14641274936931098, 0.14255993815353912, 0.1385246856136322, 0.13412549648578886, 0.12931834730262026, 0.12398143139457267, 0.11792176723154829, 0.11080023688575831, 0.10191825118962777, 0.10884264286101097, 0.12334861530089672]
        self.cpL = [0.410563890840458, 0.4120582194901983, 0.4139654645591056, 0.41606318006075754, 0.4184443327669981, 0.42051047805444747, 0.42305806122483297, 0.42593009814351046, 0.4302254335165214, 0.4361253313515996, 0.4440758747582739, 0.4543429761865254, 0.46780089373794614, 0.48147278803905647, 0.49759467790671724, 0.5192519776100322, 0.5507432312976915, 0.6021500614379416, 0.7038459317261772, 1.008291826681731, 18.396297021903806]
        self.hvapL = [271.44188648695274, 266.07322259490917, 260.5308830191426, 254.7990636735425, 248.85948595329964, 242.69082622595616, 236.26796578480764, 229.56098742479543, 222.53380616114154, 215.14225767014491, 207.33135826155322, 199.0312535158623, 190.15100212514153, 180.5685997099522, 170.11404889636913, 158.53850232573964, 145.45242065403306, 130.18392966374057, 111.38050246419716, 85.37890405509583, 0.0]
        self.surfL = [0.00035843762350144413, 0.0003366564073978576, 0.0003151285618114468, 0.0002938649784028657, 0.0002728776823326132, 0.0002521800281806303, 0.00023178694501641069, 0.00021171524733885717, 0.00019198403601798847, 0.0001726152249647681, 0.00015363424798738406, 0.00013507103171900273, 0.00011696137561726245, 9.934898195960706e-05, 8.228857984013421e-05, 6.585101732367089e-05, 5.013221773705823e-05, 3.5270694962739834e-05, 2.1487771001086603e-05, 9.210131197803118e-06, 0.0]    
        self.SG_liqL = [1.7017797924796512, 1.6736840291979689, 1.6449897492575076, 1.6156424956024393, 1.585579300793067, 1.554726725032792, 1.5229982761141796, 1.4902909566420537, 1.4564805503508342, 1.4214150381349768, 1.3849051542388495, 1.3467104109900332, 1.3065176332518864, 1.2639064625738292, 1.2182907161552312, 1.1688112677781157, 1.1141207276506349, 1.0518882387182729, 0.9773983180249233, 0.8777546382499488, 0.5368502137736204]
        self.log10SG_vapL = [-5.605058595847039, -4.9390766118502585, -4.390250009452238, -3.9320242809014503, -3.544214168775745, -3.2113083683298607, -2.9212870497550907, -2.6647705001480433, -2.434387197158735, -2.2242928718536845, -2.029797253232693, -1.8470690435262138, -1.6728971687134842, -1.504490407694783, -1.339299604158062, -1.1748477620323001, -1.0085556268200195, -0.8375635972762143, -0.6586233421646548, -0.4685547707378855, -0.2701468696183261]
        
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

    
