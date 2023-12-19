import pycnv #otro puede ser fCNV de seabird
import datetime
import glob
import numpy as np
import matplotlib.pyplot as plt

import save
from paths import paths
import pandas as pd
import warnings
import xarray as xr
warnings.simplefilter(action='ignore', category=FutureWarning)

# Definimos paths a la data y a directorios de guardado
data_path = paths().data_path()
plot_path = paths().plots_path()
save_path = paths().save_path()
path_perfiles = data_path + 'perfiles/'

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
            row['time'] = utc_time
            row['lat'] = lat
            row['lon'] = lon
            row['pres'] = presion
            row['temp'] = data.data['t090C'][j]
            row['sal'] = data.data['sal00'][j]
            row['sigma'] = data.data['sigma-é00'][j]
            # Agregar mas

            campaign_data[years[i]] = campaign_data[years[i]].append(row, ignore_index=True)

        print('\rProgress: {}%'.format(int((count + 1) * 100 / len(files))), end='')

    # Ordenamos temporalmente
    # campaign_data[years[i]].sort_values('time', inplace=True)

# Para la campaña del 2017 donde se muestreo el mismo punto por el dia y por la noche pero con perfiles de distintas profundidades
# Me quiero quedar unicamente con el perfil que se realizó hasta el fondo.

estaciones = campaign_data[2017].drop_duplicates(subset=['lat', 'lon'], keep='last')
estaciones_sorted = estaciones.sort_values('lat')
lats = estaciones_sorted['lat'].values
lons = estaciones_sorted['lon'].values

estaciones_aux = estaciones_sorted
threshold = 0.15
cant_estaciones_repetidas = 0
i_to_drop = []
lats_to_drop = []
lons_to_drop = []
for i in range(len(lats)-1):
    if abs(lats[i]-lats[i+1]) < threshold and abs(lons[i]-lons[i+1]) < threshold:
        cant_estaciones_repetidas = cant_estaciones_repetidas+1
        if estaciones_sorted.pres.values[i] > estaciones_sorted.pres.values[i+1]:
            i_to_drop.append(i+1)
            lats_to_drop.append(estaciones_sorted.lat.values[i+1])
            lons_to_drop.append(estaciones_sorted.lon.values[i+1])
        elif estaciones_sorted.pres.values[i] < estaciones_sorted.pres.values[i+1]:
            i_to_drop.append(i)
            lats_to_drop.append(estaciones_sorted.lat.values[i])
            lons_to_drop.append(estaciones_sorted.lon.values[i])
    else:
        None

estaciones_sin_repetir = estaciones_sorted.drop(estaciones_sorted.index[np.array(i_to_drop)])

# Crea una máscara booleana para filtrar las filas
mascara_de_filtro = ~((campaign_data[2017]['lat'].isin(np.array(lats_to_drop))) & (campaign_data[2017]['lon'].isin(np.array(lons_to_drop))))

# Aplica el filtro para mantener solo las filas deseadas
datos_filtrados_campaña = campaign_data[2017][mascara_de_filtro]


# Tomamos una transecta filtrando los valores de una campaña por latitud (opcional tiempo (campaign_data[years[0]]['time'] < algo))
transecta_norte_2017 = datos_filtrados_campaña.loc[(datos_filtrados_campaña['lat'] > -44) &
                                     (datos_filtrados_campaña['lat'] < -42.9)]

transecta_central_2017 = datos_filtrados_campaña.loc[(datos_filtrados_campaña['lat'] > -45) &
                                     (datos_filtrados_campaña['lat'] < -44)]

transecta_sur_2017 = datos_filtrados_campaña.loc[(datos_filtrados_campaña['lat'] > -46.2) &
                                 (datos_filtrados_campaña['lat'] < -45.5)]


transecta_central_2021 = campaign_data[2021].loc[(campaign_data[2021]['lat'] > -44.75) &
                                     (campaign_data[2021]['lat'] < -44)]

transecta_sur_2021 = campaign_data[2021].loc[(campaign_data[2021]['lat'] > -46.2) &
                                 (campaign_data[2021]['lat'] < -45.5)]

lats_to_drop = [transecta_sur_2021.lat.unique()[3], transecta_sur_2021.lat.unique()[5]]
lons_to_drop = [transecta_sur_2021.lon.unique()[3], transecta_sur_2021.lon.unique()[5]]

transecta_sur_2021 = transecta_sur_2021.drop(index=transecta_sur_2021[transecta_sur_2021.lon.isin(lons_to_drop)].index)


