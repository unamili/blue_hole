import imageio
import imageio.v2 as imageio
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
import os
import xarray as xr
from paths import paths

##
data_path = paths().data_path()

#Datos de viento
filename = '/media/agulhas/HDD4T/Documents/Rutinas/Data/viento/reanalisis/wind_1979to2022_zoom.nc'
data = xr.open_dataset(filename)
u = data.u10
v = data.v10

u_horario = u.sel(time=slice("2017-10-10", "2017-11-06" ))
v_horario = v.sel(time=slice("2017-10-10", "2017-11-06" ))

u_diario = u_horario.resample(time='1D').mean()
v_diario = v_horario.resample(time='1D').mean()

#Datos de SST
filename = data_path + "sst_MUR/2017/sst_agujeroazul_2017_diaspreviosincluidos.nc"
data = xr.open_dataset(filename)
sst = data.analysed_sst.sel(time=slice("2017-10-10", "2017-11-06"))


lon_w = u_diario.longitude.min()
lon_e = u_diario.longitude.max()
lat_s = u_diario.latitude.min()
lat_n = u_diario.latitude.max()

lons = u_diario.longitude.values
lats = u_diario.latitude.values

lons_sst = sst.lon.values
lats_sst = sst.lat.values

u = u_diario.values
v = v_diario.values
clev = 20

var = sst.values-273

#clevs = np.linspace(-3, 3, 21)
nombre_var = 'SST'

filenames = []

for i in range(len(sst.time)):
    nombre_salida = 'SST -' + str(sst.time.values[i])[:-19]
    fig = plt.figure(figsize=(8, 8))
    ax1 = plt.subplot(projection=ccrs.Mercator())
    ax2 = plt.subplot(projection=ccrs.Mercator())
    ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
    # ax1.set_extent([-70, -55, -55, -40], crs=ccrs.PlateCarree()) # Para hacer un zoom en la patagonia
    ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
    gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                       linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
    gl.xlabels_top = gl.ylabels_right = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    cl = ax2.contourf(lons_sst, lats_sst, var[i , : , :], cmap=plt.cm.plasma, transform=ccrs.PlateCarree(), extend='both')
    cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
    ax1.quiver(lons[::5], lats[::5], u[i,::5, ::5], v[i, ::5, ::5], pivot='middle', transform=ccrs.PlateCarree(), scale=100)
    # ax1.quiver(lons[::5], lats[::5], u[::5, ::5], v[::5, ::5], pivot='middle', transform=ccrs.PlateCarree())
    cb.ax.set_title(nombre_var, fontsize=10)
    ax1.set_title(nombre_salida)
    # create file name and append it to a list
    filename = f'{i}.png'
    filenames.append(filename)

    # save frame
    plt.savefig(filename)
    plt.close()
# build gif

with imageio.get_writer('campaña2017.gif', mode='I', fps=1) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)

# Remove files
for filename in set(filenames):
    os.remove(filename)