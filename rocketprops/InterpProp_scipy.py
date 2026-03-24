# Written by Charlie Taylor <cet@appliedpython.com>
# Oct,21 2005
'''Interpolated Properties'''

from scipy import interpolate
from numpy import float64, array
import numpy as np

class InterpProp:
    '''Interpolate tables of properties
       will automatically sort input data...
       (x array must be monotonically increasing)'''
       
        
    def __call__(self, xval=0.0):
        return self.getValue( xval )

    def __name__(self):
        return 'InterpProp_scipy'
       
    def __init__(self, xInp=[0,1], yInp=[10,110], extrapOK=1, linear=0,
        minY=None, maxY=None, terp_type='Pchip'):
        """
        terp_type options: see terp_descD
        """
        
        self.terp_type = terp_type
        self.terp_descD = {} # key=terp_type, value=description
        self.terp_descD["Pchip"] = "PchipInterpolator"
        self.terp_descD["not-a-knot"] = "CubicSpline with bc_type='not-a-knot'"
        self.terp_descD["Cubic"] = "CubicSpline"
        self.terp_descD['Akima1'] = "Akima1DInterpolator"
        self.terp_descD['1D'] = "interp1d"
          
        # Sort Data to Make sure that x array is monotonically increasing
        a = map(float,xInp)  
        b = map(float,yInp)
        c = [(x,y) for x,y in zip(a,b)]
        c.sort()
        a = []
        b = []
        for aa,bb in c:
            a.append(aa)
            b.append(bb)
        
        # now turn lists into Numpy/SciPy arrays
        self.x = array(a,float64)
        self.y = array(b,float64)
        
        self.extrapOK = extrapOK
        self.linear = linear
        if len(self.x) <= 1:
            self.extrapOK = 0
        if len(self.x) <= 2:
            self.linear = 1
            
        # calculate a small step in x 
        try:
            diffs = np.diff(sorted(self.x))
            self.eps = np.min(diffs) / 1000.0
        except:
            self.eps = 1.0E-12
        
            
        if linear:
            self.Nterp = 1
        else:
            self.Nterp = 2
        
        if len(self.x) > 1:
            #self.interpFunc = interpolate.interp1d(self.x, self.y, 
            #    kind=self.Nterp, bounds_error=False)
                
            #self.interpFunc = interpolate.UnivariateSpline(self.x, self.y,  k=self.Nterp, s=0)
            
            if self.terp_type=='Pchip':
                # most smooth interpolation in my testing.
                self.interpFunc = interpolate.PchipInterpolator(self.x, self.y)
            elif self.terp_type == "not-a-knot":
                self.interpFunc = interpolate.CubicSpline(self.x, self.y, bc_type='not-a-knot')
            elif self.terp_type == "Cubic":
                self.interpFunc = interpolate.CubicSpline(self.x, self.y)
            elif self.terp_type == 'Akima1':
                self.interpFunc = interpolate.Akima1DInterpolator(self.x, self.y)
            elif self.terp_type == '1D':
                self.interpFunc = interpolate.interp1d(self.x, self.y, kind='linear', fill_value="extrapolate")
            
            #self.interpFunc = interpolate.Akima1DInterpolator(self.x, self.y)
            #self.interpFunc = interpolate.CubicSpline(self.x, self.y)
            try:
                self.derivFunc = self.interpFunc.derivative()
            except:
                # if there is no derivative method, estimate derivative
                self.derivFunc = lambda x :(self.interpFunc(x + self.eps) - self.interpFunc(x - self.eps)) / (2 * self.eps)
        else:
            self.interpFunc = lambda x : self.y[0]
            self.derivFunc = lambda X : 0.0
        
        try:
            self.minY = float(minY)
        except:
            self.minY = None
            
        try:
            self.maxY = float(maxY)
        except:
            self.maxY = None
        
        self.delX = max(self.x) - min(self.x)
        
    def getValue(self, xval=0.0):
        xval = float(xval)
        
        if not self.extrapOK:
            if xval<self.x[0]: return self.y[0]
            if xval>self.x[-1]: return self.y[-1]
            #print '1) self.interpFunc( %s ) ='%xval,self.interpFunc( xval )
            return float(self.interpFunc( xval ))
        
        # if not in data range, linearly extrapolate from end points.
        if xval<self.x[0]: 
            yval = self.y[0]+(xval-self.x[0])*(self.y[1]-self.y[0])/(self.x[1]-self.x[0])
        elif xval>self.x[-1]: 
            yval = self.y[-1]+(xval-self.x[-1])*(self.y[-1]-self.y[-2])/(self.x[-1]-self.x[-2])
        else:
            #print '2) self.interpFunc( %s ) ='%xval,self.interpFunc( xval )
            yval = float(self.interpFunc( xval ))
        
        # if limits set, use them
        if self.minY is not None: yval = max(yval, self.minY)
        if self.maxY is not None: yval = min(yval, self.maxY)
        return yval
        
    def deriv(self, xval=0.0, stepFrac=0.0001):
        
        # if possible, use UnivariateSpline for 1st derivative.
        if xval>=self.x[0] and xval<=self.x[-1]: 
            # for UnivariateSpline, linear has 0th and 1st deriv
            #                       quadratic has 0th, 1st and 2nd derivs
            
            return self.derivFunc( xval )
            #return self.interpFunc.derivatives( xval )[1] # 1 for 1st derivative 
        
        # otherwise, make a rough estimate.
        dx = self.delX * stepFrac
        return (self(xval+dx) - self(xval-dx)) / 2.0 / dx
        
    def plot(self, Npts=100, do_show=True, new_fig=True,
             title='Scipy Interpolator', xlabel='X', ylabel='Y', show_deriv=True):
        import matplotlib.pyplot as plt

        if new_fig:
            plt.figure(figsize=(9, 6))
        
        xL = []
        yL = []
        dydxL = []
        dx = (self.x[-1] - self.x[0]) / Npts
        for i in range(Npts+1):
            x = self.x[0] + i * dx
            xL.append( x )
            yL.append( self.getValue(x) )
            if show_deriv:
                dydxL.append( self.deriv( x ) )
                
        plt.plot( self.x, self.y, 'o:', label='%s Data'%ylabel, markersize=8 )
        plt.plot(xL, yL, '-', label='%s Interpolation'%ylabel)
        
        if show_deriv:
            plt.plot(xL, dydxL, '--', label='1st Derivative')

        plt.title(title + '\n(%s)'%self.terp_descD[self.terp_type], fontsize=14)
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
                
        plt.legend()
        plt.grid(True, which='both', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        plt.tight_layout()
        
        if do_show:
            plt.show()
    
          
def dev_tests( do_show=True ): #Self Test
    

    x = [1,2,6,4,5]
    y = [10,40,360,160,250]
    i = InterpProp(x,y)
    print( 'with extrapOK and no min/max' )
    print( 'interpolated x=2.5 =',i.getValue(2.5) )
    print( 'extrapolated x=0.0 =',i.getValue(0.0) )
    print( 'extrapolated x=7.0 =',i.getValue(7) )
    print('')
    i = InterpProp(x,y,extrapOK=0)
    print( 'with extrapOK=0 and no min/max')
    print( 'interpolated x=2.5 =',i.getValue(2.5))
    print( 'extrapolated x=0.0 =',i.getValue(0.0))
    print( 'extrapolated x=7.0 =',i.getValue(7))
    print('')
    i = InterpProp(x,y,minY=0.0, maxY=300)
    print( 'with extrapOK and minY=0, maxY=300')
    print( 'interpolated x=2.5 =',i.getValue(2.5))
    print( 'extrapolated x=0.0 =',i.getValue(0.0))
    print( 'extrapolated x=7.0 =',i.getValue(7))

    print('')
    x = [6, 1]
    y = [360, 10]
    i = InterpProp(x,y,linear=1)
    print( 'Two point linear with extrapOK and no min/max')
    print( 'interpolated x=2.5 =',i.getValue(2.5))
    print( 'extrapolated x=0.0 =',i.getValue(0.0))
    print( 'extrapolated x=7.0 =',i.getValue(7))
    
    print('')
    x = [6]
    y = [360]
    i = InterpProp(x,y)
    print( 'Single point with extrapOK and no min/max')
    print( 'interpolated x=2.5 =',i.getValue(2.5))
    print( 'extrapolated x=0.0 =',i.getValue(0.0))
    print( 'extrapolated x=7.0 =',i.getValue(7))

    print( '='    *55)
    # do rapid laser example from PPT file
    x = [2.,4.25,5.25,7.81,9.2,10.6]
    y = [7.2,7.1,6.,5.,3.5,5.]
    
    q = InterpProp( x, y, linear=1)
    q.plot( do_show=do_show )

    
if __name__ == "__main__":
    dev_tests()

