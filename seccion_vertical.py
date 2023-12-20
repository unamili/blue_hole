import math
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import pickle
from paths import paths
import pandas as pd
import xarray as xr

save_path = paths().save_path()
bath_path = paths().bath_path()
plots_path = paths().plots_path()

bat = xr.open_dataset(bath_path + 'gebco_2022.nc')

with open(save_path + '/Transectas/transecta_norte_2017', 'rb') as file:
    transecta = pickle.load(file)
with open(save_path + '/Transectas/transecta_central_2017', 'rb') as file:
    transecta = pickle.load(file)
with open(save_path + '/Transectas/transecta_sur_2017', 'rb') as file:
    transecta = pickle.load(file)
with open(save_path + '/Transectas/transecta_sur_2021', 'rb') as file:
    transecta = pickle.load(file)
with open(save_path + '/Transectas/transecta_central_2021', 'rb') as file:
    transecta = pickle.load(file)


transecta = transecta.sort_values(by=['lon', 'pres'])


cant_estaciones = len(transecta.lat.unique())
lats = transecta.lat.unique()
lons = transecta.lon.unique()
prof_max = transecta.pres.max()

#distancia entre estaciones dentro de la seccion
dist_entre_est = [0]*cant_estaciones #me armo una lista de ceros del tamaño de la cantidad de estaciones
dist = [0]*cant_estaciones #mismo para la distancia desde el cero
for i in range(1,cant_estaciones):
    a = 90-lats[i-1]
    b = 90-lats[i]
    phi = lons[i-1]-lons[i]
    cosp = math.cos(math.radians(a))*math.cos(math.radians(b))+math.sin(math.radians(a))*math.sin(math.radians(b))*math.cos(math.radians(phi))
    p = math.degrees(math.acos(cosp))
    dist_entre_est[i] = p*6371*math.pi/180  #dist km
    dist[0] = 0
    dist[i] = dist_entre_est[i]+dist[i-1]

#array de profundidades:
z = np.linspace(0, prof_max, round(prof_max+1))

#Seccion de temperatura con nan
temp = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())
sal = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())
sigma = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())

# Iteramos en las filas de la transecta, completando el df de temp (o sal) con los valores obtenidos para la longitud y profundidad correspondientes
for i, row in transecta.iterrows():
    temp.iloc[int(row['pres'])][row['lon']] = row['temp']
    sal.iloc[int(row['pres'])][row['lon']] = row['sal']
    sigma.iloc[int(row['pres'])][row['lon']] = row['sigma']

temp_array = temp.values
sal_array = sal.values
sigma_array = sigma.values

for st in range(0, cant_estaciones):
    primero_con_nan_S = len(temp_array[:, st][np.isnan(temp_array[:, st]) == False]) #primero_con_nan es el primer valor del perfil en tener un nan
    temp_array[primero_con_nan_S:, st] = temp_array[primero_con_nan_S-1, st] #completa el perfil con el ultimo valor distinto de nan
    sal_array[primero_con_nan_S:, st] = sal_array[primero_con_nan_S-1, st]
    sigma_array[primero_con_nan_S:, st] = sigma_array[primero_con_nan_S-1, st]


#Interpolacion entre estaciones con una resolucion de 100ptos por seccion:
dist_aux, z_aux = np.meshgrid(dist, z)
points = (dist_aux.flatten(), z_aux.flatten())
values_T = temp_array.flatten()
values_S = sal_array.flatten()
values_sigma = sigma_array.flatten()
x, p = np.meshgrid(np.linspace(0, dist[-1], 100), z)
data_T = griddata(points, values_T, (x, p), method='linear')
data_S = griddata(points, values_S, (x, p), method='linear')
data_sigma = griddata(points, values_sigma, (x, p), method='linear')

#Luego suaviza los datos, con algun criterio y lo vuelve a llamar data_S

#BATIMETRIA
bat_transecta = [0]*cant_estaciones
for st in range(cant_estaciones):
   bat_transecta[st] = -bat.sel(lat=lats[st], lon=lons[st], method='nearest').elevation.values


### PLOTS

#SECCION - TEMPERATURA - NORTE

#Niveles
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
levels_contorno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

