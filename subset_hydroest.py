###SUBSET HOURLY NOAA HYDRO-ESTIMATOR PRODUCT
##############################
##IMPORT MODULES
import datetime as dt
import pytz
import urllib2
import struct
import numpy as np
import gzip
import os
##############################
##USER INPUTS
rawhead = '/d2/dbroman/hydroestimator/raw/'
rawid = 'world1hr.'
rawext = '.gz'
# dattyp_raw = # not defined for hydroestimator
subhead = '/d2/dbroman/hydroestimator/india/' 
subid = 'hydroest_indiasub.'
subext = '.bin'
dattyp_sub = 'int16'
##############################
lonlen = 8001 #from documentation
latlen = 3111 #from documentation
lonvec = np.loadtxt('/d2/dbroman/hydroestimator/dims/hydroest_lons.txt')
latvec = np.loadtxt('/d2/dbroman/hydroestimator/dims/hydroest_lats.txt')
##############################
lonbounds = [73 , 98] #lon subset bounds
latbounds = [22 , 32] #lat subset bounds
##############################
##FIND SUBSET INDICES AND BUILD SUBSET FILE PATH
d = dt.datetime.now(tz = pytz.utc) - dt.timedelta(hours = hlag)
year = str(d.year)
month = str('%02d' % (int(d.month)))
day = str('%02d' % (int(d.day)))
doy = str('%02d' % int(d.strftime('%j')))
hour = str('%02d' % (int(d.hour)))
hoursav = str('%04d' % (int(hour) * 100))
##############################
latli = np.argmin(np.abs(latvec - latbounds[0]))
latui = np.argmin(np.abs(latvec - latbounds[1]))
lonli = np.argmin(np.abs(lonvec - lonbounds[0]))
lonui = np.argmin(np.abs(lonvec - lonbounds[1]))
rawsav = rawhead + rawid + year + month + day + '.' + hoursav + rawext
subsav = subhead + subid + year + month + day + '.' + hoursav + subext
##############################
if os.path.isfile(subsav) is False:
    try:
        varin = gzip.open(rawsav).read() #open file into np array
        vartem = [int(i) for i in varin.split()]
        var = np.array(vartem[2:]).reshape(latlen, lonlen).swapaxes(1,0) #reshape raw data to lon, lat dims
        var = (var - 2) * 0.30 #convert to mm (see documentation)
        var = np.flipud(var) #flip array lat
        var = np.fliplr(var) #flip array lon
        varsub = var[lonli:lonui, latli:latui] #subset to india
        varsub.astype(dattyp_sub).tofile(subsav) #save subset to file
        except (RuntimeError, TypeError, NameError, IOError):
            continue
