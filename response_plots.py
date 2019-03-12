def response_plot(variable1, variable2, time0, time1):
    from data_extractor import data_extractor
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    '''Extracting the flight data from matlab.mat'''
    flightdata = data_extractor()
    
    
    if str(variable1) == "time":
        
        ''' Getting the time data and zeroing it out'''
        x = np.round(np.asarray(flightdata.get('time').get('data')),3)
        x = np.asarray(flightdata.get('time').get('data')) - min(x)
        
        if str(time1) == "end":
            endind = -1
        else:
            endind = list(x).index(time1)
        startind = list(x).index(time0)
            
    else:
        x = np.asarray(list(itertools.chain.from_iterable(flightdata.get(variable1).get('data'))))
        
    x = x[startind:endind]
    y = np.asarray(list(itertools.chain.from_iterable(flightdata.get(variable2).get('data'))))[startind:endind]
    
    plt.xlabel(str(flightdata.get(variable1).get('description')) + ' [' + str(flightdata.get(variable1).get('units')) + ']', fontsize=10)
    plt.ylabel(str(flightdata.get(variable2).get('description')) + ' [' + str(flightdata.get(variable2).get('units')) + ']', fontsize=10)
    
    plt.plot(x,y)
    return plt.show()


def response_plot_all(variable1, variable2):
    from data_extractor import data_extractor
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    '''Extracting the flight data from matlab.mat'''
    flightdata = data_extractor()
    
    if variable1 == 'time':
        x = np.round(np.asarray(flightdata.get('time').get('data')),3)
        x = np.asarray(flightdata.get('time').get('data')) - min(x)
    else:
        x = np.asarray(list(itertools.chain.from_iterable(flightdata.get(str(variable1)).get('data'))))
    y = np.asarray(list(itertools.chain.from_iterable(flightdata.get(str(variable2)).get('data'))))
    
    plt.xlabel(str(flightdata.get(variable1).get('description')) + ' [' + str(flightdata.get(variable1).get('units')) + ']', fontsize=10)
    plt.ylabel(str(flightdata.get(variable2).get('description')) + ' [' + str(flightdata.get(variable2).get('units')) + ']', fontsize=10)
    
    plt.plot(x,y)
    return plt.show()

response_plot('time', 'Dadc1_bcAlt', 3200, 3450)