import os
from comprobante import Comprobante

class Spooler(object):
    def __init__(self, env, sp_config, ftp_config):
        self.env = env
        self.sp_config = sp_config
        self.ftp_config = ftp_config

    def procesarFactura(self, filename=''):
        c = Comprobante(filename)
        self.guardar(c.out)
        

    def guardar(self, bs):
        archivo_destino = os.path.join(self.sp_config['SUCCESS_FOLDER'], "hola.xml")
        with open(archivo_destino, 'w+') as fw:
            fw.write(str(bs))

    def enviar(self):
        pass

