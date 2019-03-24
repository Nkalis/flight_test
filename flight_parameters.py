def flight_parameters(h,m,theta,alpha,tdata,t):
    from isa import ISA
    
    if t == 'start': 
        index = 0 
    else: 
        index = tdata.get("data").index(t)
        
    h0 = (h.get("data")[index])[0]
    theta0 = (theta.get("data")[index])[0]
    alpha0 = (alpha.get("data")[index])[0]
    m0 = m[index]
    rho0 = ISA(h0)
    
    data = (h0, m0, theta0, alpha0, rho0)
    return data