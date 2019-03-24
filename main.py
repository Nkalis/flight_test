'''             ALL VARIABLES AVAILABLE TO PLOT FROM FLIGHT DATA 
VARIABLE NAME           VARIABLE DESCRIPTION 
Ahrs1_Pitch             = Pitch Angle 
Ahrs1_Roll              = Roll Angle 
Ahrs1_VertAcc           = Vertical Acceleration 
Ahrs1_aHdgAcc           = Along Heading Accel 
Ahrs1_bLatAcc           = Body Lat Acceleration 
Ahrs1_bLongAcc          = Body Lon Acceleration 
Ahrs1_bNormAcc          = Body Normal Acceleration 
Ahrs1_bPitchRat         = Body Pitch Rate 
Ahrs1_bRollRate         = Body Roll Rate 
Ahrs1_bYawRate          = Body Yaw Rate 
Ahrs1_xHdgAcc           = Cross Heading Acceleration 
Dadc1_altRate           = Altitude Rate 
Dadc1_bcAlt             = Barometric Altitude 
Dadc1_cas               = Computed Airspeed 
Dadc1_mach              = Mach 
Dadc1_sat               = Satic Air Temperature 
Dadc1_tas               = True Air Speed 
Dadc1_tat               = True Air Temperature 
Gps_lat                 = GPS Latitude 
Gps_long                = GPS Longitude 
column_fe               = Force on Elevator Control Wheel 
delta_a                 = Deflection Aileron 
delta_e                 = Deflection Elevon 
delta_r                 = Deflection Rudder 
elevator_dte            = Deflection of Elevator Trim 
lh_engine_FMF           = Left Engine Fuel Mass Flow 
lh_engine_FU            = Left Engine Fuel Used 
rh_engine_FMF           = Right Engine Fuel Mass Flow 
rh_engine_FU            = Right Engine Fuel Used 
time                    = Time 
vane_AOA                = Angle of Attack 
''' 
 
from data_extractor import data_extractor #data_extractor() 
from fuel_calc import fuel_calc #fuel_calc(initial_l, initial_r, fuel_lef, fuel_rig, timedata, time) 
from map_plot import map_plot #map_plot(timedata, t0, t1, gps_lon, gps_lat, alt) 
from response_plots import response_plot_data, state_space_plot #response_plot(variable1, variable2, time0, time1) 
from cg_calculator import cg_calculator #(x_coord,m_lt,m_rt) 
from postflightdata import post_flight_data 
from flight_parameters import flight_parameters
import matplotlib.pyplot as plt 
 
''' Getting the flight data from both sources''' 
flightdata = data_extractor() 
testdata = post_flight_data()
# (h,m,theta,alpha,tdata,t)
''' Getting the time data from the flight data ''' 
timedata = flightdata.get('time') 
t0 = 'start'
t1 = 'end'

''' Example of plotting two variables against eachother ''' 
variable1 = flightdata.get('time') 
variable2 = flightdata.get('vane_AOA')
alt = flightdata.get('Dadc1_bcAlt')

response_plot_data(timedata, variable1, variable2, t0, t1) 
 
#''' Example of a map plot ''' 
#gps_lon = flightdata.get('Gps_long') 
#gps_lat = flightdata.get('Gps_lat') 
#alt = flightdata.get('Dadc1_bcAlt') 
#map_plot(timedata, t0, t1, gps_lon, gps_lat, alt) 
# 
''' Calculating the fuel left in the tanks ''' 
fuel_used_l = flightdata.get('lh_engine_FU') 
fuel_used_r = flightdata.get('rh_engine_FU') 
initial_fuel_l = 4050/2
initial_fuel_r = 4050/2
fuel_mass = fuel_calc(initial_fuel_l, initial_fuel_r, fuel_used_l, fuel_used_r, testdata[-3])

flightparameters = flight_parameters(flightdata.get('Dadc1_bcAlt'), fuel_mass[2], flightdata.get('Ahrs1_Pitch'), flightdata.get('vane_AOA'), timedata, t0)
print(flightparameters)
state_space_plot(flightparameters, -0.02, 'phugoid')