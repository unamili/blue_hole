import os

class paths():

    def __init__(self):
        self.name = os.popen('whoami').read()

        # Define el path al disco rigido, para poder correr las cosas desde cualquier pc usando el disco externo
        if self.name == 'agulhas\n':
            self.samsung_path = '/media/agulhas/Samsung_T5/'
        # Aca, una vez en la mac, correr la linea de arriba, os.popen('whoami').read, y cambiar el nombre 'mac\n' por el que aparezca
        if self.name == 'mac\n':
            self.samsung_path = '/Volumes/Samsung_T5/'

    def data_path(self):
        '''
        Path to data directory.
        A partir del path del disco, ya obtenido para la computadora actual, defineel path a los datos.

        :return:
        path as str
        '''

        data_path = self.samsung_path + 'proyectos_doc/Data/blue_hole/'

        return data_path

    def plots_path(self):
        '''
        Path to plots directory

        :return:
        path as str
        '''

        plots_path = self.samsung_path + 'proyectos_doc/blue_hole/Plots/'

        os.makedirs(plots_path, exist_ok=True)
        return plots_path

    def save_path(self):
        '''
        Path to save directory

        :return:
        path as str
        '''

        save_path = self.samsung_path + 'proyectos_doc/blue_hole/Save/'

        os.makedirs(save_path, exist_ok=True)

        return save_path


path_Rutinas = '/media/agulhas/HDD4T/california/Documents/disco2T/Rutinas'
path_Figuras = '/media/agulhas/HDD4T/california/Documents/disco2T/Rutinas/Proyecto_doc/Figuras'

path_Rutinas_disco = '/Volumes/Samsung_T5/COMPU CALIFORNIA/Rutinas'
path_Figuras_disco = '/Volumes/Samsung_T5/COMPU CALIFORNIA/Rutinas/Proyecto_doc/Figuras'

path_Datos_disco = '/Volumes/Samsung_T5/COMPU CALIFORNIA/Datos'

path_perfiles_agujeroazul_2021 = '/Volumes/Samsung_T5/Datos Agujero Azul/perfiles/CTD_AA_2021/'
path_perfiles_agujeroazul_2017 = '/Volumes/Samsung_T5/Datos Agujero Azul/perfiles/CTD_AU042017/'
path_perfiles_agujeroazul = '/Volumes/Samsung_T5/Datos Agujero Azul/perfiles/'