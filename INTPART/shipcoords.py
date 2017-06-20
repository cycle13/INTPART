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
directorydata = '/Volumes/INTPARTshare/'
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
time,lat,lon = np.genfromtxt(directorydata + 'shipcoords.txt',unpack=True,
                     usecols=[0,1,2])

### Plot coords
### Call parameters
plt.rcParams['text.usetex']=True
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Avant Garde'

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
ax = plt.subplot(121)

latmin = 82
latmax = 75
lonmin = 390
lonmax = 355

m = polar_stere(lonmin,lonmax,latmin,latmax, resolution='h')    
            
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='dimgrey',linewidth=1)
parallels = np.arange(50,90,10)
meridians = np.arange(-180,180,30)
m.drawparallels(parallels,labels=[True,True,True,True],
                linewidth=1,color='k',fontsize=10)
m.drawmeridians(meridians,labels=[False,True,False,True],
                linewidth=1,color='k',fontsize=10)
m.drawlsmask(land_color='dimgrey',ocean_color='mintcream')

cs = m.plot(lon,lat,latlon=True,linewidth=3,color='dodgerblue')

###########################################################################
###########################################################################
###########################################################################
ax = plt.subplot(122)

latmin = 80.2
latmax = 79
lonmin = 371
lonmax = 360

m = polar_stere(lonmin,lonmax,latmin,latmax, resolution='h')    
            
m.drawmapboundary(fill_color='white')
m.drawcoastlines(color='dimgrey',linewidth=2)
m.drawlsmask(land_color='dimgrey',ocean_color='mintcream')

cs = m.plot(lon,lat,latlon=True,linewidth=1,color='dodgerblue')

fig.suptitle(r'\textbf{Ship Track - R/V Lance}',fontsize=13)

fig.subplots_adjust(bottom=0.38)
             
plt.savefig(directoryfigure + 'shiptrack.png',dpi=300)                     