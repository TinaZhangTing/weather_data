#http://joehamman.com/2013/10/12/plotting-netCDF-data-with-Python/
#https://wizardforcel.gitbooks.io/matplotlib-intro-tut/matplotlib/27.html

from netCDF4 import Dataset
from netCDF4 import num2date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm

my_example_nc_file = 'ECMWF_data/_grib2netcdf-atls00-98f536083ae965b31b0d04811be6f4c6-YC7oFn.nc'
fh = Dataset(my_example_nc_file, mode='r')

#print(fh.variables)
print(fh.variables.keys())

lons = fh.variables['longitude'][:]
lats = fh.variables['latitude'][:]
time= fh.variables['time'][:]
u10= fh.variables['u10'][:]
v10= fh.variables['v10'][:]
swh=fh.variables['swh'][:]
mwd=fh.variables['mwd'][:]
mwp=fh.variables['mwp'][:]

latcorners = fh.variables['latitude'][:]
loncorners = -fh.variables['longitude'][:]

#导出时间,将gregorian时间转换为标准时间
dates = num2date(time, fh.variables['time'].units, fh.variables['time'].calendar)
df=pd.DataFrame(dates,columns=['dates'])
#df.to_csv('saved_data/1/time.csv')

u10_units = fh.variables['u10'].units
v10_units = fh.variables['v10'].units
swh_units = fh.variables['swh'].units
mwd_units = fh.variables['mwd'].units
mwp_units = fh.variables['mwp'].units

fh.close()

# Get some parameters for the Stereographic Projection
lon_0 = lons.mean()
lat_0 = lats.mean()
#print(lon_0)
#print(lat_0)

#各个参数是什么意思
#m = Basemap(width=10000000,height=5000000,resolution='l',projection='stere',\
#            lat_ts=40,lat_0=50,lon_0=0)
plt.figure(figsize=(12,6))
m = Basemap(width=12000000,
            height=8000000,
            resolution='l',
            projection='mill',
            llcrnrlat = -50,
            llcrnrlon = 0,
            urcrnrlat = 70,
            urcrnrlon = 180)

'''Basemap的参数解析：
projection: stere立体投影
法1设置边界经纬度：llcrnrlon地图左边经度，urcrnrlon地图右边经度，llcrnrlat地图下方纬度，urcrnrlat地图上方纬度
法2设置中心点高与宽：width宽，height高，lon_0中心点的经度，lat_0中心点的纬度'''


# Because our lon and lat variables are 1D,use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

#画u10、v10、swh、mwd、mwp图
i=0
title=['10 metre U wind component','10 metre v wind component','significant height of combined waves and swell',
       'mean wave direction', 'mean wave period']
units=[u10_units,v10_units,swh_units,mwd_units,mwp_units]

for xx in [u10,v10,swh,mwd,mwp]:
    xx_=xx[1,:,:]
    # Plot Data
    cs = m.pcolor(xi,yi,np.squeeze(xx_),cmap=plt.cm.jet)
#    print('xi.shape',xi.shape)
#    print('yi.shape', yi.shape)
#    print('np.squeeze shape',np.squeeze(xx_).shape)
    #cs = m.pcolor(xi, yi, np.squeeze(xx_))
    # Add Grid Lines
    m.drawparallels(np.arange(-80., 81., 20.), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(-180., 181., 20.), labels=[0,0,0,1], fontsize=10)

    # Add Coastlines, States, and Country Boundaries
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    m.fillcontinents(color='coral', lake_color='aqua')
    #m.shadedrelief()
    m.etopo()
    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="5%")
    cbar.set_label(units[i])
    # Add Title
    plt.title(title[i])
    plt.show()
    #plt.savefig('saved_data/1/%s.jpg'%title[i])
    i+=1

