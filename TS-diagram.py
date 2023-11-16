import numpy as np
import pandas as pd
import gsw
from paths import paths

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plots_path = paths().plots_path()

data = campaign_data[2017]

data = transecta_central_2021

temp= data.temp
sal = data.sal
cant_datos= temp.size

mint = temp.min()
maxt = temp.max()

mins = sal.min()
maxs = sal.max()

tempL = np.linspace(mint - 1, maxt + 1, cant_datos)
salL = np.linspace(mins - 1, maxs + 1, cant_datos)

Tg, Sg = np.meshgrid(tempL, salL)
sigma_theta = gsw.sigma0(Sg, Tg)
#cnt = np.linspace(sigma_theta.min(), sigma_theta.max(), cant_datos)

fig, ax = plt.subplots(figsize=(10, 10))
# fig.suptitle(‘programmer:Hafez Ahmad’, fontsize=14, fontweight=’bold’)
cs = ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder = 1)
cl = plt.clabel(cs, fontsize=10, inline=True, fmt='%.1f')

sc = plt.scatter(sal.values, temp.values, s = 2, c = 'grey')

ax.set_xlabel('Salinity')
ax.set_ylabel('Temperature[$ ^ \circ$C]')
ax.set_title('TS Diagram', fontsize = 14, fontweight ='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')
cb.ax.tick_params(direction='out')
cb.set_label('Density[kg m$ ^ {-3}$]')
plt.tight_layout()

lons = sorted(data.lon.unique())
lats = sorted(data.lat.unique())

df = data
#perfil0 = df[df['lon'] == lons[1]]
perfil1 = df[df['lon'] == lons[1]]
perfil2 =  df[df['lon'] == lons[3]]
perfil3 = df[df['lon'] == lons[5]]
perfil4 = df[df['lon'] == lons[7]]

sc = plt.scatter(perfil1.sal.values, perfil1.temp.values, s = 2, c = 'yellow')
sc = plt.scatter(perfil2.sal.values, perfil2.temp.values, s = 2, c = 'orange')
sc = plt.scatter(perfil3.sal.values, perfil3.temp.values, s = 2, c = 'red')
sc = plt.scatter(perfil4.sal.values, perfil4.temp.values, s = 2, c = 'purple')

plt.savefig(plots_path + 'TS_2021.png')




