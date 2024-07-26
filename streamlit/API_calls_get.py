import requests
import pandas as pd
from logging_config import logger

def flatten_json(data, prefix=''):
    result = {}
    for key, value in data.items():
        new_key = f"{prefix}{key}"
        if isinstance(value, dict):
            result.update(flatten_json(value, new_key + '_'))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                result.update(flatten_json(item, f"{new_key}{i}_"))
        else:
            result[new_key] = value
    return result

def get_citas_autor(nombre_autor):
    base_url = 'http://localhost:8000/autor/citas'

    # Nombre del alumno y parámetros adicionales
    params = {
        'nombre_autor': nombre_autor,
    }

    # Construir la URL completa con los parámetros
    url = f'{base_url}'
    query_params = '&'.join([f'{key}={value.replace(" ", "%20")}' for key, value in params.items()])
    url = f'{url}?{query_params}'

    # Encabezados de la solicitud
    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar el estado de la solicitud
    if response.status_code == 404:
            print(f'El autor "{nombre_autor}" no se encontró (Error 404).')
            return None
    
    elif response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON a un diccionario Python
        return data
    
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')

def get_cita_aleatoria(nombre_autor):
    base_url = 'http://localhost:8000/autor/cita_random'

    params = {
        'nombre_autor': nombre_autor,
    }

    # Construir la URL completa con los parámetros
    url = f'{base_url}'
    query_params = '&'.join([f'{key}={value.replace(" ", "%20")}' for key, value in params.items()])
    url = f'{url}?{query_params}'

    # Encabezados de la solicitud
    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar el estado de la solicitud
    if response.status_code == 404:
            print(f'El autor "{nombre_autor}" no se encontró (Error 404).')
            return None
    
    elif response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON a un diccionario Python
        return data
    
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')


def get_cita_dia():
    base_url = 'http://localhost:8000/cita_dia'
    
    # Encabezados de la solicitud
    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(base_url, headers=headers)

    built_url = response.url
    print(f'Generated URL: {built_url}')

    if response.status_code == 200:
        data = response.json()  # Convertir la respuesta JSON a un diccionario Python
        return data
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')


def get_descuentos(descripcion):
    base_url = 'http://api:8000/descuentos/get'

    params = {
        'descuento': descripcion
    }

    # Encabezados de la solicitud
    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        data_list = [data]
        df = pd.DataFrame(data_list)
        return data_list, df
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')


def get_all_alumnos():
    base_url = 'http://api:8000/alumnos/all'

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return data, df
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')


def get_all_profesores():
    base_url = 'http://api:8000/profesores/all'

    response = requests.get(base_url)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        return data, df
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')

