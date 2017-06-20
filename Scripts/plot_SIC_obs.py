"""
Script plots sea ice concentration observations from the R/V Lance
in the Fram Strait during May 19-23rd.
 
Notes
-----
    Author : Zachary Labe
    Date   : 20 June 2017
"""

### Import modules
import datetime
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import nclcmaps as ncm
import matplotlib

### Define directories
directorydata = '/home/zlabe/Documents/Projects/INTPART/Data/'
directoryfigure = '/home/zlabe/Documents/Projects/INTPART/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print '\n' '----Plot SIC in situ observations - %s----' % titletime 

### Read in ship coords
time,latship,lonship = np.genfromtxt(directorydata + 'shipcoords.txt',
                                     unpack=True,
                                     usecols=[0,1,2])

### Read in sic data 
year,month,day,lat,lon,sicq = np.genfromtxt(directorydata + \
                                            'SICobs_2017.txt',
                                            skip_header=0,
                                            delimiter=',',
                                            unpack=True)

print 'Completed: Read data!'
                                           
### Alott time series
yearmin = year.min()
yearmax = year.max()
years = np.arange(yearmin,yearmax+1,1)

daymin = day.min()
daymax = day.max()
days = np.arange(daymin,daymax+1,1)

months = np.unique(month)

### Adjust SIC units
sic = sicq * 100.

### Plot Figure
plt.rc('text',usetex=True)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Avant Garde']}) 

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
        
def cmap_discretize(cmap, N):
       """Return a discrete colormap from the continuous colormap cmap.
     
           cmap: colormap instance, eg. cm.jet. 
           N: number of colors.
     
       Example
           x = resize(arange(100), (5,100))
           djet = cmap_discretize(cm.jet, 5)
           imshow(x, cmap=djet)
       """
       
       if type(cmap) == str:
           cmap = plt.get_cmap(cmap)
       colors_i = np.concatenate((np.linspace(0, 1., N), (0.,0.,0.,0.)))
       colors_rgba = cmap(colors_i)
       indices = np.linspace(0, 1., N+1)
       cdict = {}
       for ki,key in enumerate(('red','green','blue')):
           cdict[key] = [ (indices[i], colors_rgba[i-1,ki], colors_rgba[i,ki]) for i in xrange(N+1) ]
       # Return colormap object.
       return matplotlib.colors.LinearSegmentedColormap(cmap.name + "_%d"%N, cdict, 1024)

plt.figure()
ax = plt.subplot(111)
adjust_spines(ax, ['left', 'bottom'])
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
ax.spines['left'].set_color('darkgrey')
ax.spines['bottom'].set_color('darkgrey')
ax.tick_params('both',length=4,width=1.5,which='major',color='darkgrey')

kolor=10
cc = cmap_discretize('plasma',kolor)

plt.plot(lonship,latship,linestyle='-',color='dimgrey',
         linewidth=1,zorder=1,label=r'\textbf{R/V Lance}')
plt.scatter(lon,lat,c=sic,cmap=cc,edgecolors='dimgrey',s=40,
            linewidth=0.2,alpha=0.7,zorder=2)

plt.yticks(np.arange(78.8,80.6,0.2),map(str,np.arange(78.8,80.6,0.2)),
           rotation=0,fontsize=10)
plt.xticks(np.arange(6,13,1),map(str,np.arange(6,13,1)),
           rotation=0,fontsize=10)
plt.xlim([6,12])
plt.ylim([78.8,80.40001])
           
plt.xlabel(r'\textbf{Longitude}',fontsize=11)
plt.ylabel(r'\textbf{Latitude}',fontsize=11)

plt.legend(shadow=False,fontsize=11,loc='center',
                       fancybox=True,ncol=4,bbox_to_anchor=(0.123,0.05),
                        frameon=False)

###########################################################################
a = plt.axes([.65, .5, .25, .4], axisbg='w')
for axis in ['top','bottom','left','right']:
  a.spines[axis].set_linewidth(2)
  a.spines[axis].set_color('darkgrey')
a.tick_params('both',length=4,width=2,which='major',color='darkgrey')
a.set_axis_bgcolor('lightcyan')

plt.plot(lonship,latship,linestyle='-',color='dimgrey',
         linewidth=1,zorder=1)
cs = a.scatter(lon,lat,c=sic,cmap=cc,edgecolors='dimgrey',s=27,
            linewidth=0.1,alpha=0.8,zorder=2)  
            
plt.yticks(np.arange(78.8,80.6,0.2),map(str,np.arange(78.8,80.6,0.2)),
           rotation=0,fontsize=6)
plt.xticks(np.arange(6,13,1),map(str,np.arange(6,13,1)),
           rotation=0,fontsize=6)
a.tick_params(axis='x',direction='out')
a.tick_params(axis='y',direction='out')
plt.xlim([6,8])
plt.ylim([79.8,80.2])

cbar = plt.colorbar(cs,orientation='bottom',
             drawedges=False)

labels = map(str,np.arange(0,101,10))
cbar.ax.set_xticklabels(labels,fontsize=7)
cbar.ax.tick_params(axis='x', size=.01)
cbar.set_label(r'\textbf{Sea Ice Concentration}',fontsize=8,
               color='darkgrey')
cbar.outline.set_edgecolor('darkgrey')
cbar.outline.set_linewidth(0.5)

plt.subplots_adjust(bottom=0.15)

plt.savefig(directoryfigure + 'sic_obs.png',dpi=300)

print 'Completed: Plotted figure!'

print 'Completed: Finished script!'