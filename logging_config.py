import logging

def setup_logger():

    logger = logging.getLogger('logs') # Inicializar el gestor de logs.
    logger.setLevel(logging.DEBUG)
   
    # Se ha configurado el nivel de logging a DEBUG para capturar todos los niveles de log (DEBUG, INFO, WARNING, ERROR, CRITICAL).

    log_file_path = '/app/logs/app.log'

    # Crear un gestor de archivo con encoding UTF-8
    fh = logging.FileHandler(log_file_path, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    
    # Crear un gestor de consola ('ch' console handler) para mostrar también los mensajes en la consola.
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    
    # Definir el formato del log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # fecha actual y hora, nivel de gravedad del mensaje, mensaje que se quiere loggear.
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    # Agregar los gestores al logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger # Devolver el logger para utilizarlo en el cuerpo principal de la aplicación.

# Configurar el logger
logger = setup_logger()