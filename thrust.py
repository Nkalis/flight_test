# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:17:13 2019

@author: TUDelftSID
"""

from math import *
import numpy as np
from postflightdata import post_flight_data

#------------------------------------------------------------------------------

data = post_flight_data()
# hp, IAS, a, FFl, FFr, F_used, TAT, Payl, Payload, BEM, BFuel, M_r, M_t, W_t

#------------------------------------------------------------------------------

""" Stationary measurements CL-CD series 1 """

# Pressure altitude
hp = data[0]
print ("Pressure altitude (ft): ", hp)

# Indicated airspeed
IAS = data[1]
print ("Indicated airspeed (kts) : ", IAS)

# Angle of attack
a = data[2]
print ("Angle of attack (deg): ", a)

# Fuel flow left
FFl = data[3]
print ("Fuel flow left (lbs/hr): ", FFl)

# Fuel flow right
FFr = data[4]
print ("Fuel flow right (lbs/hr): ", FFr)

# Fuel used
F_used = data[5]
print ("Fuel used (lbs): ", F_used)

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

#------------------------------------------------------------------------------

""" Pressure altitude """
# Conversion to m
for i in range(len(hp)):
    hp[i] = hp[i] * 0.3048
print ("Pressure altitude (m):", hp)

#------------------------------------------------------------------------------

""" Temperature conversion """
# conversion to K
for i in range(len(TAT)):
    TAT[i] = TAT[i] + 273.15
print ("Total air temperature (K):", TAT)

""" Calibrated airspeed """
CAS = []
for i in range(len(IAS)):
    CAS1 = IAS[i] - 2.
    CAS.append(CAS1)
print ("Calibrated airspeed (kts): ", CAS)
# conversion to m/s
for i in range(len(CAS)):
    CAS[i] = CAS[i] * 0.514444444
print ("Calibrated airspeed (m/s): ", CAS)

""" ISA Temperature """
TISA = []
for i in range(len(hp)):
    TISA1 = T_0 + ah * hp[i]
    TISA.append(TISA1)
print ("ISA temperature (K): ", TISA)

""" Density """
rho = []
for i in range(len(hp)):
    rho1 = rho_0 * (TISA[i]/T_0)**(-((g/(ah*R)) + 1.))
    rho.append(rho1)
print ("Air density (kg/m^3): ", rho)

""" True airspeed """
TAS = []
for i in range(len(CAS)):
    TAS1 = CAS[i] * sqrt(rho_0/rho[i])
    TAS.append(TAS1)
print ("True airspeed (m/s): ", TAS)

""" Sound of speed at sea level """
sos_0 = sqrt(R*gamma*T_0)
print ("Sound of speed at sea level (m/s): ", sos_0)

#------------------------------------------------------------------------------

""" Mach number """
Mach = []
for i in range(len(TAS)):
    Mach1 = TAS[i]/(sos_0 * sqrt(TAT[i]/T_0))
    Mach.append(Mach1)
print ("Mach number (-): ", Mach)

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
    dTISA1 = TAT[i] - TISA[i]
    dTISA.append(dTISA1)
print("Temperature difference (K): ", dTISA)

#------------------------------------------------------------------------------

""" Write matlab.dat file """
g = open("matlab.dat","w")
for i in range(len(hp)):
    g.write(str(hp[i]) + " " + str(Mach[i]) + " " + str(dTISA[i]) + " " + str(Mf1[i]) + " " + str(Mf2[i]) + "\n")
g.close()