# Guardo las variables como pikles
save.var(var=transecta_norte_2017, path=save_path + 'Transectas/', fname='transecta_norte_2017')
save.var(var=transecta_central_2017, path=save_path + 'Transectas/', fname='transecta_central_2017')
save.var(var=transecta_sur_2017, path=save_path + 'Transectas/', fname='transecta_sur_2017')
save.var(var=transecta_central_2021, path=save_path + 'Transectas/', fname='transecta_central_2021')
save.var(var=transecta_sur_2021, path=save_path + 'Transectas/', fname='transecta_sur_2021')

from scipy.interpolate import griddata

transecta = transecta_norte_2017
temp = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())

# Iteramos en las filas de la transecta, completando el df de temp (o sal) con los valores obtenidos para la longitud y profundidad correspondientes
for i, row in transecta.iterrows():
    temp.iloc[int(row['pres'])][row['lon']] = row['temp']

lons_plot = np.linspace(lons[0], lons[-1], 18)

temp.drop([0,1], inplace=True)

# Crear una malla de puntos para la interpolación
xx, yy = np.meshgrid(lons_plot, np.sort(transecta_norte_2017.pres.unique()))

temp_columns_sorted = temp.reindex(sorted(temp.columns), axis=1)
lons = sorted(transecta.lon.unique())


# Obtener los puntos de entrada para la interpolación (datos originales)
pres_unique = np.sort(transecta.pres.unique())

points = np.array([(lon, pres) for lon in lons for pres in pres_unique])
values = (temp_columns_sorted.values.T.flatten())  # Asegúrate de tener los valores de temperatura en un array 1D

# Realizar la interpolación utilizando griddata
foo = griddata(points, values, (xx, yy), method='linear')

transecta_norte_2017['temp'] = transecta_norte_2017['temp'].interpolate(method='linear')

# Estamos probando seleccionar la temperatura y salinidad de una transecta y graficarla
transecta = transecta_central_2017
transecta = transecta_norte_2017
transecta = transecta_sur_2017

# Armamos el df de la variable a graficar
temp = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())
sal = pd.DataFrame(np.nan, index=np.arange(int(transecta.pres.max())+1), columns=transecta.lon.unique())

# Iteramos en las filas de la transecta, completando el df de temp (o sal) con los valores obtenidos para la longitud y profundidad correspondientes
for i, row in transecta.iterrows():
    temp.iloc[int(row['pres'])][row['lon']] = row['temp']
    sal.iloc[int(row['pres'])][row['lon']] = row['sal']

temp_columns_sorted = temp.reindex(sorted(temp.columns), axis=1)
lons = sorted(transecta.lon.unique())

# Quiero introducir la batimetria al plot de la seccion

bath_path = paths().bath_path()

bat = xr.open_dataset(bath_path + 'bat_res025_pat.nc')

bat_norte = bat.sel(lat=transecta_norte_2017.lat.values.mean(), method='nearest')
bat_norte = bat_norte.sel(lon=slice(transecta_norte_2017.lon.values.min(), transecta_norte_2017.lon.values.max()))

bat_central = bat.sel(lat=transecta_central_2017.lat.values.mean(), method='nearest')
bat_central = bat_central.sel(lon=slice(transecta_central_2017.lon.values[0], transecta_central_2017.lon.values[-1]))

bat_sur = bat.sel(lat=transecta_sur_2017.lat.values.mean(), method='nearest')
bat_sur = bat_sur.sel(lon=slice(transecta_sur_2017.lon.values[-1], transecta_sur_2017.lon.values[0]))


# Plot
fig = plt.figure()
plt.contourf(lons, temp_columns_sorted.index, temp_columns_sorted.values)
# Invertimos el eje vertical porque la presion es positiva
plt.gca().invert_yaxis()
plt.colorbar()

plt.plot(bat_sur.lon.values, -bat_sur.bat.values, 'k')
plt.fill_between(bat_sur.lon.values, -bat_sur.bat.values, plt.gca().get_ylim()[0], color='grey', alpha=0.5)


plt.plot(bat_norte.lon.values, -bat_norte.bat.values, 'k')
plt.fill_between(bat_norte.lon.values, -bat_norte.bat.values, plt.gca().get_ylim()[0], color='grey', alpha=0.5)


plt.plot(bat_central.lon.values, -bat_central.bat.values, 'k')
plt.fill_between(bat_central.lon.values, -bat_central.bat.values, plt.gca().get_ylim()[0], color='grey', alpha=0.5)

plt.plot(bat_norte.lon.values, -bat_norte.bat.values, 'k')
plt.fill_between(bat_norte.lon.values, -bat_norte.bat.values, plt.gca().get_ylim()[0], color='grey', alpha=0.5)







###

#xx, yy = np.meshgrid(lons, temp_columns_sorted.index)
#fig = plt.figure()
#plt.scatter(xx, yy, c=temp_columns_sorted.values, s=0.5)
# Invertimos el eje vertical porque la presion es positiva
#plt.gca().invert_yaxis()
#plt.colorbar()