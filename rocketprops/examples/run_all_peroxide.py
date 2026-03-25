
from rocketprops.rocket_prop import get_prop


dataD = {} # key=pname, value=SGref

for i in range( 101 ):
    pname = 'Peroxide_%i'%i
    print( pname, end=' ')

    pobj = get_prop( pname )
    print( pobj.T, pobj.SG)

