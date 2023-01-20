import glob
import os
from rocketprops.rocket_prop import get_prop
import clipboard

path = r'C:\py_proj_github\RocketProps\rocketprops\props'
propL = glob.glob( os.path.join(path, '*.py' ))

sL = [] # list of lines to output
def add( s ):
    sL.append( s )
    
def get_prop_data( prop, attr='T' ):
    val = getattr(prop, attr)
    dval = val * 0.0001
    return (val, dval)

def attr_str(prop, attr, func_val):
    val = getattr(prop, attr)
    dval = val * 0.0001
    s = '        self.assertAlmostEqual(prop.%s, %g, places=None, delta=%g)'%(attr, val, dval)
    return s

def func_str(prop, attr, func_name, param_name, frac_err=0.0001):
    val = getattr(prop, attr)
    dval = val * frac_err
    fstr = '%s( %s )'%(func_name, param_name)
    s = '        self.assertAlmostEqual(prop.%s, prop.%s, places=None, delta=%g)'%(attr, fstr, dval)
    return s

def local_str( loc_name, loc_val, func_name, param_name, frac_err=0.0001):
    dval = loc_val * frac_err
    fstr = '%s( %s )'%(func_name, param_name)
    s = '        self.assertAlmostEqual(%s, prop.%s, places=None, delta=%g)'%(loc_name, fstr, dval)
    return s

attrL = ['T', 'P', 'Pvap', 'Pc', 'Tc', 'SG', 'visc', 'cond', 'Tnbp', 'Tfreeze', 'Cp', 'MolWt',
         'Hvap', 'surf']

