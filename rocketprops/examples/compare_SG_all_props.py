
from rocketprops.rocket_prop import get_prop
from rocketprops.unit_conv_data import get_value

propL = ['A50','Methane','CLF5','Ethane','Ethanol','F2','IRFNA','LOX','M20',
         'Methanol','MMH','MHF3','MON10','MON25','MON30','N2H4','N2O','N2O4',
         'NH3','PH2','Propane','UDMH','RP1','Water','H2O2',
         'Peroxide_70','Peroxide_85','Peroxide_95', 'Peroxide_100']

dataD = {} # key=pname, value=(SGref, data string)

print( '  Propellant  density     Tref       Tnbp     SGnbp')
for pname in propL:
    pobj = get_prop( pname )
    Tref_C = get_value( pobj.T, 'degR', 'degC')
    Tnbp_C = get_value( pobj.Tnbp, 'degR', 'degC')
    SG_nbp = pobj.SGLiqAtTdegR( pobj.Tnbp )

    dataD[ pname ] = (pobj.SG, '%5.2f SG %8.1f \u00b0C'%( pobj.SG, Tref_C ) +\
                      '%8.1f \u00b0C %5.2f SG'%( Tnbp_C, SG_nbp ))
        
keyL = sorted( dataD, key=dataD.get, reverse=True )
for pname in keyL:
    print( '%12s'%pname, dataD[pname][1])
