import xarray as xr
import matplotlib.pyplot as plt

archivo_data =  '/media/agulhas/HDD4T/Documents/Rutinas/Data/satelitales/sst/MW OI/sst_1998to2022_recorte.nc'

data = xr.open_dataset(archivo_data)

sst = data.analysed_sst

serie = sst.sel(lat=-57, lon= -67, method= 'nearest')
serie = serie.sel(time=slice('2005/01/01', '2022/01/01'))
serie = serie-273.15

bins = [3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5]

fig, ax = plt.subplots()
n, bins, patches = ax.hist(serie, bins=bins, edgecolor='white')
ax.set_xlabel('SST [°C]')
ax.set_ylabel('')
for i, bar in enumerate(patches):
    height = bar.get_height()
    if height > 0:
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{int(height)}', ha='center')
plt.show()