for fname in propL:
    head,tail = os.path.split( fname )
    prop_name = tail.replace('_prop.py', '')
    if prop_name not in ['__init__.py', 'M20_scaled', 'A50_scaled']:
    
        add('    def test_%s_ref_pts(self):'%prop_name )
        add('        """Test %s reference points with interpolator calls"""'%prop_name)
        
        prop = get_prop( prop_name )
        add('        prop = get_prop( "%s" )'%prop_name)
        #add('        prop.summ_print()' )
        
        for a in attrL:
            add(  attr_str(prop, a, getattr(prop,a) )  )        
        
        add('        T = prop.T')
        add('        Tr = T / prop.Tc')
        T = prop.T
        Tr = T / prop.Tc
        
        add( func_str( prop, 'T', 'TAtTr', 'Tr' ) )
        add( local_str( 'Tr', Tr, 'TrAtT', 'T' ) )

        # T calls ===================================================
        if prop_name == 'CLF5':
            add( func_str( prop, 'T', 'TdegRAtPsat', 'prop.Pvap', frac_err=0.002 ) )
        else:
            add( func_str( prop, 'T', 'TdegRAtPsat', 'prop.Pvap' ) )
        
        if prop_name == 'CLF5':
            add( func_str( prop, 'Pvap', 'PvapAtTdegR', 'T', frac_err=0.3) )
        elif prop_name == 'RP1':
            add( func_str( prop, 'Pvap', 'PvapAtTdegR', 'T', frac_err=0.002) )
        else:
            add( func_str( prop, 'Pvap', 'PvapAtTdegR', 'T', frac_err=0.0002) )

        if prop_name == 'F2':
            add( func_str( prop, 'visc', 'ViscAtTdegR', 'T', frac_err=0.002) )
            add( func_str( prop, 'cond', 'CondAtTdegR', 'T', frac_err=0.002) )
        else:
            add( func_str( prop, 'visc', 'ViscAtTdegR', 'T', frac_err=0.0002) )
            add( func_str( prop, 'cond', 'CondAtTdegR', 'T', frac_err=0.0002) )
        
        if prop_name in ['Ethane', 'F2', 'LOX']:
            add( func_str( prop, 'Cp', 'CpAtTdegR', 'T', frac_err=0.002) )
        else:
            add( func_str( prop, 'Cp', 'CpAtTdegR', 'T', frac_err=0.0002) )
        
        add( func_str( prop, 'Hvap', 'HvapAtTdegR', 'T', frac_err=0.0002) )
        
        if prop_name == 'A50':
            add( func_str( prop, 'surf', 'SurfAtTdegR', 'T', frac_err=0.002) )
        else:
            add( func_str( prop, 'surf', 'SurfAtTdegR', 'T', frac_err=0.0002) )
        
        add( func_str( prop, 'SG', 'SGLiqAtTdegR', 'T', frac_err=0.0002) )
        
        SGvap = prop.SGVapAtTdegR( T )
        add('        SGvap = %12e'%prop.SGVapAtTdegR( T ))
        add( local_str( 'SGvap', SGvap, 'SGVapAtTdegR', 'T' ) )

        Z = prop.ZLiqAtTdegR( T )
        add('        Z = %12e'%prop.ZLiqAtTdegR( T ))
        add( local_str( 'Z', Z, 'ZLiqAtTdegR', 'T' ) )

        Z = prop.ZVapAtTdegR( T )
        add('        Z = %12e'%prop.ZVapAtTdegR( T ))
        add( local_str( 'Z', Z, 'ZVapAtTdegR', 'T' ) )
        
        # Tr calls ===================================================
        
        if prop_name == 'CLF5':
            add( func_str( prop, 'Pvap', 'PvapAtTr', 'Tr', frac_err=0.3) )
        elif prop_name == 'RP1':
            add( func_str( prop, 'Pvap', 'PvapAtTr', 'Tr', frac_err=0.002) )
        else:
            add( func_str( prop, 'Pvap', 'PvapAtTr', 'Tr', frac_err=0.0002) )

        if prop_name == 'F2':
            add( func_str( prop, 'visc', 'ViscAtTr', 'Tr', frac_err=0.002) )
            add( func_str( prop, 'cond', 'CondAtTr', 'Tr', frac_err=0.002) )
        else:
            add( func_str( prop, 'visc', 'ViscAtTr', 'Tr', frac_err=0.0002) )
            add( func_str( prop, 'cond', 'CondAtTr', 'Tr', frac_err=0.0002) )
        
        if prop_name in ['Ethane', 'F2', 'LOX']:
            add( func_str( prop, 'Cp', 'CpAtTr', 'Tr', frac_err=0.002) )
        else:
            add( func_str( prop, 'Cp', 'CpAtTr', 'Tr', frac_err=0.0002) )
        
        add( func_str( prop, 'Hvap', 'HvapAtTr', 'Tr', frac_err=0.0002) )
        
        if prop_name == 'A50':
            add( func_str( prop, 'surf', 'SurfAtTr', 'Tr', frac_err=0.002) )
        else:
            add( func_str( prop, 'surf', 'SurfAtTr', 'Tr', frac_err=0.0002) )
        
        add( func_str( prop, 'SG', 'SGLiqAtTr', 'Tr', frac_err=0.0002) )
        
        SGvap = prop.SGVapAtTr( Tr )
        add('        SGvap = %12e'%prop.SGVapAtTr( Tr ))
        add( local_str( 'SGvap', SGvap, 'SGVapAtTr', 'Tr' ) )

        Z = prop.ZLiqAtTr( Tr )
        add('        Z = %12e'%prop.ZLiqAtTr( Tr ))
        add( local_str( 'Z', Z, 'ZLiqAtTr', 'Tr' ) )

        Z = prop.ZVapAtTr( Tr )
        add('        Z = %12e'%prop.ZVapAtTr( Tr ))
        add( local_str( 'Z', Z, 'ZVapAtTr', 'Tr' ) )
            
        '''

TAtTr( Tr )
TrAtT( T )
TdegRAtPsat( Psat )
            
    # ========= methods for absolute temperature deg rankine (TdegR) =============

PvapAtTdegR( TdegR )
ViscAtTdegR( TdegR )
CondAtTdegR( TdegR )
CpAtTdegR( TdegR )
HvapAtTdegR( TdegR )
SurfAtTdegR( TdegR )
SGLiqAtTdegR( TdegR )
SGVapAtTdegR( TdegR )
ZLiqAtTdegR( TdegR )
ZVapAtTdegR( TdegR )

    # ========= methods for reduced temperature (Tr) =============

PvapAtTr( Tr )
ViscAtTr( Tr )
CondAtTr( Tr )
CpAtTr( Tr )
HvapAtTr( Tr )
SurfAtTr( Tr )
SGLiqAtTr( Tr )
SGVapAtTr( Tr )
ZLiqAtTr( Tr )
ZVapAtTr( Tr )

    # ================================================================

Tr_data_range( )
        """Return tuple of reduced temperature range, (Trmin, Trmax)"""
        return self.trL[0], self.trL[-1]
T_data_range( )
        """Return tuple of temperature range, (Tmin, Tmax) in degR"""
        return self.tL[0], self.tL[-1]
P_data_range( )
        """Return tuple of pressure range, (Pmin, Pmax) in psia"""
        Plo = 10.0**( self.log10pL[0] )
        Phi = 10.0**( self.log10pL[-1] )
        return Plo, Phi
Visc_compressed( TdegR, Ppsia )
SG_compressed( TdegR, Ppsia )
SG_compressedCOSTALD( TdegR, Ppsia )
SG_compressedCZ1( TdegR, Ppsia )
SG_compressedCZ2( TdegR, Ppsia )
SG_compressedNasrfar( TdegR, Ppsia )
        
        '''

        
        add('')

text = '\n'.join(sL)

print( text )
clipboard.copy( text )
