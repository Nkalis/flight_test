def post_flight_data():
    import numpy as np
    
    #------------------------------------------------------------------------------
    """ Open Post Flight Data Sheet csv file """
    f = open("postflightdataex2.csv","r")
    lines = f.readlines()
    f.close()
    
    """ Create an array with all the data """
    datalist = lines
    data = []
    for i in range(84):
        dataline = datalist[i]
        dataline = dataline.split(';')
        dataline = list(dataline)
        data.append(dataline)
    
    """ Remove the \n from the array """
    for j in range(84):
        for k in range(13):
            if '\n' in data[j][k]:
                data[j][k] = data[j][k][:-2]
            else:
                data[j][k] = data[j][k]
    data = np.array(data)
    
    #------------------------------------------------------------------------------
    
    """ Stationary measurements CL-CD series 1 """
    
    # Pressure altitude
    hp = []
    hp1 = data[:,3]
    for i in range(27,33):
        hp.append(float(hp1[i]))
    
    # Indicated airspeed
    IAS = []
    IAS1 = data[:,4]
    for i in range(27,33):
        IAS.append(float(IAS1[i]))
    
    # Angle of attack
    a = []
    a1 = data[:,5]
    for i in range(27,33):
        a.append(float(a1[i]))
    
    # Fuel flow left
    FFl = []
    FFl1 = data[:,6]
    for i in range(27,33):
        FFl.append(float(FFl1[i]))
    
    # Fuel flow right
    FFr = []
    FFr1 = data[:,7]
    for i in range(27,33):
        FFr.append(float(FFr1[i]))
    
    # Fuel used
    F_used = []
    F_used1 = data[:,8]
    for i in range(27,33):
        F_used.append(float(F_used1[i]))
    
    # True air temperature
    TAT = []
    TAT1 = data[:,9]
    for i in range(27,33):
        TAT.append(float(TAT1[i]))
    
    #------------------------------------------------------------------------------
    
    """ Variables """
    rho_0 = 1.225 # kg/m^3 (air density at sea level)
    g = 9.80665 # m/s^2 (gravitational constant)
    
    #------------------------------------------------------------------------------
    
    """ Masses """
    BEM = 13600. # lbs (basic empty mass)
    BFuel = float(data[17][3]) # lbs (block fuel)
    # Payload
    Payl = []
    Payl1 = data[:,7]
    for i in range(7,16):
        Payl.append(float(Payl1[i]))
    Payload = sum(Payl)
    
    """ Unit conversions """
    BEM = BEM * 0.453592 # kg (basic empty mass)
    BFuel = BFuel * 0.453592 # kg (block fuel)
    # kg (fuel used)
    for i in range(len(F_used)):
        F_used[i] = F_used[i] * 0.453592
    
    """ Ramp mass """
    M_r = BEM + BFuel + Payload
    
    """ Total mass at point in time """
    M_t = []
    for i in range(len(F_used)):
        M_t1 = M_r - F_used[i]
        M_t.append(M_t1)
    
    """ Total weight at point in time """
    # N (total weight)
    W_t = []
    for i in range(len(M_t)):
        W_t1 = M_t[i] * g
        W_t.append(W_t1)
        
    return hp, IAS, a, FFl, FFr, F_used, TAT, Payl, Payload, BEM, BFuel, M_r, M_t, W_t

data = post_flight_data()