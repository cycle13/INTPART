"""
INTPART Test Script

Author       : Zachary Labe
Reference    : INTPART Arctic Summer Field School 2017
Data         : 27 May 2017 [DAY 3]
"""

### Import modules
import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import datetime
#from PIL import Image
from skimage import io
from skimage import external
import gdal

### Current directories
directorydata = '/Volumes/INTPARTshare/'
directoryfigures = '/Users/zlabe/desktop/INTPART/Figures/'

### Define time           
now = datetime.datetime.now()
currentmn = str(now.month)
currentdy = str(now.day)
currentyr = str(now.year)
currenttime = currentmn + '_' + currentdy + '_' + currentyr
titletime = currentmn + '/' + currentdy + '/' + currentyr
print '\n' '---- INTPART TEST - %s ----' % titletime 

###########################################################################
###########################################################################
###########################################################################
### Day 1

### TIF practice
#im = io.imread(directorydata + 'RS2/ScanSAR/RS2-SLC-FQ30-DES-20-May-2017_06.14-SAR_PF-1495438173_Cal_Spk_ML_EC.tif')
#
#imq = im[:,:,0]
#imnorm = ((imq - np.nanmin(imq)) / (np.nanmax(imq) - np.nanmin(imq)))
#
#plt.figure()
#ax = plt.subplot(111)
#ax.imshow(imnorm,cmap='inferno',zorder=1)
##ax.plot(462177.3,8899791.4,marker='o', markersize=20, color='r',zorder=2)
#plt.savefig(directoryfigures + 'test.png',dpi=250)
#
#with external.tifffile.TiffFile(directorydata + 'RS2/ScanSAR/RS2-SLC-FQ30-DES-20-May-2017_06.14-SAR_PF-1495438173_Cal_Spk_ML_EC.tif') as tif:
#     data = tif.pages

gtif = gdal.Open(directorydata + 'RS2/ScanSAR/RS2-SLC-FQ30-DES-20-May-2017_06.14-SAR_PF-1495438173_Cal_Spk_ML_EC.tif')
print gtif.GetMetadata()
srcband = gtif.GetRasterBand(1)