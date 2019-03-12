import matplotlib.pyplot as plt
import numpy as np
import itertools

from mpl_toolkits.basemap import Basemap
from data_extractor import data_extractor
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm

'''Extracting the flight data from matlab.mat'''
flightdata = data_extractor()

''' Setting up the map boundaries'''
westlimit = 3.25
southlimit = 51.5
eastlimit = 6.25
northlimit = 52.5

'''Plotting the map data'''
fig, ax = plt.subplots(figsize=(10,20))

''' Selecting range of data'''
start = 0
end = 3450

time = np.round(np.asarray(flightdata.get('time').get('data')),3)
time = np.asarray(flightdata.get('time').get('data')) - min(time)

alt = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Dadc1_bcAlt').get('data'))))

startind = list(time).index(start)
endind = list(time).index(end)

plt.subplot(2, 1, 1)
m = Basemap(resolution='h', # c, l, i, h, f or None
            projection='cyl',
            lat_0=(westlimit+eastlimit)/2, lon_0=(southlimit+northlimit)/2,
            llcrnrlon=westlimit, llcrnrlat= southlimit, urcrnrlon=eastlimit, urcrnrlat=northlimit, epsg=3035)

m.drawmapboundary(fill_color='#46bcec')
m.fillcontinents(color='#eeeeee',lake_color='#46bcec')
m.drawrivers(linewidth=1, color='#46bcec', antialiased=1, ax=None, zorder=None)
m.drawcountries(color = "black")
m.drawcoastlines()
#m.arcgisimage(service = "World_Shaded_Relief", xpixels=20000) #uncomment this for super high res image

# labels = [left,right,top,bottom]
m.drawmeridians(np.arange(0, 360, 0.5), labels=[False,True,True,False])
m.drawparallels(np.arange(-90, 90, 0.25), labels=[True,False,False,True])

'''Location of Rotterdam Airport'''
rotlat = 51.9555
rotlon = 4.4399

xpt, ypt = m(rotlon, rotlat)
lonpt, latpt = m(xpt, ypt, inverse=True)
m.scatter(xpt, ypt, marker='D',color='r', s=10, zorder=11)

''' Flight GPS Data '''
lon = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_long').get('data'))))
lat = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_lat').get('data'))))

xpts, ypts = m(lon, lat)
lonpts, latpts = m(xpts, ypts, inverse=True)

norm = 1-np.asarray(list(((alt[startind:endind]-min(alt[startind:endind]))/(max(alt[startind:endind])-min(alt[startind:endind])))))

#m.scatter(xpts[startind:endind], ypts[startind:endind], c=cm.hot(norm),  edgecolor='none')
m.scatter(xpts[startind:endind], ypts[startind:endind], marker='o', c=cm.viridis(norm),  edgecolor='none', s=15, zorder=10)

plt.subplot(2, 1, 2)
plt.plot(time[startind:endind], alt[startind:endind])
plt.xlabel('Time [s]', fontsize=10)
plt.ylabel('Altitude [ft]', fontsize=10)

plt.show()