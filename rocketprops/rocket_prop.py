#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
RocketProps models liquid rocket propellants that are injected into 
liquid rocket chambers.

RocketProps calculates the various propellant properties required
to analyze a liquid propellant thrust chamber. 
This includes density, viscosity, vapor pressure,
heat of vaporization, surface tension, heat capacity and thermal conductivity. 
Other properties such as critical temperature and pressure, normal boiling point, 
molecular weight and freezing temperature are available.


RocketProps
Copyright (C) 2020  Applied Python

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

-----------------------

"""
import os
here = os.path.abspath(os.path.dirname(__file__))


# for multi-file projects see LICENSE file for authorship info
# for single file projects, insert following information
__author__ = 'Charlie Taylor'
__copyright__ = 'Copyright (c) 2020 Charlie Taylor'
__license__ = 'GPL-3'
exec( open(os.path.join( here,'_version.py' )).read() )  # creates local __version__ variable
__email__ = "cet@appliedpython.com"
__status__ = "4 - Beta" # "3 - Alpha", "4 - Beta", "5 - Production/Stable"

#
# import statements here. (built-in first, then 3rd party, then yours)
#
from math import exp, log, log10
import importlib
from rocketprops.unit_conv_data import get_value
from rocketprops.prop_names import prop_names
# from rocketprops.prop_from_dict import get_prop_from_dict
from rocketprops.mixing_functions import isMMH_N2H4_Blend, isMON_Ox, isFLOX_Ox, isN2H4_UDMH_Blend
from rocketprops.InterpProp_scipy import InterpProp

from scipy import optimize
from rocketprops.mixing_functions import Li_Tcm, mixing_simple, DIPPR9H_cond, Filippov_cond, \
                                         Winterfeld_Scriven_Davis_surf, mixing_logarithmic
from rocketprops.mixing_functions import Mnn_Freeze_terp, MON_Freeze_terp, Axx_Freeze_terp


TREF_K = get_value( 20.0, 'degC', 'degK')


def get_prop( name, suppress_warning=False ):
    """
    Return a Propellant object for the named propellant.

    :param name: name of propellant (for example "N2O4" or "LOX")
    :param suppress_warning: if True, then do not print warnings.
    :type name: string
    :type suppress_warning: boolean
    :return: Propellant object for named propellant
    :rtype: Propellant
    """
    if isMMH_N2H4_Blend(name) or isMON_Ox(name) or isFLOX_Ox(name) or isN2H4_UDMH_Blend(name):
        # print( 'building Blend', name)
        if name not in ['A50', 'MHF3', 'MON10', 'MON25', 'MON30']:
            return build_mixture( name )

    pname = prop_names.get_primary_name( name )
    if pname is None:

        if not suppress_warning:
            print('WARNING... propellant "%s" is not recognized.'%name)
        return None
    
    filename = pname + '_prop'
    
    try:
        prop_obj = importlib.import_module( 'rocketprops.props.%s'%filename )
        return prop_obj.Prop() # create instance and return it
    except:
        if not suppress_warning:
            print('WARNING... propellant "%s" import failed.'%name)
        return None
    


class Propellant(object):
    """
    RocketProps models liquid rocket propellants that are injected into liquid rocket chambers.
        
    :param name : name of propellant
    :type name : str
    :return: Propellant object
    :rtype: Propellant
    """

    def __init__(self, name='MMH'):
        """
        Standard Condition for a liquid propellant is defined here as 
        saturated liquid at Room Temperature (RT=20 C).
        
        If the propellant is not liquid at RT, then Standard Condition
        is Normal Boiling Point (NBP), i.e. saturated liquid at 1 atm pressure.
        
        NOTE: Propellant is designed as a Base Class... needs to be overriden
        by a specific propellant class.
        """
        
        self.name = name
        self.pname = prop_names.get_primary_name( name )
        self.set_std_state() # MUST Override Propellant to avoid Exception.
    
    @property
    def SGc(self):
        """Return critical specific gravity."""
        if self.Zc is None:
            return None
        
        lbm_per_cuin = self.Pc * self.MolWt / (18540.0 * self.Tc * self.Zc)
        return lbm_per_cuin * 27.67990471 # g/ml
    
    def set_std_state(self):
        raise NotImplementedError
        
    def summ_print(self):
        """Print a summary of the Propellant object."""
        print('====== RocketProps State Point of Liquid %s ====='%(self.pname, ))
        print( 'Name    =       %s'%prop_names.paren_desc( self.pname ) )
        print( 'T       = %12g'%self.T    ,'degR')
        print( 'P       = %12g'%self.P    ,'psia')
        print( 'Pvap    = %12g'%self.Pvap ,'psia')
        print( 'Pc      = %12g'%self.Pc   ,'psia')
        print( 'Tc      = %12g'%self.Tc   ,'degR')
        print( 'SGliq   = %12g'%self.SG   ,'g/cc')
        print( 'SGvap   = %12g'%self.SGVapAtTdegR( self.T )   ,'g/cc')
        print( 'visc    = %12g'%self.visc ,'poise')
        print( 'cond    = %12g'%self.cond ,'BTU/hr/ft/delF')
        print( 'Tnbp    = %12g'%self.Tnbp,'degR')
        print( 'Tfreeze = %12g'%self.Tfreeze,'degR')
        #print( 'Ttriple = %12g'%self.Ttriple,'degR')
        print( 'Cp      = %12g'%self.Cp   ,'BTU/lbm/delF')
        print( 'MolWt   = %12g'%self.MolWt,'g/gmole')
        print( 'Hvap    = %12g'%self.Hvap ,'BTU/lbm')
        if isinstance(self.surf, float):
            print( 'surf    = %12g'%self.surf ,'lbf/in')
        else:
            print( 'surf    = %12s'%self.surf ,'lbf/in')

    def TAtTr(self, Tr):
        """Given reduced temperature, return absolute temperature in degR."""
        return self.Tc * Tr

    def TrAtT(self, T):
        """Given temperature, return reduced temperature."""
        return T / self.Tc

    def TdegRAtPsat(self, Psat):
        """Given saturation pressure in psia, solve for saturation temperature in degR"""
        trmin = self.trL[0]
        trmax = 1.0
        
        for i in range(40):
            Tr = (trmin + trmax) / 2.0
            P = self.PvapAtTr(Tr)
            if P < Psat:
                trmin = Tr
            else:
                trmax = Tr
                
        return self.Tc * (trmin + trmax) / 2.0
            

    # ========= methods for absolute temperature deg rankine (TdegR) =============

    def PvapAtTdegR(self, TdegR):
        """Given temperature in degR, return saturation pressure in psia."""
        Tr = TdegR / self.Tc
        return 10.0**self.log10p_terp( Tr )

    def ViscAtTdegR(self, TdegR):
        """Given temperature in degR, return viscosity of saturated liquid in poise."""
        Tr = TdegR / self.Tc
        return 10.0**self.log10visc_terp( Tr )
        
    def CondAtTdegR(self, TdegR):
        """Given temperature in degR, return thermal conductivity of saturated liquid in BTU/hr-ft-R."""
        Tr = TdegR / self.Tc
        return self.cond_terp( Tr )

    def CpAtTdegR(self, TdegR):
        """Given temperature in degR, return Heat Capacity of saturated liquid in BTU/lbm-R."""
        Tr = TdegR / self.Tc
        return self.cp_terp( Tr )

    def HvapAtTdegR(self, TdegR):
        """Given temperature in degR, return heat of vaporization of saturated liquid in BTU/lbm."""
        Tr = TdegR / self.Tc
        return self.hvap_terp( Tr )

    def SurfAtTdegR(self, TdegR):
        """Given temperature in degR, return surface tension of saturated liquid in lbf/in."""
        Tr = TdegR / self.Tc
        return self.surf_terp( Tr )

    def SGLiqAtTdegR(self, TdegR):
        """Given temperature in degR, return specific gravity of saturated liquid in g/ml."""
        Tr = TdegR / self.Tc
        return self.SG_liq_terp( Tr )

    def SGVapAtTdegR(self, TdegR):
        """Given temperature in degR, return specific gravity of Saturated Vapor in g/ml."""
        Tr = TdegR / self.Tc
        return 10.0**self.log10SG_vap_terp( Tr )
        
    def ZLiqAtTdegR(self, TdegR):
        """Given temperature in degR, return compressibility of saturated liquid."""
        Tr = TdegR / self.Tc
        return self.ZLiqAtTr( Tr )
        
    def ZVapAtTdegR(self, TdegR):
        """Given temperature in degR, return compressibility of  Saturated Vapor."""
        Tr = TdegR / self.Tc
        return self.ZVapAtTr( Tr )

    # ========= methods for reduced temperature (Tr) =============

    def PvapAtTr(self, Tr):
        """Given reduced temperature (Tr), return vapor pressure of saturated liquid in psia."""
        return 10.0**self.log10p_terp( Tr )

    def ViscAtTr(self, Tr):
        """Given reduced temperature (Tr), return viscosity of saturated liquid in poise."""
        return 10.0**self.log10visc_terp( Tr )
        
    def CondAtTr(self, Tr):
        """Given reduced temperature (Tr), return thermal conductivity of saturated liquid in BTU/hr-ft-R."""
        return self.cond_terp( Tr )

    def CpAtTr(self, Tr):
        """Given reduced temperature (Tr), return heat capacity of saturated liquid in BTU/lbm-R."""
        return self.cp_terp( Tr )

    def HvapAtTr(self, Tr):
        """Given reduced temperature (Tr), return heat of vaporization of saturated liquid in BTU/lbm."""
        return self.hvap_terp( Tr )

    def SurfAtTr(self, Tr):
        """Given reduced temperature (Tr), return surface tension of saturated liquid in lbf/in."""
        return self.surf_terp( Tr )

    def SGLiqAtTr(self, Tr):
        """Given reduced temperature (Tr), return specific gravity of saturated liquid in g/ml."""
        return self.SG_liq_terp( Tr )

    def SGVapAtTr(self, Tr):
        """Given reduced temperature (Tr), return specific of Saturated Vapor in g/ml."""
        return 10.0**self.log10SG_vap_terp( Tr )
        
    def ZLiqAtTr(self, Tr):
        """Given reduced temperature (Tr), return compressibility of saturated liquid."""
        P = self.PvapAtTr( Tr )
        sg = self.SGLiqAtTr( Tr )
        T = Tr * self.Tc
        return P * self.MolWt / (18540.0 * T * (sg/27.67990471))
        
    def ZVapAtTr(self, Tr):
        """Given reduced temperature (Tr), return compressibility of Saturated Vapor."""
        P = self.PvapAtTr( Tr )
        sg = self.SGVapAtTr( Tr )
        T = Tr * self.Tc
        return P * self.MolWt / (18540.0 * T * (sg/27.67990471))

    # ================================================================

    def Tr_data_range(self):
        """Return tuple of reduced temperature range, (Trmin, Trmax)"""
        return self.trL[0], self.trL[-1]
        
    def T_data_range(self):
        """Return tuple of temperature range, (Tmin, Tmax) in degR"""
        return self.tL[0], self.tL[-1]

    def P_data_range(self):
        """Return tuple of pressure range, (Pmin, Pmax) in psia"""
        Plo = 10.0**( self.log10pL[0] )
        Phi = 10.0**( self.log10pL[-1] )
        return Plo, Phi

    def plot_sat_props(self, save_figures=False, show_plot=True):
        """Create and launch matplotlib plots of all saturation properties."""
        import matplotlib.pyplot as plt

        trL = [self.trL[0] + i*(self.trL[-1]-self.trL[0])/200.0 for i in range(201) ]
        
        # ================== T and P =============================
        fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
        ax1.set_title( self.name + ' Temperature and Pressure' )
        
        ax1.plot( self.trL, self.tL, 'rs', label='Temperature' )
        ax1.plot( trL, [tr*self.Tc for tr in trL], 'r-', label='degR' )
        ax1.set_ylabel( 'Temperature (degR)' )
        ax1.grid()
        ax1.legend()
        
        ax2.grid()
        ax2.set_ylabel( 'Pressure (psia)' )
        ax2.set_xlabel('Reduced Temperature (Tr)')
        ax2.semilogy( self.trL, [10.0**p for p in self.log10pL], 'gs', label='Pressure' )
        ax2.semilogy( trL, [self.PvapAtTr(tr) for tr in trL], 'g-', label='psia' )
        ax2.legend()
        fig.tight_layout()
        
        if save_figures:
            fname = '%s_TandP.png'%self.pname
            plt.savefig(fname)

        
        # ================== visc and cond =============================
        fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
        ax1.set_title( self.name + ' Viscosity and Thermal Conductivity' )
        
        try:
            ax1.semilogy( self.trL, [10.0**p for p in self.log10viscL], 'rs', label='Visc' )
            ax1.semilogy( trL, [self.ViscAtTr(tr) for tr in trL], 'r-', label='poise'  )
        except:
            pass
        ax1.set_ylabel( 'Viscosity (poise)' )
        ax1.grid()
        ax1.legend()
        
        ax2.grid()
        ax2.set_ylabel( 'Thermal Conductivity (BTU/hr-ft-F)' )
        ax2.set_xlabel('Reduced Temperature (Tr)')
        try:
            ax2.plot( self.trL, self.condL, 'gs', label='ThermCond' )
            ax2.plot( trL, [self.CondAtTr(tr) for tr in trL], 'g-', label='BTU/h-f-F' )
        except:
            pass
        ax2.legend()
        fig.tight_layout()
        
        if save_figures:
            fname = '%s_ViscCond.png'%self.pname
            plt.savefig(fname)
        
        # ================== Cp and Hvap =============================
        fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
        ax1.set_title( self.name + ' Cp and Heat of Vaporization' )

    
        if self.name=='PH2':
            CP_LIMIT = 16.0
        else:
            CP_LIMIT = 2.0
            
        def drop_high_vals( xL, yL ):
            while yL[-1] > CP_LIMIT and xL[-1]>0.9:
                xL = xL[:-1]
                yL = yL[:-1]
            return xL, yL
        xL, yL = drop_high_vals( self.trL, self.cpL )
        ax1.plot( xL, yL, 'rs', label='Cp' )
        
        xL, yL = drop_high_vals( trL, [self.CpAtTr(tr) for tr in trL])
        ax1.plot( xL, yL, 'r-', label='BTU/lbm-F' )
        ax1.set_ylabel( 'Cp (BTU/lbm-F)' )
        ax1.grid()
        ax1.legend()
        
        ax2.grid()
        ax2.set_ylabel( 'Heat of Vaporization (BTU/lbm)' )
        ax2.set_xlabel('Reduced Temperature (Tr)')
        ax2.plot( self.trL, self.hvapL, 'gs', label='Hvap' )
        ax2.plot( trL, [self.HvapAtTr(tr) for tr in trL], 'g-', label='BTU/lbm' )
        ax2.legend()
        fig.tight_layout()
        
        if save_figures:
            fname = '%s_CpHvap.png'%self.pname
            plt.savefig(fname)
        
        # ================== Surface Tension and Density =============================
        fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
        ax1.set_title( self.name + ' Surface Tension and Density' )
        
        ax1.plot( self.trL, self.surfL, 'rs', label='SurfTen' )
        ax1.plot( trL, [self.SurfAtTr(tr) for tr in trL], 'r-', label='lbf/in' )
        ax1.set_ylabel( 'Surface Tension (lbf/in)' )
        ax1.grid()
        ax1.legend()
        
        ax2.grid()
        ax2.set_ylabel( 'Specific Gravity (SG)' )
        ax2.set_xlabel('Reduced Temperature (Tr)')
        ax2.plot( self.trL, self.SG_liqL, 'gs', label='Liquid' )
        ax2.plot( trL, [self.SGLiqAtTr(tr) for tr in trL], 'g-' )
        
        ax2.plot( self.trL, [10.0**r for r in self.log10SG_vapL], 'bs', label='Vapor' )
        ax2.plot( trL, [self.SGVapAtTr(tr) for tr in trL], 'b-' )
        
        ax2.legend()
        fig.tight_layout()
        
        if save_figures:
            fname = '%s_SurfSG.png'%self.pname
            plt.savefig(fname)
        
        
        # ========================================================
        if show_plot:
            plt.show()

    def Visc_compressed(self, TdegR, Ppsia):
        r'''Adjusts viscosity of a liquid for high pressure  using an empirical
        formula developed by Lucas.

        This code is modified from thermo package: https://thermo.readthedocs.io/
        also see: equation 9-9.1  in 5th Ed. of Gases and Liquids.

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: viscosity at (TdegR, Ppsia) in poise
        '''
        # need to use thermo internal units of degK, Pa
        T = get_value( TdegR, 'degR', 'degK')
        Tc = get_value( self.Tc, 'degR', 'degK')
        P = get_value( Ppsia, 'psia', 'Pa')
        Pc = get_value( self.Pc, 'psia', 'Pa')
        P_sat = get_value( self.PvapAtTdegR( TdegR ), 'psia', 'Pa')
        
        Tr = T/Tc
        mu_sat = self.ViscAtTr( Tr )
        if P <= P_sat:
            return mu_sat
        
        C = -0.07921+2.1616*Tr - 13.4040*Tr**2 + 44.1706*Tr**3 - 84.8291*Tr**4 \
            + 96.1209*Tr**5-59.8127*Tr**6+15.6719*Tr**7
        D = 0.3257/((1.0039-Tr**2.573)**0.2906) - 0.2086
        A = 0.9991 - 4.674E-4/(1.0523*Tr**-0.03877 - 1.0513)
        dPr = (P-P_sat)/Pc
        if dPr < 0:
            dPr = 0
        return (1. + D*(dPr/2.118)**A)/(1. + C*self.omega*dPr)*mu_sat

        

    def SG_compressed(self, TdegR, Ppsia):
        """Calculates compressed-liquid specific gravity,
        unless overridden, uses COSTALD since COSTALD matched non-alcohol REFPROP propellants best.

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml        
        """
        return self.SG_compressedCOSTALD( TdegR, Ppsia )

    def SG_compressedCOSTALD(self, TdegR, Ppsia):
        r'''Calculates compressed-liquid specific gravity, using the COSTALD  CSP method.

        This code is modified from thermo package: https://thermo.readthedocs.io/index.html

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml
        '''
        a = -9.070217
        b = 62.45326
        d = -135.1102
        f = 4.79594
        g = 0.250047
        h = 1.14188
        j = 0.0861488
        k = 0.0344483
        
        # convert to internal units from thermo 
        T = get_value( TdegR, 'degR', 'degK')
        Tc = get_value( self.Tc, 'degR', 'degK')
        P = get_value( Ppsia, 'psia', 'Pa')
        Pc = get_value( self.Pc, 'psia', 'Pa')
        Psat = get_value( self.PvapAtTdegR( TdegR ), 'psia', 'Pa')
        
        SGsat = self.SGLiqAtTdegR( TdegR )
        if P < Psat:
            print('Warning... Pressure below saturation pressure for T=%g degR, P=%g psia'%(TdegR, Ppsia))
            return SGsat
        
        
        Vs = self.MolWt / SGsat # [cm^3/mol]
        
        tau = 1 - T/Tc
        e = exp(f + g*self.omega + h*self.omega**2)
        C = j + k*self.omega
        B = Pc*(-1 + a*tau**(1/3.) + b*tau**(2/3.) + d*tau + e*tau**(4/3.))
        
        try:
            V_dense =  Vs*(1 - C*log((B + P)/(B + Psat))) # [cm^3/mol]
            
            # convert to SG
            SG_dense = self.MolWt / V_dense  # g/cm^3
        except:
            print('WARNING... SG_compressed has error at T=%g R, P=%g psia'%(TdegR, Ppsia))
            return None
        return SG_dense



    def SG_compressedCZ1(self, TdegR, Ppsia):
        r'''Calculates compressed-liquid specific gravity, using the Chang Zhao method.

        This code is derived from equation 4-12.3 in 5th Ed. of Gases and Liquids.

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml
        '''
        a0 = -170.335
        a1 = -28.578
        a2 = 124.809
        a3 = -55.5393
        a4 = 130.01 
        b0 = 0.164813
        b1 = -0.0914427 
        C = exp(1) 
        D = 1.00588

        
        # convert to internal units from thermo 
        T = get_value( TdegR, 'degR', 'degK')
        Tc = get_value( self.Tc, 'degR', 'degK')
        P = get_value( Ppsia, 'psia', 'bar')
        Pc = get_value( self.Pc, 'psia', 'bar')
        Psat = get_value( self.PvapAtTdegR( TdegR ), 'psia', 'bar')
        
        SGsat = self.SGLiqAtTdegR( TdegR )
        if P < Psat:
            print('Warning in SG_compressed... Pressure below Psat for T=%g degR, P=%g psia'%(TdegR, Ppsia))
            return SGsat
        
        Vs = self.MolWt / SGsat # [cm^3/mol]
        
        Tr = T / Tc
        if Tr > 0.94:
            print('Warning in SG_compressed... Reduced Temperature > 0.95 Tr=%g '%Tr )
        
        A = a0 + a1*Tr + a2*Tr**3 + a3*Tr**6 + a4/Tr
        B = b0 + self.omega * b1
        
        numer = A*Pc + C**( (D-Tr)**B ) * (P - Psat)
        denom = A*Pc + C*(P - Psat)
        
        try:
            V_dense =  Vs * numer / denom # [cm^3/mol]
            
            # convert to SG
            SG_dense = self.MolWt / V_dense  # g/cm^3
        except:
            print('WARNING... SG_compressed has error at T=%g R, P=%g psia'%(TdegR, Ppsia))
            return None
        return SG_dense

    def SG_compressedCZ2(self, TdegR, Ppsia):
        r'''Calculates compressed-liquid specific gravity, using the Chang Zhao method
        as modified in Journal of Molecular Liquids 160 (2011) 94-102

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml
        '''
        a0= 482.85416 
        a1=-1154.2977 
        a2= 790.09727 
        a3=-212.14413
        a4= 93.4904 
        b0= 0.0264002 
        b1= 0.42711522 
        b2= 0.5
        c1= 9.2892236 
        c2= 2.5103968 
        c3= 0.5939722 
        c4= 0.0010895002
        D= 1.00001 
        E= 0.80329503
        
        Pr = Ppsia / self.Pc
        Tr = TdegR / self.Tc
        Psat = self.PvapAtTdegR( TdegR )
        Psatr = Psat / self.Pc
        
        SGsat = self.SGLiqAtTdegR( TdegR )
        if Ppsia < Psat:
            print('Warning in SG_compressed... Pressure below Psat for T=%g degR, P=%g psia'%(TdegR, Ppsia))
            return SGsat
        
        Vs = self.MolWt / SGsat # [cm^3/mol]
        
        if Tr > 0.94:
            print('Warning in SG_compressed... Reduced Temperature > 0.95 Tr=%g '%Tr )
        
        A = a0 + a1*Tr + a2*Tr**3 + a3*Tr**6 + a4/Tr
        B = b0 + b1/(b2+self.omega)
        C = c1 * (1-Tr)**c2 + (1 - (1-Tr)**c2) * exp( c3 + c4*(Pr - Psatr) )
        
        numer = A + C**( (D-Tr)**B ) * (Pr - Psatr)**E
        denom = A + C*(Pr - Psatr)**E
        
        try:
            V_dense =  Vs * numer / denom # [cm^3/mol]
            
            # convert to SG
            SG_dense = self.MolWt / V_dense  # g/cm^3
        except:
            print('WARNING... SG_compressed has error at T=%g R, P=%g psia'%(TdegR, Ppsia))
            return None
        return SG_dense


    def SG_compressedNasrfar(self, TdegR, Ppsia):
        r'''Calculates compressed-liquid specific gravity, using the Nasrfar Moshfeghian method
        from Journal of Molecular Liquids 160 (2011) 94-102

        :param TdegR: temperature in degR
        :param Ppsia: pressure in psia
        :type TdegR: float
        :type Ppsia: float
        :return: specific gravity at (TdegR, Ppsia) in g/ml
        '''
        
        Pr = Ppsia / self.Pc
        Tr = TdegR / self.Tc
        Psat = self.PvapAtTdegR( TdegR )
        Psatr = Psat / self.Pc        
        SGsat = self.SGLiqAtTdegR( TdegR )
        if Ppsia < Psat:
            print('Warning in SG_compressed... Pressure below Psat for T=%g degR, P=%g psia'%(TdegR, Ppsia))
            return SGsat
        
        Vs = self.MolWt / SGsat # [cm^3/mol]
        
        j0=1.3168E-3 
        j1=3.4448E-2 
        j2= 5.4131E-2 
        L= 9.6840E-2
        M=8.6761E-6 
        f0= 48.8756 
        G= 0.7185 
        I= 3.4031E-5
        c0= 5.5526 
        c1=-2.7659 
        Om0=7.9019E-2 
        Om1=-2.8431E-2
        R = 8.3144598 # J/mol-K  =  m^3-Pa / mol-K  =  J/mol-K
        
        J = j0 + j1*(1-Tr)**(1./3.) + j2*(1-Tr)**(2./3.)
        F = f0 * (1-Tr)
        C = c0 + c1 * self.omega
        TcK = get_value( self.Tc, 'degR', 'degK')
        PcMPa = get_value( self.Pc, 'psia', 'MPa')
        
        Om = Om0 + Om1*self.omega
        Vinf =  Om * R * TcK / PcMPa  # cm^3/mol
        
        if Tr > 0.94:
            print('Warning in SG_compressed... Reduced Temperature > 0.95 Tr=%g '%Tr )
                
        dpr = max(0, Pr - Psatr)
        numer = J + L*dpr + M*dpr**3
        denom = F + G*dpr + I*dpr**3
        
        vrat = C * numer / denom
        V_dense = vrat * (Vinf - Vs) + Vs # [cm^3/mol]
        
        SG_dense = self.MolWt / (V_dense)  # g/cm^3
        
        return SG_dense

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


def solve_Tnbp( tL, pvapL ):
    """
    Given Temperature list, tL and Vapor Pressure list, pvapL, solve for Tnbp
    tL = temperature list, degR
    pvapL = vapor pressure list, psia
    Return:
    Tnbp = normal boiling point, degR
    """
    
    Pvap_terp = InterpProp( tL, pvapL, extrapOK=True)
    
    def func( T ):
        return 14.6959 - max(0.0, Pvap_terp( T ))
    
    sol = optimize.root_scalar(func, bracket=[tL[0], tL[-1]], method='brentq')
    # print( 'sol.root=',sol.root )
    return sol.root


def build_mixture( prop_name=''): #, prop_objL=None, mass_fracL=None):
    """
    Build a mixture of MMH + N2H4 (e.g. M20), N2O4 + NO (e.g. MON25) or LOX + F2 (e.g. FLOX70)

    Args:

    Returns: Propellant object of mixture
    """
    # prop_objL  list of Propellant objects to be mixed. 
    # mass_fracL list of WEIGHT Fractions for each Propellant object.

    mmhPcent = isMMH_N2H4_Blend( prop_name )
    noPcent  = isMON_Ox( prop_name )
    f2Pcent  = isFLOX_Ox( prop_name )
    n2h4Pcent = isN2H4_UDMH_Blend( prop_name )

    if not prop_names.is_primary_name( prop_name ):
        prop_names.add_primary_name( prop_name )

    if mmhPcent:
        prop_names.add_associated_name( prop_name, f"{mmhPcent}% MMH + {100-mmhPcent}% N2H4" )

        Tfreeze = Mnn_Freeze_terp( mmhPcent )

        """  
        #         mass_fracL calculation
        # To get percentage goal (p3) from starting percentages (p1 and P2)
        # Use fraction (f) of p1 and unit value of p2
        (f*p1 + p2) / (f + 1) = p3
        f*p1 + p2 = f*p3 + p3
        p2 - p3 = f*(p3 - p1)
        f = (p2 - p3) / (p3 - p1)
        """
        if mmhPcent <= 86.0:
            mmh_lo_prop = get_prop('N2H4')
            mmh_hi_prop = get_prop('MHF3')
            # mass_fracL=[noPcent, 100-noPcent]
            mass_fracL=[(86-mmhPcent)/(mmhPcent), 1.0]
        else:
            mmh_lo_prop = get_prop('MHF3')
            mmh_hi_prop = get_prop('MMH')
            mass_fracL=[(100-mmhPcent)/(mmhPcent-86), 1.0]

        prop_objL=[mmh_lo_prop, mmh_hi_prop]  # will normalize below
        # print( 'mmh_lo_prop.name =', mmh_lo_prop.name)
        # print( 'mmh_hi_prop.name =', mmh_hi_prop.name)

    elif n2h4Pcent:
        prop_names.add_associated_name( prop_name, f"{n2h4Pcent}% N2H4 + {100-n2h4Pcent}% UDMH" )

        Tfreeze = Axx_Freeze_terp( 100.0 - n2h4Pcent )

        if n2h4Pcent <= 50.0:
            mmh_lo_prop = get_prop('UDMH')
            mmh_hi_prop = get_prop('A50')
            # mass_fracL=[noPcent, 100-noPcent]
            mass_fracL=[(50-n2h4Pcent)/(n2h4Pcent), 1.0]
        else:
            mmh_lo_prop = get_prop('A50')
            mmh_hi_prop = get_prop('N2H4')
            mass_fracL=[(100-n2h4Pcent)/(n2h4Pcent-50), 1.0]

        prop_objL=[mmh_lo_prop, mmh_hi_prop]  # will normalize below
        print( 'mmh_lo_prop.name =', mmh_lo_prop.name)
        print( 'mmh_hi_prop.name =', mmh_hi_prop.name)

    elif noPcent:
        # if a well-documented MON, return the file-based version
        prop_str = 'MON%g'%noPcent
        if prop_str in ['MON10', 'MON25', 'MON30']:
            return get_prop( prop_str )

        prop_names.add_associated_name( prop_name, f"{noPcent}% NO + {100-noPcent}% N2O4" )


        """  
        #         mass_fracL calculation
        # To get percentage goal (p3) from starting percentages (p1 and P2)
        # Use fraction (f) of p1 and unit value of p2
        (f*p1 + p2) / (f + 1) = p3
        f*p1 + p2 = f*p3 + p3
        p2 - p3 = f*(p3 - p1)
        f = (p2 - p3) / (p3 - p1)
        """
        if noPcent <= 10.0:
            mon_lo_prop = get_prop('N2O4')
            mon_hi_prop = get_prop('MON10')
            # mass_fracL=[noPcent, 100-noPcent]
            mass_fracL=[(10-noPcent)/(noPcent), 1.0]
        elif noPcent <= 25.0:
            mon_lo_prop = get_prop('MON10')
            mon_hi_prop = get_prop('MON25')
            mass_fracL=[(25-noPcent)/(noPcent-10), 1.0]
        elif noPcent <= 30.0:
            mon_lo_prop = get_prop('MON25')
            mon_hi_prop = get_prop('MON30')
            mass_fracL=[(30-noPcent)/(noPcent-25), 1.0]
        else:
            raise Exception('Maximum MON value allowed in RocketProps is MON30.')

        prop_objL=[mon_lo_prop, mon_hi_prop]  # will normalize below
        print( 'mon_lo_prop.name =', mon_lo_prop.name)
        print( 'mon_hi_prop.name =', mon_hi_prop.name)

        Tfreeze = MON_Freeze_terp( noPcent )
        # raise Exception('MON logic needs work')
    elif f2Pcent:
        lox_prop = get_prop('LOX')
        lf2_prop = get_prop('LF2')
        prop_objL=[lf2_prop, lox_prop]
        mass_fracL=[f2Pcent, 100-f2Pcent]  # will normalize below

        prop_names.add_associated_name( prop_name, f"{f2Pcent}% LF2 + {100-f2Pcent}% LOX" )

        # Assume we don't need an accurate freeze temperature
        Tfreeze = (f2Pcent*lf2_prop.Tfreeze + (100.0-f2Pcent)*lox_prop.Tfreeze) / 100.0
    else:
        raise Exception('Mixtures only implemented for MMH+N2H4 or MON oxidizer or FLOX oxidizer')


    if len(prop_objL) > 2:
        raise Exception('ONLY Binary mixtures allowed.')

    # Change reference fluids to allow extrapolation
    def change_terp_extrap( terp_obj ):
        terp_obj.extrapOK = 1
        terp_obj.linear = 1
        if terp_obj.linear:
            terp_obj.Nterp = 1
        else:
            terp_obj.Nterp = 2

    for Pobj in prop_objL:
        
        change_terp_extrap( Pobj.log10p_terp )
        change_terp_extrap( Pobj.log10visc_terp )
        change_terp_extrap( Pobj.cond_terp )
        change_terp_extrap( Pobj.cp_terp )
        change_terp_extrap( Pobj.hvap_terp )
        change_terp_extrap( Pobj.surf_terp )
        change_terp_extrap( Pobj.SG_liq_terp )
        change_terp_extrap( Pobj.log10SG_vap_terp )

    def pTr(Pobj, T, Tr):
        """Make a pseudo temperature for each object to smooth high Tr values"""
        limit = 0.7
        # Tr_p = max(limit, min(1.0, T / Pobj.Tc))
        Tr_p =  T / Pobj.Tc
        if Tr_p < limit:
            return Tr_p
        
        Tc_mix = T / Tr
        T_at_limit = limit * Pobj.Tc
        Tr_mix_at_Tr_p_limit = T_at_limit / Tc_mix

        Tr_range = 1.0 - limit

        return limit + Tr_range * (Tr-Tr_mix_at_Tr_p_limit)/(1.0-Tr_mix_at_Tr_p_limit)


    # Normalize mass_fracL to make sure it adds up to 1.0
    total = sum( mass_fracL )
    mass_fracL = [ f/total for f in mass_fracL ]

    # calculate mole fractions
    moleL = [ f_mass/Pobj.MolWt for (f_mass, Pobj) in zip(mass_fracL, prop_objL) ]
    mole_total = sum( moleL )
    mole_fracL = [m/mole_total for m in moleL]
    # print( 'mole_fracL =', mole_fracL)
    # print( 'mass_fracL =', mass_fracL)

    tmpD = {} # index=parameter name, value=string or numeric value

    dataSrc = 'Mixture Rules'     

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.3
    omega = mixing_simple(mole_fracL, [Pobj.omega for Pobj in prop_objL]) 
    tmpD['omega'] = omega

    tmpD['dataSrc'] = dataSrc
    # tmpD['class_name'] = prop_name 
    tmpD['prop_name'] = prop_name 

    MolWt = sum( [mole_frac*Pobj.MolWt for (mole_frac,Pobj) in zip(mole_fracL, prop_objL)] )
    tmpD['MolWt'] = MolWt

    # make mixture reference point the mole average of constituents
    T = mixing_simple(mole_fracL, [Pobj.T for Pobj in prop_objL])
    tmpD['T'] = T  # degR
    tmpD['P'] = mixing_simple(mole_fracL, [Pobj.P for Pobj in prop_objL])  # psia

    # Vc = MolWt / SGc # (cm**3/gmole)
    VcL = [ Pobj.MolWt/Pobj.SGc for Pobj in prop_objL ]

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.1
    # Switch to Li method from mixing_simple:  tmpD['Tc'] = mixing_simple(mole_fracL, [Pobj.Tc for Pobj in prop_objL])  # degR

    # thermo package: https://thermo.readthedocs.io/
    TcL = [Pobj.Tc for Pobj in prop_objL]

    # if prop_name.startswith('MON'):
    #     Tc = mixing_simple(mole_fracL, TcL)  # degR
    # else:
    Tc = Li_Tcm(mole_fracL, TcL, VcL)
    # Tc = mixing_simple(mole_fracL, TcL)  # degR
    # print( 'Tc =', Tc)

    tmpD['Tc'] = Tc # (zs, Tcs, Vcs)

    Tr = T / Tc

    # Zc is the mechanical compressibility for mixtures as well as pure fluids
    Zc = mixing_simple(mole_fracL, [Pobj.Zc for Pobj in prop_objL])
    tmpD['Zc'] = Zc


    # get mixture critical volume
    Vcm =  mixing_simple( mole_fracL, VcL )
    Vcm = get_value( Vcm, 'cm**3', 'inch**3')

    # Properties of Liquids and Gases 5th Ed. Eqn 5-3.2
    R = 18540.0 / 453.59237 # psi-in**3 / gmole-degR (i.e. 453.59 converts lbmole to gmole)
    Pc = Zc  * R * Tc / Vcm 
    tmpD['Pc'] = Pc


    # get Pvap at T
    Pvap = sum( [y* Pobj.PvapAtTr( pTr(Pobj, T, Tr) ) for (y,Pobj) in zip(mole_fracL, prop_objL)] )
    tmpD['Pvap'] = Pvap

    # Vm = MolWt / SG # (cm**3/gmole)
    VmL = [ Pobj.MolWt/Pobj.SGLiqAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL ]
    Vm = mixing_simple( mole_fracL, VmL )
    # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
    tmpD['SG'] = MolWt / Vm  


    tmpD['Cp']   = mixing_simple(mass_fracL, [Pobj.CpAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL])
    tmpD['Hvap'] = mixing_simple(mass_fracL, [Pobj.HvapAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL])
    
    tmp_condL = [Pobj.CondAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]
    if len(mass_fracL) == 2:
        # Recommended in Perry Handbook 8th Ed. page 2-512
        tmpD['cond'] =  Filippov_cond( mass_fracL, tmp_condL )
    else:
        tmpD['cond'] =  DIPPR9H_cond( mass_fracL, tmp_condL )

    # sigmas_TbL = [Pobj.SurfAtTr( Pobj.Tnbp ) for Pobj in prop_objL]
    # TbsL = [Pobj.Tnbp for Pobj in prop_objL]
    # tmpD['surf'] =  Diguilio_Teja_surften(T, mole_fracL, sigmas_TbL, TbsL, TcL)

    surfL = [Pobj.SurfAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]
    # tmpD['surf'] =  mixing_simple( mass_fracL, surfL )

    tmpD['surf'] = Winterfeld_Scriven_Davis_surf(mole_fracL, surfL, VmL)

    #  D. Perry's Chemical Engineering Handbook. 6th Ed
    viscL = [Pobj.ViscAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]
    # tmpD['visc'] = mixing_simple( mass_fracL, viscL)

    tmpD['visc'] = mixing_logarithmic( mass_fracL, viscL) # ChEDL recommendation

    tmpD['Tfreeze'] = Tfreeze
    tmpD['Ttriple'] = Tfreeze



    # start building the arrays of values
    NsatPts = 21

    # Use Raoult's Law to calculate vapor pressure vs temperature
    TfreezeL = [Pobj.Tfreeze for Pobj in prop_objL]
    Tlo = Tfreeze
    Thi = max( TcL )
    if Thi > Tc:
        Thi = Tc
    dT = (Thi - Tlo) / (NsatPts - 1)

    
    trL = []
    tL  = []
    pL  = []
    viscL = []
    condL = []
    cpL = []
    hvapL = []
    surfL = []    
    SG_liqL = []
    SG_vapL = []

    # print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))

    # iterate over temperature range
    for i in range( NsatPts ):
        T =  Tlo + i*dT
        Tr = T / Tc
        if i == NsatPts-1:
            T = Thi
            Tr = 1.0

        tL.append( T )
        trL.append( T/Tc )
        # liquid density
        VmL = [ Pobj.MolWt/Pobj.SGLiqAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL ]

        pL.append( sum( [y* Pobj.PvapAtTr( pTr(Pobj, T, Tr) ) for (y,Pobj) in zip(mole_fracL, prop_objL)] ) ) # Raoult's Law

        cpL.append( mixing_simple(mass_fracL, [ Pobj.CpAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]) )

        hvapL.append( mixing_simple(mass_fracL, [ Pobj.HvapAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]) )
        
        # surfL.append( mixing_simple(mass_fracL, [ Pobj.SurfAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]) )
        sL = [ Pobj.SurfAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]
        if Tr < 1.0:
            surfL.append( Winterfeld_Scriven_Davis_surf(mole_fracL, sL, VmL) )
        else:
            surfL.append( 0.0 )
        
        # viscL.append( mixing_simple     (mass_fracL, [ Pobj.ViscAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]) )
        viscL.append( mixing_logarithmic(mass_fracL, [ Pobj.ViscAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]) )
        
        # thermal conductivity
        tmp_condL = [Pobj.CondAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL]
        if len(mass_fracL) == 2:
            # Recommended in Perry Handbook 8th Ed. page 2-512
            condL.append(  Filippov_cond( mass_fracL, tmp_condL ) )
        else:
            condL.append(   DIPPR9H_cond( mass_fracL, tmp_condL ) )

        
        Vm = mixing_simple( mole_fracL, VmL )
        # Amgat mixing rule from thermo package: https://thermo.readthedocs.io/
        SG_liqL.append( MolWt / Vm )

        Z = mixing_simple(mole_fracL, [Pobj.ZVapAtTr( pTr(Pobj, T, Tr) ) for Pobj in prop_objL])

        MW = sum( [y*Pobj.MolWt* Pobj.PvapAtTr( pTr(Pobj, T, Tr) ) \
                   for (y,Pobj) in zip(mole_fracL, prop_objL)] ) / pL[-1]

        # print( 'MW =',MW, '  MolWt =', MolWt)
        SGg = pL[-1] * MW / (18540.0 * T * (Z/27.67990471)) # g/ml
        # SGg = pL[-1] * MolWt / (18540.0 * T * (Z/27.67990471)) # g/ml
        
        SG_vapL.append( SGg )



    tmpD['Tnbp'] = solve_Tnbp( tL, pL )

    tmpD['NsatPts'] = NsatPts
    tmpD['trL'] = trL
    tmpD['tL'] = tL
    tmpD['log10pL'] =  [log10(p) for p in pL]
    
    tmpD['log10viscL'] =  [log10(v) for v in viscL]
    tmpD['condL'] = condL
    tmpD['cpL'] = cpL
    tmpD['hvapL'] = hvapL
    tmpD['surfL'] = surfL
    tmpD['SG_liqL'] = SG_liqL
    tmpD['log10SG_vapL'] =  [log10(v) for v in SG_vapL]


    # =============== Temporary output =====================
    if 0:
        kL = sorted( tmpD.keys(), key=str.lower )
        for k in kL:
            try:
                print( '%20s'%k, tmpD[k][:2], tmpD[k][-2:] )
            except:
                print( '%20s'%k, tmpD[k] )

        # show T limits
        print( 'Tlo=%g,  Thi=%g'%(Tlo, Thi))
        print( 'Tfreeze of pure propellants:', TfreezeL, '  of blend =', Tfreeze)
        print( 'Tc of pure propellants:', TcL, '  of blend =', Tc)
        # src = template.format( **tmpD )
        # print( src )

        # from math import log10
        # from rocketprops.rocket_prop import Propellant
        # from rocketprops.unit_conv_data import get_value
        # from rocketprops.InterpProp_scipy import InterpProp

        # exec( src )
        print()
        # print( repr(tmpD) )

    # use tmpD values to build mixture Propellant object
    return Prop( valueD=tmpD )




if __name__ == '__main__':
    from rocketprops.plot_multi_props import make_plots
    
    C = get_prop('M20')
    C.summ_print()
    # if C:
    #     C.summ_print()
    #     C.plot_sat_props()
    
    make_plots( prop_nameL=['MHF3', 'MMH', 'N2H4'], prop_objL=[C], 
                abs_T=0, ref_scaled=False, Tmin=450, Tmax=700)

    # make_plots( prop_nameL=['A50', 'UDMH', 'N2H4'], prop_objL=[C], 
    #             abs_T=1, ref_scaled=False, Tmin=450, Tmax=700)
