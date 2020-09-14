# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:29:20 2020

@author: aicter
"""

import warnings
warnings.filterwarnings('ignore')
from netCDF4 import Dataset
from netCDF4 import num2date
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  
#import matplotlib as mpl  
from scipy import interpolate  
import matplotlib.cm as cm  
import matplotlib.pyplot as plt

my_example_nc_file = 'ECMWF_data/adaptor.mars.internal-1599635587.0598102-422-29-f533d004-1770-4307-9fb8-0a7095fd1f46.nc'
fh = Dataset(my_example_nc_file, mode='r')

#print(fh.variables)
print(fh.variables.keys())

lons = fh.variables['longitude'][:]
lats = fh.variables['latitude'][:]
time= fh.variables['time'][:]
u10= fh.variables['u10'][:]
v10= fh.variables['v10'][:]
mwd=fh.variables['mwd'][:]
mwp=fh.variables['mwp'][:]
swh=fh.variables['swh'][:]

print('u10 shape',u10.shape)
print('lons shape',lons.shape)
print('lats shape',lats.shape)
print('mwd shape',mwd.shape)
print('mwp shape', mwp.shape)
print('swh shape',swh.shape)