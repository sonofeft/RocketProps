import os
import glob

"""
Give primary name and alternate names for included propellants.

Examples of vehicles that use specific propellants
https://www.britannica.com/technology/rocket-jet-propulsion-device-and-vehicle/Liquid-propellant-rocket-engines
"""

class PropNames:
    def __init__(self):
        """Hold primary names and associated alternate names."""
        
        self.primary_nameD = {} # index=primary name, value=set of alternate names
        
        # allow for case mis-matches.
        self.primary_lowerD = {} # index=primary lower case, value=primary
        self.alternate_lowerD = {} # index=alternate lower case, value=primary
    
    def primary_name_list(self):
        """Return a list of the primary name of all propellants in RockeProps"""
        return list( self.primary_nameD.keys() )
    
    def alternate_name_list(self, name):
        """Return a list of all recognized names for the input propellant name."""
        primary = self.get_primary_name( name )
        if primary is None:
            return ['']
        else:
            altL = sorted( list(self.primary_nameD[ primary ]), key=str.lower )
            return altL
    
    def description(self, name):
        """Return a description for the input propellant name."""
        primary = self.get_primary_name( name )
        if primary is None:
            return 'No Description Available'
        else:
            altL = sorted( list(self.primary_nameD[ primary ]), key=str.lower )
            #altL = ['(%s)'%a for a in altL]
            return '%s == %s'%(primary, ' == '.join(altL) )
    
    def paren_desc(self, name):
        """Return a description for the input propellant name."""
        primary = self.get_primary_name( name )
        if primary is None:
            return 'No Description Available'
        else:
            altL = sorted( list(self.primary_nameD[ primary ]), key=str.lower )
            if len(altL) == 0:
                return primary
            else:
                return '%s  (%s)'%(primary, ', '.join(altL) )
    
    def add_primary_name(self, name):
        """Add a propellant primary name to the RockeProps library."""
        if name not in self.primary_nameD:
            self.primary_nameD[ name ] = set()
            self.primary_lowerD[ name.lower() ] = name
        else:
            print('WARNING... attempted to duplicate primary name.', name)
            
    def is_primary_name(self, name):
        """Check if input name is a primary name (allow for case mis-matches)"""
        return name.lower() in self.primary_lowerD
        
    def get_primary_name(self, name):
        """Get the primary name for the input propellant name."""
        pname = self.primary_lowerD.get( str(name).lower(), None )
        if pname is None:
            pname = self.alternate_lowerD.get( str(name).lower(), None )
        return pname
        
    def add_associated_name(self, primary, associated):
        """Add an associated name for the given primary propellant name."""
        if associated in self.primary_nameD:
            raise Exception('Attempted to revert %s to an associated name'%associated)
        
        if not primary in self.primary_nameD:
            raise Exception('Attempted to create primary="%s" with associated name="%s"'%(primary, associated) )
            
        self.primary_nameD[ primary ].add( associated )
        
        self.alternate_lowerD[ associated.lower() ] = primary
            
    def summ_print(self):
        """Print a summary of the primary propellant names in RockeProps."""
        nameL = sorted( list( self.primary_nameD.keys() ), key=str.lower )
        print('============ Propellant Names ===============')
        for name in nameL:
            print( '%10s -->'%name, self.primary_nameD[name] )
    
prop_names = PropNames()
prop_names.add_primary_name('A50')
prop_names.add_primary_name('Methane')
prop_names.add_primary_name('CLF5')
prop_names.add_primary_name('Ethane')
prop_names.add_primary_name('Ethanol')
prop_names.add_primary_name('F2')
prop_names.add_primary_name('IRFNA')
prop_names.add_primary_name('LOX')
#prop_names.add_primary_name('M20')
prop_names.add_primary_name('Methanol')
prop_names.add_primary_name('MMH')
prop_names.add_primary_name('MHF3')
prop_names.add_primary_name('MON10')
prop_names.add_primary_name('MON25')
prop_names.add_primary_name('MON30')
prop_names.add_primary_name('N2H4')
prop_names.add_primary_name('N2O')
prop_names.add_primary_name('N2O4')
prop_names.add_primary_name('NH3')
prop_names.add_primary_name('PH2')
prop_names.add_primary_name('Propane')
prop_names.add_primary_name('UDMH')
prop_names.add_primary_name('RP1')
prop_names.add_primary_name('Water')


