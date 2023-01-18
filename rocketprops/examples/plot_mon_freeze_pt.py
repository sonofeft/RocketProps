

from rocketprops.mixing_functions import Mnn_Freeze_terp, MON_Freeze_terp, Axx_Freeze_terp
from pylab import *
MARKERL = ['o','v','^','<','>','d','X','P','s','p','*','.']
COLORL = ['r', 'g','b','y','#FFA500','m','c']


wtPcentONL       = [0.0,    2.54567, 5.03106,7.51645,10.0684,12.5477,15.0717,17.0373,18.8689,20.0974,22.0183,22.6214,23.8275,25.1454,26.6196,27.6917,28.8085,29.7913,30.7294,31.5335,32.293,33.0077,33.7895,35.018,37.5197,40.0213]
MONfreezeL_degRL = [471.241,466.135, 461.159,455.529,449.709,443.27,436.026,429.945,423.596,418.23,409.824,406.336,399.897,391.223,380.223,370.297,360.281,350.354,340.338,330.054,320.306,310.111,298.486,303.315,308.502,310.737]

i_last = len( wtPcentONL ) -1
for i,v in enumerate(wtPcentONL):
    i_last = i
    if v > 30.0:
        break

fig, ax = subplots()

terpL = [MON_Freeze_terp]
dataL = [ (wtPcentONL, MONfreezeL_degRL)]

n2o4_Tfreeze = 471.4
mon10_Tfreeze = 450.0
mon25_Tfreeze  = 389.1
mon30_Tfreeze = 345.9

for i,additive in enumerate([ 'AFRPL-TR-76-76 data']):
    xL = []
    yL = []
    for pcent in range(0, 31, 1):
        xL.append( pcent )
        yL.append( terpL[i](pcent) )

    # Generate data...
    plot( xL, yL, COLORL[i], color=COLORL[i], linewidth=5 ) # , label=additive

    xL,yL = dataL[i]
    plot( xL[:i_last], yL[:i_last], label=additive, marker=MARKERL[i], color=COLORL[i], 
                  markersize=10, linewidth=0, markeredgecolor='k', alpha=.5 )

text(0.0, n2o4_Tfreeze+4, 'N2O4', ha='center', rotation=-12)
text(10, mon10_Tfreeze+4, 'MON10', ha='center', rotation=-23)
text(25, mon25_Tfreeze+7, 'MON25', ha='center', rotation=-45)
text(30, mon30_Tfreeze+7, 'MON30', ha='center', rotation=-60)

legend()
grid( True )
title('Freezing Points of Mixed Oxides of Nitrogen')
ylabel('Freezing Point (degR)')
xlabel('Weight Percentage of NO')

# majorFormatter = FormatStrFormatter('%g')
# gca().xaxis.set_major_formatter(majorFormatter)

ax.tick_params(axis='y', which='major', labelsize=10)

savefig( 'mon_corr_freeze_pts.png' )
show() 

