from scipy import optimize
from math import *

def buzzelli_ffact(eod, ReNum):
    '''From the "Fluid Power" article for single pass evaluation of colebrook
       by Dennis Buzzelli June 19, 2008'''
       
    if ReNum < 4000.0:
        return 64.0 / ReNum
    
    # universal A is better... ignore eod>0 value of A
    if 0: #eod>0.02: 
        # A value for eod>0
        A = -2.0*log10( eod/3.7 + 1.9*(-2.0*log10(eod/3.7))/ReNum )
    else:
        # universal A value has better accuracy at very low roughness/Diam
        A = ( (0.774* log(ReNum))-1.41 ) / ( 1.0 + 1.32*sqrt(eod) )
    
    B = ReNum*eod/3.7 + 2.51*A
    
    rhs = A -  (A+2.0*log10(B/ReNum) ) / (1.0 + 2.18/B)
    
    ffact = (1.0/rhs)**2
    return ffact
    
def ffact(eod, ReNum):
    '''Use buzzelli as 1st approximation and plug into colebrook
       Loop a few times to get many, many decimal points of accuracy
       (better than 1.6E-7 PERCENT ERROR everywhere)
    '''
    
    if ReNum < 4000.0:
        return 64.0 / ReNum

    ff = buzzelli_ffact(eod, ReNum)
    
    term1 = eod / 3.7
    term2 = 2.51 / ReNum
    
    # iterate a few times... percent error is less than 1.6E-7 with 6 loops
    #                                                   (6E-6 with 4 loops)
    for i in range(6):
        sqrtTerm = sqrt(ff)
        ff = (-2.0 * log10(term1 + term2/sqrtTerm))**-2
    
    return ff

def colebrook_ffact(roughness, diam, ReNum):
    '''
    c... Solve for the Colebrook Equation for Friction Factor
    c
    c  1/sqrt(f) = -2 log10[  roughness/3.7/D + 2.51/ReNum/sqrt(f) ]
    c
    c ===> INPUT
    c roughness in inches
    c diam in inches
    c ReNum is the Reynolds number (dimensionless)
    c
    c
    c ===> INPUT
    cf2py intent(in) roughness
    cf2py intent(in) diam
    cf2py intent(in) ReNum
    c ===> OUTPUT
    c... friction factor
    '''
    if ReNum < 4000.0:
        return 64.0 / ReNum

    term1 = roughness / 3.7 / diam
    term2 = 2.51 / ReNum
    def calcF(ff):
        '''helper function to calc iterations on Colebrook eqn'''
        sqrtTerm = sqrt(ff)
        eval = 1.0/sqrtTerm + 2.0 * log10(term1 + term2/sqrtTerm)
        #print( 'eval=',eval,'at ff=',ff )
        return eval

    eod = roughness / diam
    init_guess =  buzzelli_ffact(eod, ReNum)
    sol = optimize.root_scalar(calcF, x0=init_guess,  bracket=(0.005, 0.1), xtol=1.0E-12, maxiter=100)
    #print( sol.root, sol.iterations, sol.function_calls )
    
    return sol.root


if __name__ == "__main__":
    import sys
    import matplotlib.pyplot as plt
    
    fig = plt.figure()

    e = 5.0e-6
    diam = 1.0
    eList = [.03, .01, .003, .001, .0003, .0001, .00001, .000001]

    cycle = [1.0]
    while cycle[-1]<10.0:
        cycle.append( cycle[-1] * 1.1 )
    cycle = cycle[:-1]

    ReList = [1.E3, 1.E4, 1.E5, 1.E6, 1.E7]
    
    for e in eList:
        xRe = []
        yFF = []
        ybFF = []

        for ReBase in ReList:
            for cyVal in cycle:
                ReNum = ReBase * cyVal
                ff = colebrook_ffact(e,diam,ReNum)
                #print( ReNum, ff )
                print( ffact(e/diam, ReNum) - ff )
                xRe.append( ReNum )
                yFF.append( ff )
                
                bff = buzzelli_ffact( e/diam, ReNum )
                ybFF.append( bff )
        
        plt.semilogx(xRe,yFF,'--',linewidth=3, label='Ce/D=%G'%e )
        plt.semilogx(xRe,ybFF,linewidth=1, label='Be/D=%G'%e )
    
    plt.legend(loc='best')

    plt.grid(True)
    plt.title( "Friction Factor" )
    plt.xlabel( "Reynolds Number" )
    plt.ylabel( "Friction Factor" )
    
    plt.xlim( (1.0E3, 1.0E8) )

    try:
        if __file__ == sys.argv[0]:
            plt.show()
    except:
        pass