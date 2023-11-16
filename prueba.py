import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# Extraer datos de longitud, profundidad y temperatura
longitudes = df['Longitud'].unique()
profundidades = df['Profundidad'].unique()
temperaturas = df['Temperatura']

# Aumentar la resolución en el eje x (longitud)
new_longitudes = np.linspace(longitudes.min(), longitudes.max(), num=16)  # Nueva grilla de longitud con mayor resolución

# Interpolar los datos de temperatura para la nueva grilla de longitud
interpolated_temps = np.zeros((len(profundidades), len(new_longitudes)))

for i, depth in enumerate(profundidades):
    # Seleccionar los datos de temperatura para una profundidad específica
    data_depth = df[df['Profundidad'] == depth]
    # Interpolar los datos de temperatura para la nueva grilla de longitud
    f = interp1d(data_depth['Longitud'], data_depth['Temperatura'], kind='cubic', fill_value='extrapolate')
    interpolated_temps[i, :] = f(new_longitudes)

# Disminuir la resolución en el eje y (profundidad)
reduced_depths = profundidades[::10]  # Tomar cada décimo valor de profundidad

# Seleccionar solo los valores de temperatura correspondientes a las profundidades reducidas
reduced_temps = interpolated_temps[::10, :]

# Crear el gráfico de contorno de temperatura
plt.figure(figsize=(10, 6))
contour = plt.contourf(new_longitudes, reduced_depths, reduced_temps, cmap='viridis')
plt.colorbar(contour, label='Temperatura')  # Agregar una barra de color para la escala de temperatura
plt.xlabel('Longitud')
plt.ylabel('Profundidad')
plt.title('Contorno de Temperatura en función de Longitud y Profundidad (resolución ajustada)')

plt.show()