prop_names.add_associated_name( 'A50', "50% N2H4 + 50% UDMH" )
prop_names.add_associated_name( 'A50', 'Aerozine50' )
prop_names.add_associated_name( 'CLF5', "ChlorinePentafluoride" )
prop_names.add_associated_name( 'Methane', "CH4" )
prop_names.add_associated_name( 'Ethane', "C2H6" )
prop_names.add_associated_name( 'Ethanol', "C2H6O" )
prop_names.add_associated_name( 'F2', "Fluorine" )
prop_names.add_associated_name( 'F2', "LF2" )
prop_names.add_associated_name( 'LOX', "O2(L)" )
prop_names.add_associated_name( 'LOX', "Oxygen" )
prop_names.add_associated_name( 'Methanol', "CH4O" )

prop_names.add_associated_name( 'IRFNA', "85% HNO3 + 15% NO2" )

#prop_names.add_associated_name( 'M20', "20% MMH + 80% N2H4" )


prop_names.add_associated_name( 'MHF3', "MHF-3" )
prop_names.add_associated_name( 'MHF3', "86% MMH + 14% N2H4" )
prop_names.add_associated_name( 'MHF3', 'MixedHydrazineFuel-3' )

prop_names.add_associated_name( 'MON10', "90% N2O4 + 10% NO" )
prop_names.add_associated_name( 'MON25', "75% N2O4 + 25% NO" )
prop_names.add_associated_name( 'MON30', "70% N2O4 + 30% NO" )

prop_names.add_associated_name( 'N2H4', "Hydrazine" )
prop_names.add_associated_name( 'MMH', "MonoMethylHydrazine" )
prop_names.add_associated_name('N2O', 'NitrousOxide')
prop_names.add_associated_name('N2O', 'Dinitrogen Oxide')

prop_names.add_associated_name('N2O4', 'MON-3')
# prop_names.add_associated_name('N2O4', 'MON3')
prop_names.add_associated_name('NH3', 'Ammonia')
prop_names.add_associated_name('PH2', 'H2(L)')
prop_names.add_associated_name('PH2', 'LH2')
prop_names.add_associated_name('PH2', 'ParaHydrogen')
prop_names.add_associated_name('PH2', 'Hydrogen')
prop_names.add_associated_name('Propane', 'C3H8')
prop_names.add_associated_name('RP1', 'RP-1')
prop_names.add_associated_name('UDMH', 'UnsymmetricDiMethylHydrazine')
prop_names.add_associated_name('Water', 'H2O')


# look for scaled propellants
here = os.path.abspath(os.path.dirname(__file__))
prop_dir = os.path.join( here, 'props')
scaledL = glob.glob( os.path.join( prop_dir, '*_scaled_prop.py' ) )

for scaled_prop in scaledL:
    head,tail = os.path.split( scaled_prop )
    prop_name = tail.replace( '_prop.py', '' )
    prop_names.add_primary_name( prop_name )


if __name__ == "__main__":            
    
    pn = PropNames()
    pn.add_primary_name('MMH')
    pn.add_primary_name('N2H4')
    
    pn.add_associated_name( 'MMH', 'monomethylhydrazine')
    pn.add_associated_name( 'N2H4', 'hydrazine')
    
    pn.summ_print()
    
    print('Is "mmh" a primary name:', pn.is_primary_name('mmh'))
    
    print('Primary for "Hydrazine" = ', pn.get_primary_name("Hydrazine") )


    print( '=*66')
    prop_names.summ_print()
    

