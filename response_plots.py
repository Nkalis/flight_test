def response_plot(timedata, variable1, variable2, time0, time1):
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    time = np.round(np.asarray(timedata.get('data')),3)
    time = np.asarray(timedata.get('data')) - min(time)
    
    startind = list(time).index(time0)
    if str(time1) == "end":
        endind = -1
    else:
        endind = list(time).index(time1)
        
    x = np.asarray(list(itertools.chain.from_iterable(variable1.get('data'))))[startind:endind]
    y = np.asarray(list(itertools.chain.from_iterable(variable2.get('data'))))[startind:endind]
    
    plt.xlabel(str(variable1.get('description')) + ' [' + str(variable1.get('units')) + ']', fontsize=10)
    plt.ylabel(str(variable2.get('description')) + ' [' + str(variable2.get('units')) + ']', fontsize=10)
    
    plt.plot(x,y)
    return plt.show()


def response_plot_full(variable1, variable2):
    import matplotlib.pyplot as plt
    import numpy as np
    import itertools
    
    if variable1 == 'time':
        ''' Getting the time data and zeroing it out'''
        x = np.round(np.asarray(variable1.get('data')),3)
        x = np.asarray(variable1.get('data')) - min(x)
    else:
        x = np.asarray(list(itertools.chain.from_iterable(variable1.get('data'))))
    y = np.asarray(list(itertools.chain.from_iterable(variable2.get('data'))))
    
    plt.xlabel(str(variable1.get('description')) + ' [' + str(variable1.get('units')) + ']', fontsize=10)
    plt.ylabel(str(variable2.get('description')) + ' [' + str(variable2.get('units')) + ']', fontsize=10)
    
    plt.plot(x,y)
    return plt.show()