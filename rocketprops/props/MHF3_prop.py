
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of MHF3
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='MHF3')

    def set_std_state(self):
        """Set properties and standard state of Propellant, MHF3"""
        
        self.dataSrc = 'RocketProps'        
        self.T       = 527.67 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 0.7493486372133038 # psia
        self.Pc      = 1373 # psia
        self.Tc      = 1076.67 # degR
        self.Zc      = 0.27370789973182236 # Z at critical pt
        self.omega   = 0.2522409042478171 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.8948129886444842 # SG
        self.visc    = 0.00941388813416724 # poise
        self.cond    = 0.16074004753960566 # BTU/hr/ft/delF
        self.Tnbp    = 653.07 # degR
        self.Tfreeze = 394.67 # degR
        self.Ttriple = 394.67 # degR
        self.Cp      = 0.7176629642526471 # BTU/lbm/delF
        self.MolWt   = 43.412 # g/gmole
        self.Hvap    = 370.00018121582707 # BTU/lbm
        self.surf    = 0.00020386476428192377 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 21
        self.trL = [0.36656542859000435, 0.3982371571605041, 0.42990888573100394, 0.4615806143015037, 0.4932523428720035, 0.5249240714425032, 0.556595800013003, 0.5882675285835028, 0.6199392571540026, 0.6516109857245024, 0.6832827142950022, 0.7149544428655019, 0.7466261714360017, 0.7782979000065016, 0.8099696285770013, 0.8416413571475011, 0.8733130857180009, 0.9049848142885006, 0.9366565428590004, 0.9683282714295003, 1.0]
        self.tL = [394.67, 428.77, 462.87000000000006, 496.97, 531.07, 565.17, 599.27, 633.37, 667.47, 701.57, 735.6700000000001, 769.77, 803.87, 837.9700000000001, 872.07, 906.1700000000001, 940.2700000000001, 974.37, 1008.47, 1042.5700000000002, 1076.67]
        
        self.log10pL  = [-2.3536302384781065, -1.6585005082248108, -1.0597964688187924, -0.5390283494544632, -0.08234509031776199, 0.32085746189117065, 0.6788528883214686, 0.998204168790244, 1.2841931598422436, 1.5411242348354752, 1.7725426918070812, 1.9813940288612057, 2.170141140238441, 2.340850607731237, 2.49525516553194, 2.6347960905864887, 2.760645552168551, 2.873702313609776, 2.9745355776238855, 3.0631709869746855, 3.137670537236755]
        self.log10viscL = [-0.5566843404790347, -1.2915949634370973, -1.6538301892025917, -1.8718474180777849, -2.041492720200839, -2.1784114884962866, -2.2962061668646667, -2.3974218663987785, -2.491765232953522, -2.5846007789536354, -2.6751296508328646, -2.760595416760874, -2.841807652187691, -2.9191693423699467, -2.99302965602023, -3.0636913287159326, -3.1314204437344024, -3.196450304470829, -3.2589881925752806, -3.3192178133578407, -3.3773036621600885]
        self.condL = [0.17528459370877955, 0.17194953012081146, 0.16850038479042675, 0.16461490190458106, 0.16028982829138788, 0.15552505617896736, 0.14912476778416062, 0.14407278608183519, 0.13854470465277569, 0.13205030344699653, 0.12548830092926744, 0.118818708774929, 0.11201172556534375, 0.10503076218415859, 0.09782477393924792, 0.09031895914913379, 0.08239626661110779, 0.07385503545608221, 0.06427698549523214, 0.06520506387461866, 0.07466492338290213]
        self.cpL = [0.6932399135238326, 0.697032018563982, 0.7040702538961863, 0.7111805126795013, 0.7184403606767857, 0.727138037798523, 0.7388038854812384, 0.7542818143596177, 0.7684247082753282, 0.7837535278887428, 0.8004572457290187, 0.8188670337821706, 0.8395288626937414, 0.863341893635176, 0.8918373408247865, 0.9277915782643477, 0.9767526951963058, 1.0515962942662314, 1.1906566064893118, 1.5841700765290057, 24.853651103540983]
        self.hvapL = [401.94652820523237, 394.14879100718, 386.09533745902155, 377.762781042564, 369.1240620998886, 360.14759904135514, 350.7961719520985, 341.0254283683915, 330.78184323530604, 319.99986943053216, 308.59785098790576, 296.47197669890005, 283.4869965935696, 269.46131184269984, 254.14165059545036, 237.1568673951032, 217.92524765813326, 195.44191439843348, 167.6799689715828, 129.13365933468006, 0.0]
        self.surfL = [0.00024399760691236385, 0.00023505435132472458, 0.0002243815174316999, 0.00021362500565832952, 0.0002027791842237302, 0.00019183764804854016, 0.00018079306728265102, 0.0001696370132322921, 0.00015835959765360082, 0.00014694924981470807, 0.00013539198284220427, 0.00012367097854209527, 0.0001117650983063049, 9.964781707232982e-05, 8.728386167308722e-05, 7.462573300615587e-05, 6.160402775776805e-05, 4.811194854558135e-05, 3.395870389385227e-05, 1.8727002496563563e-05, 2.041903151468603e-08]    
        self.SG_liqL = [0.9594020982020899, 0.9433469619887201, 0.9269635551414349, 0.9102214943646774, 0.893085640099638, 0.8755149991004092, 0.8574612811188177, 0.8388669671484125, 0.8196626719040259, 0.7997634593479678, 0.7790635571718194, 0.7574285341502258, 0.7346832833218557, 0.7105927081221362, 0.6848288856473294, 0.656911076147374, 0.6260851195404782, 0.5910460258199831, 0.5491529338601719, 0.4931810174796308, 0.3019710076154732]
        self.log10SG_vapL = [-6.138130847629917, -5.478862315602451, -4.913090199355217, -4.422551435938386, -3.9934438865407027, -3.615033723623284, -3.2787469649473895, -2.977570738922501, -2.705656701456016, -2.4580557974490853, -2.2305365722489645, -2.019455845064008, -1.8216636424893284, -1.6344352751522389, -1.4554342230310722, -1.282723985889619, -1.1148737359552856, -0.9512614331614736, -0.792823798998496, -0.6439542414824684, -0.5200347518674954]
        
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

    
