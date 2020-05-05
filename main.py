from spooler import Spooler
from comprobante import Comprobante
from configuracion import GlobalConfiguration
import os

def configurar():
    return GlobalConfiguration()


if __name__ == "__main__":

    BASE_DIR = os.getcwd()
    cfg = configurar()
    INBOX = os.path.join(BASE_DIR, cfg.config_global['INBOX_FOLDER'])
    RESULTS = os.path.join(BASE_DIR, cfg.config_global['SUCCESS_FOLDER'])
    ERRORS = os.path.join(BASE_DIR, cfg.config_global['ERRORS_FOLDER'])

    cfg.config_global['INBOX_FOLDER'] = INBOX
    cfg.config_global['SUCCESS_FOLDER'] = RESULTS
    cfg.config_global['ERRORS_FOLDER'] = ERRORS

    sp = Spooler(
        env=cfg.entorno, ftp_config=cfg.configuracion_ftp, 
        sp_config=cfg.config_global
    )
    
    files = os.listdir(INBOX)
    for fil in files:
        fullPathFile = os.path.join(INBOX, fil)
        sp.procesarFactura(fullPathFile)