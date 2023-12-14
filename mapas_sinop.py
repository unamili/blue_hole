import xarray as xr
from paths import paths
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import numpy as np
import pickle

data_path = paths().data_path()
save_path = paths().save_path()
plots_path = paths().plots_path()

filename = data_path + "sst_MUR/2017/sst_agujeroazul_2017_diaspreviosincluidos.nc"
data = xr.open_dataset(filename)
sst = data.analysed_sst

sst_sur = sst.sel(time=slice("2017-10-27", "2017-10-29")).mean(dim="time")
sst_central = sst.sel(time=slice("2017-10-31", "2017-11-02")).mean(dim="time")
sst_norte = sst.sel(time=slice("2017-11-03", "2017-11-06")).mean(dim="time")

sst_campaña = sst.sel(time=slice("2017-10-27", "2017-11-06")).mean(dim="time")

#Load info de transectas
file = open(save_path + "/Transectas/transecta_sur_2017",'rb')
transecta_sur_2017 = pickle.load(file)
file = open(save_path + "/Transectas/transecta_central_2017",'rb')
transecta_central_2017 = pickle.load(file)
file = open(save_path + "/Transectas/transecta_norte_2017",'rb')
transecta_norte_2017 = pickle.load(file)
file = open(save_path + "/Transectas/transecta_sur_2021",'rb')
transecta_sur_2021 = pickle.load(file)
file = open(save_path + "/Transectas/transecta_central_2021",'rb')
transecta_central_2021 = pickle.load(file)


#DATOS VIENTO
filename = '/media/agulhas/HDD4T/Documents/Rutinas/Data/viento/reanalisis/wind_1979to2022_zoom.nc'
data = xr.open_dataset(filename)
u = data.u10
v = data.v10

u_sur = u.sel(time=slice("2017-10-27", "2017-10-29")).mean(dim="time")
u_central = u.sel(time=slice("2017-10-31", "2017-11-02")).mean(dim="time")
u_norte = u.sel(time=slice("2017-11-03", "2017-11-06")).mean(dim="time")
v_sur = v.sel(time=slice("2017-10-27", "2017-10-29")).mean(dim="time")
v_central = v.sel(time=slice("2017-10-31", "2017-11-02")).mean(dim="time")
v_norte = v.sel(time=slice("2017-11-03", "2017-11-06")).mean(dim="time")

u_campaña = u.sel(time=slice("2017-10-27", "2017-11-06" )).mean(dim="time")
v_campaña = v.sel(time=slice("2017-10-27", "2017-11-06" )).mean(dim="time")

#Parametros para graficar
lon_w = -68
lon_e = -55
lat_s = -48
lat_n = -42

var = sst_sur.values-273
cmap = 'plasma'
lons = sst_sur.lon
lats = sst_sur.lat

transecta = transecta_sur_2017
lons_cast = transecta.lon.unique()
lats_cast = transecta.lat.unique()

fig = plt.figure(figsize=(8, 8))
ax1 = plt.subplot(projection=ccrs.Mercator())
ax2 = plt.subplot(projection=ccrs.Mercator())
ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                       linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cl = ax2.contourf(lons, lats, var, cmap=cmap, alpha=0.9, transform=ccrs.PlateCarree(), extend='both')
ax2.scatter(lons_cast, lats_cast, transform=ccrs.PlateCarree(), color='white')
cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
cb.ax.set_title('Temperature [°C]', fontsize=10)
ax1.set_title("Transecta Sur")
quiv = ax2.quiver(u_sur.longitude.values[::4], v_sur.latitude.values[::4], u_sur.values[::4,::4] , v_sur.values[::4,::4], pivot='middle', transform=ccrs.PlateCarree(), alpha=0.8, scale=100)
ax1.quiverkey(quiv, X=0.1, Y=0.95, U=5, label='5 m/s', labelpos='E')

fig.savefig(plots_path + 'sst_transecta_sur+viento' + '.png', dpi=300, bbox_inches='tight')


#CENTRAL
var = sst_central.values-273
cmap = 'plasma'
lons = sst_central.lon
lats = sst_central.lat

transecta = transecta_central_2017
lons_cast = transecta.lon.unique()
lats_cast = transecta.lat.unique()

