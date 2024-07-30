# Webscrapper 
Clonar el repositorio en la localización deseada.
Crear en primer lugar el archivo .env en aquellos ficheros que contienen un dockerfile, el formato es:

  - DB_TYPE=postgresql+asyncpg
  - DB_HOST=quotes-db # Por defecto el docker de la base de datos se construye con este nombre
  - DB_PORT=5432
  - DB_NAME= quotes
  - DB_SCHEMA= quotes
  - DB_USER= admin_user
  - DB_PASSWORD = 1234
  - SECRET_KEY= secret_key
  - DEBUG=true

Modificar con los valores que cada uno considere.

Después ejecutar en la terminal dentro de la carpeta del proyecto:

  docker-compose up --build

De esta forma se ejecuta la creación de la base de datos, se comienza el proceso de scraping con las dos arañas y el proceso de inserción en la base de datos. Despues se levanta la API y la interfaz gráfica, permitiendo interactuar con la base de datos.
El usuario para entrar en la GUI es admin y la contraseña es 1234.
Curioseen las funciones.


