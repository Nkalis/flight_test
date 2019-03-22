from math import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from postflightdata import post_flight_data

#------------------------------------------------------------------------------

data = post_flight_data()
# hp, IAS, alpha, FFl, FFr, F_used, TAT, Payl, Payload, BEM, BFuel, M_r, M_t, W_t

#------------------------------------------------------------------------------

""" Stationary measurements CL-CD series 1 """

# Pressure altitude
hp = data[0]
print ("Pressure altitude (ft): ", hp)

# Indicated airspeed
IAS = data[1]
print ("Indicated airspeed (kts) : ", IAS)

# Angle of attack
alpha = data[2]
print ("Angle of attack (deg): ", alpha)

# Fuel flow left
FFl = data[3]
print ("Fuel flow left (lbs/hr): ", FFl)

# Fuel flow right
FFr = data[4]
print ("Fuel flow right (lbs/hr): ", FFr)

# Fuel used
F_used = data[5]
print ("Fuel used (kg): ", F_used)

# True air temperature
TAT = data[6]
print ("Total air temperature (C): ", TAT)

#------------------------------------------------------------------------------

""" Variables """
rho_0 = 1.225 # kg/m^3 (air density at sea level)
g = 9.80665 # m/s^2 (gravitational constant)
T_0 = 288.15 # K (temperature at sea level)
p_0 = 101325. # Pa (pressure at sea level)
ah = -0.0065
R = 287.00
gamma = 1.4
S = 30. # m^2 (wing surface area)

#------------------------------------------------------------------------------

# Payload
Payl = data[7]
print ("Independent payloads (kg): ", Payl)
Payload = data[8]
print ("Total payload (kg): ", Payload)

""" Unit conversions """
BEM = data[9] # kg (basic empty mass)
BFuel = data[10] # kg (block fuel)

""" Ramp mass """
M_r = data[11]

""" Total mass at point in time """
M_t = data[12]
print ("Total mass at point in time (kg): ", M_t)

""" Total weight at point in time """
# N (total weight)
W_t = data[13]
print ("Total weight at point in time (N): ", W_t)

#------------------------------------------------------------------------------

""" Conversions """

# Pressure altitude - conversion to m
for i in range(len(hp)):
    hp[i] = hp[i] * 0.3048
print ("Pressure altitude (m):", hp)

# Total air temperature - conversion to K
for i in range(len(TAT)):
    TAT[i] = TAT[i] + 274.15
print ("Total air temperature (K):", TAT)

#------------------------------------------------------------------------------

""" Calibrated airspeed """
CAS = []
for i in range(len(IAS)):
    CAS1 = IAS[i] - 2.
    CAS.append(CAS1)
print ("Calibrated airspeed (kts): ", CAS)
# Calibrated airspeed - conversion to m/s
for i in range(len(CAS)):
    CAS[i] = CAS[i] * 0.514444444
print ("Calibrated airspeed (m/s): ", CAS)

""" Pressure calibration """
p = []
for i in range(len(hp)):
    p1 = p_0 * (1. + (ah*hp[i])/(T_0))**(-g/(ah*R))
    p.append(p1)
print ("Pressure calibration (Pa): ", p)

""" Mach number """
M = []
for i in range(len(p)):
    M1 = sqrt( (2./(gamma - 1.)) * ((1. + (p_0/p[i]) * ((1. + (gamma - 1.)/(2.*gamma) * (rho_0/p_0) * CAS[i]**2.)**(gamma/(gamma - 1.)) - 1.))**((gamma - 1.)/gamma) - 1.) )
    M.append(M1)
print ("Mach number (-): ", M)

""" Corrected total air temperature """
Ts = []
for i in range(len(M)):
    Ts1 = TAT[i]/(1. + (((gamma - 1.)/2.) * M[i]**2.))
    Ts.append(Ts1)
print ("Corrected total air temperature (K): ", Ts)

""" Speed of sound """
a = []
for i in range(len(Ts)):
    a1 = sqrt( gamma * R * Ts[i] )
    a.append(a1)
print ("Speed of sound (m/s): ", a)

