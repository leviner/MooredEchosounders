import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import seawater

tsFiles = glob('E:/MooredEchosounders/data/physicalData/*TS.csv')
site=[1,11,4]
dt = ['2018-08-15','2018-08-12','2018-08-15']
dfs = []
fig, (ax1,ax2,ax3) = plt.subplots(3,1,figsize=(15,8))
for i in [0,1,2]:
    a = pd.read_csv(tsFiles[i])
    a['time (UTC)'] = pd.to_datetime(a['time (UTC)'])
    y = a[a['time (UTC)'] < pd.to_datetime(dt[i]).tz_localize('UTC')]
    print('Site C',str(site[i]),'2017-2018: \n - T:',round(y['temperature (degree_C)'].mean(),3),'\n - S:',round(y['salinity'].mean(),3),
          '\n - C:',round(seawater.eos80.svel(y['salinity'].mean(),y['temperature (degree_C)'].mean(),0),3),
          '(',round(seawater.eos80.svel(y['salinity'],y['temperature (degree_C)'],0).min(),3),
          round(seawater.eos80.svel(y['salinity'],y['temperature (degree_C)'],0).max(),3),')')
    y['temperature (degree_C)'].plot(ax=fig.axes[i],secondary_y=False,color='skyblue',linewidth=2, label = 'Temperature')
    y['salinity'].plot(ax=fig.axes[i],secondary_y=True,color='mediumpurple',linewidth=2, label = 'Salinity')
    y = a[a['time (UTC)'] > pd.to_datetime(dt[i]).tz_localize('UTC')]
    print('Site C',str(site[i]),'2018-2019: \n - T:',round(y['temperature (degree_C)'].mean(),3),'\n - S:',round(y['salinity'].mean(),3),
          '\n - C:',round(seawater.eos80.svel(y['salinity'].mean(),y['temperature (degree_C)'].mean(),0),3),
          '(',round(seawater.eos80.svel(y['salinity'],y['temperature (degree_C)'],0).min(),3),
          round(seawater.eos80.svel(y['salinity'],y['temperature (degree_C)'],0).max(),3),')')
    y['temperature (degree_C)'].plot(ax=fig.axes[i],secondary_y=False,color='deepskyblue',linewidth=2, label = 'Temperature')
    y['salinity'].plot(ax=fig.axes[i],secondary_y=True,color='purple',linewidth=2, label = 'Salinity')
    plt.title('Purple = Salinity         Blue = Temperature')
plt.show()