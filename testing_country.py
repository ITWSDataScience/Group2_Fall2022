import xarray as xr
from geopy.geocoders import Nominatim
from geopy.point import Point
import pandas as pd

precip_nc_file = '20220101.nc4'

ds = xr.open_dataset(precip_nc_file)
df = ds.to_dataframe()
#73.6753792663, 18.197700914, 135.026311477, 53.4588044297
df = df.query('lon >= -72.3049515449 and lon <= -61.7582848782 and lat >= 7.50 and lat <= 12.1623070337')
df = df.groupby(level = ['lat', 'lon'])['precipitationCal'].mean()


for i in range(2,13):
    if i< 10:
        precip_nc_file = '20220'+str(i)+'01.nc4'
        
    else:
        precip_nc_file = '2022'+str(i)+'01.nc4'
        
    if i < 11:
        before = '20220'+str(i-1)+'01.nc4'
    else:
        before = '2022'+str(i-1)+'01.nc4'

    ds1 = xr.open_dataset(precip_nc_file)
    df1 = ds1.to_dataframe()
    #-73.3049515449, 0.724452215982, -59.7582848782, 12.1623070337
    df1 = df1.query('lon >= -73.3049515449 and lon <= -59.7582848782 and lat >= 7.50 and lat <= 12.1623070337')
    df1 = df1.groupby(level = ['lat', 'lon'])['precipitationCal'].mean()
    
    df = pd.merge(df, df1, how='inner', on=['lat', 'lon'], suffixes=(before, precip_nc_file))
    
    geolocator = Nominatim(user_agent="geoapiExcercise")
    for i in range(len(df)):
        location = geolocator.reverse(Point(df.index[i][0],df.index[i][1]))
        if not location:
            print("none")
            continue
        else:
            address = location.raw['address']
            country = address.get('country', '')
            print(country)
            
  
#df.to_csv('syria.csv',index=True, header=True)

