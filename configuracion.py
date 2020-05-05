import configparser


class GlobalConfiguration(object):
    
    def __init__(self):

        """
        Clase que permite cargar la configuración contenida en el archivo
        config.ini
        
        """
        
        print("Iniciando configuración del ETL............")

        configuracion_global = configparser.ConfigParser()
        configuracion_global.read("config.ini")
        entorno = configuracion_global['DEFAULTS']['ENVIROMENT']

        self.entorno = entorno
        
        entorno = str(entorno).upper()
        
        self.configuracion_ftp = {
            'servidor': configuracion_global[entorno]['FTP_SERVER'],
            'usuario': configuracion_global[entorno]['FTP_USER'],
            'secret': configuracion_global[entorno]['FTP_PASSWORD'],
            'ruta_destino': configuracion_global[entorno]['FTP_PATH'],
            'puerto': configuracion_global[entorno]['FTP_PORT']
        }

        self.config_global = configuracion_global['DEFAULTS']

        self.entorno_carvajal = configuracion_global[entorno]["CARVAJAL_ENV"]