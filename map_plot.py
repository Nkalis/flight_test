def map_plot(t0, t1):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    from mpl_toolkits.basemap import Basemap
    from data_extractor import data_extractor
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
    start = t0
    end = t1
    
    ''' Getting the time data and zeroing it out'''
    time = np.round(np.asarray(flightdata.get('time').get('data')),3)
    time = np.asarray(flightdata.get('time').get('data')) - min(time)
    
    ''' Indexing where to start plots from '''
    if str(end) == "end":
        endind = -1
    else:
        endind = list(time).index(end)
    startind = list(time).index(start)
    
    ''' Getting the altitude data '''
    alt = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Dadc1_bcAlt').get('data'))))
    
    ''' Setting up the basemap plot '''
    m = Basemap(resolution='i', # c, l, i, h, f or None
                projection='cyl',
                lat_0=(westlimit+eastlimit)/2, lon_0=(southlimit+northlimit)/2,
                llcrnrlon=westlimit, llcrnrlat= southlimit, urcrnrlon=eastlimit, urcrnrlat=northlimit, epsg=3035)
    
    ''' Including parameters for the map plot'''
    '''         Uncomment below for less detailed plot      '''
    m.drawmapboundary(fill_color='#46bcec')
    m.fillcontinents(color='#eeeeee',lake_color='#46bcec')
    m.drawrivers(linewidth=1, color='#46bcec', antialiased=1, ax=None, zorder=None)
    m.drawcountries(color = "black")
    m.drawcoastlines()
    '''         Uncomment below for detailed plot           '''
    #m.arcgisimage(service = "World_Shaded_Relief", xpixels=8000) #uncomment this for super high res image
    
    '''drawing the meridian and parralel lines, labels = [left,right,top,bottom] '''
    m.drawmeridians(np.arange(0, 360, 0.5), labels=[False,True,True,False])
    m.drawparallels(np.arange(-90, 90, 0.25), labels=[True,False,False,True])
    
    '''Plotting location of Rotterdam Airport'''
    rotlat = 51.9555
    rotlon = 4.4399
    
    xpt, ypt = m(rotlon, rotlat)
    lonpt, latpt = m(xpt, ypt, inverse=True)
    m.scatter(xpt, ypt, marker='D',color='r', s=10, zorder=11)
    
    '''Plotting Flight GPS Data '''
    lon = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_long').get('data'))))
    lat = np.asarray(list(itertools.chain.from_iterable(flightdata.get('Gps_lat').get('data'))))
    
    xpts, ypts = m(lon, lat)
    lonpts, latpts = m(xpts, ypts, inverse=True)
    
    norm = 1-np.asarray(list(((alt[startind:endind]-min(alt[startind:endind]))/(max(alt[startind:endind])-min(alt[startind:endind])))))
    m.scatter(xpts[startind:endind], ypts[startind:endind], marker='o', c=cm.viridis(norm),  edgecolor='none', s=15, zorder=10)
    
    ''' Returning the map plot '''
#    return plt.show()
    return flightdata

m = map_plot(0, 10)