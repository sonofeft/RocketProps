
template = '''
from math import log10
from rocketprops.rocket_prop import Propellant
from rocketprops.unit_conv_data import get_value
from rocketprops.InterpProp_scipy import InterpProp

class Prop( Propellant ):
    
    def __init__(self):
        
        Propellant.__init__(self, name='{prop_name}')

    def set_std_state(self):
        """Set properties and standard state of Propellant, {prop_name}"""
        
        self.dataSrc = '{dataSrc}'        
        self.T       = {T} # degR
        self.P       = {P} # psia
        self.Pvap    = {Pvap} # psia
        self.Pc      = {Pc} # psia
        self.Tc      = {Tc} # degR
        self.Zc      = {Zc} # Z at critical pt
        self.omega   = {omega} # omega  = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        self.SG      = {SG} # SG
        self.visc    = {visc} # poise
        self.cond    = {cond} # BTU/hr/ft/delF
        self.Tnbp    = {Tnbp} # degR
        self.Tfreeze = {Tfreeze} # degR
        self.Ttriple = {Ttriple} # degR
        self.Cp      = {Cp} # BTU/lbm/delF
        self.MolWt   = {MolWt} # g/gmole
        self.Hvap    = {Hvap} # BTU/lbm
        self.surf    = {surf} # lbf/in
    
        # ======= saturation curves =========
        self.NsatPts = {NsatPts}
        self.trL = {trL}
        self.tL = {tL}
        
        self.log10pL  = {log10pL}
        self.log10viscL = {log10viscL}
        self.condL = {condL}
        self.cpL = {cpL}
        self.hvapL = {hvapL}
        self.surfL = {surfL}    
        self.SG_liqL = {SG_liqL}
        self.log10SG_vapL = {log10SG_vapL}
        
        # ========== save dataSrc for each value ===========
        data_srcD = dict() # index=parameter, value=data source
        data_srcD["main"]    = "Scaled Reference Point"
        data_srcD["T"]       = "Scaled Reference Point" # degR
        data_srcD["P"]       = "Scaled Reference Point" # psia
        data_srcD["Pvap"]    = "Scaled Reference Point" # psia
        data_srcD["Pc"]      = "Scaled Reference Point" # psia
        data_srcD["Tc"]      = "Scaled Reference Point" # degR
        data_srcD["Zc"]      = "Scaled Reference Point" # Z at critical pt
        data_srcD["omega"]   = "Scaled Reference Point" # define: omega = -1.0 - log10( Pvap(0.7 * Tc) / Pc )
        data_srcD["SG"]      = "Scaled Reference Point" # SG
        data_srcD["visc"]    = "Scaled Reference Point" # poise
        data_srcD["cond"]    = "Scaled Reference Point" # BTU/hr/ft/delF
        data_srcD["Tnbp"]    = "Scaled Reference Point" # degR
        data_srcD["Tfreeze"] = "Scaled Reference Point" # degR
        data_srcD["Ttriple"] = "Scaled Reference Point" # degR
        data_srcD["Cp"]      = "Scaled Reference Point" # BTU/lbm/delF
        data_srcD["MolWt"]   = "Scaled Reference Point" # g/gmole
        data_srcD["Hvap"]    = "Scaled Reference Point" # BTU/lbm
        data_srcD["surf"]    = "Scaled Reference Point" # lbf/in

        data_srcD["trL"]     = "Scaled Reference Point"
        data_srcD["tL"]      = "Scaled Reference Point"

        data_srcD["log10pL"]      = "Scaled Reference Point"
        data_srcD["log10viscL"]   = "Scaled Reference Point"
        data_srcD["condL"]        = "Scaled Reference Point"
        data_srcD["cpL"]          = "Scaled Reference Point"
        data_srcD["hvapL"]        = "Scaled Reference Point"
        data_srcD["surfL"]        = "Scaled Reference Point"    
        data_srcD["SG_liqL"]      = "Scaled Reference Point"
        data_srcD["log10SG_vapL"] = "Scaled Reference Point"
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
    C = Prop()
    print('T = %g R = %g K'%( C.T, C.T/1.8 ))
    print('SurfaceTension = %g lbf/in'%C.surf, ' = ', get_value(C.surf, 'lbf/in', 'mN/m'), 'mN/m' )
    
    print()
    print('Tr_data_range =', C.Tr_data_range())
    print('  T_data_range=',C.T_data_range())
    print('  P_data_range=', C.P_data_range())
    
    C.plot_sat_props()

    
'''

