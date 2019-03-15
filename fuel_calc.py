def fuel_calc(initial_l, initial_r, fuel_lef, fuel_rig, timedata, t):
    
    import numpy as np
    import itertools
    
    time = np.round(np.asarray(timedata.get('data')),3)
    time = np.asarray(timedata.get('data')) - min(time)
    
    if str(t) == "end":
        index = -1
    else:
        index = list(time).index(t)
    
    lefttank = initial_l - np.asarray(list(itertools.chain.from_iterable(fuel_lef.get('data'))))[index]
    righttank = initial_r - np.asarray(list(itertools.chain.from_iterable(fuel_rig.get('data'))))[index]
    
    return lefttank, righttank