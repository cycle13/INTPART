"""
INTPART plots sea ice extent for the Greenland Sea

Author       : Zachary Labe
Reference    : INTPART Arctic Summer Field School 2017
Date         : 28 June 2017
"""

### Import modules
import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
import calendar as cal

### Current directories
directorydata = '/home/zlabe/Documents/Projects/INTPART/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/INTPART/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print '\n' '---- Greenland Sea SIE - %s ----' % titletime 

###########################################################################
###########################################################################
###########################################################################
### Sea ice extent
data = np.genfromtxt(directorydata + 'GreenlandSeaDaily.txt',
                     unpack=True,delimiter=',',skip_header=1,
                     usecols=np.arange(1,42,1))
days = data[0]  

totaldays = 0.
for i in xrange(5):
    totaldays += cal.monthrange(2016,i+1)[1]

sieall = data[1:,:] / 1e6
sie = data[1:,:int(totaldays)] / 1e6
siemay = sie[:,-31:] 

###########################################################################
###########################################################################
###########################################################################
### Call parameters
plt.rcParams['text.usetex']=True
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avant Garde'

### Plot time series
fig = plt.figure()
ax = plt.subplot(111)

### Adjust axes in time series plots 
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
    
### Call parameters
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('darkgrey')
ax.spines['bottom'].set_color('darkgrey')
ax.tick_params('both',length=4,width=1.5,which='major',color='darkgrey')

color=iter(plt.cm.viridis(np.linspace(0,1,sieall.shape[0])))
for i in xrange(sieall.shape[0]):
    c=next(color)
    plt.plot(sieall[i],linewidth=0.9,color=c,alpha=1)

plt.plot(sieall[-1],linewidth=2.3,color='r',linestyle='-')   

xlabels = [r'Jan',r'Feb',r'Mar',r'Apr',r'May',r'Jun',r'Jul',
          r'Aug',r'Sep',r'Oct',r'Nov',r'Dec',r'Jan'] 
plt.xticks(np.arange(0,366,30.4),xlabels,rotation=0,fontsize=9)
plt.yticks(np.arange(0,1.4,0.2),map(str,np.arange(0,1.4,0.2)),
           rotation=0,fontsize=9)
plt.xlim([0,365])
plt.ylabel(r'\textbf{Sea Ice Extent} [$\times$10$^{6}$ \textbf{km}$^2$]',
           fontsize=11,labelpad=3)
           
plt.text(0,0,r'\textbf{GREENLAND SEA}',fontsize=20,color='darkgrey',
         ha='left')           

###########################################################################
###########################################################################
###########################################################################
a = plt.axes([.555, .69, .25, .25], axisbg='w')

a.spines['top'].set_linewidth(2)
a.spines['right'].set_linewidth(2) 
a.spines['bottom'].set_linewidth(2)
a.spines['left'].set_linewidth(2)
a.spines['top'].set_color('k')
a.spines['right'].set_color('k')
a.spines['bottom'].set_color('k')
a.spines['left'].set_color('k')
a.tick_params('both',length=4,width=2,which='major',color='k',
              direction='outward') 
        
color=plt.cm.viridis(np.linspace(0,1,siemay.shape[0]))
for i,c in zip(xrange(siemay.shape[0]),color):
    if i == (siemay.shape[0]-1):
        c = 'red'
        l = 2.3
    else:
        l = 0.7   
    plt.plot(siemay[i],c=c,linewidth=l,zorder=1)
plt.axvline(17,linestyle='-',linewidth=2,color='k')
plt.axvline(23,linestyle='-',linewidth=2,color='k')
plt.xlim([0,30])
plt.ylim([0.5,1.1])
labelsx2 = map(str,np.arange(1,32,3))
labelsy2 = map(str,np.arange(0.5,1.2,0.25))
plt.xticks(np.arange(0,31,3),labelsx2,fontsize=7)
plt.yticks(np.arange(0.5,1.2,0.25),labelsy2,fontsize=7)
plt.ylabel(r'\textbf{SIE} [$\times$10$^{6}$ \textbf{km}$^2$]',fontsize=9,
           labelpad=1)
plt.xlabel(r'\textbf{May}',fontsize=9,labelpad=1)

plt.savefig(directoryfigure + 'GreenlandSea_SIE.png',dpi=300)