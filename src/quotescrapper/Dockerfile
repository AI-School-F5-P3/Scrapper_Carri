# Imagen de python
FROM python:3.12

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos
COPY requirements.txt /app/

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . /app/

WORKDIR /app/quotescrapper/spiders

# Define el comando por defecto para ejecutar el contenedor
CMD ["python", "quotegetter.py"]