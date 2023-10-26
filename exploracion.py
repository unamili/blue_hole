import pycnv #otro puede ser fCNV de seabird
import pylab as pl
import paths
import datetime
import time
import pickle
import glob
import numpy as np
import matplotlib.pyplot as plt
from paths import paths
import save
import pandas as pd
import plot

# Definimos paths a la data y a directorios de guardado
data_path = paths().data_path()
plot_path = paths().plots_path()
save_path = paths().save_path()
path_perfiles = data_path + 'perfiles/'

# Definimos el nombre de esta corrida para guardar en una sub carpeta
nombre_especifico_de_esta_corrida = 'cast_loc/'

# Definimos el directorio de guardado de plots de esta corrida
save_plot_path = plot_path + nombre_especifico_de_esta_corrida
save_data_path = save_path + nombre_especifico_de_esta_corrida

# Tomamos las carpetas de datos
folders = glob.glob(path_perfiles + '/*')[::-1]  # Invierte el orden de los elementos
Data = {}
cast_time = {}
folder_names = []
years = [int(folder[-4:]) for folder in folders]
campaign_data = {}

reference_dates = [datetime.datetime(2016, 12, 31), datetime.datetime(2020, 12, 31)]

# zip es una funcion que itera tomando los elementos de cada una de las cosas que se pasan como argumento.
# Al iterar
# for x, y in zip([1, 2], [3, 4]): en la primera iteracion se obtiene x = 1, y = 3, y en la segunda, x = 2, y = 4.
# enumerate enumera el contenido, que en este caso son dos cosas, porque zip tiene 2 iteraciones.

for i, (reference_date, folder) in enumerate(zip(reference_dates, folders)):
    folder_name = folder.split('perfiles/')[-1]
    folder_names.append(folder_name)
    files = glob.glob(folder + '/*')
    Data[years[i]] = {}

    campaign_data[years[i]] = pd.DataFrame()

    for count, file in enumerate(files):
        cast_name = file[-9:-4]
        Data[years[i]][cast_name] = {}
        data = pycnv.pycnv(file)
        Data[years[i]][cast_name] = data

        # tiempo de la estacion
        utc_time = reference_date + datetime.timedelta(days=data.data['timeJ'][count])
        # latitud de la estacion
        lat = data.data['latitude'][0]
        # longitud de la estacion
        lon = data.data['longitude'][0]

        # presines de la estacion
        presiones = data.data['prDM']

        for j, presion in enumerate(presiones):
            # Nueva fila del dataframe
            row = {}

            # Agregamos la data a la fila
            row['time'] = utc_time.strftime("%Y-%m-%d %H:%M:%S")
            row['lat'] = lat
            row['lon'] = lon
            row['pres'] = presion
            row['temp'] = data.data['t090C'][j]
            row['sal'] = data.data['sal00'][j]
            # Agregar mas

            campaign_data[years[i]] = campaign_data[years[i]].append(row, ignore_index=True)

        print('\rProgress: {}%'.format(int((count + 1) * 100 / len(files))), end='')

    # Ordenamos temporalmente
    # campaign_data[years[i]].sort_values('time', inplace=True)

# Toamos una transecta filtrando los valores de una campaña por latitud (opcional tiempo (campaign_data[years[0]]['time'] < algo))
transecta = campaign_data[years[0]].loc[(campaign_data[years[0]]['lat'] > -45) &
                                     (campaign_data[years[0]]['lat'] < -44) &
                                     (campaign_data[years[0]]['time'])]

# Tomamos las longitudes unicas para que sean las columnas del dataframe de la variable a graficar
cant_lons = len(transecta.lon.unique())

# Armamos el df de la variable a graficar
temp = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())

# Iteramos en las filas de la transecta, completando el df de temp (o sal) con los valores obtenidos para la longitud y profundidad correspondientes
for i, row in transecta.iterrows():
    temp.iloc[int(row['pres'])][row['lon']] = row['temp']


plt.contourf(temp)
# Invertimos el eje vertical porque la presion es positiva
plt.gca().invert_yaxis()
plt.colorbar()