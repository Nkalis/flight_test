# Citation 550 - Linear simulation

# xcg = 0.25 * c

import numpy as np
from flight_parameters import flight_parameters
from data_extractor import data_extractor
import control.matlab as control 
from fuel_calc import fuel_calc
from postflightdata import post_flight_data

'''Choose Time'''
t0 = 1200

''' Getting the flight data from both sources''' 
flightdata = data_extractor() 
testdata = post_flight_data()
# (h,m,theta,alpha,tdata,t)
''' Getting the time data from the flight data ''' 
timedata = flightdata.get('time') 

''' Example of plotting two variables against eachother ''' 
variable1 = flightdata.get('time') 
variable2 = flightdata.get('delta_a')
alt = flightdata.get('Dadc1_bcAlt')

''' Calculating the fuel left in the tanks ''' 
fuel_used_l = flightdata.get('lh_engine_FU') 
fuel_used_r = flightdata.get('rh_engine_FU') 
initial_fuel_l = 4050/2
initial_fuel_r = 4050/2
fuel_mass = fuel_calc(initial_fuel_l, initial_fuel_r, fuel_used_l, fuel_used_r, testdata[-3])

# Stationary flight condition
flightdata = data_extractor()
fp     = flight_parameters(flightdata.get('Dadc1_bcAlt'), fuel_mass[2], flightdata.get('Ahrs1_Pitch'), flightdata.get('vane_AOA'), timedata, t0, flightdata.get('Dadc1_tas'), flightdata.get('Ahrs1_Roll'), flightdata.get('Ahrs1_bRollRate'), flightdata.get('Ahrs1_bYawRate'))
hp0    = post_flight_data()[0]      	      # pressure altitude in the stationary flight condition [m]
V     = fp[6]            # true airspeed in the stationary flight condition [m/sec]
alpha0 = fp[3]            # angle of attack in the stationary flight condition [rad]
th0    = fp[2]            # pitch angle in the stationary flight condition [rad]

# Aircraft mass
m      = fp[1]         # mass [kg]

# aerodynamic properties
e      = 0.8            # Oswald factor [ ]
C_D0    = 0.04            # Zero lift drag coefficient [ ]
C_La    = 5.497727037013767            # Slope of CL-alpha curve [ ]

# Longitudinal stability
C_ma    = -0.4521130159681127  #VAN KIM!!!!          # longitudinal stabilty [ ]
C_mde   = -0.9876726725787773            # elevator effectiveness [ ]

# Aircraft geometry

S      = 30.00	          # wing area [m^2]
Sh     = 0.2 * S         # stabiliser area [m^2]
Sh_S   = Sh / S	          # [ ]
lh     = 0.71 * 5.968    # tail length [m]
c      = 2.0569	          # mean aerodynamic cord [m]
lh_c   = lh / c	          # [ ]
b      = 15.911	          # wing span [m]
bh     = 5.791	          # stabilser span [m]
A      = b ** 2 / S      # wing aspect ratio [ ]
Ah     = bh ** 2 / Sh    # stabilser aspect ratio [ ]
Vh_V   = 1	          # [ ]
ih     = -2 * np.pi / 180   # stabiliser angle of incidence [rad]

# Constant values concerning atmosphere and gravity

rho0   = 1.2250          # air density at sea level [kg/m^3] 
lam    = -0.0065         # temperature gradient in ISA [K/m]
Temp0  = 288.15          # temperature at sea level in ISA [K]
R      = 287.05          # specific gas constant [m^2/sec^2K]
g      = 9.81            # [m/sec^2] (gravity constant)

# air density [kg/m^3]  
rho    = fp[4] 
W      = m * g            # [N]       (aircraft weight)

# Constant values concerning aircraft inertia

muc    = m / (rho * S * c)
mub    = m / (rho * S * b)
Ks_xx    = 0.019
Ks_zz    = 0.042
Ks_xz    = 0.002
Ks_yy    = 1.25 * 1.114

# Aerodynamic constants

C_mac   = 0                      # Moment coefficient about the aerodynamic centre [ ]
C_Nwa   = C_La                    # Wing normal force slope [ ]
C_Nha   = 2 * np.pi * Ah / (Ah + 2) # Stabiliser normal force slope [ ]
depsda = 4 / (A + 2)            # Downwash gradient [ ]

