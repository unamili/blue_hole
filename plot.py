import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import save

def plot_locations(df, fig=None, save_fig=False, path=None, fname=None):

    # Si no le pasamos una figura, la crea
    if fig == None:
        fig = plt.figure()

    # Titulo con el año
    year = df.time[0][:4]
    plt.title(year)

    # Definimos colormap rainbow
    cmap = plt.cm.rainbow

    # Define los bins de colores y la normalizacion para que el primer punto sea el primer color y el ultimo el ultimo del cmap
    bounds = np.linspace(1, len(df) + 1, len(df) + 1)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

    # Ploteamos los putos con colores
    plt.scatter(df['lons'], df['lats'], c=df.index, cmap=cmap, norm=norm)

    # Nombramos los ejes
    plt.xlabel('Longitud')
    plt.ylabel('Latitud')

    # Ponemos el colorbar
    cbar = plt.colorbar()
    cbar.set_label('Paso del tiempo', rotation=270)

    # Ajustamos la figura
    fig.tight_layout()

    # Guardamos la figura
    if save_fig:
        if fname == None:
            fname = f'cast_localization_{year}'
        if path == None:
            path = ''
        save.fig(fig=fig, path=path, fname=fname)
