# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 15:33:38 2020

@author: aicter
"""

#https://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(0,10,num=11,endpoint=True)
y=np.cos(-x**2/9.0)
f=interp1d(x,y,kind='cubic')

#重要备注： cubic为三阶样条曲线插值。插值与拟合的不同之处在于，插值要求曲线通过所有的已知数据

xnew=np.linspace(0,10,num=41,endpoint=True)
plt.plot(x,y,'o',xnew,f(xnew),'--')

plt.legend(['data','cubic'],loc='best')
plt.show()

#用主机的数据做测试
a=[1600,1360,1200,800,400]
b=[195.3,192.2,192.8,200.6,225.4]
fu= interp1d(a,b,kind='cubic')
#anew=np.linspace(1200,1500,num=3001,endpoint=True)
anew=np.linspace(400,1600,num=12001,endpoint=True)
plt.plot(a,b,'o',anew,fu(anew),'--')
plt.legend(['data','cubic'],loc='best')
plt.show()

