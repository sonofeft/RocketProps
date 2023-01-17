

from rocketprops.mixing_functions import Mnn_Freeze_terp, MON_Freeze_terp, Axx_Freeze_terp
from pylab import *
MARKERL = ['o','v','^','<','>','d','X','P','s','p','*','.']
COLORL = ['r', 'g','b','y','#FFA500','m','c']

wtPcentMMHL =       [0.0,    16.1057,26.3705,35.4891,43.3123,50.8364,59.9052, 86.0,    100.0]
pcentMMH_FreezeRL = [494.4204, 485.91, 479.3688, 472.7538, 466.5024, 459.8874, 451.1646, 394.6698, 397.3698] # degR
#                   N2H4                                                              MMH

wtPcentUdmhL = [0.0,  0.509356, 5.5297, 10.5275, 15.5006, 20.4669, 25.3909, 30.2954, 35.169, 40.0084, 44.8015, 49.5659, 54.2762, 58.9317, 100.0]
Axx_Freeze_degRL = [494.42, 494.973, 494.6094, 493.9272, 492.9858, 491.8734, 490.4586, 488.8638, 487.0782, 485.0856, 482.8608, 480.4902, 477.9126, 475.0776, 388.73]
#                   N2H4  ---> UDMH

fig, ax = subplots()

terpL = [Axx_Freeze_terp,  Mnn_Freeze_terp]
dataL = [ (wtPcentUdmhL, Axx_Freeze_degRL),  (wtPcentMMHL, pcentMMH_FreezeRL)]

mhf3_Tfreeze = 394.67
n2h4_Tfreeze = 494.42
mmh_Tfreeze  = 397.37
udmh_Tfreeze = 388.73

for i,additive in enumerate([ 'UDMH data', 'MMH data']):
    xL = []
    yL = []
    for pcent in range(0, 101, 1):
        xL.append( pcent )
        yL.append( terpL[i](pcent) )

    # Generate data...
    plot( xL, yL, COLORL[i], color=COLORL[i] ) # , label=additive

    xL,yL = dataL[i]
    plot( xL, yL, label=additive, marker=MARKERL[i], color=COLORL[i], 
                  markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )

text(86.0, mhf3_Tfreeze-7, 'MHF3', ha='center')
text(0, n2h4_Tfreeze-7, 'N2H4', ha='center')
text(103, mmh_Tfreeze, 'MMH', ha='left')
text(103, udmh_Tfreeze, 'UDMH', ha='left')

legend()
grid( True )
title('Freezing Points of Hydrazine Mixtures')
ylabel('Freezing Point (degR)')
xlabel('Weight Percentage of Additive')

# majorFormatter = FormatStrFormatter('%g')
# gca().xaxis.set_major_formatter(majorFormatter)

ax.tick_params(axis='y', which='major', labelsize=10)

savefig( 'n2h4_mixture_freeze_pts.png' )
show() 

