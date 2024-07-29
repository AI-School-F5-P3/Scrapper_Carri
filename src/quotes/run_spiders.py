import subprocess
import time

def run_spiders():
    # Ejecutar la araña de autores
    subprocess.run(['scrapy', 'crawl', 'authors'], check=True)
    print("Spider de autores completado")

    # Esperar a que el archivo de datos esté listo (ajustar según sea necesario)
    time.sleep(10)

    # Ejecutar la araña de citas
    subprocess.run(['scrapy', 'crawl', 'quotes'], check=True)
    print("Spider de citas completado")

    # Ejecutar la inserción en la base de datos
    subprocess.run(['python', 'insert_data_authors.py'], check=True)
    subprocess.run(['python', 'insert_data_quotes.py'], check=True)
    print("Datos insertados en la base de datos")

if __name__ == '__main__':
    run_spiders()