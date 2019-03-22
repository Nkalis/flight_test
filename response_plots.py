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
 
def state_space_plot(X0, motion): 
    import numpy as np 
    import control.matlab as control 
    import matplotlib.pyplot as plt 
    from state_space_con import state_space_conv 
     
    X0 = np.transpose(np.asmatrix(X0)) 
    symsys, asymsys = state_space_conv()[0],[2] 
     
    if motion == 'phugoid': 
         
        timesim = 300 
        t = np.linspace(0, timesim, 1001) 
        U = np.zeros(len(t)) 
        U[0:90]= 0.15 
        yout, T, xout = control.lsim(symsys, U, t, X0) 
         
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Symmetric Flight - Phugoid Motion') 
         
        ax1.plot(T[250:-1], np.transpose(yout)[0][250:-1]) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Velocity [m/s]') 
         
        ax2.plot(T[250:-1], np.rad2deg(np.transpose(yout)[1][250:-1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Angle of Attack [deg]') 
         
        ax3.plot(T[250:-1], np.rad2deg(np.transpose(yout)[2][250:-1])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Angle [deg]')# 
         
        ax4.plot(T[250:-1], np.rad2deg(np.transpose(yout)[3][250:-1])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Rate [deg/s]') 
        return plt.show() 
     
    if motion == 'quick': 
         
        timesim = 20 
        t = np.linspace(0, timesim, 1001) 
        U = np.zeros(len(t)) 
        U[0:-1]= 0.15 
        yout, T, xout = control.lsim(symsys, U, t, X0) 
         
        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2) 
        f.suptitle('Symmetric Flight - Phugoid Motion') 
         
        ax1.plot(T, np.transpose(yout)[0]) 
        ax1.set(xlabel = 'Simulation time T [s]', ylabel = 'Velocity [m/s]') 
         
        ax2.plot(T, np.rad2deg(np.transpose(yout)[1])) 
        ax2.set(Xlabel = 'Simulation time T [s]', ylabel = 'Angle of Attack [deg]') 
         
        ax3.plot(T, np.rad2deg(np.transpose(yout)[2])) 
        ax3.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Angle [deg]')# 
         
        ax4.plot(T, np.rad2deg(np.transpose(yout)[3])) 
        ax4.set(xlabel = 'Simulation time T [s]', ylabel = 'Pitch Rate [deg/s]') 
        return plt.show() 
 
state_space_plot([0,0,0,0], 'quick')