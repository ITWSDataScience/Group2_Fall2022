import xarray as xr
import pandas as pd
import csv


def clean(df, region, time):
    df = df.groupby(['lat', 'lon']).agg({'PS': 'mean'})
    df = df.reset_index()

    print(df.keys())

    df['region'] = df.apply(lambda row: region, axis=1)
    df['time'] = df.apply(lambda row: time, axis=1)
    return df


# precip_nc_file = ['2021_01_01.nc4', '2021_02_01.nc4', '2021_03_01.nc4', '2021_04_01.nc4', '2021_05_01.nc4',
#                  '2021_06_01.nc4', '2021_07_01.nc4', '2021_08_01.nc4', '2021_09_01.nc4', '2021_10_01.nc4',
#                  '2021_11_01.nc4', '2021_12_01.nc4']

dates = ['2021_01_01', '2021_02_01', '2021_03_01', '2021_04_01', '2021_05_01',
                  '2021_06_01', '2021_07_01', '2021_08_01', '2021_09_01', '2021_10_01',
                  '2021_11_01', '2021_12_01']

for i in dates:
    filename = i + '.nc4'
    ds = xr.open_dataset(filename)
    df1 = ds.to_dataframe()


    query = ['lon >= -72.3049515449 and lon <= -61.7582848782 and lat >= 7.50 and lat <= 12.1623070337',
             'lon >= -3.14 and lon <= 1.3 and lat >= 51.15  and lat <= 54.74']
    country = ['Venezuela', 'England']
    time = i
    for q in [0, 1]:
        df = df1.query(query[q])
        df = clean(df, country[q], time)
        csv_name = country[q] + time + '.csv'
        df.to_csv(csv_name)