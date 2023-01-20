"""Plot multiple propellants on same chart for comparison"""
import matplotlib.pyplot as plt
from rocketprops.rocket_prop import get_prop

MARKERL = ['o','v','^','<','>','d','X','P','s','p','*','.']
COLORL = ['g','c','b','y','#FFA500','m','r']
REVCOLORL = list(reversed( COLORL ))

def get_marker(i):
    return MARKERL[ i % len(MARKERL) ]

def get_color(i):
    return COLORL[ i % len(COLORL) ]

def make_plots( prop_nameL=None, prop_objL=None, abs_T=False, ref_scaled=False,
                Tmin=None, Tmax=None, show_gas_dens=False, save_figures=False,
                show_plots=True):
    
    propL = []
    if prop_nameL is not None:
        propL = [get_prop( name ) for name in prop_nameL]
    if prop_objL is not None:
        propL.extend( prop_objL )

    # print( 'prop_nameL =', prop_nameL)
    # print( 'prop_objL =', prop_objL)

    if Tmin is None:
        Tmin = min( [prop.tL[0] for prop in propL] )
    if Tmax is None:
        Tmax = max( [prop.tL[-1] for prop in propL])

    Tr_min = min( [Tmin/prop.Tc for prop in propL] )
    Tr_max = max( [Tmax/prop.Tc for prop in propL] )

    trLL = [] # list of trL 
    TLL = []  # list of TL
    for prop in propL:
        if abs_T:
            t_start = max(Tmin, prop.tL[0])
            t_end   = min(Tmax, prop.tL[-1])
            tL = [t_start + i*(t_end-t_start)/200.0 for i in range(201) ]
            TLL.append( tL )
            trLL.append( [t/prop.Tc for t in tL] )

            prop.Tr = prop.T / prop.Tc # needed for Tr plots
        else:
            tr_start = max(Tr_min, prop.trL[0])
            tr_end = min(Tr_max, prop.trL[-1])

            # trL = [prop.trL[0] + i*(prop.trL[-1]-prop.trL[0])/200.0 for i in range(201) ]
            trL = [tr_start + i*(tr_end-tr_start)/200.0 for i in range(201) ]
            trLL.append( trL )
            TLL.append( [tr*prop.Tc for tr in trL] )
    
    name_set = set([prop.name for prop in propL])
    name_str = ', '.join( name_set )
    name_underscore_str = '_'.join( [prop.name for prop in propL] )
    
    # =========== general functions =======================
    def set_xlabel( ax ):
        if abs_T:
            ax.set_xlabel('Temperature (degR)')
        else:
            ax.set_xlabel('Reduced Temperature (Tr)')
    
    def set_ylabel(ax, name, units):
        if ref_scaled:
            ax.set_ylabel( name + ' / Ref Pt (-)' )
        else:
            ax.set_ylabel( '%s %s'%(name, units) )
    
    def get_xy_plot_lists( i, prop_name, list_name, func_name ):
        # e.g. get_xy_plot_lists( i, 'T', 'tL', 'TAtTr' )
        prop = propL[i]
        trL = trLL[i]
        TL = TLL[i]

        i_start = 0
        for i in range( len(prop.tL) ):
            i_start = i
            if prop.tL[i] >= Tmin:
                break
            
        i_end = len(prop.tL) - 1
        for i in range( len(prop.tL) ):
            if prop.tL[i] > Tmax:
                i_end = i 
                break

        # make reference point
        if hasattr( prop, prop_name ) and prop.T>=Tmin and prop.T<=Tmax:
            
            y_refL = [ getattr( prop, prop_name ) ]
            if abs_T:
                x_refL = [ prop.T ]
            else:
                x_refL = [ prop.T / prop.Tc ]

        else:
            x_refL, y_refL = None, None
                
        # make full data list
        if hasattr( prop, list_name ):
            y_dataL = getattr( prop, list_name )[i_start: i_end]
            if list_name.startswith('log10'):
                y_dataL = [10.0**y for y in y_dataL]
                
            if abs_T:
                x_dataL = prop.tL[i_start: i_end]
            else:
                x_dataL = prop.trL[i_start: i_end]
        else:
            x_dataL, y_dataL = None, None
                
        # make interpolated curve 
        if hasattr( prop, func_name ):
            func = getattr( prop, func_name )
            
            y_terpL = [func(tr) for tr in trL]
            if abs_T:
                x_terpL = TL
            else:
                x_terpL = trL
        else:
            x_terpL, y_terpL = None, None
        
        if ref_scaled:
            if y_refL:
                scale_val = y_refL[0]
            elif y_dataL:
                scale_val = max( y_dataL )
            elif y_terpL:
                scale_val = max( y_terpL )
            else:
                scale_val = 1.0
                
            if y_refL:
                y_refL = [ y/scale_val for y in y_refL ]
            if y_dataL:
                y_dataL = [ y/scale_val for y in y_dataL ]
            if y_terpL:
                y_terpL = [ y/scale_val for y in y_terpL ]

        
        return x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL
    
    # ================== T and P =============================
    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
    ax1.set_title( name_str + '\nTemperature and Pressure' )
    
    for i,prop in enumerate(propL):
        lab = prop.name + '(%s)'%prop.dataSrc
        
        if abs_T:
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'Tr', 'trL', 'TAtTr' )
            y_terpL = [T/prop.Tc for T in y_terpL]
        else:
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'T', 'tL', 'TAtTr' )

        ax1.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
        ax1.plot( x_terpL, y_terpL, '-', color=get_color(i) )
        ax1.plot( x_refL, y_refL, marker=get_marker(i), color=get_color(i), 
                  markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
        
    if abs_T:
        set_ylabel(ax1, 'Reduced Temperature', '(-)')
    else:
        set_ylabel(ax1, 'Temperature', '(degR)')
            
    ax1.grid()
    ax1.legend( framealpha=0.5 )
    
    ax2.grid()
    set_xlabel( ax2 )
    set_ylabel(ax2, 'Pressure', '(psia)')
        
    for i,prop in enumerate(propL):
        lab = prop.name + '(%s)'%prop.dataSrc
        x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'Pvap', 'log10pL', 'PvapAtTr' )

        # print('Pressure Plot data')
        # print( 'x_refL =', x_refL)
        # print( 'y_refL =', y_refL)
        # print( 'x_dataL =', x_dataL[:5])
        # print( 'y_dataL =', y_dataL[:5], y_dataL[-5:])
        # print( 'x_terpL =', x_terpL[:5])
        # print( 'y_terpL =', y_terpL[:5], y_terpL[-5:])

        ax2.semilogy( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
        ax2.semilogy( x_terpL, y_terpL, '-', color=get_color(i) )
        ax2.semilogy( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
    ax2.legend( framealpha=0.5 )
    fig.tight_layout()

    if save_figures:
        fname = '%s_TandP.png'%name_underscore_str
        plt.savefig(fname)    
    # ================== visc and cond =============================
    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
    ax1.set_title( name_str + '\nViscosity and Thermal Conductivity' )
    
    for i,prop in enumerate(propL):
        if not None in prop.log10viscL:
            lab = prop.name + '(%s)'%prop.dataSrc
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'visc', 'log10viscL', 'ViscAtTr' )

            ax1.semilogy( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
            ax1.semilogy( x_terpL, y_terpL, '-', color=get_color(i) )
            ax1.semilogy( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
            
            
    set_ylabel(ax1, 'Viscosity', '(poise)')
    ax1.grid()
    ax1.legend( framealpha=0.5 )
    
    ax2.grid()
    set_ylabel(ax2, 'Thermal Conductivity', '(BTU/hr-ft-F)')
    set_xlabel( ax2 )

    for i,prop in enumerate(propL):
        if not None in prop.condL:
            lab = prop.name + '(%s)'%prop.dataSrc
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'cond', 'condL', 'CondAtTr' )

            ax2.semilogy( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
            ax2.semilogy( x_terpL, y_terpL, '-', color=get_color(i) )
            ax2.semilogy( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
                        
    ax2.legend( framealpha=0.5 )
    fig.tight_layout()
        
    if save_figures:
        fname = '%s_ViscCond.png'%name_underscore_str
        plt.savefig(fname)
    
    # ================== Cp and Hvap =============================
    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
    ax1.set_title( name_str + '\nCp and Heat of Vaporization' )
    
    cp_max = 0.0 # fix last point being VERY large
    for i,prop in enumerate(propL):
        lab = prop.name + '(%s)'%prop.dataSrc
        
        x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'Cp', 'cpL', 'CpAtTr' )

        ax1.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
        ax1.plot( x_terpL, y_terpL, '-', color=get_color(i) )
        ax1.plot( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )

        cp_max = max(cp_max, 2.0 * y_dataL[-2] )
        
    set_ylabel(ax1, 'Cp', '(BTU/lbm-F)')
    ax1.grid()
    ax1.legend( framealpha=0.5 )

    (ylo, yhi) = ax1.get_ylim()
    if ylo < 0.0:
        ylo = 0.0
    if yhi > cp_max:
        yhi = cp_max
    ax1.set_ylim( [ylo, yhi] )
    
    ax2.grid()
    set_ylabel(ax2, 'Heat of Vaporization', '(BTU/lbm)')
    set_xlabel( ax2 )
    for i,prop in enumerate(propL):
        lab = prop.name + '(%s)'%prop.dataSrc
        
        x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'Hvap', 'hvapL', 'HvapAtTr' )

        ax2.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
        ax2.plot( x_terpL, y_terpL, '-', color=get_color(i) )
        ax2.plot( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
        
    ax2.legend( framealpha=0.5 )
    fig.tight_layout()
        
    if save_figures:
        fname = '%s_CpHvap.png'%name_underscore_str
        plt.savefig(fname)
    
    # ================== Surface Tension and Density =============================
    fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(6,8))
    ax1.set_title( name_str + '\nSurface Tension and Density' )
    
    for i,prop in enumerate(propL):
        if max(prop.surfL) > 0.0:
            lab = prop.name + '(%s)'%prop.dataSrc
        
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'surf', 'surfL', 'SurfAtTr' )

            ax1.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
            ax1.plot( x_terpL, y_terpL, '-', color=get_color(i) )
            ax1.plot( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
            
    set_ylabel(ax1, 'Surface Tension', '(lbf/in)')
    ax1.grid()
    ax1.legend( framealpha=0.5 )
    
    ax2.grid()
    set_ylabel(ax2, 'Specific Gravity', '(SG)')
    set_xlabel( ax2 )
    for i,prop in enumerate(propL):
        lab = prop.name + '(%s)'%prop.dataSrc
        
        x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, 'SG', 'SG_liqL', 'SGLiqAtTr' )

        ax2.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), label=lab, linewidth=0 )
        ax2.plot( x_terpL, y_terpL, '-', color=get_color(i) )
        ax2.plot( x_refL, y_refL, marker=get_marker(i), color=get_color(i), markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )
        
        if show_gas_dens:
            x_refL, y_refL, x_dataL, y_dataL, x_terpL, y_terpL = get_xy_plot_lists( i, '', 'log10SG_vapL', 'SGVapAtTr' )

            ax2.plot( x_dataL, y_dataL, marker=get_marker(i), color=get_color(i), linewidth=0 )
            ax2.plot( x_terpL, y_terpL, '-', color=get_color(i) )
            
    ax2.legend( framealpha=0.5 )
    fig.tight_layout()
        
    if save_figures:
        fname = '%s_SurfSG.png'%name_underscore_str
        plt.savefig(fname)
    
    
    # ========================================================
    if show_plots:
        plt.show()

if __name__ == '__main__':

    from rocketprops.prop_names import prop_names
    

    
    #make_plots( ['A50_scaled', 'A50'], abs_T=0, ref_scaled=False)
    # make_plots( ['MMH', 'N2H4'], abs_T=0, ref_scaled=True)
    
    #make_plots( ['C2H6', 'C3H8', 'CH4'], abs_T=0, ref_scaled=True)
    #make_plots( ['N2O', 'NH3'], abs_T=0, ref_scaled=True)
    # make_plots( ['CH4','LOX','MMH','N2H4','NH3','Propane'], abs_T=0, ref_scaled=True)
    
    #make_plots( ['LOX', 'F2', 'PH2'], abs_T=False, ref_scaled=True)
    #make_plots( ['LOX', 'F2'], abs_T=False, ref_scaled=True)


    # make_plots( ['MON30', 'MON25', 'MON10', 'MON3', 'N2O4'], abs_T=True, 
    #             Tmin=480, Tmax=600, save_figures=False)

    make_plots( ['UDMH','A25', 'A50', 'N2H4'], abs_T=1,
                Tmin=430, Tmax=560, save_figures=False)
