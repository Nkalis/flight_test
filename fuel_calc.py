def fuel_calc(initial_l, initial_r, fuel_lef, fuel_rig): 
     
    import numpy as np 
    import itertools 

    lefttank = initial_l - np.asarray(list(itertools.chain.from_iterable(fuel_lef.get('data')))) 
    righttank = initial_r - np.asarray(list(itertools.chain.from_iterable(fuel_rig.get('data')))) 
     
    return lefttank, righttank