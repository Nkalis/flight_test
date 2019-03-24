def response_plot_data(timedata, variable1, variable2, time0, time1): 
    import matplotlib.pyplot as plt 
    import numpy as np 
    import itertools 
     
    time = np.round(np.asarray(timedata.get('data')),3) 
     
    if time0 == 'start': 
        startind = 0 
    else: 
        startind = list(time).index(time0) 
    if time1 == 'end': 
        endind = -1 
    else: 
        endind = list(time).index(time1) 
    if variable1.get('description') == 'Time': 
        x = time[startind:endind] 
    else: 
        x = np.asarray(list(itertools.chain.from_iterable(variable1.get('data'))))[startind:endind] 
    y = np.asarray(list(itertools.chain.from_iterable(variable2.get('data'))))[startind:endind] 
     
    plt.xlabel(str(variable1.get('description')) + ' [' + str(variable1.get('units')) + ']', fontsize=10) 
    plt.ylabel(str(variable2.get('description')) + ' [' + str(variable2.get('units')) + ']', fontsize=10) 
     
    plt.plot(x,y) 
    return plt.show() 
 
def state_space_plot(data, dist_input, motion): 
    import numpy as np 
    import control.matlab as control 
    import matplotlib.pyplot as plt 
    from state_space_con import state_space_conv 
    
    X0 = np.transpose(np.matrix([95, data[3], data[2], 0]))
#    X0 = np.transpose(np.matrix([0, 0, 0, 0]))
    states = state_space_conv(data)
    symsys = states[0]
    asymsys = states[2]
     
    if motion == 'phugoid': 
         
        timesim = 400 
        t = np.linspace(0, timesim, 1001) 
        U = np.zeros(len(t)) 
        U[0:90]= dist_input 
        yout, T, xout = control.lsim(symsys, U, t, X0) 
         
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Symmetric Flight - Phugoid Motion') 
        T = np.ndarray.tolist(T)
        yout = np.ndarray.tolist(yout)
        
        ax1.plot(T[T.index(100):T.index(220)], np.transpose(yout)[0][T.index(100):T.index(220)]) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Velocity [m/s]') 
         
        ax2.plot(T[T.index(100):T.index(220)], np.rad2deg(np.transpose(yout)[1][T.index(100):T.index(220)])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Angle of Attack [deg]') 
         
        ax3.plot(T[T.index(100):T.index(220)], np.rad2deg(np.transpose(yout)[2][T.index(100):T.index(220)])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Angle [deg]')# 
         
        ax4.plot(T[T.index(100):T.index(220)], np.rad2deg(np.transpose(yout)[3][T.index(100):T.index(220)])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Rate [deg/s]') 
        return plt.show() 
     
    if motion == 'short': 
         
        timesim = 20 
        t = np.linspace(0, timesim, 1001) 
        U = np.zeros(len(t)) 
        U[0:-1]= dist_input 
        yout, T, xout = control.lsim(symsys, U, t, X0) 
         
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Symmetric Flight - Short Period Motion') 
         
        ax1.plot(T, np.transpose(yout)[0]) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Velocity [m/s]') 
         
        ax2.plot(T, np.rad2deg(np.transpose(yout)[1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Angle of Attack [deg]') 
         
        ax3.plot(T, np.rad2deg(np.transpose(yout)[2])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Angle [deg]')# 
         
        ax4.plot(T, np.rad2deg(np.transpose(yout)[3])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Rate [deg/s]') 
        return plt.show() 
    
    if motion == 'aperiodic':
        
        timesim = 20
        t = np.linspace(0, timesim, 1001)
        U1, U2 = np.zeros(len(t)),np.zeros(len(t))
        U1[0:30] = dist_input 
        U = np.transpose(np.matrix([U1, U2]))

        yout, T, xout = control.lsim(asymsys, U, t, X0)
        
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Asymmetric Flight - Aperiodic Roll Motion') 
         
        ax1.plot(T, np.rad2deg(np.transpose(yout)[0])) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Andle of Side Slip [deg]') 
         
        ax2.plot(T, np.rad2deg(np.transpose(yout)[1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Yaw Angle [deg]') 
         
        ax3.plot(T, np.rad2deg(np.transpose(yout)[2])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Roll Rate [deg/s]')# 
         
        ax4.plot(T, np.rad2deg(np.transpose(yout)[3])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Yaw Rate [deg/s]') 
        return plt.show()
    
    if motion == 'dutch':
        
        timesim = 200
        t = np.linspace(0, timesim, 1001)
        U1, U2 = np.zeros(len(t)),np.zeros(len(t))
        U1[0:30] = dist_input 
        U1[31:60] = -dist_input 
        U1[61:90] = dist_input 
        U = np.transpose(np.matrix([U1, U2]))

        yout, T, xout = control.lsim(asymsys, U, t, X0)
        
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Asymmetric Flight - Dutch Roll Motion') 
         
        ax1.plot(T, np.rad2deg(np.transpose(yout)[0])) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Andle of Side Slip [deg]') 
         
        ax2.plot(T, np.rad2deg(np.transpose(yout)[1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Yaw Angle [deg]') 
         
        ax3.plot(T, np.rad2deg(np.transpose(yout)[2])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Roll Rate [deg/s]')# 
         
        ax4.plot(T, np.rad2deg(np.transpose(yout)[3])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Yaw Rate [deg/s]') 
        return plt.show()
    
    if motion == 'spiral':
        
        timesim = 200
        t = np.linspace(0, timesim, 1001)
        U1, U2 = np.zeros(len(t)),np.zeros(len(t))
        U = np.transpose(np.matrix([U1, U2]))

        yout, T, xout = control.lsim(asymsys, U, t, X0)
        
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Asymmetric Flight - Spiral Motion') 
         
        ax1.plot(T, np.rad2deg(np.transpose(yout)[0])) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Andle of Side Slip [deg]') 
         
        ax2.plot(T, np.rad2deg(np.transpose(yout)[1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Yaw Angle [deg]') 
         
        ax3.plot(T, np.rad2deg(np.transpose(yout)[2])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Roll Rate [deg/s]')# 
         
        ax4.plot(T, np.rad2deg(np.transpose(yout)[3])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Yaw Rate [deg/s]') 
        return plt.show()