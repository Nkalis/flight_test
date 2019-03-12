def state_space_conv(P,Q,R,sym_or_asym):
    import numpy as np
    import control.matlab as c
    
    #Symmetrical Case
    if sym_or_asym == "sym":
        A = -np.linalg.inv(P)*Q
        B = -np.linalg.inv(P)*R
        C = np.identity(4)
        D = np.zeros((4,1)) #Only elevator
        sys = c.ss(A,B,C,D)
        return sys
    #Asymmetrical Case
    elif sym_or_asym == "asym":
        A = -np.linalg.inv(P)*Q
        B = -np.linalg.inv(P)*R
        C = np.identity(4)
        D = np.zeros((4,2)) #Because both aileron and rudder displacement
        sys = c.ss(A,B,C,D)
        return sys
    else:
        return print("Please tell me if it is symmetric (sym) or asymmetric (asym)")