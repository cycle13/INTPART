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
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, addcyclic, shiftgrid
import nclcmaps as ncm
import matplotlib
import math

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
year,month,day,latobs,lonobs,sicq = np.genfromtxt(directorydata + \
                                            'SICobs_2017.txt',
                                            skip_header=0,
                                            delimiter=',',
                                            unpack=True)

print 'Completed: Read R/V Lance data!'
                                           
### Alott time series
yearmin = year.min()
yearmax = year.max()
years = np.arange(yearmin,yearmax+1,1)

daymin = day.min()
daymax = day.max()
days = np.arange(daymin,daymax+1,1)

months = np.unique(month)

### Adjust SIC units
sic = sicq 

### Read in AMSR Data
sics = np.empty((len(days),3584, 2432))
for i in xrange(days.shape[0]):
    filename = directorydata + 'sic_05%s2017.nc' % int(days[i])
    data = Dataset(filename)
    ice = data.variables['sea_ice_concentration'][:]
    lat = data.variables['latitude'][:]    
    lon = data.variables['longitude'][:]
    data.close()
    
    ### Mask arrays to make 1-10
    ice = np.asarray(np.squeeze(ice/100.))
    ice[np.where((ice >= 0.999) & (ice <= 1))] = 0.999
    ice[np.where(ice > 1)] = np.nan
    sics[i] = np.rint(ice*10)
    
### Calculate daily mean
sicmean = np.nanmean(sics,axis=0)
    
print 'Completed: Read AMSR data!'

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
       
def polar_stere(lon_w, lon_e, lat_s, lat_n, **kwargs):
    '''Returns a Basemap object (NPS/SPS) focused in a region.
    
    lon_w, lon_e, lat_s, lat_n -- Graphic limits in geographical coordinates.
                                  W and S directions are negative.
    **kwargs -- Aditional arguments for Basemap object.
    
    '''
    lon_0 = lon_w + (lon_e - lon_w) / 2.
    ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
    lat_0 = math.copysign(90., ref)
    proj = 'npstere' if lat_0 > 0 else 'spstere'
    prj = Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                          boundinglat=0, resolution='l')
    #prj = pyproj.Proj(proj='stere', lon_0=lon_0, lat_0=lat_0)
    lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
    lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
    x, y = prj(lons, lats)
    ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
    ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
    return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                       llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                       urcrnrlon=ur_lon, urcrnrlat=ur_lat, round=False,
                       resolution='l') 

fig = plt.figure()                     
ax = plt.subplot(111)

latmin = 81
latmax = 78
lonmin = 390
lonmax = 360

m = polar_stere(lonmin,lonmax,latmin,latmax, resolution='h')    
            
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='dimgrey',linewidth=1)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[True,True,True,True],
                linewidth=1,color='k',fontsize=10)
m.drawmeridians(meridians,labels=[True,True,False,False],
                linewidth=1,color='k',fontsize=10)
m.drawlsmask(land_color='dimgrey',ocean_color='mintcream')

cs = m.contourf(lon,lat,sicmean[:,:],np.arange(0,11,1),latlon=True)

kolor=10
cc1 = cmap_discretize('cubehelix',kolor)        
cs.set_cmap(cc1)

cbar = m.colorbar(cs,location='right',pad = 0.55,drawedges=True)
ticks = np.arange(0,11,2)
labels = map(str,np.arange(0,11,2))
cbar.set_ticklabels(ticks,labels)

perc = r'$\bf{\%}$' 
cbar.set_label(r'\textbf{SIC ($\bf{\times}$10%s)}' % perc,fontsize=13)
cbar.ax.tick_params(axis='y', size=.01)

cs = m.plot(lonship,latship,latlon=True,linewidth=1,color='gold',
            alpha=0.75,zorder=5)
cs = m.scatter(lonobs,latobs,c=sic,latlon=True,cmap=cc1,alpha=0.8,
               marker='o',edgecolors='gold',linewidth=0.3,s=25,
               zorder=6,vmin=0,vmax=10)
               
m.fillcontinents(color='darkgrey')

plt.savefig(directoryfigure + 'sic_AMSR_obs.png',dpi=300)

###########################################################################
###########################################################################
###########################################################################
fig = plt.figure()                     

latmin = 80.3
latmax = 79.4
lonmin = 369
lonmax = 366

m = polar_stere(lonmin,lonmax,latmin,latmax, resolution='h')   

for i in xrange(days.shape[0]):
    
    ax = plt.subplot(2,3,i+1)
    valday = np.where(day == days[i])[0]
    sicday = sic[valday]
    lonobsday = lonobs[valday]
    latobsday = latobs[valday]
            
    m.drawmapboundary(fill_color='white')
    m.drawcoastlines(color='dimgrey',linewidth=1)
    parallels = np.arange(50,90,10)
    meridians = np.arange(-180,180,30)
    m.drawparallels(parallels,labels=[True,True,True,True],
                    linewidth=0.5,color='darkgrey',fontsize=4)
    m.drawmeridians(meridians,labels=[True,True,False,False],
                    linewidth=0.5,color='darkgrey',fontsize=4)
    m.drawlsmask(land_color='dimgrey',ocean_color='mintcream')
    
    cs = m.contourf(lon,lat,sics[i,:,:],np.arange(0,11,1),latlon=True)
    
    kolor=10
    cc1 = cmap_discretize('cubehelix',kolor)        
    cs.set_cmap(cc1)

#cbar = m.colorbar(cs,location='right',pad = 0.55,drawedges=True)
#ticks = np.arange(0,11,2)
#labels = map(str,np.arange(0,11,2))
#cbar.set_ticklabels(ticks,labels)

    cs = m.scatter(lonobsday,latobsday,c=sicday,latlon=True,
                   cmap=cc1,alpha=0.9,marker='o',edgecolors='gold',
                   linewidth=0.5,s=35,zorder=6,vmin=0,vmax=10)          

    m.fillcontinents(color='darkgrey')
    
    ax.text(0.18,0.06,r'\textbf{May %s}' % int(days[i]),size='8',
            ha= 'center',backgroundcolor='white',va= 'center',
            color='k',bbox=dict(facecolor='white',edgecolor='k',alpha=0.9),
                                transform=ax.transAxes) 

cbar_ax = fig.add_axes([0.312,0.105,0.4,0.03])                
cbar = fig.colorbar(cs,cax=cbar_ax,orientation='horizontal')

cbar.set_label(r'\textbf{SIC ($\bf{\times}$10%s)}' % perc,fontsize=13)
barlim = np.arange(0,11,1)
cbar.set_ticks(barlim)
cbar.set_ticklabels(map(str,barlim)) 
cbar.ax.tick_params(axis='x', size=.01)   
    
plt.subplots_adjust(bottom=0.15)
plt.subplots_adjust(wspace=-0.3)
plt.subplots_adjust(hspace=0.05)

plt.savefig(directoryfigure + 'sic_AMSR_obs_zoom.png',dpi=300)

print 'Completed: Plotted figures!'

print 'Completed: Finished script!'