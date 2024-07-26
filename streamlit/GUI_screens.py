import streamlit as st
import pandas as pd
from logging_config import logger
from deep_translator import GoogleTranslator
from API_calls_get import get_citas_autor, get_cita_aleatoria, get_cita_dia

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
                    texto_cita = cita["cita"]
                    st.markdown(f'<div class="great-vibes-text">{i}. "{texto_cita}"</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True) 
        
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

       
    if st.button('Sobre el autor'):
        st.write('Mostrando información sobre el autor...')
        st.markdown(f'<div class="great-vibes-text">Mostrando todas las citas del autor {nombre_autor}.</div>', unsafe_allow_html=True)

def screen_tags():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Gestión de profesores</h2>""", unsafe_allow_html=True)

    lista_de_tags = ['love']

    st.selectbox('Elegir etiqueta 1', options = lista_de_tags)

    st.selectbox('Elegir etiqueta 2', options = lista_de_tags)
    
    st.selectbox('Elegir etiqueta 3', options = lista_de_tags)

    st.selectbox('Elegir etiqueta 4', options = lista_de_tags)
    
    st.selectbox('Elegir etiqueta 5', options = lista_de_tags)

    st.selectbox('Elegir etiqueta 6', options = lista_de_tags)

    st.selectbox('Elegir etiqueta 7', options = lista_de_tags)

    st.selectbox('Elegir etiqueta 8', options = lista_de_tags)

    st.text_input('Autor/a a buscar:')

    if st.button('Enviar'):
        st.write('Cita con tags')


def screen_search():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Gestión de finanzas</h2>""", unsafe_allow_html=True)

    st.write('En construccion')





