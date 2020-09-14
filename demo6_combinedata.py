# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:18:52 2020

@author: aicter
"""

import pandas as pd
import os

route_file='E:\\weather_data\\route_Tianjinship.csv'
weather_month_file=os.listdir('E:\weather_data\Windspeed_Tianjin_month')
weather_filelist=[]
for file in weather_month_file:
    weather_filelist.append(os.path.join('E:\weather_data\Windspeed_Tianjin_month',file))
    
#print(weather_filelist)
#print(weather_month_file)
#route_data=pd.read_csv(route_file)
#print(route_data.head())
#weather_data=pd.read_csv(weather_filelist[0])
#print(weather_data.head())

i=1    
for file in weather_filelist:
    route_data=pd.read_csv(route_file)
    route_data= route_data.iloc[:,1:]
    weather_data=pd.read_csv(file)
    weather_data= weather_data.iloc[:,1:]
    combined_data= pd.concat([route_data, weather_data], axis=1)
    file_name='weather_Tianjin'+'_month_'+str(i)
    file='E:/weather_data/'+file_name+'.csv'    
    combined_data.to_csv(file)
    i+=1