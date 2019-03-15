# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 11:17:13 2019

@author: TUDelftSID
"""

from math import *
import numpy as np

#------------------------------------------------------------------------------
""" Open Post Flight Data Sheet csv file """
f = open("postflightdataex2.csv","r")
lines = f.readlines()
f.close()

""" Create an array with all the data """
datalist = lines
data = []
for i in range(84):
    dataline = datalist[i]
    dataline = dataline.split(';')
    dataline = list(dataline)
    data.append(dataline)

""" Remove the \n from the array """
for j in range(84):
    for k in range(13):
        if '\n' in data[j][k]:
            data[j][k] = data[j][k][:-2]
        else:
            data[j][k] = data[j][k]
data = np.array(data)

#------------------------------------------------------------------------------

""" Stationary measurements CL-CD series 1 """

# Pressure altitude
hp = []
hp1 = data[:,3]
for i in range(27,33):
    hp.append(float(hp1[i]))
print ("Pressure altitude (ft): ", hp)

# Indicated airspeed
IAS = []
IAS1 = data[:,4]
for i in range(27,33):
    IAS.append(float(IAS1[i]))
print ("Indicated airspeed (kts) : ", IAS)

# Angle of attack
a = []
a1 = data[:,5]
for i in range(27,33):
    a.append(float(a1[i]))
print ("Angle of attack (deg): ", a)

# Fuel flow left
FFl = []
FFl1 = data[:,6]
for i in range(27,33):
    FFl.append(float(FFl1[i]))
print ("Fuel flow left (lbs/hr): ", FFl)

# Fuel flow right
FFr = []
FFr1 = data[:,7]
for i in range(27,33):
    FFr.append(float(FFr1[i]))
print ("Fuel flow right (lbs/hr): ", FFr)

# Fuel used
F_used = []
F_used1 = data[:,8]
for i in range(27,33):
    F_used.append(float(F_used1[i]))
print ("Fuel used (lbs): ", F_used)

# True air temperature
TAT = []
TAT1 = data[:,9]
for i in range(27,33):
    TAT.append(float(TAT1[i]))
print ("Total air temperature (C): ", TAT)

#------------------------------------------------------------------------------

""" Variables """
rho_0 = 1.225 # kg/m^3 (air density at sea level)
g = 9.80665 # m/s^2 (gravitational constant)
T_0 = 288.15 # K (temperature at sea level)
p_0 = 101325. # Pa (pressure at sea level)
a = -0.0065
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
    TISA1 = T_0 + a * hp[i]
    TISA.append(TISA1)
print ("ISA temperature (K): ", TISA)

""" Density """
rho = []
for i in range(len(hp)):
    rho1 = rho_0 * (TISA[i]/T_0)**(-((g/(a*R)) + 1.))
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
#sos = []
#for i in range(len(TAT)):
#    sos1 = sqrt(R*gamma*TAT[i])
#    sos.append(sos1)
#print (sos)

#------------------------------------------------------------------------------

""" Mach number """
Mach = []
for i in range(len(TAS)):
    Mach1 = TAS[i]/(sos_0 * sqrt(TAT[i]/T_0))
    Mach.append(Mach1)
print ("Mach number (-): ", Mach)
#M = []
#for i in range(len(TAS)):
#    M1 = TAS[i]/sos[i]
#    M.append(M1)
#print (M)

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
    dTISA1 = abs(TAT[i] - TISA[i])
    dTISA.append(dTISA1)
print("Temperature difference (K): ", dTISA)

#------------------------------------------------------------------------------

g = open("matlab.dat","w")
for i in range(len(hp)):
    g.write(str(hp[i]) + " " + str(Mach[i]) + " " + str(dTISA[i]) + " " + str(Mf1[i]) + " " + str(Mf2[i]) + "\n")
g.close()










#""" Masses """
#BEM = 13600. # lbs (basic empty mass)
#BFuel = float(data[17][3]) # lbs (block fuel)
## Payload
#Payl = []
#Payl1 = data[:,7]
#for i in range(7,16):
#    Payl.append(float(Payl1[i]))
#print (Payl)
#Payload = sum(Payl)
#print (Payload)
#
#""" Unit conversions """
#BEM = BEM * 0.453592 # kg (basic empty mass)
#BFuel = BFuel * 0.453592 # kg (block fuel)
## kg (fuel used)
#for i in range(len(F_used)):
#    F_used[i] = F_used[i] * 0.453592
#print (F_used)
#
#""" Ramp mass """
#M_r = BEM + BFuel + Payload
#
#""" Total mass at point in time """
#M_t = []
#for i in range(len(F_used)):
#    M_t1 = M_r - F_used[i]
#    M_t.append(M_t1)
#print (M_t)
#
#""" Total weight at point in time """
## N (total weight)
#W_t = []
#for i in range(len(M_t)):
#    W_t1 = M_t[i] * g
#    W_t.append(W_t1)
#print (W_t)