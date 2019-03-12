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
from map_plot import map_plot #map_plot(t0, t1)
from response_plots import response_plot #response_plot(variable1, variable2, time0, time1)
from state_space_con import state_space_conv #state_space_conv(A, B, C, D)
#from eom import equation_inputs #equation_inputs()

t0 = 0
t1 = 'end'

data = data_extractor()
#map_plot(t0, t1)
response_plot('rh_engine_FMF', 'lh_engine_FMF', t0, t1)