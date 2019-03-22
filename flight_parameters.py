def flight_parameters(h,m,theta,alpha,tdata,t):
    import numpy as np
    from isa import ISA
    
    index = tdata.get("data").index(t)
    h0 = h.get("data")[index]
    theta0 = theta.get("data")[index]
    alpha0 = alpha.get("data")[index]
    m0 = m[index]
    rho0 = ISA(h0)
    
    data = np.array([[h0],[m0],[theta0],[alpha0],[rho0]])
    
    return data