# Lift and drag coefficient

C_L = 2 * W / (rho * V ** 2 * S)              # Lift coefficient [ ]
C_D = C_D0 + (C_La * alpha0) ** 2 / (np.pi * A * e) # Drag coefficient [ ]

# Stabiblity derivatives

C_X0    = W * np.sin(th0) / (0.5 * rho * V ** 2 * S)
C_Xu    = -0.02792
C_Xa    = -0.47966
C_Xadot = +0.08330
C_Xq    = -0.28170
C_Xde   = -0.03728

C_Z0    = -W * np.cos(th0) / (0.5 * rho * V ** 2 * S)
C_Zu    = -0.37616
C_Za    = -5.74340
C_Zadot = -0.00350
C_Zq    = -5.66290
C_Zde   = -0.69612

C_mu    = +0.06990
C_madot = +0.17800
C_mq    = -8.79415

C_Yb    = -0.7500
C_Ybdot =  0     
C_Yp    = -0.0304
C_Yr    = +0.8495
C_Yda   = -0.0400
C_Ydr   = +0.2300

C_lb    = -0.10260
C_lp    = -0.71085
C_lr    = +0.23760
C_lda   = -0.23088
C_ldr   = +0.03440

C_nb    =  +0.1348
C_nbdot =   0     
C_np    =  -0.0602
C_nr    =  -0.2061
C_nda   =  -0.0120
C_ndr   =  -0.0939

D_c = c/V
D_b = b/V
mu_c = m/(rho*S*c)
mu_b = m/(rho*S*b)

'''Symmetrical'''
Psym = np.matrix([[-2*mu_c*D_c/V, 0, 0, 0], 
                     [0, (C_Zadot-2*mu_c)*D_c, 0, 0], 
                     [0, 0, -D_c, 0], 
                     [0, C_madot*D_c, 0, -2*mu_c*Ks_yy*D_c*D_c]]) 
     
Qsym = -1*np.matrix([[C_Xu/V, C_Xa, C_Z0, 0], 
                     [C_Zu/V, C_Za, C_X0, (C_Zq+2*mu_c)*D_c], 
                     [0, 0, 0, 1*D_c], 
                     [C_mu/V, C_ma, 0, C_mq*D_c]]) 
     
Rsym = np.matrix([[-C_Xde], 
                  [-C_Zde], 
                  [0], 
                  [-C_mde]]) 

'''Asymmetrical''' 
Pasym = np.matrix([[(C_Ybdot-2*mu_b)*D_b, 0, 0, 0], 
                    [0, -0.5*D_b, 0, 0], 
                    [0, 0, -4*mu_b*Ks_xx*D_b*D_b/2, 4*mu_b*Ks_xz*D_b*D_b/2], 
                    [C_nbdot*D_b, 0, 4*mu_b*Ks_xz*D_b*D_b/2, -4*mu_b*Ks_zz*D_b*D_b/2]]) 
     
Qasym = -1*np.matrix([[C_Yb, C_L, C_Yp*D_b/2, (C_Yr-4*mu_b)*D_b/2], 
                      [0, 0, -1*D_b/2, 0],
                      [C_lb, 0, C_lp*D_b/2, C_lr*D_b/2], 
                      [C_nb, 0, C_np*D_b/2, C_nr*D_b/2]]) 
     
Rasym = np.matrix([[-C_Yda, -C_Ydr], 
                     [0,0], 
                     [-C_lda, -C_ldr], 
                     [-C_nda, -C_ndr]]) 

#Symmetrical Case 
A = np.linalg.inv(Psym)*Qsym 
B = np.linalg.inv(Psym)*Rsym 
C = np.identity(4) 
D = np.zeros((4,1)) #Only elevator 
symsys = control.ss(A,B,C,D) 

#Asymmetrical Case 
A = np.linalg.inv(Pasym)*Qasym 
B = np.linalg.inv(Pasym)*Rasym 
C = np.identity(4) 
D = np.zeros((4,2)) #Because both aileron and rudder displacement 
asymsys = control.ss(A,B,C,D) 

print(symsys,asymsys)