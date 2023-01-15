
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

class Prop( Propellant ):
    
    def __init__(self, valueD=None):
        """Use an input dictionary to initialize Propellant object

        Args:
            valueD (dict, optional): holds all required values for "set_std_state" call. Defaults to None.
        """
        self.valueD = valueD
        Propellant.__init__(self, name=valueD['prop_name'])

    def set_std_state(self):
        """Set properties and standard state of Propellant"""
        
        self.dataSrc = self.valueD['dataSrc']
        self.T       = self.valueD['T'] # degR
        self.P       = self.valueD['P'] # psia
        self.Pvap    = self.valueD['Pvap'] # psia
        self.Pc      = self.valueD['Pc'] # psia
        self.Tc      = self.valueD['Tc'] # degR
        self.Zc      = self.valueD['Zc'] # Z at critical pt
        self.omega   = self.valueD['omega'] # omega  = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = self.valueD['SG'] # SG
        self.visc    = self.valueD['visc'] # poise
        self.cond    = self.valueD['cond'] # BTU/hr/ft/delF
        self.Tnbp    = self.valueD['Tnbp'] # degR
        self.Tfreeze = self.valueD['Tfreeze'] # degR
        self.Ttriple = self.valueD['Ttriple'] # degR
        self.Cp      = self.valueD['Cp'] # BTU/lbm/delF
        self.MolWt   = self.valueD['MolWt'] # g/gmole
        self.Hvap    = self.valueD['Hvap'] # BTU/lbm
        self.surf    = self.valueD['surf'] # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = self.valueD['NsatPts']
        self.trL = self.valueD['trL']
        self.tL = self.valueD['tL']
        
        self.log10pL  = self.valueD['log10pL']
        self.log10viscL = self.valueD['log10viscL']
        self.condL = self.valueD['condL']
        self.cpL = self.valueD['cpL']
        self.hvapL = self.valueD['hvapL']
        self.surfL = self.valueD['surfL']    
        self.SG_liqL = self.valueD['SG_liqL']
        self.log10SG_vapL = self.valueD['log10SG_vapL']
        
        # ========== save dataSrc for each value ===========
        data_srcD = dict() # index=parameter, value=data source
        data_srcD["main"]    = self.valueD['dataSrc']
        data_srcD["T"]       = self.valueD['dataSrc'] # degR
        data_srcD["P"]       = self.valueD['dataSrc'] # psia
        data_srcD["Pvap"]    = self.valueD['dataSrc'] # psia
        data_srcD["Pc"]      = self.valueD['dataSrc'] # psia
        data_srcD["Tc"]      = self.valueD['dataSrc'] # degR
        data_srcD["Zc"]      = self.valueD['dataSrc'] # Z at critical pt
        data_srcD["omega"]   = self.valueD['dataSrc'] # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        data_srcD["SG"]      = self.valueD['dataSrc'] # SG
        data_srcD["visc"]    = self.valueD['dataSrc'] # poise
        data_srcD["cond"]    = self.valueD['dataSrc'] # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = self.valueD['dataSrc'] # degR
        data_srcD["Tfreeze"] = self.valueD['dataSrc'] # degR
        data_srcD["Ttriple"] = self.valueD['dataSrc'] # degR
        data_srcD["Cp"]      = self.valueD['dataSrc'] # BTU/lbm/delF
        data_srcD["MolWt"]   = self.valueD['dataSrc'] # g/gmole
        data_srcD["Hvap"]    = self.valueD['dataSrc'] # BTU/lbm
        data_srcD["surf"]    = self.valueD['dataSrc'] # lbf/in

        data_srcD["trL"]     = self.valueD['dataSrc']
        data_srcD["tL"]      = self.valueD['dataSrc']

        data_srcD["log10pL"]      = self.valueD['dataSrc']
        data_srcD["log10viscL"]   = self.valueD['dataSrc']
        data_srcD["condL"]        = self.valueD['dataSrc']
        data_srcD["cpL"]          = self.valueD['dataSrc']
        data_srcD["hvapL"]        = self.valueD['dataSrc']
        data_srcD["surfL"]        = self.valueD['dataSrc']    
        data_srcD["SG_liqL"]      = self.valueD['dataSrc']
        data_srcD["log10SG_vapL"] = self.valueD['dataSrc']
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
    
        # calculate omega from definition (make self-consistent with Pvap.)
        self.omega = -1.0 - log10( self.PvapAtTr(0.7) / self.Pc )
    
if __name__ == '__main__':
    from rocketprops.unit_conv_data import get_value
    from rocketprops.mixture_prop import build_mixture
    from rocketprops.plot_multi_props import make_plots

    tmpD = build_mixture( prop_name='M20' )

    C = Prop( valueD=tmpD )
    print('T = %g R = %g K'%( C.T, C.T/1.8 ))
    print('SurfaceTension = %g lbf/in'%C.surf, ' = ', get_value(C.surf, 'lbf/in', 'mN/m'), 'mN/m' )
    
    print()
    print('Tr_data_range =', C.Tr_data_range())
    print('  T_data_range=',C.T_data_range())
    print('  P_data_range=', C.P_data_range())
    
    # C.plot_sat_props()
    make_plots( prop_nameL=[ 'MMH', 'N2H4'], prop_objL=[C], abs_T=1, ref_scaled=False)

