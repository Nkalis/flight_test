from math import *
import numpy as np
from postflightdata import post_flight_data

#------------------------------------------------------------------------------

data = post_flight_data()
# hp, IAS, alpha, FFl, FFr, F_used, TAT, Payl, Payload, BEM, BFuel, M_r, M_t, W_t

#------------------------------------------------------------------------------

""" Stationary measurements from postflightdata.py """

# Pressure altitude (ft)
hp = data[0]
print ("Pressure altitude (ft): ", hp)

# Indicated airspeed (kts)
IAS = data[1]
print ("Indicated airspeed (kts) : ", IAS)

# Angle of attack (deg)
alpha = data[2]
print ("Angle of attack (deg): ", alpha)

# Fuel flow left (lbs/hr)
FFl = data[3]
print ("Fuel flow left (lbs/hr): ", FFl)

# Fuel flow right (lbs/hr)
FFr = data[4]
print ("Fuel flow right (lbs/hr): ", FFr)

# Fuel used (kg)
F_used = data[5]
print ("Fuel used (kg): ", F_used)

# True air temperature (C)
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

""" Fuel flow left engine"""
# conversion to kg/s
Mf1 = []
for i in range(len(FFl)):
    Mf1l = FFl[i] * 0.000125997881
    Mf1.append(Mf1l)
print ("Fuel flow left engine (kg/s): ", Mf1)

#------------------------------------------------------------------------------

""" Fuel flow right engine """
# conversion to kg/s
Mf2 = []
for i in range(len(FFr)):
    Mf2r = FFr[i] * 0.000125997881
    Mf2.append(Mf2r)
print ("Fuel flow right engine (kg/s): ", Mf2)

#------------------------------------------------------------------------------

""" Temperature difference """
dTISA = []
for i in range(len(TISA)):
    dTISA1 = Ts[i] - TISA[i]
    dTISA.append(dTISA1)
print("Temperature difference (K): ", dTISA)

#------------------------------------------------------------------------------

""" Write matlab.dat file """
g = open("matlab.dat","w")
for i in range(len(hp)):
    g.write(str(hp[i]) + " " + str(M[i]) + " " + str(dTISA[i]) + " " + str(Mf1[i]) + " " + str(Mf2[i]) + "\n")
g.close()
