from netCDF4 import Dataset
from netCDF4 import num2date
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D  
#import matplotlib as mpl  
from scipy import interpolate  
import matplotlib.cm as cm  
import matplotlib.pyplot as plt

my_example_nc_file = 'ECMWF_data/_grib2netcdf-atls06-a82bacafb5c306db76464bc7e824bb75-aC8jVF.nc'
fh = Dataset(my_example_nc_file, mode='r')

#print(fh.variables)
print(fh.variables.keys())

lons = fh.variables['longitude'][:]
lats = fh.variables['latitude'][:]
time= fh.variables['time'][:]
u10= fh.variables['u10'][:]
v10= fh.variables['v10'][:]
si10=fh.variables['si10'][:]

dates = num2date(time, fh.variables['time'].units, fh.variables['time'].calendar)
df=pd.DataFrame(dates,columns=['dates'])
df.to_csv('ECMWF_data/aCdata/time.csv')

df2=pd.DataFrame(lons,columns=['lons'])
df2.to_csv('ECMWF_data/aCdata/lons.csv')

df3= pd.DataFrame(lats,columns=['lats'])
df3.to_csv('ECMWF_data/aCdata/lats.csv')

#for i in range(10):
#    u=u10[i,:,:]
#    file_name='u10'+'_'+str(i+1)
#    file='ECMWF_data/7jdata/'+file_name+'.csv'
#    df= pd.DataFrame(u)
#    df.to_csv(file,index=None, columns=None)
    
#
#for i in range(10):
#    v=v10[i,:,:]
#    file_name='v10'+'_'+str(i+1)
#    file='ECMWF_data/7jdata/'+file_name+'.csv'
#    df= pd.DataFrame(v)
#    df.to_csv(file)
#    
#for i in range(10):
#    si=si10[i,:,:]
#    file_name='si10'+'_'+str(i+1)
#    file='ECMWF_data/7jdata/'+file_name+'.csv'
#    df= pd.DataFrame(si)
#    df.to_csv(file)
    
x=pd.read_csv('ECMWF_data/aCdata/lons.csv')
x=x.iloc[:,1]

y=pd.read_csv('ECMWF_data/aCdata/lats.csv')
y=y.iloc[:,1]

#1月份的u10数据
u10_1=u10[0,:,:]

x_,y_=np.meshgrid(x,y)
z=np.squeeze(u10_1)

fig = plt.figure(figsize=(12, 6)) 
#Draw sub-graph1  
c_map=cm.coolwarm
#ax=plt.subplot(1, 2, 1,projection = '3d')
ax = fig.gca(projection='3d')   
surf = ax.plot_surface(x_, y_, z, rstride=2, cstride=2, cmap=c_map,linewidth=0.5, antialiased=True)  
ax.set_xlabel('x')  
ax.set_ylabel('y')  
ax.set_zlabel('u10 wind speed')  
#plt.colorbar(surf, shrink=0.5, aspect=5)#标注 

#二维插值  
newfunc = interpolate.interp2d(x, y, z, kind='cubic')#newfunc为一个函数
#备注： cubic为三阶样条曲线插值

# 计算100*100的网格上的插值  
xnew = np.arange(0,360,0.1)#x  
ynew = np.arange(90,-90,-0.1)#y  
fnew = newfunc(xnew, ynew)#仅仅是y值   100*100的值  np.shape(fnew) is 100*100  
xnew, ynew = np.meshgrid(xnew, ynew)  
ax2=plt.subplot(1, 2, 2,projection = '3d')  
surf2 = ax2.plot_surface(xnew, ynew, fnew, rstride=2, cstride=2, cmap=c_map,linewidth=0.5, antialiased=True)  
ax2.set_xlabel('xnew')  
ax2.set_ylabel('ynew')  
ax2.set_zlabel('fnew')  
#plt.colorbar(surf2, shrink=0.5, aspect=5)#标注  
  
plt.show()
#plt.savefig('ECMWF_data/aCdata/newprojection.png')

#天津船航路点气象数据提取
route=pd.read_csv('ECMWF_data/route_port_Tianjinship_weather.csv')
routedata=route.iloc[:,4:6]
routedata=np.round(routedata,1)

x_array=np.round(np.arange(0,360,0.1),1) #lon在此查找
x_array=x_array.tolist() 

y_array=np.round(np.arange(90,-90,-0.1),1)#lat在此查找
y_array=y_array.tolist()
windspeed_list=[]

for i in range(routedata.shape[0]):
    lat_value=routedata.iloc[i,0]
    lon_value=routedata.iloc[i,1]
    lat_index= y_array.index(lat_value)
    lon_index= x_array.index(lon_value)
    windspeed=fnew[lat_index,lon_index]
    windspeed_list.append(windspeed)

windspeed_df=pd.DataFrame(data=windspeed_list, columns=['windspeed'])    
windspeed_df.to_csv('windspeed_tianjin_u10_1.csv')

