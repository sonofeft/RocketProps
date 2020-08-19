import matplotlib.pyplot as plt
from rocketprops.rocket_prop import get_prop
from engcoolprop.ec_fluid import EC_Fluid
from rocketprops.unit_conv_data import get_value

Tr = 0.9

for name in ['N2O','Fluorine','Oxygen','Propane','Ethane','Methane','Methanol','Ethanol','Ammonia']:

    ec = EC_Fluid(name)
    p = get_prop(name)

    sg_ecL = []
    sg_p1L  = []
    sg_p2L  = []
    sg_p3L  = []
    sg_p4L  = []
    
    Psat_ec, DliqSat, DgasSat = ec.getSatPandDens( Tr * ec.Tc )
    Psat = p.PvapAtTr( Tr )

    dpL = [dp for dp in range(0,6000, 100)]
    for dp in dpL:
        T = Tr * p.Tc
        P = Psat + dp + 1
        P_ec = Psat_ec + dp + 1
        ec.setTP( T=Tr*ec.Tc, P=P_ec )
        
        sg_ecL.append( get_value( ec.rho, 'lbm/in**3', 'SG' ) )
        
        sg_p1L.append( p.SG_compressedCOSTALD( T, P) )
        sg_p2L.append( p.SG_compressedCZ1( T, P) )
        sg_p3L.append( p.SG_compressedCZ2( T, P ) )
        sg_p4L.append( p.SG_compressedNasrfar(T, P) )

    fig = plt.figure()
    plt.title( p.pname + ' SG Compressed Comparison at Tr=%g'%Tr )

    plt.plot( dpL, sg_ecL, '--', label='CoolProp', linewidth=5)
    plt.plot( dpL, sg_p1L, '--', label='COSTALD-Default', linewidth=3)
    plt.plot( dpL, sg_p2L, '-', label='CZ1')
    plt.plot( dpL, sg_p3L, '-', label='CZ2')
    plt.plot( dpL, sg_p4L, '-', label='Nasrfar')

    plt.legend()
    plt.grid()
plt.show()
