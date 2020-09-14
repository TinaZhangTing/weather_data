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

#将时间、经纬度都存下来
#dates = num2date(time, fh.variables['time'].units, fh.variables['time'].calendar)
#df=pd.DataFrame(dates,columns=['dates'])
#df.to_csv('ECMWF_data/aCdata/time.csv')
#
#df2=pd.DataFrame(lons,columns=['lons'])
#df2.to_csv('ECMWF_data/aCdata/lons.csv')
#
#df3= pd.DataFrame(lats,columns=['lats'])
#df3.to_csv('ECMWF_data/aCdata/lats.csv')

#将u10存下来
#for i in range(10):
#    u=u10[i,:,:]
#    file_name='u10'+'_'+str(i+1)
#    file='ECMWF_data/aCdata/'+file_name+'.csv'
#    df= pd.DataFrame(u)
#    df.to_csv(file,index=None, columns=None)
#    
# 将v10存下来
#for i in range(10):
#    v=v10[i,:,:]
#    file_name='v10'+'_'+str(i+1)
#    file='ECMWF_data/7jdata/'+file_name+'.csv'
#    df= pd.DataFrame(v)
#    df.to_csv(file)

# 将si存下来    
#for i in range(10):
#    si=si10[i,:,:]
#    file_name='si10'+'_'+str(i+1)
#    file='ECMWF_data/7jdata/'+file_name+'.csv'
#    df= pd.DataFrame(si)
#    df.to_csv(file)

#经度    
x=pd.read_csv('ECMWF_data/aCdata/lons.csv')
x=x.iloc[:,1]

#纬度
y=pd.read_csv('ECMWF_data/aCdata/lats.csv')
y=y.iloc[:,1]

#天津船航路点气象数据提取
route=pd.read_csv('ECMWF_data/route_port_Tianjinship_weather.csv')
routedata=route.iloc[:,4:6]
routedata=np.round(routedata,1)

x_array=np.round(np.arange(0,360,0.1),1) #lon在此查找
x_array=x_array.tolist() 

y_array=np.round(np.arange(90,-90,-0.1),1)#lat在此查找
y_array=y_array.tolist()

#speed_item=[u10,v10,si10]
#for speed_data in speed_item:
for i in range(12):
    #按月份取数据
    u10_m=u10[i,:,:]
    v10_m=v10[i,:,:]
    si10_m=si10[i,:,:]
    
    x_,y_=np.meshgrid(x,y)
    z_u10=np.squeeze(u10_m)
    z_v10=np.squeeze(v10_m)
    z_si10=np.squeeze(si10_m)
    
#    fig = plt.figure(figsize=(12, 6)) 
#    #Draw sub-graph1  
#    c_map=cm.coolwarm
#    #ax=plt.subplot(1, 2, 1,projection = '3d')
#    ax = fig.gca(projection='3d')   
#    surf = ax.plot_surface(x_, y_, z, rstride=2, cstride=2, cmap=c_map,linewidth=0.5, antialiased=True)  
#    ax.set_xlabel('x')  
#    ax.set_ylabel('y')  
#    ax.set_zlabel('u10 wind speed')  
#    #plt.colorbar(surf, shrink=0.5, aspect=5)#标注
#    plt.show() 
    
    #二维插值  
    newfunc_u10 = interpolate.interp2d(x, y, z_u10, kind='cubic')#newfunc为一个函数
    newfunc_v10 = interpolate.interp2d(x, y, z_v10, kind='cubic')
    newfunc_si10 = interpolate.interp2d(x, y, z_si10, kind='cubic')
    
    # 计算100*100的网格上的插值  
    xnew = np.arange(0,360,0.1)#x  
    ynew = np.arange(90,-90,-0.1)#y  
    fnew_u10 = newfunc_u10(xnew, ynew)#仅仅是y值   100*100的值  np.shape(fnew) is 100*100  
    fnew_v10 = newfunc_v10(xnew, ynew)
    fnew_si10 = newfunc_si10(xnew, ynew)
    
#    xnew, ynew = np.meshgrid(xnew, ynew)  
#    ax2=plt.subplot(1, 2, 2,projection = '3d')  
#    surf2 = ax2.plot_surface(xnew, ynew, fnew, rstride=2, cstride=2, cmap=c_map,linewidth=0.5, antialiased=True)  
#    ax2.set_xlabel('xnew')  
#    ax2.set_ylabel('ynew')  
#    ax2.set_zlabel('fnew')  
#    #plt.colorbar(surf2, shrink=0.5, aspect=5)#标注  
#      
#    plt.show()
    #plt.savefig('ECMWF_data/aCdata/newprojection.png')
    
    
    u10_list=[]
    v10_list=[]
    si10_list=[]
    item_list=[u10_list, v10_list, si10_list]
    fnew_list=[fnew_u10, fnew_v10, fnew_si10]
    for j in range(3):
        speed_item=item_list[j]
        fnew=fnew_list[j]
        for k in range(routedata.shape[0]):
            lat_value=routedata.iloc[k,0]
            lon_value=routedata.iloc[k,1]
            lat_index= y_array.index(lat_value)
            lon_index= x_array.index(lon_value)
            speeditem=fnew[lat_index,lon_index]
            speed_item.append(speeditem)
            
    u10_list=pd.Series(u10_list)
    v10_list=pd.Series(v10_list)
    si10_list=pd.Series(si10_list)
    
    windspeed_data=pd.concat([u10_list,v10_list,si10_list],axis=1)
    windspeed_data.columns=['u10','v10','si10']
    
    file_name='Windspeed_Tianjin'+'_month_'+str(i+1)
    file='ECMWF_data/aCdata/'+file_name+'.csv'    
    windspeed_data.to_csv(file)