fig = plt.figure(figsize=(8, 8))
ax1 = plt.subplot(projection=ccrs.Mercator())
ax2 = plt.subplot(projection=ccrs.Mercator())
ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                       linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cl = ax2.contourf(lons, lats, var, cmap=cmap, alpha=0.9, transform=ccrs.PlateCarree(), extend='both')
ax2.scatter(lons_cast, lats_cast, transform=ccrs.PlateCarree(), color='white')
cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
cb.ax.set_title('Temperature [°C]', fontsize=10)
ax1.set_title("Transecta Central")
quiv = ax2.quiver(u_central.longitude.values[::4], v_central.latitude.values[::4], u_central.values[::4,::4] , v_central.values[::4,::4], pivot='middle', transform=ccrs.PlateCarree(), alpha=0.8, scale=100)
ax1.quiverkey(quiv, X=0.1, Y=0.95, U=5, label='5 m/s', labelpos='E')

fig.savefig(plots_path + 'sst_transecta_central+viento' + '.png', dpi=300, bbox_inches='tight')


#NORTE
var = sst_norte.values-273
cmap = 'plasma'
lons = sst_norte.lon
lats = sst_norte.lat

transecta = transecta_norte_2017
lons_cast = transecta.lon.unique()
lats_cast = transecta.lat.unique()

fig = plt.figure(figsize=(8, 8))
ax1 = plt.subplot(projection=ccrs.Mercator())
ax2 = plt.subplot(projection=ccrs.Mercator())
ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                       linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cl = ax2.contourf(lons, lats, var, cmap=cmap, alpha=0.9, transform=ccrs.PlateCarree(), extend='both')
ax2.scatter(lons_cast, lats_cast, transform=ccrs.PlateCarree(), color='white')
cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
cb.ax.set_title('Temperature [°C]', fontsize=10)
ax1.set_title("Transecta Norte")
quiv = ax2.quiver(u_norte.longitude.values[::4], v_norte.latitude.values[::4], u_norte.values[::4,::4] , v_norte.values[::4,::4], pivot='middle', transform=ccrs.PlateCarree(), alpha=0.8, scale=100)
ax1.quiverkey(quiv, X=0.1, Y=0.95, U=5, label='5 m/s', labelpos='E')

fig.savefig(plots_path + 'sst_transecta_norte+viento' + '.png', dpi=300, bbox_inches='tight')


#Grafico medio de toda la campaña
lons_campaña = np.hstack((transecta_sur_2017.lon.unique(), transecta_central_2017.lon.unique(), transecta_norte_2017.lon.unique()))
lats_campaña = np.hstack((transecta_sur_2017.lat.unique(), transecta_central_2017.lat.unique(), transecta_norte_2017.lat.unique()))

fig = plt.figure(figsize=(8, 8))
ax1 = plt.subplot(projection=ccrs.Mercator())
ax2 = plt.subplot(projection=ccrs.Mercator())
ax1.set_extent([lon_w, lon_e, lat_s, lat_n], crs=ccrs.PlateCarree())
ax1.coastlines(resolution='50m', color='black', linewidths=0.4, zorder=5)
gl = ax1.gridlines(crs=ccrs.PlateCarree(central_longitude=0), draw_labels=True,
                       linewidth=.5, color='gray', alpha=0.5, linestyle='--', zorder=6)
gl.xlabels_top = gl.ylabels_right = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
cl = ax2.contourf(sst_campaña.lon.values, sst_campaña.lat.values, sst_campaña.values-273, cmap=cmap, alpha=0.9, transform=ccrs.PlateCarree(), extend='both')
ax2.scatter(lons_campaña, lats_campaña, transform=ccrs.PlateCarree(), color='white')
cb = fig.colorbar(cl, aspect=40, orientation='horizontal', pad=0.09)
cb.ax.set_title('Temperature [°C]', fontsize=10)
ax1.set_title("Valores medios - campaña 2017")
quiv = ax2.quiver(u_campaña.longitude.values[::4], v_campaña.latitude.values[::4], u_campaña.values[::4,::4] , v_campaña.values[::4,::4], pivot='middle', transform=ccrs.PlateCarree(), alpha=0.8, scale=100 )
ax1.quiverkey(quiv, X=0.1, Y=0.95, U=5, label='5 m/s', labelpos='E')

fig.savefig(plots_path + 'sst_viento_medio_camp_2017' + '.png', dpi=300, bbox_inches='tight')

