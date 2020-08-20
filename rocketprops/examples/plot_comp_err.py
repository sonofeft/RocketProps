import matplotlib.pyplot as plt
from rocketprops.rocket_prop import get_prop
from engcoolprop.ec_fluid import EC_Fluid
from rocketprops.unit_conv_data import get_value
import numpy as np

COLORL = ['g','purple','b','orange','m','r']


def get_pcstd( refL, sgL ):
    pcerrL = [ (sg-ref)/ref for sg,ref in zip(sgL, refL) ]
    pcstd = np.std( pcerrL ) * 100
    ave_errL.append( pcstd )
    return '%%SD=%.2f'%pcstd

orderedL = []
for name in ['Water','N2O','Fluorine','Oxygen','Propane','Ethane','Methane','Methanol','Ethanol','Ammonia','Hydrogen']:


    ec = EC_Fluid(name)
    p = get_prop(name)

    # run at either normal boiling point or room temp
    T = min( p.Tnbp, 530 )
    if T < 530:
        Tstr = 'NBP(%.1f R)'%T
    else:
        Tstr = '%g R'%T

    Tr = T / p.Tc
    Psat = p.PvapAtTr( Tr )
    Psat_ec, DliqSat, DgasSat = ec.getSatPandDens( Tr * ec.Tc )

    fig = plt.figure( figsize=(6,5) )

    dpL = [dp for dp in range(0,6000, 100)]
    sg_ecL = []
    sg_p0L  = []
    sg_p1L  = []
    sg_p2L  = []
    sg_p3L  = []
    sg_p4L  = []

    for dp in dpL:
        P = Psat + dp + 1
        P_ec = Psat_ec + dp + 1
        ec.setTP( T=Tr*ec.Tc, P=P_ec )
        
        sg_ecL.append( get_value( ec.rho, 'lbm/in**3', 'SG' ) )
        
        sg_p0L.append( p.SG_compressed( T, P) )
        sg_p1L.append( p.SG_compressedCOSTALD( T, P) )
        sg_p2L.append( p.SG_compressedCZ1( T, P) )
        sg_p3L.append( p.SG_compressedCZ2( T, P ) )
        sg_p4L.append( p.SG_compressedNasrfar(T, P) )


    ave_errL = []
    plt.plot( dpL, sg_ecL, '-', label='CoolProp', linewidth=7, color=COLORL[0], alpha=0.7)
    plt.plot( dpL, sg_p0L, '-', label='RocketProp '+get_pcstd( sg_ecL, sg_p0L ), linewidth=3, color=COLORL[5])
    ave_errL = []
    plt.plot( dpL, sg_p1L, ':', label='COSTALD '+get_pcstd( sg_ecL, sg_p1L ), linewidth=3, color=COLORL[1])
    plt.plot( dpL, sg_p2L, '-', label='Chang Zhao 1 '+get_pcstd( sg_ecL, sg_p2L ), color=COLORL[2])
    plt.plot( dpL, sg_p3L, '-', label='Chang Zhao 2 '+get_pcstd( sg_ecL, sg_p3L ), color=COLORL[3])
    plt.plot( dpL, sg_p4L, '-', label='Nasrfar '+get_pcstd( sg_ecL, sg_p4L ), color=COLORL[4])

    ave_err = sum(ave_errL)/len(ave_errL) * 3.0
    plt.title( p.pname + ' SG Model Comparison at T=%s, Tr=%g'%(Tstr,Tr) + '\nAve 3 sigma model Error = %.2f%%'%ave_err )

    plt.xlabel('P - Psat (psid)')
    plt.ylabel( 'Specific Gravity (g/ml)' )
    plt.legend()
    plt.grid()
    fig.tight_layout()
    
    fname = '%s_sg_compare.png'%p.pname
    plt.savefig( fname )
    
    orderedL.append( (ave_err, '.. image:: ./_static/%s'%fname) )
    #print( '.. image:: ./_static/%s'%fname )
    
plt.show()

orderedL.sort( reverse=True )
for e,s in orderedL:
    print(s)
