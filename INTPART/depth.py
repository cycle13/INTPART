"""
INTPART Test Script

Author       : Zachary Labe
Reference    : INTPART Arctic Summer Field School 2017
Data         : 27 May 2017 [DAY 3]
"""

### Import modules
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
import operator

### Current directories
directorydata = '/Volumes/INTPARTshare/Position_Data/Lance_track/'
directoryfigure = '/Users/zlabe/desktop/INTPART/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print '\n' '---- INTPART Depth - %s ----' % titletime 

###########################################################################
###########################################################################
###########################################################################
### Wind data
times = np.arange(17,24+1,1)
depthsq = []
for i in xrange(times.shape[0]):
    day = directorydata + '%s052017depth.txt' % times[i]
    depth = np.genfromtxt(day,unpack=True,delimiter=',',usecols=[4])
    list(depth)
    depthsq.append(depth)

depths = [item for sublist in depthsq for item in sublist]
    
### Plot coords
### Call parameters
plt.rcParams['text.usetex']=True
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avant Garde'

fig = plt.figure()                     
ax = plt.subplot(111)

def adjust_spines(ax, spines):
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))
        else:
            spine.set_color('none')  
    if 'left' in spines:
        ax.yaxis.set_ticks_position('left')
    else:
        ax.yaxis.set_ticks([])

    if 'bottom' in spines:
        ax.xaxis.set_ticks_position('bottom')
    else:
        ax.xaxis.set_ticks([]) 

adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('darkgrey')
ax.spines['bottom'].set_color('darkgrey')
ax.tick_params('both',length=4,width=1.5,which='major',color='darkgrey')
 
plt.plot(depths,linewidth=1,linestyle='-',color='m')      
plt.xlim([0,len(depths)])

plt.gca().invert_yaxis()

fig.suptitle(r'\textbf{Depth (m)}',fontsize=13)   
        
plt.savefig(directoryfigure + 'depth.png',dpi=300)                     