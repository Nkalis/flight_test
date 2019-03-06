# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 16:05:26 2019

@author: nkali
"""

""" DATA READER """

import mat4py
import numpy as np
import matplotlib.pyplot as plt

data = mat4py.loadmat("matlab.mat")

flightdata = data.get('flightdata', {})
time = np.array(flightdata.get('time').get('data'))
pitch = np.array(flightdata.get('Ahrs1_Pitch').get('data'))

gps_lat = np.array(flightdata.get('Gps_lat').get('data'))
gps_long = np.array(flightdata.get('Gps_long').get('data'))

plt.plot(time, pitch)