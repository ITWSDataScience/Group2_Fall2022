import h5py
import numpy as np
import pandas as pd

dataset = h5py.File(r"C:\Users\shant\Downloads\percipitation.HDF5", 'r')
grid = dataset['Grid']
print(grid.keys())

longitude_values = np.repeat(list(grid['lon']), 1800)
latitude_values = list(grid['lat'])*3600
precipitation_values = np.array(list(grid['precipitationUncal'])).flatten()

dataset = pd.DataFrame({"lon": longitude_values, "lat": latitude_values, "precipitationUncal": precipitation_values})
dataset.columns = [grid['lon'].attrs['standard_name'].decode() + " (" + grid['lon'].attrs['units'].decode() + ")",
                   grid['lat'].attrs['standard_name'].decode() + " (" + grid['lat'].attrs['units'].decode() + ")",
                   "Precipitation (" + grid['precipitationUncal'].attrs['units'].decode() + ")",]
dataset.head()

dataset['Precipitation (mm/hr)'] = dataset['Precipitation (mm/hr)'].mask(
                                    dataset['Precipitation (mm/hr)'] == -9999.9, 0)

dataset.to_csv("precipitation_jan_2020.csv", index = False)

print('abc')