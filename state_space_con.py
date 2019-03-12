def state_space_conv(P,Q,R,sym_or_asym):
    import numpy as np
    import control.matlab as c
    
    if sym_or_asym == "sym":
        A = -np.linalg.inv(P)*Q
        B = -np.linalg.inv(P)*R
        C = np.identity(4)
        D = np.zeros((4,1))
        sys = c.ss(A,B,C,D)
        return sys
    elif sym_or_asym == "asym":
        A = -np.linalg.inv(P)*Q
        B = -np.linalg.inv(P)*R
        C = np.identity(4)
        D = np.zeros((4,2))
        sys = c.ss(A,B,C,D)
        return sys
    else:
        return print("Please tell me if it is symmetric (sym) or asymmetric (asym)")