cmap = plt.cm.get_cmap('Reds', 50)
#cmap = 'autumn'
nombre_salida = 'seccion_norte_2017_temperatura'
txt = 'North - 2017'
txt2 = ''
txt3 = 'Temperature (°C)'
vmin, vmax = np.nanmin(data_T), np.nanmax(data_T)

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#pimeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_T[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_T[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
ax1.plot(dist[0:5], bat_transecta[0:5], color='grey')
plt.fill_between(dist[:5], bat_transecta[:5], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_T[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_T[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000, 2500],size = 18)
#ax2.text(3, 830, txt2, size=24)
#ax2.axis([0, 156, 850, 200])
plt.gca().invert_yaxis()
ax2.plot(dist[4:], bat_transecta[4:], color='grey')
plt.fill_between(dist[4:], bat_transecta[4:], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(dist[:5], [298, 298, 298, 298, 298], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


#SECCION SALINIDAD - NORTE
#Niveles
levels = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]
levels_contorno = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]

cmap = plt.cm.get_cmap('Blues', 50)

nombre_salida = 'seccion_norte_2017_salinidad'
txt = 'North - 2017'
txt2 = ''
txt3 = 'Salinity (UPS)'
vmin, vmax = np.nanmin(data_S), np.nanmax(data_S)

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#primeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_S[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_S[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
ax1.plot(dist[0:5], bat_transecta[0:5], color='grey')
plt.fill_between(dist[:5], bat_transecta[:5], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt , size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_S[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_S[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
#ax2.scatter(dist, 200*np.ones(len(dist)), marker = "v",color = 'k',s=200)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000, 2500],size = 18)
#ax2.text(3, 830, txt2, size=24)
#ax2.axis([0, 156, 850, 200])
plt.gca().invert_yaxis()
ax2.plot(dist[4:], bat_transecta[4:], color='grey')
plt.fill_between(dist[4:], bat_transecta[4:], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(dist[:5], [298, 298, 298, 298, 298], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')

##
#SECCION - TEMPERATURA - CENTRAL

#Niveles
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
levels_contorno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

cmap = plt.cm.get_cmap('Reds', 50)
#cmap = 'autumn'
nombre_salida = 'seccion_central_2017_temperatura'
txt = 'Central - 2017'
txt2 = ''
txt3 = 'Temperature (°C)'
vmin, vmax = np.nanmin(data_T), np.nanmax(data_T)

x_aux_linea_bat = [100.5238, 105.13, 133.7544]
y_aux_linea_bat = [127, 299, 1374]

#Plot
fig1 = plt.figure(figsize=(16, 7))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43
#pimeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_T[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_T[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
ax1.plot(dist[0:4], bat_transecta[0:4], color='grey')
plt.fill_between(dist[:4], bat_transecta[:4], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(x_aux_linea_bat[:2], y_aux_linea_bat[:2], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[300:, :], p[300:, :], data_T[300:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[300:, :], p[300:, :], data_T[300:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000, 2500], size=18)
#ax2.text(3, 830, txt2, size=24)
#ax2.axis([0, 156, 850, 200])
plt.gca().invert_yaxis()
ax2.plot(dist[4:], bat_transecta[4:], color='grey')
plt.fill_between(dist[4:], bat_transecta[4:], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between([dist[0], dist[1], dist[2], dist[3], 105.13], [300, 300, 300, 300, 300], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(x_aux_linea_bat[1:], [300, 1374], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


#SECCION SALINIDAD - CENTRAL
#Niveles
levels = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]
levels_contorno = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]

cmap = plt.cm.get_cmap('Blues', 50)

nombre_salida = 'seccion_central_2017_salinidad'
txt = 'Central - 2017'
txt2 = ''
txt3 = 'Salinity (UPS)'
vmin, vmax = np.nanmin(data_S), np.nanmax(data_S)

#Plot
fig1 = plt.figure(figsize=(16, 7))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43
#primeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_S[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_S[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
ax1.plot(dist[0:4], bat_transecta[0:4], color='grey')
plt.fill_between(dist[:4], bat_transecta[:4], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(x_aux_linea_bat[:2], y_aux_linea_bat[:2], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

ax1.set_title(txt , size=18)

for est in range(0, cant_estaciones):
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_S[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_S[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
#ax2.scatter(dist, 200*np.ones(len(dist)), marker = "v",color = 'k',s=200)
ax2.set_xlabel('Distance (km)', size=20)
#ax4.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000, 2500],size = 18)
plt.gca().invert_yaxis()
ax2.plot(dist[4:], bat_transecta[4:], color='grey')
plt.fill_between(dist[4:], bat_transecta[4:], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between([dist[0], dist[1], dist[2], dist[3], 105.13], [300, 300, 300, 300, 300], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
plt.fill_between(x_aux_linea_bat[1:], [300, 1374], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)

plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')

##
#SECCION - TEMPERATURA - SUR

#Niveles
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
levels_contorno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

cmap = plt.cm.get_cmap('Reds', 50)
#cmap = 'autumn'
nombre_salida = 'seccion_sur_2017_temperatura'
txt = 'South - 2017'
txt2 = ''
txt3 = 'Temperature (°C)'
vmin, vmax = np.nanmin(data_T), np.nanmax(data_T)

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#pimeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_T[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_T[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()

dist_aux = [dist[0], dist[1], dist[2], dist[3], dist[4], dist[5], 128.7, dist[6], dist[7], dist[8]]
bat_transecta_aux = [bat_transecta[0], bat_transecta[1], bat_transecta[2], bat_transecta[3], bat_transecta[4], bat_transecta[5], 299, bat_transecta[6], bat_transecta[7], bat_transecta[8]]
plt.fill_between(dist_aux[:7], bat_transecta_aux[:7], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
bat_transecta_aux2 = [300, 300, 300, 300, 300, 300, 300, 851, 1268, 1799]

ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[300:, :], p[300:, :], data_T[300:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[300:, :], p[300:, :], data_T[300:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500],size = 18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux, bat_transecta_aux2, plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)

plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


#SECCION SALINIDAD - SUR
#Niveles
levels = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]
levels_contorno = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]

cmap = plt.cm.get_cmap('Blues', 50)

nombre_salida = 'seccion_sur_2017_salinidad'
txt = 'South - 2017'
txt2 = ''
txt3 = 'Salinity (UPS)'
vmin, vmax = np.nanmin(data_S), np.nanmax(data_S)

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#primeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_S[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_S[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux[:7], bat_transecta_aux[:7], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_S[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_S[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
#ax2.scatter(dist, 200*np.ones(len(dist)), marker = "v",color = 'k',s=200)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500],size = 18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux, bat_transecta_aux2, plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')

########### CAMPAÑA 2021 ###############

#SECCION - TEMPERATURA - SUR

#Niveles
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
levels_contorno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

cmap = plt.cm.get_cmap('Reds', 50)
#cmap = 'autumn'
nombre_salida = 'seccion_sur_2021_temperatura'
txt = 'South - 2021'
txt2 = ''
txt3 = 'Temperature (°C)'
vmin, vmax = np.nanmin(data_T), np.nanmax(data_T)

#parametros auxiliares de la recta de la batimetria que une los puntos de un grafico y del otro (el de los primeros 300 m y el de 300 al fondo)
m = (-bat_transecta[5]-(-bat_transecta_aux[4]))/(dist[5]-dist[4])
b = -bat_transecta[5] - (m*dist[5])
valor_aux_para_graf = (-300-b)/m

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#pimeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_T[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_T[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()

dist_aux = [dist[0], dist[1], dist[2], dist[3], dist[4], valor_aux_para_graf, dist[5], dist[6], dist[7]]
bat_transecta_aux = [bat_transecta[0], bat_transecta[1], bat_transecta[2], bat_transecta[3], bat_transecta[4], 299, bat_transecta[5], bat_transecta[6], bat_transecta[7]]

plt.fill_between(dist_aux[:6], bat_transecta_aux[:6], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
bat_transecta_aux2 = [300, 300, 300, 300, 300, 300, bat_transecta[5], bat_transecta[6], bat_transecta[7]]

ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[300:, :], p[300:, :], data_T[300:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[300:, :], p[300:, :], data_T[300:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500],size = 18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux, bat_transecta_aux2, plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)

plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


#SECCION SALINIDAD - SUR
#Niveles
levels = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]
levels_contorno = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]

cmap = plt.cm.get_cmap('Blues', 50)

nombre_salida = 'seccion_sur_2021_salinidad'
txt = 'South - 2021'
txt2 = ''
txt3 = 'Salinity (UPS)'
vmin, vmax = np.nanmin(data_S), np.nanmax(data_S)

#Plot
fig1 = plt.figure(figsize=(16, 8))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43

#primeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_S[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_S[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux[:6], bat_transecta_aux[:6], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_S[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_S[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
#ax2.scatter(dist, 200*np.ones(len(dist)), marker = "v",color = 'k',s=200)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500], size=18)
plt.gca().invert_yaxis()
plt.fill_between(dist_aux, bat_transecta_aux2, plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')

#

#SECCION - TEMPERATURA - CENTRAL
#Niveles
levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
levels_contorno = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
cmap = plt.cm.get_cmap('Reds', 50)
#cmap = 'autumn'
nombre_salida = 'seccion_central_2021_temperatura'
txt = 'Central - 2021'
txt2 = ''
txt3 = 'Temperature (°C)'
vmin, vmax = np.nanmin(data_T), np.nanmax(data_T)

m = (-bat_transecta[4]-(-bat_transecta[3]))/(dist[4]-dist[3])
b = -bat_transecta[4] - (m*dist[4])
valor_aux_para_graf = (-300-b)/m

x_aux_bat = [dist[0], dist[1], dist[2], dist[3], valor_aux_para_graf, dist[4], dist[5], dist[6], dist[7]]
y_aux_bat = [bat_transecta[0], bat_transecta[1], bat_transecta[2], bat_transecta[3], 299, bat_transecta[4], bat_transecta[5], bat_transecta[6], bat_transecta[7]]

#Plot
fig1 = plt.figure(figsize=(16, 7))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43
#pimeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_T[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_T[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
plt.fill_between(x_aux_bat[:5], y_aux_bat[:5], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)
ax1.set_title(txt, size=18)

for est in range(0, cant_estaciones):
    #ax1.text(dist[est]-2, -4, 'nombre de estacion', size=24)
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[300:, :], p[300:, :], data_T[300:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax2.contour(x[300:, :], p[300:, :], data_T[300:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
ax2.set_xlabel('Distance (km)', size=20)
ax2.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000], size=18)
plt.gca().invert_yaxis()
y_aux_bat2 = [300, 300, 300, 300, 300, bat_transecta[4], bat_transecta[5], bat_transecta[6], bat_transecta[7]]
plt.fill_between(x_aux_bat, y_aux_bat2, 2229, color='grey', alpha=1, zorder=7)
cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)
plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


#SECCION SALINIDAD - CENTRAL
#Niveles
levels = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]
levels_contorno = [33.5, 33.6, 33.7, 33.8, 33.9, 34, 34.1, 34.2, 34.3, 34.4, 34.5, 34.6, 34.7, 34.8, 34.9]

cmap = plt.cm.get_cmap('Blues', 50)

nombre_salida = 'seccion_central_2021_salinidad'
txt = 'Central - 2021'
txt2 = ''
txt3 = 'Salinity (UPS)'
vmin, vmax = np.nanmin(data_S), np.nanmax(data_S)

#Plot
fig1 = plt.figure(figsize=(16, 7))
xo, yo1, yo2 = 0.07, 0.55, 0.08
dx = 0.37
dy1 = 0.4
dy2 = 0.43
#primeros 300 metros
ax1 = fig1.add_axes([xo, yo1, dx, dy1])
CF = ax1.contourf(x[:300, :], p[:300, :], data_S[:300, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend='max')
CC = ax1.contour(x[:300, :], p[:300, :], data_S[:300, :], levels, colors='k', linewidths=1.5)
CS = ax1.contour(x[:300, :], p[:300, :], data_sigma[:300, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax1.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
plt.gca().invert_yaxis()
plt.fill_between(x_aux_bat[:5], y_aux_bat[:5], plt.gca().get_ylim()[0], color='grey', alpha=1, zorder=7)

ax1.set_title(txt , size=18)

for est in range(0, cant_estaciones):
    ax1.scatter(dist, np.zeros(len(dist)), marker="v", color='k', s=200)
    plt.xticks(size=0)
    plt.yticks([0, 50, 100, 200, 300], size=18)

#de 300 al fondo
ax2 = fig1.add_axes([xo, yo2, dx, dy2])
CF = ax2.contourf(x[298:, :], p[298:, :], data_S[298:, :], levels, cmap=cmap, vmin=vmin, vmax=vmax, extend = 'max')
CC = ax2.contour(x[298:, :], p[298:, :], data_S[298:, :], levels_contorno, colors='k', linewidths=1.5)
CS = ax2.contour(x[300:, :], p[300:, :], data_sigma[300:, :], colors='white', linewidths=1.5, linestyles='dashed', zorder=6)
ax2.clabel(CC, inline=1, fmt='%1.1f', fontsize=18)
#ax2.scatter(dist, 200*np.ones(len(dist)), marker = "v",color = 'k',s=200)
ax2.set_xlabel('Distance (km)', size=20)
#ax4.set_ylabel('Pressure (db)', size=20)
plt.xticks(size=18)
plt.yticks([500, 1000, 1500, 2000],size = 18)
plt.gca().invert_yaxis()
plt.fill_between(x_aux_bat, y_aux_bat2,2229, color='grey', alpha=1, zorder=7)

cax_sal = fig1.add_axes([xo+dx+0.02, 0.08, 0.02, 0.87])
cbar = fig1.colorbar(CF, orientation='vertical', cax=cax_sal)
cbar.set_label(label=txt3, fontsize=18)
cbar.ax.tick_params(labelsize=18)

plt.savefig(plots_path + nombre_salida + '.png', dpi=300, bbox_inches='tight')


