import matplotlib.pyplot as plt
import numpy as np
import itertools

from mpl_toolkits.basemap import Basemap
from data_extractor import data_extractor

'''Extracting the flight data from matlab.mat'''
flightdata = data_extractor()

''' Setting up the map boundaries'''
westlimit = 3.06
southlimit = 51.23
eastlimit = 6.70
northlimit = 52.56 

'''Plotting the map'''
fig, ax = plt.subplots(figsize=(10,20))

m = Basemap(resolution='h', # c, l, i, h, f or None
            projection='merc',
            lat_0=(westlimit+eastlimit)/2, lon_0=(southlimit+northlimit)/2,
            llcrnrlon=westlimit, llcrnrlat= southlimit, urcrnrlon=eastlimit, urcrnrlat=northlimit)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#f2f2f2',lake_color='#46bcec')
m.drawcountries(color = "black")
m.drawcoastlines()


'''Location of Rotterdam Airport'''
rotlat = 51.9555
rotlon = 4.4399

xpt, ypt = m(rotlon, rotlat)
lonpt, latpt = m(xpt, ypt, inverse=True)
m.plot(xpt, ypt, marker='D',color='r')


''' Flight GPS Data '''
lon = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_long').get('data'))))
lat = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_lat').get('data'))))

alt = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Dadc1_bcAlt').get('data'))))
time = flightdata.get('time').get('data')

xpts, ypts = m(lon, lat)
lonpts, latpts = m(xpts, ypts, inverse=True)
m.plot(xpts, ypts, color = 'm')

plt.show()