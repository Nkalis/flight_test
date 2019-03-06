import matplotlib.pyplot as plt
import matplotlib.cm

from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize

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
plt.show()