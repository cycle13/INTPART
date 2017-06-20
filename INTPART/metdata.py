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
print '\n' '---- INTPART Ship Coords - %s ----' % titletime 

###########################################################################
###########################################################################
###########################################################################
### Ship coords
times = np.arange(17,23+1,1)
totaltemps = []
for i in xrange(times.shape[0]):
    day1 = directorydata + '%s052017met.txt' % times[i]
    
    temp = []
    with open(day1, 'r') as f:
        next(f)
        for line in f:
            temp.append(line)
            for skip in range(10):
                try:
                    next(f)
                except StopIteration:
                    break
                
    temp1 = temp[3][26:30]
    temps = []
    for i in xrange(3,len(temp),10):
        data = temp[i]
        temps.append(data)
    temps = np.asarray(temps)
    
    airt = np.empty((temps.shape[0]))
    for i in xrange(len(temps)):
        airt[i] = temps[i][26:30]
    
    fulltemp = np.append(temp1,airt)
    totaltemps.append(fulltemp)
    
totaltemps = np.ravel(np.asarray(totaltemps))
    
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
        
plt.plot(totaltemps,linewidth=2,color='indianred',zorder=2)     
plt.plot([0]*len(totaltemps),linewidth=3,color='k',linestyle='--',zorder=1)

plt.xlim([0,len(totaltemps)])
plt.ylim([-15,15])

fig.suptitle(r'\textbf{Air Temperatures (}$^{\circ}$\textbf{C)}',fontsize=13)   
        
plt.savefig(directoryfigure + 'airtemp.png',dpi=300)                     