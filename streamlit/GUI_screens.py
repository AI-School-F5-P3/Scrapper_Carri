import streamlit as st
import pandas as pd
from logging_config import logger
from deep_translator import GoogleTranslator
from API_calls_get import get_citas_autor, get_cita_aleatoria, get_cita_dia, get_about_autor, get_all_tags, get_cita_tags, get_palabra_clave

def change_screen(new_screen):
    st.session_state.screen = new_screen

def home_screen():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Bienvenido/a a la página de gestión de su base de datos.</h2>""", unsafe_allow_html=True)

    if 'data' not in st.session_state:
        st.session_state.data = get_cita_dia()

    data = st.session_state.data
    nombre = data.get("nombre_autor")
    cita = data.get("cita")

    st.markdown(f'<div class="great-vibes-text">{cita} {nombre}.</div>', unsafe_allow_html=True)



def screen_autor():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    
    # Encabezados
    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Busqueda de citas por autores</h2>""", unsafe_allow_html=True)

    # Campo de entrada para el nombre del autor
    nombre_autor = st.text_input('Nombre y apellidos del autor/a')

    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ukraniano'])

    if st.button('Mostrar todas las citas del autor/a'):
        if nombre_autor:
            data = get_citas_autor(nombre_autor)
            if data is None:
                st.warning('No se han encontrado citas para este autor')
            else:
                logger.info(f'Obtenidas citas de {nombre_autor}')
                nombre = data.get("nombre_autor")
                citas = data.get("citas")

                for i, cita in enumerate(citas, 1):
                    if idioma == 'Inglés':
                        texto_cita = cita["cita"]
                        st.markdown(f'<div class="great-vibes-text">{i}. "{texto_cita}"</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True) 
                    if idioma == 'Español':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='es')
                        cita_es = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_es}"</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True) 
                    if idioma == 'Portugués':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='pt')
                        cita_pt = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_pt}"</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    if idioma == 'Ukraniano':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='uk')
                        cita_uk = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_uk}"</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True) 
        else:
            st.warning('Tiene que especificar un nombre de autor')

        
    if st.button('Cita aleatoria del autor'):
        if nombre_autor:
            data = get_cita_aleatoria(nombre_autor)
            if data is None:
                st.warning('No se han encontrado citas para este autor')
            else:
                logger.info(f'Obtenida cita aleatoria de {nombre_autor}')
                nombre = data.get("nombre_autor")
                cita = data.get("citas")
                if idioma == 'Inglés':
                    st.markdown(f'<div class="great-vibes-text">{cita} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Español':
                    translator = GoogleTranslator(source='en', target='es')
                    cita_es = translator.translate(cita)
                    st.markdown(f'<div class="great-vibes-text">{cita_es} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Portugués':
                    translator = GoogleTranslator(source = 'en', target = 'pt')
                    cita_pt = translator.translate(cita)
                    st.markdown(f'<div class="great-vibes-text">{cita_pt} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Ukraniano':
                    translator = GoogleTranslator(source = 'en', target = 'uk')
                    cita_uk = translator.translate(cita)
                    st.markdown(f'<div class="great-vibes-text">{cita_uk} {nombre}.</div>', unsafe_allow_html=True)
        else:
            st.warning('Tiene que especificar un nombre de autor')

       
    if st.button('Sobre el autor'):
        if nombre_autor:
            data = get_about_autor(nombre_autor)
            if data is None:
                st.warning('No se han encontrado citas para este autor')
            else:
                logger.info(f'Obtenida about de {nombre_autor}')
                nombre = data.get('nombre_autor')
                about = data.get("about")
                if idioma == 'Inglés':
                    st.markdown(f'<div class="great-vibes-text">{about} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Español':
                    translator = GoogleTranslator(source='en', target='es')
                    about_es = translator.translate(about)
                    st.markdown(f'<div class="great-vibes-text">{about_es} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Portugués':
                    translator = GoogleTranslator(source = 'en', target = 'pt')
                    about_pt = translator.translate(about)
                    st.markdown(f'<div class="great-vibes-text">{about_pt} {nombre}.</div>', unsafe_allow_html=True)
                elif idioma == 'Ukraniano':
                    translator = GoogleTranslator(source = 'en', target = 'uk')
                    about_uk = translator.translate(about)
                    st.markdown(f'<div class="great-vibes-text">{about_uk} {nombre}.</div>', unsafe_allow_html=True)
        else:
            st.warning('Tiene que especificar un nombre de autor')

def screen_tags():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Gestión de profesores</h2>""", unsafe_allow_html=True)

    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ukraniano'])

    lista_de_tags = ['None'] + get_all_tags()

    tag_1 = st.selectbox('Elegir etiqueta 1', options = lista_de_tags)

    tag_2 = st.selectbox('Elegir etiqueta 2', options = lista_de_tags)
    
    tag_3 = st.selectbox('Elegir etiqueta 3', options = lista_de_tags)

    tag_4 = st.selectbox('Elegir etiqueta 4', options = lista_de_tags)
    
    tag_5 = st.selectbox('Elegir etiqueta 5', options = lista_de_tags)

    tag_6 = st.selectbox('Elegir etiqueta 6', options = lista_de_tags)

    tag_7 = st.selectbox('Elegir etiqueta 7', options = lista_de_tags)

    tag_8 = st.selectbox('Elegir etiqueta 8', options = lista_de_tags)

    name = st.text_input('Autor/a a buscar:')

    nombre_autor = name if name else None

    if st.button('Enviar'):
        data = get_cita_tags(tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, tag_7, tag_8, nombre_autor)
        if data is None:
            logger.error('No se han encontrado citas para estas tags o autor')
            st.warning('No se han encontrado citas para estas tags o autor')
        else:
            for i, cita in enumerate(data, 1):
                nombre_autor = cita["nombre_autor"]
                texto_cita = cita["cita"]

                if idioma == 'Inglés':
                    st.markdown(f'<div class="great-vibes-text">{i}. "{texto_cita}" {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Español':
                    translator = GoogleTranslator(source='en', target='es')
                    cita_es = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. "{cita_es}" {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Portugués':
                    translator = GoogleTranslator(source='en', target='pt')
                    cita_pt = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. "{cita_pt} {nombre_autor}"</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Ukraniano':
                    translator = GoogleTranslator(source='en', target='uk')
                    cita_uk = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. "{cita_uk}" {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)

            logger.info(f'Obtenidas citas por tags')


def screen_search():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Gestión de finanzas</h2>""", unsafe_allow_html=True)

    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ukraniano'])

    palabra_clave = st.text_input('Palabra a buscar: ')
    
    if st.button('Buscar'):
        if palabra_clave:
            data = get_palabra_clave(palabra_clave)
            if data is None:
                logger.error('No se han encontrado citas para esta palabra clave')
                st.warning('No se han encontrado citas para esta palabra clave')
            else:
                for i, cita in enumerate(data, 1):
                    nombre_autor = cita["nombre_autor"]
                    texto_cita = cita["cita"]

                    if idioma == 'Inglés':
                        st.markdown(f'<div class="great-vibes-text">{i}. "{texto_cita}" {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Español':
                        translator = GoogleTranslator(source='en', target='es')
                        cita_es = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_es}" {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Portugués':
                        translator = GoogleTranslator(source='en', target='pt')
                        cita_pt = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_pt} {nombre_autor}"</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Ukraniano':
                        translator = GoogleTranslator(source='en', target='uk')
                        cita_uk = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. "{cita_uk}" {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.warning('Se debe incluir una palabra clave para iniciar la búsqueda.')





