
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

# properties and standard state of Ethane
class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='Ethane')

    def set_std_state(self):
        """Set properties and standard state of Propellant, Ethane"""
        
        self.dataSrc = 'RefProp'        
        self.T       = 332.2242 # degR
        self.P       = 14.6959 # psia
        self.Pvap    = 14.6962718391 # psia
        self.Pc      = 706.65268194 # psia
        self.Tc      = 549.5796 # degR
        self.Zc      = 0.279968551854 # Z at critical pt
        self.omega   = 0.09951478010449266 # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = 0.543828684994 # SG
        self.visc    = 0.00166370428863 # poise
        self.cond    = 0.0965367883076 # BTU/hr/ft/delF
        self.Tnbp    = 332.2242 # degR
        self.Tfreeze = 162.6624 # degR
        self.Ttriple = 162.6624 # degR
        self.Cp      = 0.5826612769139092 # BTU/lbm/delF
        self.MolWt   = 30.06904 # g/gmole
        self.Hvap    = 210.546545621 # BTU/lbm
        self.surf    = 9.15614939259e-05 # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = 20
        self.trL = [0.2959760515128291, 0.33302994353846965, 0.3700838355641102, 0.40713772758975075, 0.44419161961539133, 0.4812455116410319, 0.5182994036666725, 0.5553532956923131, 0.5924071877179536, 0.6294610797435943, 0.6665149717692348, 0.7035688637948754, 0.740622755820516, 0.7776766478461565, 0.814730539871797, 0.8517844318974376, 0.8888383239230783, 0.9258922159487188, 0.9629461079743594, 1.0]
        self.tL = [162.6624, 183.02646315789474, 203.39052631578946, 223.7545894736842, 244.11865263157893, 264.4827157894737, 284.8467789473684, 305.21084210526317, 325.5749052631579, 345.93896842105266, 366.30303157894735, 386.6670947368421, 407.03115789473685, 427.3952210526316, 447.7592842105263, 468.12334736842104, 488.4874105263158, 508.85147368421053, 529.2155368421053, 549.5796]
        
        self.log10pL  = [-3.780812731962593, -2.64252182427513, -1.751276386905904, -1.0373125420663174, -0.4545957850410371, 0.02858589473173526, 0.43484439603175085, 0.7807464925282539, 1.078673162663614, 1.338012930792127, 1.565977372700845, 1.7681789609465792, 1.9490431452768753, 2.112103402896782, 2.2602170239327894, 2.395729895828948, 2.520612827809801, 2.6365925750015977, 2.7453417598026815, 2.849206009581995]
        self.log10viscL = [-1.8925218868323843, -2.084380740499991, -2.2350468261362013, -2.3574102268224943, -2.459686044596319, -2.5475051563882163, -2.624850696871857, -2.694595612870186, -2.7588524866946886, -2.8192138103188262, -2.876922559764939, -2.9329990750540427, -2.9883448310924146, -3.0438439969289774, -3.1004921701710924, -3.159606992955197, -3.22324668138216, -3.295351119156506, -3.3865383689467046, -3.66157138014803]
        self.condL = [0.14779051112192043, 0.1424677310343604, 0.1366861754466549, 0.13056544998159134, 0.124232429821267, 0.11779437679490334, 0.111334595706625, 0.10491514581055182, 0.09858095806838088, 0.09238962425627897, 0.08635115178648532, 0.0804636339275741, 0.0747394983250411, 0.06917931798334435, 0.06377381558734652, 0.058500558105127755, 0.053318955618612406, 0.04816780933429772, 0.04310087719435985, 0.06239969066527472]
        self.cpL = [0.5558829408939255, 0.5447729776185293, 0.5434795482606309, 0.5460940407095414, 0.5504363609427285, 0.5558591084015186, 0.5623420161092066, 0.5701204838160393, 0.5795460593063466, 0.5910544679028004, 0.605194166666527, 0.6227086918403848, 0.6446995840090536, 0.6729504119650717, 0.710622641436089, 0.7612190343824613, 0.8469243437630064, 1.0256826007777098, 1.5741785220880637, 41.66084540188294]
        self.hvapL = [255.87652986451843, 250.4331657563339, 245.20435242540498, 240.04450840872212, 234.87280782574578, 229.62842410569644, 224.24061287527624, 218.60753964633065, 212.60630686245707, 206.11666988194781, 199.0255793031078, 191.20961342845158, 182.51104710666715, 172.71544486301292, 161.52307589703162, 148.49226584520005, 132.90143107269535, 113.36480667478513, 86.29207566121292, 0.0]
        self.surfL = [0.00018082019806916084, 0.00016992874839266185, 0.00015905328343313225, 0.00014820686055231412, 0.00013740355185362142, 0.00012665861594752744, 0.00011598871405426533, 0.00010541218628954107, 9.494941145996856e-05, 8.462328571989427e-05, 7.445987550861224e-05, 6.448933518580844e-05, 5.4747244129065145e-05, 4.5276644216937084e-05, 3.613132669757283e-05, 2.7381549583116633e-05, 1.9125083791150868e-05, 1.1512225076787946e-05, 4.820672267051293e-06, 0.0]    
        self.SG_liqL = [0.6515305575928686, 0.6391061005944224, 0.6266826699205624, 0.6141739497742428, 0.601525732217622, 0.5886877656773712, 0.5756042595215314, 0.5622100626536362, 0.5484279223024336, 0.5341650466819601, 0.5193078997140985, 0.5037139157453215, 0.48719774380827136, 0.46950708338128594, 0.450277278228001, 0.428939645161394, 0.40452043730707715, 0.3750813326095813, 0.3353851937180192, 0.20618024569837898]
        self.log10SG_vapL = [-7.340020286976712, -6.252944196573508, -5.407450189524555, -4.73470097449129, -4.1892356142757246, -3.7396626040540335, -3.3634917978658443, -3.044135721205785, -2.7691431192108014, -2.529070193637874, -2.3166547277247402, -2.126182295997105, -1.9530129910183773, -1.7932236561768977, -1.6432957379898119, -1.499750694813456, -1.3585327327417085, -1.2135383385079526, -1.0509436798704646, -0.6857529471764796]
        
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
        data_srcD["Cp"]      = "CoolProp" # BTU/lbm/delF
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
        RefProp calculations for Ethane  (C2H6). 
        
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
        
        trL = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
        
        # build a list of (SG - SGsat)/SG vs Tr
        dsg_o_sgL = []
        
        # build interpolator for (SG - SGsat)/SG vs Tr at Ppsia

        psat = self.PvapAtTr( 0.3 ) # saturation pressure at Tr=0.3
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3640.730393562185 + psat))  # Fit Standard Deviation = 2.338719373192911e-07
        dsg_o_sgL.append(  0.03233242402285083*log10x + 0.03105309251929221*log10x**2 + 0.01940732579311245*log10x**3  )

        psat = self.PvapAtTr( 0.35 ) # saturation pressure at Tr=0.35
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2664.6118783005377 + psat))  # Fit Standard Deviation = 4.972506613746668e-07
        dsg_o_sgL.append(  0.028183492039283574*log10x + 0.027651388597404753*log10x**2 + 0.018866117493693955*log10x**3  )

        psat = self.PvapAtTr( 0.4 ) # saturation pressure at Tr=0.4
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1999.4696917908293 + psat))  # Fit Standard Deviation = 1.00850822811095e-06
        dsg_o_sgL.append(  0.02524887845910932*log10x + 0.024770721451089158*log10x**2 + 0.018550522259343668*log10x**3  )

        psat = self.PvapAtTr( 0.45 ) # saturation pressure at Tr=0.45
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (9302.184392870637 + psat))  # Fit Standard Deviation = 1.2374618622576555e-09
        dsg_o_sgL.append(  0.1405162282784313*log10x + 0.05677561546861795*log10x**2 + -0.006573234437047919*log10x**3  )

        psat = self.PvapAtTr( 0.5 ) # saturation pressure at Tr=0.5
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1030.1735997955268 + psat))  # Fit Standard Deviation = 4.192528196052104e-06
        dsg_o_sgL.append(  0.019106421198635815*log10x + 0.01786663354847461*log10x**2 + 0.017758610071341066*log10x**3  )

        psat = self.PvapAtTr( 0.55 ) # saturation pressure at Tr=0.55
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (683.1359397268751 + psat))  # Fit Standard Deviation = 8.649118646587409e-06
        dsg_o_sgL.append(  0.015866651522188028*log10x + 0.013606611452907407*log10x**2 + 0.017190383542933813*log10x**3  )

        psat = self.PvapAtTr( 0.6 ) # saturation pressure at Tr=0.6
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (414.07373187605646 + psat))  # Fit Standard Deviation = 1.7935159184691528e-05
        dsg_o_sgL.append(  0.012716241685388378*log10x + 0.008747189923077771*log10x**2 + 0.016468348440512814*log10x**3  )

        psat = self.PvapAtTr( 0.65 ) # saturation pressure at Tr=0.65
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (4290.420342533632 + psat))  # Fit Standard Deviation = 6.140859669964164e-07
        dsg_o_sgL.append(  0.1550384752171683*log10x + 0.04294567298682377*log10x**2 + -0.005085243259766905*log10x**3  )

        psat = self.PvapAtTr( 0.7 ) # saturation pressure at Tr=0.7
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (3160.148325387464 + psat))  # Fit Standard Deviation = 1.304080585859677e-06
        dsg_o_sgL.append(  0.1520509551557447*log10x + 0.042673119915774715*log10x**2 + -0.005738946829100536*log10x**3  )

        psat = self.PvapAtTr( 0.75 ) # saturation pressure at Tr=0.75
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (2193.292865845392 + psat))  # Fit Standard Deviation = 2.6377448489227672e-06
        dsg_o_sgL.append(  0.1486216518466331*log10x + 0.042613347313886996*log10x**2 + -0.006524667862620398*log10x**3  )

        psat = self.PvapAtTr( 0.8 ) # saturation pressure at Tr=0.8
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (1366.9743135274675 + psat))  # Fit Standard Deviation = 5.5236103708504305e-06
        dsg_o_sgL.append(  0.14403365197032625*log10x + 0.042945829272460594*log10x**2 + -0.007337012226269114*log10x**3  )

        psat = self.PvapAtTr( 0.85 ) # saturation pressure at Tr=0.85
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (664.4967158205939 + psat))  # Fit Standard Deviation = 1.2416441933112653e-05
        dsg_o_sgL.append(  0.1369130536367487*log10x + 0.043852434777548*log10x**2 + -0.00802591376605673*log10x**3  )

        psat = self.PvapAtTr( 0.9 ) # saturation pressure at Tr=0.9
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (80.45276890764484 + psat))  # Fit Standard Deviation = 2.641351263085312e-05
        dsg_o_sgL.append(  0.12486797431961583*log10x + 0.04551571888568812*log10x**2 + -0.00847374872206692*log10x**3  )

        psat = self.PvapAtTr( 0.95 ) # saturation pressure at Tr=0.95
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (9.67519130413478e-07 + psat))  # Fit Standard Deviation = 0.0008449224734538883
        dsg_o_sgL.append(  0.33889504570492773*log10x + -0.1513197501398535*log10x**2 + 0.05610201840850644*log10x**3  )

        psat = self.PvapAtTr( 1.0 ) # saturation pressure at Tr=1.0
        dp = max(0.0, Ppsia - psat)
        log10x = log10(1 + dp / (5.201356283849731e-09 + psat))  # Fit Standard Deviation = 0.03753927550797725
        dsg_o_sgL.append(  2.322413741479554*log10x + -3.3886979410513347*log10x**2 + 1.6206842930314775*log10x**3  )

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

    
