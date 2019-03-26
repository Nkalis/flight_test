def cg_calculator(x_nic,m_lt,m_rt):
    import numpy as np
    #mass import
    from postflightdata import post_flight_data
    m_people = np.array(post_flight_data()[7])
    #seat positions in meters from nose
    x1 = 131*0.0254
    x2 = 131*0.0254
    x3 = 214*0.0254
    x4 = 214*0.0254
    x5 = 251*0.0254
    x6 = 251*0.0254
    x7 = 288*0.0254
    x10 = 170*0.0254
    x_seats = np.array([x1,x2,x3,x4,x5,x6,x7,x_nic,x10])
    #moment arm empty aircraft
    x_ac = 292.18*0.0254
    m_ac = (post_flight_data()[9])
    #moment arm fuel
    mass = [None]*50
    mass[0] = 0
    value = 0
    for i in range(49):
        value = value+100
        mass[i+1] = value
    mass[49] = 5008
    ma = [0,298.16,591.18,879.08,1165.42,1448.4,1732.53,2014.8,2298.84,2581.92,2866.3,3150.18,3434.52,3718.52,4003.23,4287.76,4572.24,4856.56,5141.16,5425.64,5709.9,5994.94,\
          6278.47,6562.82,6846.96,7131,7415.33,7699.6,7984.34,8269.06,8554.05,8839.04,9124.8,9410.62,9696.97,9983.4,10270.08,10556.84,10843.87,11131,11418.2,11705.5,11993.31,\
          12281.18,12569.04,12856.86,13144.73,13432.48,13720.56,14008.46,14320.34]
    for i in range(len(mass)):
        if m_lt <= mass[i]:
            ma_lt = ma[i-1]+(ma[i]-ma[i-1])/(mass[i]-mass[i-1])*(m_lt-mass[i-1])
            if m_lt != 0:
                m_lt = m_lt*0.45359237
                ma_lt = ma_lt*0.112984829
                x_lt = (ma_lt*100/(m_lt*9.81))
            else:
                x_lt = 0
            break
    for i in range(len(mass)):
        if m_rt <= mass[i]:
            ma_rt = ma[i-1]+(ma[i]-ma[i-1])/(mass[i]-mass[i-1])*(m_rt-mass[i-1])
            if m_lt != 0:
                m_rt = m_rt*0.45359237
                ma_rt = ma_rt*0.112984829
                x_rt = (ma_rt*100/(m_rt*9.81))
            else:
                x_rt = 0
            break
    #cg positions
    cg_people = (np.sum(m_people*x_seats))/np.sum(m_people)
    cg_tot = (cg_people*np.sum(m_people)+x_ac*m_ac+x_lt*m_lt+x_rt*m_rt)/(np.sum(m_people)+m_ac+m_lt+m_rt)
    return cg_tot