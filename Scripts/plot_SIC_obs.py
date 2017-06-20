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

### Read in data 
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

print 'Completed: Plotted figure!'

print 'Completed: Finished script!'