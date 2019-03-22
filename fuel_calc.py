def fuel_calc(initial_l, initial_r, fuel_lef, fuel_rig, M_r): 
     
    import numpy as np 
    import itertools 

    lefttank = initial_l - np.asarray(list(itertools.chain.from_iterable(fuel_lef.get('data')))) 
    righttank = initial_r - np.asarray(list(itertools.chain.from_iterable(fuel_rig.get('data'))))
    mass = np.zeros(len(lefttank))
    mass[0:-1] = M_r
    mass = mass + lefttank + righttank
    
    return lefttank, righttank, mass