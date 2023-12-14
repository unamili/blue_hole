import numpy as np
import pandas as pd
import gsw
from paths import paths

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plots_path = paths().plots_path()

#data = campaign_data[2017]

data = transecta_central_2021

temp= data.temp
sal = data.sal
cant_datos= temp.size

mint = temp.min()
maxt = temp.max()

mins = sal.min()
maxs = sal.max()

#tempL = np.linspace(mint - 1, maxt + 1, cant_datos)
#salL = np.linspace(mins - 1, maxs + 1, cant_datos)

tempL = np.linspace(0, 14, cant_datos)
salL = np.linspace(33, 35, cant_datos)

Tg, Sg = np.meshgrid(tempL, salL)
sigma_theta = gsw.sigma0(Sg, Tg)
#cnt = np.linspace(sigma_theta.min(), sigma_theta.max(), cant_datos)
lons = sorted(data.lon.unique())
lats = sorted(data.lat.unique())
df = data
#perfil0 = df[df['lon'] == lons[0]]
perfil1 = df[df['lon'] == lons[1]]
perfil2 = df[df['lon'] == lons[3]]
perfil3 = df[df['lon'] == lons[5]]
perfil4 = df[df['lon'] == lons[7]]

perfil_curioso = df[df['lon'] == lons[6]]

fig, ax = plt.subplots(figsize=(10, 10))
# fig.suptitle(‘programmer:Hafez Ahmad’, fontsize=14, fontweight=’bold’)
cs = ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder = 1)
cl = plt.clabel(cs, fontsize=10, inline=True, fmt='%.1f')

sc = plt.scatter(sal.values, temp.values, s = 2, c = 'grey')
sc = plt.scatter(perfil1.sal.values, perfil1.temp.values, s = 2, c = 'yellow')
sc = plt.scatter(perfil2.sal.values, perfil2.temp.values, s = 2, c = 'orange')
sc = plt.scatter(perfil3.sal.values, perfil3.temp.values, s = 2, c = 'red')
sc = plt.scatter(perfil4.sal.values, perfil4.temp.values, s = 2, c = 'purple')
ax.set_xlabel('Salinity')
ax.set_ylabel('Temperature[$ ^ \circ$C]')
ax.set_title('TS Diagram', fontsize = 14, fontweight ='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')
cb.ax.tick_params(direction='out')
cb.set_label('Density[kg m$ ^ {-3}$]')
plt.tight_layout()

plt.savefig(plots_path + 'TS_transectacentral_2021.png')


fig, ax = plt.subplots(figsize=(5, 10))
plt.plot(perfil_curioso.temp.values, perfil_curioso.pres.values, 'r')
plt.gca().invert_yaxis()
ax.set_xlabel('Temperature [$^\circ$C]')
ax.set_ylabel('Pressure [dbar]')
ax.set_title('', fontsize=14, fontweight='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')

# Colocar ticks y labels del eje x en la parte superior
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.show()


fig, ax = plt.subplots(figsize=(5, 10))
plt.plot(perfil_curioso.sal.values, perfil_curioso.pres.values)
plt.gca().invert_yaxis()
ax.set_xlabel('Salinity [UPS]')
ax.set_ylabel('Pressure [dbar]')
ax.set_title('', fontsize=14, fontweight='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')

# Colocar ticks y labels del eje x en la parte superior
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

plt.tight_layout()
plt.show()


fig, ax1 = plt.subplots(figsize=(6, 10))

# Graficar la temperatura en el primer eje y y primer eje x
ax1.plot(perfil_curioso.temp.values, perfil_curioso.pres.values, 'r')
ax1.xaxis.tick_top()
ax1.xaxis.set_label_position('top')
ax1.set_ylabel('Pressure [dbar]')
ax1.tick_params(axis='x', labelcolor='red')
ax1.invert_yaxis()
ax1.set_xlabel('Temperature [$^\circ$C]', c='r')
ax1.xaxis.set_label_position('bottom')


# Crear un segundo eje x alineado con el eje y original
ax2 = ax1.twiny()

# Graficar la salinidad en el segundo eje x y el eje y original
ax2.plot(perfil_curioso.sal.values, perfil_curioso.pres.values, 'b')
ax2.tick_params(axis='x', labelcolor='blue')
ax2.set_xlabel('Salinity [UPS]', c='blue')
ax2.xaxis.set_label_position('top')

plt.tight_layout()
plt.show()