""" True airspeed """
TAS = []
for i in range(len(a)):
    TAS1 = M[i] * a[i]
    TAS.append(TAS1)
print ("True airspeed (m/s): ", TAS)

""" Density """
rho = []
for i in range(len(p)):
    rho1 = p[i]/(R*Ts[i])
    rho.append(rho1)
print ("Density (kg/m^3): ", rho)

""" Equivalent airspeed """
EAS = []
for i in range(len(TAS)):
    EAS1 = TAS[i] * sqrt(rho[i]/rho_0)
    EAS.append(EAS1)
print ("Equivalent airspeed (m/s): ", EAS)

""" ISA Temperature """
TISA = []
for i in range(len(hp)):
    TISA1 = T_0 + ah * hp[i]
    TISA.append(TISA1)
print ("ISA temperature (K): ", TISA)

#------------------------------------------------------------------------------

""" CL """
# Lift (= weight)
L = []
for i in range(len(W_t)):
    L1 = W_t[i]
    L.append(L1)
print ("Lift (N): ", L)
# CL
CL = []
for i in range(len(L)):
    CL1 = (2.*L[i])/(rho[i]*S*(EAS[i])**2.)
    CL.append(CL1)
print ("CL (-): ", CL)
# CL squared
CL2 = []
for i in range(len(CL)):
    CL21 = (CL[i])**2.
    CL2.append(CL21)
print ("CL squared (-): ", CL2)

#------------------------------------------------------------------------------

""" CD """

# Get thrust data
g = open("thrust.dat", "r")
thrustls = g.readlines()
g.close()
# Create an array with thrust data
thrustd = thrustls
thrust = []
for i in range(6):
    thrustl = thrustls[i]
    thrustl = thrustl.split('\t')
    thrustl = list(thrustl)
    thrust.append(thrustl)
# Remove the \n from the array
for j in range(6):
    for k in range(2):
        if '\n' in thrust[j][k]:
            thrust[j][k] = thrust[j][k][:-2]
        else:
            thrust[j][k] = thrust[j][k]
        thrust[j][k] = float(thrust[j][k])
thrust = np.array(thrust)
# Thrust
T = []
for i in range(6):
    T1 = thrust[i][0] + thrust[i][1]
    T.append(T1)
print ("Total thrust (N): ", T)
# Drag (= thrust)
D = []
for i in range(len(T)):
    D1 = T[i]
    D.append(D1)
print ("Drag (N): ", D)
# CD
CD = []
for i in range(len(D)):
    CD1 = (2.*D[i])/(rho[i]*S*(EAS[i])**2.)
    CD.append(CD1)
print ("CD (-): ", CD)

#------------------------------------------------------------------------------

""" CD0 and oswald efficiency factor via interpolation """

K,CD0,r_value,p_value,std_err = stats.linregress(CL2,CD)
print ("Zero lift drag coefficient: ", CD0)

e = 1./(pi*K*S)
print ("Oswald efficiency factor: ", e)

CDr = []
for i in range(len(CD)):
    CDr1 = CD0 + K*CL2[i]
    CDr.append(CDr1)
    
#plt.scatter(CL2, CD)
#plt.plot(CL2, CDr, "r")
#plt.title("CL_squared vs. CD interpolation")
#plt.xlabel("CL_squared (-)")
#plt.ylabel("CD (-)")
#plt.show()

#------------------------------------------------------------------------------

""" CL, CD - curve """

plt.plot(CDr, CL)
plt.title("CL - CD curve")
plt.xlabel("CD (-)")
plt.ylabel("CL (-)")
plt.show()

""" CL, alpha - curve """

plt.scatter(alpha, CL)
plt.plot(alpha, CL, "r")
plt.title("CL - alpha curve")
plt.xlabel("alpha (deg)")
plt.ylabel("CL (-)")
plt.show()

""" CD, alpha - curve """

plt.scatter(alpha, CDr)
plt.plot(alpha, CDr, "r")
plt.title("CD - alpha curve")
plt.xlabel("alpha (deg)")
plt.ylabel("CD (-)")
plt.show()
