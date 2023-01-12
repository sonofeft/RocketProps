#!/usr/bin/env python
# -*- coding: ascii -*-

r"""
CubicEOS models cubic equations of state.

CubicEOS takes the equations of state from the Wikipedia page:
https://en.wikipedia.org/wiki/Equation_of_state. 


CubicEOS
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

Equation Form:
P = R*T/(V-b)  -  a*alpha(T)/(V**2 + 2*b*V + -b**2)

 a is called the attraction parameter and 
 b the repulsion parameter or the effective molecular volume.
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
import numpy as np
from math import log10, log, exp, sqrt
import cmath
from abc import ABC, abstractmethod

RGAS = 83.145 # bar-cm**3 / gmole-K

class CubicEqnOfState(ABC):
    """CubicEOS models cubic equations of state.
    """

    def __init__(self, eos_name='Unknown', fluid_name='CH4', 
                 T_R=201.4, P_psia=14.7, omega=0.008,
                 Tc_R=343.0, Pc_psia=673.3, Tnbp_R=201.4, MolWt=16.04):
        """Inits CubicEqnOfState."""
        self.eos_name   = eos_name
        self.fluid_name = fluid_name
        self.Tc_R       = Tc_R
        self.Tc_K       = Tc_R / 1.8
        self.Pc_psia    = Pc_psia
        self.Pc_bar     = Pc_psia / 14.5038
        self.Tnbp_R     = Tnbp_R
        self.MolWt      = MolWt
        self.omega      = omega

        self.Zc         = 0.3074013086987 # Peng-Robinson EOS 
        
        self.Pvap = self.lvpres(T_R)
        
        self.num_soln = 0
        
        # set constants for EOS
        self.set_eos_constants() # <-- required method in child classes
        self.set_TP( T_R, P_psia )

    @abstractmethod
    def set_eos_constants(self):
        pass

    def get_liq_Vm(self):
        """Return Vm for current state."""
        try:
            Vm = self.SG_to_Vm( self.SGliq )
            return Vm
        except:
            print("ERROR in get_liq_Vm. SGliq =", self.SGliq)
            return None

    def calc_psia_from_tv(self, T_K=100.0, Vm=1000.0):
        P_bar = self.calc_p_from_tv( T_K=T_K, Vm=Vm)
        P_psia = P_bar * 14.5038
        return P_psia
    
    def SG_to_Vm(self, SG):
        """Given a specific gravity of this fluid, calc Vm (cm**3/gmole)"""
        return self.MolWt / SG
    
    def set_TD(self, T_R, D_lbcuft):
        """Set Temperature and Density, Calculate Pressure"""
        
        self.T_R = T_R
        self.T_K = T_R / 1.8
        self.D = D_lbcuft
        self.SG = self.D / 62.428
        
        self.Vm = self.SG_to_Vm( D_lbcuft/62.428 )
        
        self.P_bar = self.calc_p_from_tv( T_K=T_R/1.8, Vm=self.Vm)
        self.P_psia = self.P_bar * 14.5038
        self.Pvap = self.lvpres(T_R)

        if T_R<self.Tc_R and self.Pvap<self.P_psia:
            # fluid is two phase
            self.set_TP( T_R, self.Pvap )
        else:
            self.Vmliq, self.Zliq = None, None
            self.Vmgas, self.Zgas = None, None
            self.SGliq = None
            self.Dliq = None
            self.SGgas = None
            self.Dgas = None
    
    def set_TP(self, T_R, P_psia):
        self.T_R        = T_R
        self.P_psia     = P_psia   

        self.T_K = self.T_R / 1.8
        self.P_bar = self.P_psia / 14.5038

        self.Tr = T_R / self.Tc_R
        self.Pr = P_psia / self.Pc_psia
        
        self.Pvap = self.lvpres(T_R)
        
        good_z_rootL = self.solve_z_roots()
        self.set_density_from_Zroots( good_z_rootL )
    
    def get_density(self, phase=0):
        """
        phase = 0: return liq or gas depending on Pvap
        phase = 1: return liq if available
        phase = 2: return gas if available
        """
        if self.num_soln==0:
            return 0.0
        elif self.num_soln==1:
            return self.D
        else:
            if self.num_soln > 1:
                if phase==1:
                    return self.Dliq
                elif phase==2:
                    return self.Dgas
                else:
                    if self.Pvap < self.P_psia:
                        return self.Dliq
                    else:
                        return self.Dgas
            else:
                return self.D
                    
    
    def set_density_from_Zroots(self, good_solL ):
        """good_solL is a list of tuples (Vm, Z) for T,P solution."""
        
        good_solL.sort() # put in increasing Vm
        
        self.num_soln = len( good_solL )
        
        if self.num_soln==0:
            self.Vmliq, self.Zliq = None, None
            self.Vmgas, self.Zgas = None, None
            self.SGliq = None
            self.Dliq = None
            self.SGgas = None
            self.Dgas = None
            
            self.Vm, self.Z = None, None
            self.SG = None
            self.D = None
            
        elif self.num_soln==1:
            self.Vm, self.Z = good_solL[0]
            self.SG = self.MolWt * self.P_bar / RGAS / self.T_K / self.Z
            self.D = self.SG * 62.428
            
            self.Vmliq, self.Zliq = None, None
            self.Vmgas, self.Zgas = None, None
            self.SGliq = None
            self.Dliq = None
            self.SGgas = None
            self.Dgas = None
            
        else:
            self.Vmliq, self.Zliq = good_solL[0]
            self.Vmgas, self.Zgas = good_solL[-1]
            self.SGliq = self.MolWt * self.P_bar / RGAS / self.T_K / self.Zliq
            self.Dliq = self.SGliq * 62.428
            self.SGgas = self.MolWt * self.P_bar / RGAS / self.T_K / self.Zgas
            self.Dgas = self.SGgas * 62.428
            
            self.Vm, self.Z = None, None
            self.SG = None
            self.D = None

    def printProps(self):
        '''print property summary with units'''
        print("for fluid",self.fluid_name,'  with EOS:', self.eos_name)
        print("T     =%8g"%self.T_R," degR (Tc=%8g R"%self.Tc_R,", Tnbp=%8g R"%self.Tnbp_R,")")
        print("      =%8g"%self.T_K," degK (Tc=%8g K"%(self.Tc_R/1.8,),", Tnbp=%8g K"%(self.Tnbp_R/1.8,),")")
        print("P     =%8g"%self.P_psia," psia (Pc=%8g psia"%self.Pc_psia,")")
        print("      =%8g"%self.P_bar, "  bar (Pc=%8g bar"%(self.Pc_psia/14.5038,),")")
        print("MW    =%8g"%self.MolWt," lbm/lbmmole")
        print("Pvap  =%8g"%self.Pvap," psia")
        print("omega = %8g"%self.omega)
        
        if self.D is None and self.Dliq is None:
            pass
        elif self.Dliq is None:
            print("D     =%8g"%self.D," lbm/cu ft")
            print("SG    =%8.5f"%self.SG," g/cc")
            #print("Vm    =%8g"%(self.SG_to_Vm(self.SG),),"(cm**3/gmole)" )
            print("Vm    =%8g"%self.Vm,"(cm**3/gmole)" )
        else:
            print("Dliq  =%8g"%self.Dliq," lbm/cu ft")
            print("SGliq =%8.5f"%self.SGliq," g/cc")
            print("Vmliq =%8g"%(self.SG_to_Vm(self.SGliq),),"(cm**3/gmole)" )
            print("Zliq  =%8g"%self.Zliq )
            print("Dgas  =%8g"%self.Dgas," lbm/cu ft")
            print("SGgas =%8.5f"%self.SGgas," g/cc")
            print("Vmgas =%8g"%(self.SG_to_Vm(self.SGgas),),"(cm**3/gmole)" )
            print("Zgas  =%8g"%self.Zgas )
        
    def calc_z_from_tv(self, T_K, Vm):
        """T_K is deg K, Vm is cm**3/gmole"""
        
        P = self.calc_p_from_tv(T_K=T_K, Vm=Vm)
        Z = P*Vm/RGAS/T_K
        return Z

    def lvpres(self, T):
        """
        Estimate liquid vapor pressure using 
        critical point and normal boiling point (page 206 of Properties of Gases and Liquids 4th ed.)
        
        T = temperature, degR
        Returns:
        PVP = Vapor Pressure (psia)
        """
        TR=T/self.Tc_R
        if TR > 1.0:
            PVP = self.Pc_psia
        else:
            TBR=self.Tnbp_R/self.Tc_R
            
            H=TBR*log(self.Pc_psia/14.5038)/(1.-TBR)  # pressure in bar
            
            G=.4835+.4605*H
            SK=(H/G-(1.+TBR))/((3.+TBR)*(1.-TBR)**2)
            PVPRLN=-G/TR*(1.-TR**2+SK*(3.+TR)*(1.-TR)**3)
            PVP=self.Pc_psia*exp(PVPRLN)
        return PVP
        
    def estimate_Vm_from_Z(self, Z):
        """
        Estimate the Vm value used in the EOS. 
        NOTE: this is only used to identify gas and liquid states.
        UNITS: cm**3/gmole WHEN: RGAS = 83.145 # bar-cm**3 / gmole-K
        """
        VmEqn = Z * RGAS * self.T_K / self.P_bar
        return VmEqn
    
    def select_good_roots(self, z_rootL):
        """Remove imaginary solutions from roots list."""
        good_solL = []
        for Z in z_rootL:
            if isinstance(Z, complex):
                rpart,ipart = Z.real, Z.imag
                if abs(ipart) < 1.0E-8 and rpart > 0.0:
                    Vm = self.estimate_Vm_from_Z( rpart )
                    good_solL.append( (Vm,rpart) )
            elif Z > 0.0:
                Vm = self.estimate_Vm_from_Z( Z )
                #print('At Z=%8g,  Vm=%8g cm**3/gmole'%(Z, Vm))
                
                good_solL.append( (Vm, Z) )
            else:
                print('Bad Z:', Z)
        if len(good_solL)==0:
            print('-->  No Solutions found.')
        #print()
        #print('z_rootL =',z_rootL)
        #print('good_solL =',good_solL)
        
        return good_solL
        
    
    def solve_z_roots(self):
        """
        Given current settings of T_K and P_bar, solve Z roots.
        """
        #  use direct equations from sympy solve.
        z_rootL = self.sympy_solve_z_roots()
        
        return self.select_good_roots( z_rootL )
    
    def numpy_solve_z_roots(self):
        """
        ORIGINAL ROUTINE... DEPRECATED FOR sympy_solve_z_roots
        a3*Z**3 + a2*Z**2 + a1*Z + a0 = 0
        """
        
        a0, a1, a2, a3 = self.get_z_cubic_coeff()
            
        z_rootL = np.roots( [a3, a2, a1, a0] )
        print( 'numpy roots = ', z_rootL )
        return z_rootL
        
    
    def sympy_solve_z_roots(self):
        """
        Given current settings of T_K and P_bar, solve Z roots.
        a3*Z**3 + a2*Z**2 + a1*Z + a0 = 0
        """
        a0, a1, a2, a3 = self.get_z_cubic_coeff()
        I = complex(0,1)
            
        #one not explicitly imaginary
        Z1 = -a2/(3*a3) - (-3*a1/a3 + a2**2/a3**2)/(3*(27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)) - (27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)/3

        #two imaginary
        Z2 = -a2/(3*a3) - (-3*a1/a3 + a2**2/a3**2)/(3*(-0.5 - cmath.sqrt(3)*I/2)*(27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)) - (-0.5 - cmath.sqrt(3)*I/2)*(27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)/3.0
        Z3 = -a2/(3*a3) - (-3*a1/a3 + a2**2/a3**2)/(3*(-0.5 + cmath.sqrt(3)*I/2)*(27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)) - (-0.5 + cmath.sqrt(3)*I/2)*(27*a0/(2*a3) - 9*a1*a2/(2*a3**2) + a2**3/a3**3 + cmath.sqrt(-4*(-3*a1/a3 + a2**2/a3**2)**3 + (27*a0/a3 - 9*a1*a2/a3**2 + 2*a2**3/a3**3)**2)/2)**(1.0/3.0)/3.0

        z_rootL = [Z1, Z2, Z3]
        #print( 'sympy roots = ', z_rootL )
        return z_rootL

class PReos( CubicEqnOfState ):
    """
    Peng-Robinson equation of state.

    Wikipedia Description:
    The Peng-Robinson equation of state (PR EOS) was developed in 1976 at The University of 
    Alberta by Ding-Yu Peng and Donald Robinson in order to satisfy the following goals:

    1) The parameters should be expressible in terms of the critical properties and the acentric factor.
    2) The model should provide reasonable accuracy near the critical point, particularly for 
    calculations of the compressibility factor and liquid density.
    3) The mixing rules should not employ more than a single binary interaction parameter, 
    which should be independent of temperature, pressure, and composition.
    4) The equation should be applicable to all calculations of all fluid properties in natural gas processes.

    For the most part the Peng-Robinson equation exhibits performance similar to the 
    Soave equation, although it is generally superior in predicting the liquid densities 
    of many materials, especially nonpolar ones. 

    Equation Form:
    P = R*T/(V-b)  -  a*alpha(T)/(V**2 + 2*b*V + -b**2)

    """
    
    def __init__(self, fluid_name='CH4', 
                 T_R=201.4, P_psia=14.7, omega=0.008,
                 Tc_R=343.0, Pc_psia=673.3, Tnbp_R=201.4, MolWt=16.04):
        """Inits CubicEqnOfState."""
        CubicEqnOfState.__init__(self, eos_name='PengRobinson', fluid_name=fluid_name, 
            T_R=T_R, P_psia=P_psia, Tc_R=Tc_R, Pc_psia=Pc_psia, Tnbp_R=Tnbp_R, 
            MolWt=MolWt, omega=omega)

    
    def set_eos_constants(self):
        R, Tc, Pc = RGAS, self.Tc_K, self.Pc_bar
            
        self.a       = 0.45724 * R**2 * Tc**2 / Pc
        self.b       = 0.0778 * R * Tc / Pc
                
    def alphaFunc(self, Tr ):
        k = 0.37464 + 1.54226*self.omega - 0.26993*self.omega**2
        return (1 + k * (1 - Tr**0.5) )**2

    def calc_p_from_tv(self, T_K=100.0, Vm=1000.0):
        """T_K is deg K, Vm is cm**3/gmole"""
        Tr = T_K/self.Tc_K
            
        # let (Vm - eta) / (Vm - b) == 1
        P = RGAS*T_K / (Vm - self.b) - self.a * self.alphaFunc( Tr ) \
            /( Vm**2 + 2*self.b*Vm - self.b**2 )
        return P
        
    def get_z_cubic_coeff(self):
        """
        Given current settings of T_K and P_bar, solve Z roots.
        a3*Z**3 + a2*Z**2 + a1*Z + a0 = 0
        """
        b = self.b
        a = self.a
        alpha = self.alphaFunc( self.Tr )
        R = RGAS
        T = self.T_K
        P = self.P_bar
        
        #print('Solving:',self.eos_name)
        #print('Solving for T=%g, P=%g, R=%g, a=%g, b=%g, alpha=%g, Tr=%g'%(T,P,R,a,b,alpha,T/self.Tc_K))
        
        A = a * alpha * P / (R * T)**2
        B = b * P / (R * T)
        #print('A=%g'%A, '   B=%g'%B)
        
        # make terms in Z cubic polynomial
        #a3 = 1.0
        #a2 = -1.0 
        #a1 = A - 3*B**2 - 2*B
        #a0 = -(A*B - B**2 - B**3)
        
        a3 = 1.0
        a2 = -(1.0 - B)
        a1 = A - 2*B - 3*B**2
        a0 = -(A*B - B**2 - B**3)
        
        return a0, a1, a2, a3
    

if __name__ == '__main__':
    
    
                        
    Cpr = PReos( fluid_name='Propane', 
                        T_R=300.0*1.8, P_psia=9.9742*14.5038, omega=0.152, 
                        Tc_R=369.83*1.8, Pc_psia=42.477*14.5038, Tnbp_R=415.865, MolWt=44.0956)

    
    print('========= expecting Vvapor=2036.5 cm**3/mol,  Vliq=90.077 cm**3/mol')
    for Vm in [1500,2038,2500]:
        print( 'PR at 300K, Vm=%g, P=%g bar,   Z=%g'%(Vm, Cpr.calc_p_from_tv(T_K=300, Vm=Vm), Cpr.calc_z_from_tv(300, Vm)) )
        print('      ---')
    
    
    print()
    print('-'*55)
    T, P = 540, 144.66
    Cpr.set_TP( T, P )
    print('Dliq=%s,  Dgas=%s,   D=%s,  P=%g psia'%(Cpr.Dliq, Cpr.Dgas, Cpr.D, Cpr.P_psia) )
    
    print()
    Cpr.printProps()
    print()

    Cpr.set_TD( T, 33 )
    print('Dliq=%s,  Dgas=%s,   D=%s,  P=%g psia'%(Cpr.Dliq, Cpr.Dgas, Cpr.D, Cpr.P_psia) )

    Cpr.set_TP( T, 771.4 )
    print('Dliq=%s,  Dgas=%s,   D=%s,  P=%g psia'%(Cpr.Dliq, Cpr.Dgas, Cpr.D, Cpr.P_psia) )
