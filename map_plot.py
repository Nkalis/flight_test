def map_plot(timedata, t0, t1, gps_lon, gps_lat, alt):
    
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    from mpl_toolkits.basemap import Basemap
    from matplotlib import cm
    
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
    time = np.round(np.asarray(timedata.get('data')),3)
    time = np.asarray(timedata.get('data')) - min(time)
    
    ''' Indexing where to start plots from '''
    if str(end) == "end":
        endind = -1
    else:
        endind = list(time).index(end)
    startind = list(time).index(start)

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
    lon = np.asarray(list(itertools.chain.from_iterable(gps_lon.get('data'))))[startind:endind]
    lat = np.asarray(list(itertools.chain.from_iterable(gps_lat.get('data'))))[startind:endind]
    alt = np.asarray(list(itertools.chain.from_iterable(alt.get('data'))))[startind:endind]
    print(lon, lat)
    
    xpts, ypts = m(lon, lat)
    lonpts, latpts = m(xpts, ypts, inverse=True)
    
    norm = 1-(((alt-np.min(alt))/(np.max(alt)-np.min(alt))))
    m.scatter(xpts, ypts, marker='o', c=cm.viridis(norm),  edgecolor='none', s=15, zorder=10)
    
    ''' Returning the map plot '''
    return plt.show()