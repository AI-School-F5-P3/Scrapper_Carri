import subprocess
import time
from logging_config import logger

def run_spiders():
    '''
    Script para ejecutar las dos arañas que se requieren para extraer los datos. Se utiliza la librera subprocess para que se ejecuten en procesos separados, ya que de lo contrario puede dar problemas ya que scrapy no permite ejecutar más de una araña en un mismo proceso. Una vez se consiguen los datos de las arañas, se ejecutan las funciones de inserción en la base de datos y se confirma.
    '''
    # Ejecutar la araña de autores
    logger.info('Comienza proceso de scrap')
    subprocess.run(['scrapy', 'crawl', 'authors'], check=True)
    logger.info("Spider de autores completado")

    # Esperar a que el archivo de datos esté listo (ajustar según sea necesario)
    time.sleep(2)

    # Ejecutar la araña de citas
    subprocess.run(['scrapy', 'crawl', 'quotes'], check=True)
    logger.info("Spider de citas completado")

    # Ejecutar la inserción en la base de datos
    logger.info('Inicio de inserción en la base de datos')
    subprocess.run(['python', 'insert_data_authors.py'], check=True)
    subprocess.run(['python', 'insert_data_quotes.py'], check=True)
    logger.info("Datos insertados en la base de datos")

if __name__ == '__main__':
    run_spiders()