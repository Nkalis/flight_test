'''             ALL VARIABLES AVAILABLE FROM FLIGHT DATA
Ahrs1_Pitch
Ahrs1_Roll
Ahrs1_VertAcc
Ahrs1_aHdgAcc
Ahrs1_bLatAcc
Ahrs1_bLongAcc
Ahrs1_bNormAcc
Ahrs1_bPitchRate
Ahrs1_bRollRate
Ahrs1_bYawRate
Ahrs1_xHdgAcc
Dadc1_alt
Dadc1_altRate
Dadc1_bcAlt
Dadc1_bcAltMb
Dadc1_cas
Dadc1_mach
Dadc1_sat
Dadc1_tas
Dadc1_tat
Fms1_trueHeading
Gps_date
Gps_lat
Gps_long
Gps_utcSec
column_fe
delta_a
delta_e
delta_r
display_active_screen
display_graph_state
elevator_dte
lh_engine_FMF
lh_engine_FU
lh_engine_OP
lh_engine_fan_N1
lh_engine_itt
lh_engine_turbine_N2
measurement_n_rdy
measurement_running
rh_engine_FMF
rh_engine_FU
rh_engine_OP
rh_engine_fan_N1
rh_engine_itt
rh_engine_turbine_N2
time
vane_AOA
'''

from data_extractor import data_extractor #data_extractor()
from fuel_calc import fuel_calc #fuel_calc(initial_l, initial_r, fuel_lef, fuel_rig, timedata, time)
from map_plot import map_plot #map_plot(timedata, t0, t1, gps_lon, gps_lat, alt)
from response_plots import response_plot #response_plot(variable1, variable2, time0, time1)
from cg_calculator import cg_calculator #(x_coord,m_lt,m_rt)

import matplotlib.pyplot as plt

flightdata = data_extractor()
timedata = flightdata.get('time')

''' Example of plotting two variables against eachother '''
t0 = 0
t1 = 100
variable1 = flightdata.get('time')
variable2 = flightdata.get('rh_engine_FMF')
#response_plot(timedata, variable1, variable2, t0, t1)

''' Example of a map plot '''
gps_lon = flightdata.get('Gps_long')
gps_lat = flightdata.get('Gps_lat')
alt = flightdata.get('Dadc1_bcAlt')
map_plot(timedata, t0, t1, gps_lon, gps_lat, alt)

''' Calculating the fuel left in the tanks '''
fuel_used_l = flightdata.get('lh_engine_FU')
fuel_used_r = flightdata.get('rh_engine_FU')
initial_fuel_l = 2000
initial_fuel_r = 2000
print(cg_calculator(288, 5008, 5008))
print(cg_calculator(288, 0, 0))
fuel_left = fuel_calc(initial_fuel_l, initial_fuel_r, fuel_used_l, fuel_used_r, timedata, t0)