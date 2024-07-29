import requests
import pandas as pd
from urllib.parse import urlencode
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


def get_about_autor(nombre_autor):
    base_url = 'http://localhost:8000/autor/about'

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

def get_all_tags():
    url = 'http://localhost:8000/tags/list'

    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # Ocurrió un error
        logger.error(f'Error al hacer la solicitud: {response.status_code}')
        print(f'Error al hacer la solicitud: {response.status_code}')


def get_cita_tags(tag_1, tag_2=None, tag_3=None, tag_4=None, tag_5=None, tag_6=None, tag_7=None, tag_8=None, nombre_autor=None):
    url = 'http://localhost:8000/tags/cita'

    # Construir los parámetros de consulta
    params = {
        'tag1': tag_1,
        'tag2': tag_2,
        'tag3': tag_3,
        'tag4': tag_4,
        'tag5': tag_5,
        'tag6': tag_6,
        'tag7': tag_7,
        'tag8': tag_8,
        'nombre_autor': nombre_autor
    }
    
    # Filtrar los parámetros que son None
    params = {key: value for key, value in params.items() if value not in ('None', None)}

    # Codificar los parámetros en una cadena de consulta
    query_params = urlencode(params, doseq=True)

    # Construir la URL completa con los parámetros
    full_url = f'{url}?{query_params}'

    # Hacer la solicitud GET con los parámetros
    response = requests.get(full_url, headers={'accept': 'application/json'})

    if response.status_code == 200:
        data = response.json()  # Convertir la respuesta JSON en una lista o diccionario
        return data
    else:
        response.raise_for_status() 

def get_palabra_clave(palabra_clave):
    base_url = 'http://localhost:8000/word'

    params = {
        'palabra': palabra_clave,
    }

    # Construir la URL completa con los parámetros
    url = f'{base_url}'
    query_params = '&'.join([f'{key}={value.replace(" ", "%20")}' for key, value in params.items()])
    url = f'{url}?{query_params}'

    headers = {
        'accept': 'application/json'
    }

    # Realizar la solicitud GET
    response = requests.get(url, headers=headers)

    # Verificar el estado de la solicitud
    if response.status_code == 404:
            print(f'No se encuentran citas con la palabra {palabra_clave}.')
            return None
    
    elif response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON a un diccionario Python
        return data





