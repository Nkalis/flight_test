def state_space_conv(data):
    from eom import eom
    import numpy as np 
    import control.matlab as c 
    
    eoms = eom(data)
    Psym, Qsym, Rsym, Pasym, Qasym, Rasym = eoms 
    #Symmetrical Case 
    A = np.linalg.inv(Psym)*Qsym 
    B = np.linalg.inv(Psym)*Rsym 
    C = np.identity(4) 
    D = np.zeros((4,1)) #Only elevator 
    symsys = c.ss(A,B,C,D) 
    symeig = np.linalg.eigvals(A) 
    count = 0 
    for i in range(len(symeig)): 
        if np.real(symeig[i])<0: 
            count=count+1 
        else: 
            break 
    if count == len(symeig): 
        print("System is stable") 
    else: 
        print("System is unstable") 
         
    #Asymmetrical Case 
    A = np.linalg.inv(Pasym)*Qasym 
    B = np.linalg.inv(Pasym)*Rasym 
    C = np.identity(4) 
    D = np.zeros((4,2)) #Because both aileron and rudder displacement 
    asymsys = c.ss(A,B,C,D) 
    asymeig = np.linalg.eigvals(A) 
    count = 0 
    for i in range(len(asymeig)-1): 
        if np.real(asymeig[i])<0: 
            count=count+1 
        else: 
            break 
    if count == len(asymeig): 
        print("System is stable") 
    else: 
        print("System is unstable") 
     
    return symsys, symeig, asymsys, asymeig