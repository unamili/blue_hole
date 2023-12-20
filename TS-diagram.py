import numpy as np
import pandas as pd
import gsw
from paths import paths
import pickle

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

plots_path = paths().plots_path()
save_path = paths().save_path()

with open(save_path + '/Transectas/transecta_central_2017', 'rb') as file:
    transecta_central_2017 = pickle.load(file)
with open(save_path + '/Transectas/transecta_sur_2017', 'rb') as file:
    transecta_sur_2017 = pickle.load(file)
with open(save_path + '/Transectas/transecta_sur_2021', 'rb') as file:
    transecta_sur_2021 = pickle.load(file)
with open(save_path + '/Transectas/transecta_central_2021', 'rb') as file:
    transecta_central_2021 = pickle.load(file)
with open(save_path + '/Transectas/transecta_norte_2017', 'rb') as file:
    transecta_norte_2017 = pickle.load(file)



#temp= data.temp
#sal= data.sal
#cant_datos= temp.size
#mint = temp.min()
#maxt = temp.max()
#mins = sal.min()
#maxs = sal.max()
#tempL = np.linspace(mint - 1, maxt + 1, cant_datos)
#salL = np.linspace(mins - 1, maxs + 1, cant_datos)

tempL = np.linspace(0, 14, 1000)
salL = np.linspace(33, 35, 1000)

Tg, Sg = np.meshgrid(tempL, salL)
sigma_theta = gsw.sigma0(Sg, Tg)

#TS comparacion entre ambas campañas
fig, ax = plt.subplots(figsize=(10, 10))
# fig.suptitle(‘programmer:Hafez Ahmad’, fontsize=14, fontweight=’bold’)
cs = ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1)
cl = plt.clabel(cs, fontsize=10, inline=True, fmt='%.1f')
#sc5 = plt.scatter(transecta_norte_2017['sal'].values, transecta_norte_2017['temp'].values, s=2, c='grey', label='2017 Norte')
sc1 = plt.scatter(transecta_sur_2017['sal'].values, transecta_sur_2017['temp'].values, s=2, c='yellowgreen', label='2017 Sur')
sc2 = plt.scatter(transecta_central_2017['sal'].values, transecta_central_2017['temp'].values, s=2, c='darkolivegreen', label='2017 Central')
sc3 = plt.scatter(transecta_sur_2021['sal'].values, transecta_sur_2021['temp'].values, s=2, c='royalblue', label='2021 Sur')
sc4 = plt.scatter(transecta_central_2021['sal'].values, transecta_central_2021['temp'].values, s=2, c='darkblue', label='2021 Central')
ax.legend()
ax.set_xlabel('Salinity [UPS]')
ax.set_ylabel('Temperature [$^\circ$C]')
ax.set_title('TS Diagram', fontsize = 14, fontweight ='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')
plt.tight_layout()
plt.savefig(plots_path + 'TS_comp_campañas.png')

#TS dentro de una misma campaña con distintos colores las transectas
#2017
fig, ax = plt.subplots(figsize=(10, 10))
cs = ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1)
cl = plt.clabel(cs, fontsize=10, inline=True, fmt='%.1f')
sc1 = plt.scatter(transecta_sur_2017['sal'].values, transecta_sur_2017['temp'].values, s=2, c='gold', label='2017 Sur')
sc2 = plt.scatter(transecta_central_2017['sal'].values, transecta_central_2017['temp'].values, s=2, c='green', label='2017 Central')
sc3 = plt.scatter(transecta_norte_2017['sal'].values, transecta_norte_2017['temp'].values, s=2, c='darkblue', label='2017 Norte')
ax.legend()
ax.set_xlabel('Salinity [UPS]')
ax.set_ylabel('Temperature [$^\circ$C]')
ax.set_title('TS Diagram', fontsize = 14, fontweight ='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')
plt.tight_layout()
plt.savefig(plots_path + 'TS_2017.png')

#2021
fig, ax = plt.subplots(figsize=(10, 10))
cs = ax.contour(Sg, Tg, sigma_theta, colors='grey', zorder=1)
cl = plt.clabel(cs, fontsize=10, inline=True, fmt='%.1f')
sc1 = plt.scatter(transecta_sur_2021['sal'].values, transecta_sur_2021['temp'].values, s=2, c='gold', label='2021 Sur')
sc2 = plt.scatter(transecta_central_2021['sal'].values, transecta_central_2021['temp'].values, s=2, c='green', label='2021 Central')
ax.legend()
ax.set_xlabel('Salinity [UPS]')
ax.set_ylabel('Temperature [$^\circ$C]')
ax.set_title('TS Diagram', fontsize = 14, fontweight ='bold')
ax.xaxis.set_major_locator(MaxNLocator(nbins=6))
ax.yaxis.set_major_locator(MaxNLocator(nbins=8))
ax.tick_params(direction='out')
plt.tight_layout()
plt.savefig(plots_path + 'TS_2021.png')


#Grafico de un perfil
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

