# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:33:47 2019

@author: TUDelftSID
"""

from math import *
import numpy as np
from postflightdatatrim import post_flight_data_trim

#------------------------------------------------------------------------------

data = post_flight_data_trim()
print(data)
#hp, IAS, a, de, detr, Fe, FFl, FFr, F_used, TAT, Payl, Payload, BEM, BFuel, M_r, M_t, W_t

#------------------------------------------------------------------------------

""" Stationary measurements elevator trim curve """

# Pressure altitude (ft)
hp = data[0]
print ("Pressure altitude (ft): ", hp)

# Indicated airspeed (kts)
IAS = data[1]
print ("Indicated airspeed (kts) : ", IAS)

# Angle of attack (deg)
a = data[2]
print ("Angle of attack (deg): ", a)

# Elevator deflection (deg)
de = data[3]
print ("Elevator deflection (deg): ", de)

# Delta elevator trim (deg)
detr = data[4]
print ("Delta elevator trim (deg): ", detr)

# Stick force (N)
Fe = data[5]
print ("Stick force (N): ", Fe)

# Fuel flow left
FFl = data[6]
print ("Fuel flow left (lbs/hr): ", FFl)

# Fuel flow right
FFr = data[7]
print ("Fuel flow right (lbs/hr): ", FFr)

# Fuel used
F_used = data[8]
print ("Fuel used (kg): ", F_used)

# True air temperature
TAT = data[9]
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
Payl = data[10]
print ("Independent payloads (kg): ", Payl)
Payload = data[11]
print ("Total payload (kg): ", Payload)

""" Unit conversions """
BEM = data[12] # kg (basic empty mass)
BFuel = data[13] # kg (block fuel)

""" Ramp mass """
M_r = data[14]

""" Total mass at point in time """
M_t = data[15]
print ("Total mass at point in time (kg): ", M_t)

""" Total weight at point in time """
# N (total weight)
W_t = data[16]
print ("Total weight at point in time (N): ", W_t)

#------------------------------------------------------------------------------

""" Pressure altitude """
# Conversion to m
for i in range(len(hp)):
    hp[i] = hp[i] * 0.3048
print ("Pressure altitude (m):", hp)

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