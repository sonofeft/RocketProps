
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Ethanol
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Ethanol')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Ethanol"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 527.67 # degR
        self.P       = 0.859280396363 # psia
        self.Pvap    = 0.859280396363 # psia
        self.Pc      = 891.6917796 # psia
        self.Tc      = 925.02 # degR
        self.Zc      = 0.240228835494 # Z at critical pt
        self.omega   = 0.6441084599084665 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.789590003732 # SG
        self.visc    = 0.0119518602784 # poise
        self.cond    = 0.0961559585666 # BTU/hr/ft/delF
        self.Tnbp    = 632.502 # degR
        self.Tfreeze = 286.29 # degR
        self.Ttriple = 286.2 # degR
        self.Cp      = 0.600415436505 # BTU/lbm/delF
        self.MolWt   = 46.06844 # g/gmole
        self.Hvap    = 398.635729849 # BTU/lbm
        self.surf    = 0.000127987775828 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.48678947482216606, 0.5138005550946836, 0.5408116353672012, 0.5678227156397188, 0.5948337959122364, 0.6218448761847539, 0.6488559564572715, 0.6758670367297891, 0.7028781170023066, 0.7298891972748242, 0.7569002775473418, 0.7839113578198594, 0.810922438092377, 0.8379335183648946, 0.8649445986374121, 0.8919556789099296, 0.9189667591824472, 0.9459778394549648, 0.9729889197274824, 1.0]
        self.tL = [450.29, 475.2757894736842, 500.26157894736843, 525.2473684210527, 550.2331578947369, 575.218947368421, 600.2047368421053, 625.1905263157895, 650.1763157894736, 675.1621052631579, 700.1478947368421, 725.1336842105263, 750.1194736842106, 775.1052631578948, 800.0910526315789, 825.076842105263, 850.0626315789473, 875.0484210526315, 900.0342105263157, 925.02]
        
        self.log10pL  = [-1.401087700193988, -0.9178912291521807, -0.4869492655722022, -0.10110645598090445, 0.24554860377516544, 0.5580011408259609, 0.840514496522542, 1.0967651418700168, 1.3299363911974271, 1.5427880523004585, 1.7377120573406577, 1.9167794962974611, 2.0817817821861304, 2.2342673493215677, 2.375574880190049, 2.5068643614787898, 2.629148498444035, 2.7433304429199343, 2.8502670105147385, 2.9502147630508158]
        self.log10viscL = [-1.5047208970599042, -1.6514843160731318, -1.7863842644796888, -1.9109826784373027, -2.0265350296428832, -2.13410891565285, -2.2346612236214076, -2.329083530209076, -2.418224244263965, -2.5028956347308373, -2.5838736885715488, -2.6618986957182447, -2.737685193016377, -2.811953030260887, -2.885500959341479, -2.959373033124009, -3.0352649388161153, -3.11671731616373, -3.2139411701750054, -3.511522997375527]
        self.condL = [0.10295228112506566, 0.10051841789233044, 0.09834265855391512, 0.09634298647447403, 0.09445628008026882, 0.09263688764188444, 0.09085325597142939, 0.08908478458349274, 0.08731929670576852, 0.08555115772857026, 0.08377999118192843, 0.08200999585107609, 0.08025005668347653, 0.07851529824488465, 0.07683190811585959, 0.07525064083582626, 0.07388776185427595, 0.07306856738956324, 0.0737808612033847, 0.08752147808355934]
        self.cpL = [0.485978261932733, 0.5177757514284722, 0.5558391800678898, 0.596439584257601, 0.6372616227158867, 0.6769933037229069, 0.7149986568057448, 0.7510927572417216, 0.7843565390397178, 0.8176118653848417, 0.850394114413171, 0.8825753584244883, 0.916179948523236, 0.9502651245514139, 0.9974939075395666, 1.0555067630512822, 1.1423890113918245, 1.3015943579777618, 1.7351676611911142, 10.734672762393409]
        self.hvapL = [412.6185136579695, 408.88203148367, 404.45193054529915, 399.1929420685968, 393.026326175303, 385.8985676930854, 377.7617940221355, 368.56294996522763, 358.23815209517375, 346.7090483513246, 333.87875004407323, 319.6254096453961, 303.79131012634144, 286.1638202530751, 266.4402998925415, 244.1572726698435, 218.526916731523, 187.97448382751907, 148.28203223948844, 0.0]
        self.surfL = [0.0001601522525834626, 0.00014960526258306998, 0.00013920959027455187, 0.00012897177960645198, 0.00011889908178151342, 0.00010899958370285987, 9.928237055393625e-05, 8.975773490134745e-05, 8.043745061431876e-05, 7.133513940816689e-05, 6.246677373301538e-05, 5.385138754826308e-05, 4.5512117786489784e-05, 3.747780004568466e-05, 2.9785556575249417e-05, 2.2485321593004948e-05, 1.5648629032451656e-05, 9.388610213390157e-06, 3.920157484711962e-06, 0.0]    
        self.SG_liqL = [0.8250123608410154, 0.8135474853603035, 0.8021822275393701, 0.7907142628978503, 0.778964437074446, 0.7667757955909226, 0.7540083920378612, 0.7405327352868347, 0.7262226707371285, 0.7109474320551499, 0.6945618591420409, 0.6768929076730881, 0.6577190663007355, 0.6367361370605923, 0.6134953285939753, 0.587279200008803, 0.5568149059345211, 0.519452795969785, 0.46784871547051216, 0.2759963529269803]
        self.log10SG_vapL = [-5.217059566841733, -4.757101288293936, -4.347988145677314, -3.982551298536135, -3.6548099770463134, -3.3596627849725347, -3.092696254243818, -2.850062885764845, -2.6283969011932835, -2.424747726922287, -2.2365195866183973, -2.061410365364967, -1.8973439816635962, -1.7423872625214147, -1.5946318194970532, -1.4519926963007015, -1.3117864922168945, -1.1696014939911799, -1.014887294050611, -0.5590966567541754]
        
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
        RefProp calculations for Ethanol  (C2H6O). 
        
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
        log10x = log10(1 + dp / (6716.9084776444615 + psat))  # Fit Standard Deviation = 6.754122768654532e-08
        dsg_o_sgL.append(  0.05685195731369135*log10x + 0.050750720270686556*log10x**2 + 0.022718619050779532*log10x**3  )

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3337.8766756666514 + psat))  # Fit Standard Deviation = 2.7605661701663134e-07
        dsg_o_sgL.append(  0.0336388914607049*log10x + 0.032437639185754166*log10x**2 + 0.019440445350163257*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2174.803798135084 + psat))  # Fit Standard Deviation = 7.874965453614401e-07
        dsg_o_sgL.append(  0.02592002322579428*log10x + 0.025335974155103597*log10x**2 + 0.017796940591427977*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1520.6162373238344 + psat))  # Fit Standard Deviation = 1.7363504697431384e-06
        dsg_o_sgL.append(  0.021364448690808155*log10x + 0.02070280082754*log10x**2 + 0.01700110816084074*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1088.4955499867824 + psat))  # Fit Standard Deviation = 3.5469367564177814e-06
        dsg_o_sgL.append(  0.018138567625080027*log10x + 0.017067014190050755*log10x**2 + 0.016529659517177137*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (759.0144976029792 + psat))  # Fit Standard Deviation = 7.033779098241361e-06
        dsg_o_sgL.append(  0.015317724535069126*log10x + 0.013439803889556732*log10x**2 + 0.01616216263390056*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (495.3561207579135 + psat))  # Fit Standard Deviation = 1.40799175203111e-05
        dsg_o_sgL.append(  0.012659513677177202*log10x + 0.009406476615758396*log10x**2 + 0.015768432289839956*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (281.96816482020256 + psat))  # Fit Standard Deviation = 2.8933669074538373e-05
        dsg_o_sgL.append(  0.010177039546444847*log10x + 0.004660155161066048*log10x**2 + 0.0152472451495923*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4038.2634629559325 + psat))  # Fit Standard Deviation = 3.237127033069103e-07
        dsg_o_sgL.append(  0.16225494232540924*log10x + 0.03815355436212424*log10x**2 + -0.009841182106666643*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2841.6891496878966 + psat))  # Fit Standard Deviation = 7.929121454707049e-07
        dsg_o_sgL.append(  0.16221234599011614*log10x + 0.03905799399215637*log10x**2 + -0.01084265816194678*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1706.3152631460016 + psat))  # Fit Standard Deviation = 2.4344710361886877e-06
        dsg_o_sgL.append(  0.1587461070574572*log10x + 0.040876988199883314*log10x**2 + -0.011408627923251225*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (661.3283555015076 + psat))  # Fit Standard Deviation = 8.462028160039289e-06
        dsg_o_sgL.append(  0.1490240844714985*log10x + 0.043712185008529025*log10x**2 + -0.011367120217619441*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.711228203578035e-06 + psat))  # Fit Standard Deviation = 0.00012990817434083986
        dsg_o_sgL.append(  0.2131462428955479*log10x + -0.014290539004323*log10x**2 + 0.006480702467154469*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2.95999575302026e-08 + psat))  # Fit Standard Deviation = 0.04220889947135327
        dsg_o_sgL.append(  2.6659848974693507*log10x + -4.330179836514001*log10x**2 + 2.2786363053116867*log10x**3  )

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

    
