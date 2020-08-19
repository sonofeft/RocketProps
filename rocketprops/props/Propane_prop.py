
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Propane
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Propane')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Propane"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 415.8648 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6958058153 # psia
        self.Pc      = 616.58427024 # psia
        self.Tc      = 665.802 # degR
        self.Zc      = 0.276527391503 # Z at critical pt
        self.omega   = 0.1521488883550095 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.58088416082 # SG
        self.visc    = 0.00197219172996 # poise
        self.cond    = 0.0746900326141 # BTU/hr/ft/delF
        self.Tnbp    = 415.8648 # degR
        self.Tfreeze = 153.954 # degR
        self.Ttriple = 153.954 # degR
        self.Cp      = 0.536816717207 # BTU/lbm/delF
        self.MolWt   = 44.09562 # g/gmole
        self.Hvap    = 183.093953736 # BTU/lbm
        self.surf    = 9.0396388009e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.23123090648571198, 0.27169243772330604, 0.3121539689609002, 0.3526155001984943, 0.3930770314360884, 0.4335385626736825, 0.47400009391127657, 0.5144616251488707, 0.5549231563864647, 0.5953846876240589, 0.635846218861653, 0.6763077500992472, 0.7167692813368413, 0.7572308125744353, 0.7976923438120295, 0.8381538750496235, 0.8786154062872177, 0.9190769375248118, 0.9595384687624058, 1.0]
        self.tL = [153.954, 180.89336842105263, 207.83273684210528, 234.7721052631579, 261.71147368421055, 288.65084210526317, 315.5902105263158, 342.52957894736846, 369.468947368421, 396.4083157894737, 423.3476842105263, 450.28705263157894, 477.22642105263157, 504.1657894736842, 531.1051578947369, 558.0445263157894, 584.9838947368421, 611.9232631578948, 638.8626315789473, 665.802]
        
        self.log10pL  = [-7.597986554461786, -5.373586445183324, -3.767195206544576, -2.562393871984301, -1.6308642226602796, -0.8930006039193253, -0.2967535165678111, 0.19338489403817513, 0.6024634895692386, 0.9486185945588201, 1.245251102093942, 1.5024260600639228, 1.727811168854374, 1.9273280407578304, 2.105615903329954, 2.2663714380503923, 2.4126115401354222, 2.5469073560892608, 2.6716541820305384, 2.789988828263198]
        self.log10viscL = [-0.9674210682951633, -1.4356836041197907, -1.748395686192659, -1.9723406688437266, -2.140872001343849, -2.274554292882243, -2.386096905261269, -2.483161227668683, -2.570344587508167, -2.650480854292912, -2.7254357032533587, -2.796574406351548, -2.8650455840657654, -2.931987728288788, -2.9987279270415295, -3.0670468047595256, -3.139687009740333, -3.2217252802603182, -3.326258110633149, -3.640378722829692]
        self.condL = [0.12021238081645925, 0.11737290557191643, 0.11367484517282721, 0.10935286858600701, 0.10458611799962873, 0.09951707040210314, 0.09426526836115791, 0.08893400413515729, 0.0836111521151499, 0.07838139674438616, 0.0732929190219696, 0.06838476309284873, 0.06369085180484606, 0.05923377992079389, 0.05502415761984296, 0.05105692396228332, 0.047304196073651716, 0.043702917489278716, 0.040192119582264395, 0.05704578069992043]
        self.cpL = [0.4579001173215112, 0.46150399252928703, 0.46618399989506926, 0.4714807315178626, 0.4774557877702252, 0.4842508212500957, 0.4920427560469284, 0.5012874021704394, 0.5124285151692837, 0.5256915675081597, 0.541470565154075, 0.5601138261988625, 0.582255641542714, 0.6088830390475157, 0.6419115964586036, 0.6851763622277052, 0.747666394217293, 0.856327240251729, 1.1456782875457994, 29.627422953797755]
        self.hvapL = [242.16344693739651, 235.63417991388022, 229.3604469787158, 223.29535304519334, 217.3928533893784, 211.60111135037067, 205.8522897404481, 200.0552240564306, 194.0986279410287, 187.85696183144023, 181.1913700470683, 173.9470042438498, 165.94585425100516, 156.97140952493118, 146.74072359331433, 134.8493197195775, 120.64391889736811, 102.85244482224348, 78.10771184705752, 0.0]
        self.surfL = [0.0002153289742806457, 0.00020191246429843878, 0.00018858988767149612, 0.00017537283388877566, 0.0001622740168139948, 0.0001493074724138256, 0.00013648880820251735, 0.00012383552299323524, 0.0001113674243479388, 9.910718527265687e-05, 8.708110533783623e-05, 7.5320182636373e-05, 6.386167882143163e-05, 5.2751508168702454e-05, 4.2048097605553144e-05, 3.18291097243737e-05, 2.220444405243921e-05, 1.3345689997870757e-05, 5.574274670012015e-06, 0.0]    
        self.SG_liqL = [0.7331211931638861, 0.7176400177780226, 0.7023890089262246, 0.6872552500641538, 0.6721279762844364, 0.6569028899693746, 0.6414859207811862, 0.6257905381136502, 0.6097276641257721, 0.5931928148461598, 0.5760539960219353, 0.5581417798945977, 0.5392371209987827, 0.5190465126486742, 0.4971517847900266, 0.47290917710257796, 0.4452198854069712, 0.4118816698540439, 0.3668820443975166, 0.2204783627297867]
        self.log10SG_vapL = [-10.97102573509308, -8.812617935664345, -7.266554465329765, -6.114669258908208, -5.23022432535968, -4.534578826748879, -3.976207612320839, -3.519816067813417, -3.140384210956637, -2.819709623710781, -2.544273468013013, -2.303844470429245, -2.090507747213453, -1.8979451173751591, -1.7208543465936181, -1.5543840236328055, -1.3933534456812808, -1.230506430547346, -1.050247806882113, -0.6566340248271633]
        
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
        RefProp calculations for Propane  (C3H8). 
        
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
        
        trL = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.25 ) # saturation pressure at Tr=0.25
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4489.526414515147 + psat))  # Fit Standard Deviation = 1.1806401919493343e-07
        dsg_o_sgL.append(  0.03210796425342723*log10x + 0.03134452413905674*log10x**2 + 0.018902297477788082*log10x**3  )

        psat = self.PvapAtTr( 0.3 ) # saturation pressure at Tr=0.3
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3504.277452680509 + psat))  # Fit Standard Deviation = 2.4064133961618757e-07
        dsg_o_sgL.append(  0.02973590709545385*log10x + 0.029151670491853094*log10x**2 + 0.018593916966230528*log10x**3  )

        psat = self.PvapAtTr( 0.35 ) # saturation pressure at Tr=0.35
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2683.3076884028014 + psat))  # Fit Standard Deviation = 4.93700276431377e-07
        dsg_o_sgL.append(  0.02712713781936896*log10x + 0.02666310335980988*log10x**2 + 0.018291885097002993*log10x**3  )

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2001.1521798136064 + psat))  # Fit Standard Deviation = 1.0196626174160892e-06
        dsg_o_sgL.append(  0.0242812593202276*log10x + 0.023802310566271762*log10x**2 + 0.017948225687984782*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1441.6111342605955 + psat))  # Fit Standard Deviation = 2.122156089229505e-06
        dsg_o_sgL.append(  0.021224653158298145*log10x + 0.020507640417292618*log10x**2 + 0.01753898695643472*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (993.9407244261331 + psat))  # Fit Standard Deviation = 4.445197388622298e-06
        dsg_o_sgL.append(  0.01803437480661249*log10x + 0.016738253775691016*log10x**2 + 0.017056041149095185*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (647.3609814543248 + psat))  # Fit Standard Deviation = 9.33227617053365e-06
        dsg_o_sgL.append(  0.014844975590916569*log10x + 0.012468364870132772*log10x**2 + 0.016489094979021165*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (387.7788234810322 + psat))  # Fit Standard Deviation = 1.9528872731392007e-05
        dsg_o_sgL.append(  0.011840641023693841*log10x + 0.007666949860147655*log10x**2 + 0.01580773090869891*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4202.75075698245 + psat))  # Fit Standard Deviation = 9.27667043579542e-07
        dsg_o_sgL.append(  0.1516212339069132*log10x + 0.04124082440942832*log10x**2 + -0.00555650964315269*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3088.647188274697 + psat))  # Fit Standard Deviation = 1.8432894988381076e-06
        dsg_o_sgL.append(  0.14893466159444227*log10x + 0.04128893331272782*log10x**2 + -0.006106773011907361*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2135.5673429147073 + psat))  # Fit Standard Deviation = 3.743016431249955e-06
        dsg_o_sgL.append(  0.14534988342217628*log10x + 0.041569436457007745*log10x**2 + -0.0066864134458166444*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1330.3150122020318 + psat))  # Fit Standard Deviation = 7.483500421914647e-06
        dsg_o_sgL.append(  0.14055066223442542*log10x + 0.0421745674105996*log10x**2 + -0.007334211191995056*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (658.76332513581 + psat))  # Fit Standard Deviation = 1.4652041731003838e-05
        dsg_o_sgL.append(  0.13359952834437366*log10x + 0.043286110516623816*log10x**2 + -0.007998778281660165*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (109.92562648462216 + psat))  # Fit Standard Deviation = 2.7865024782801508e-05
        dsg_o_sgL.append(  0.12219895215696282*log10x + 0.045113758236648455*log10x**2 + -0.008497796342494656*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.1203702169267732e-05 + psat))  # Fit Standard Deviation = 0.0007463590953336765
        dsg_o_sgL.append(  0.3120055440036059*log10x + -0.12072918330516035*log10x**2 + 0.04265955049228919*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1.3030239047213313e-07 + psat))  # Fit Standard Deviation = 0.03643415490891989
        dsg_o_sgL.append(  2.215472154327446*log10x + -3.06114759069659*log10x**2 + 1.3889281694361562*log10x**3  )

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

    
