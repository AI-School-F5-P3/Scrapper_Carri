import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from logging_config import logger
from deep_translator import GoogleTranslator
from API_calls_get import get_citas_autor, get_cita_aleatoria, get_cita_dia, get_about_autor, get_all_tags, get_cita_tags, get_palabra_clave, get_stats

def change_screen(new_screen):
    st.session_state.screen = new_screen

def home_screen():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Bienvenido/a Quotter, la app nº1 en citas célebres.</h2>""", unsafe_allow_html=True)
    st.markdown("""<h3 style="text-align: center;">Cita del día:</h2>""", unsafe_allow_html=True)

    # Generación de una cita aleatoria cada vez que se inicia sesión en la aplicación

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

    # Idioma en el que mostrar los resultados
    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ucraniano'])

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
                        # st.markdown permite escribir el texto con la definición de tipo de fuente y tamaño que hemos definido en GUI.py
                        st.markdown(f'<div class="great-vibes-text">{i}. {texto_cita}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True) 
                    if idioma == 'Español':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='es') # Para usar el traductor fijar en source el idioma de entrada y en target el idioma de salida, las abreviaturas se pueden mirar en la página de translate.
                        cita_es = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_es}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True) 
                    if idioma == 'Portugués':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='pt')
                        cita_pt = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_pt}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    if idioma == 'Ucraniano':
                        texto_cita = cita["cita"]
                        translator = GoogleTranslator(source='en', target='uk')
                        cita_uk = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_uk}</div>', unsafe_allow_html=True)
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
                elif idioma == 'Ucraniano':
                    translator = GoogleTranslator(source = 'en', target = 'uk')
                    cita_uk = translator.translate(cita)
                    st.markdown(f'<div class="great-vibes-text">{cita_uk} {nombre}.</div>', unsafe_allow_html=True)
        else:
            st.warning('Tiene que especificar un nombre de autor')

       
    if st.button('Sobre el autor'):
        if nombre_autor:
            data = get_about_autor(nombre_autor)
            if data is None:
                st.warning('No se han encontrado la biografía de ese autor')
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
                elif idioma == 'Ucraniano':
                    translator = GoogleTranslator(source = 'en', target = 'uk')
                    about_uk = translator.translate(about)
                    st.markdown(f'<div class="great-vibes-text">{about_uk} {nombre}.</div>', unsafe_allow_html=True)
        else:
            st.warning('Tiene que especificar un nombre de autor')

def screen_tags():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Búsqueda de citas por tags</h2>""", unsafe_allow_html=True)

    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ucraniano'])

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
                    st.markdown(f'<div class="great-vibes-text">{i}. {texto_cita} {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Español':
                    translator = GoogleTranslator(source='en', target='es')
                    cita_es = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. {cita_es} {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Portugués':
                    translator = GoogleTranslator(source='en', target='pt')
                    cita_pt = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. {cita_pt} {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)
                elif idioma == 'Ucraniano':
                    translator = GoogleTranslator(source='en', target='uk')
                    cita_uk = translator.translate(texto_cita)
                    st.markdown(f'<div class="great-vibes-text">{i}. {cita_uk} {nombre_autor}</div>', unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                    st.markdown("<br>", unsafe_allow_html=True)

            logger.info(f'Obtenidas citas por tags')


def screen_search():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Búsqueda de citas por palabra clave</h2>""", unsafe_allow_html=True)

    idioma = st.selectbox('Idioma a mostrar', options = ['Inglés', 'Español', 'Portugués', 'Ucraniano'])

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
                        st.markdown(f'<div class="great-vibes-text">{i}. {texto_cita} {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Español':
                        translator = GoogleTranslator(source='en', target='es')
                        cita_es = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_es} {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Portugués':
                        translator = GoogleTranslator(source='en', target='pt')
                        cita_pt = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_pt} {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)
                    elif idioma == 'Ucraniano':
                        translator = GoogleTranslator(source='en', target='uk')
                        cita_uk = translator.translate(texto_cita)
                        st.markdown(f'<div class="great-vibes-text">{i}. {cita_uk} {nombre_autor}</div>', unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)  # Añadir espaciado entre citas
                        st.markdown("<br>", unsafe_allow_html=True)

        else:
            st.warning('Se debe incluir una palabra clave para iniciar la búsqueda.')

def screen_stats():
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Estadísticas de citas</h2>""", unsafe_allow_html=True)
    st.markdown("""<h3 style="text-align: center;">Solo se incluyen aquellos casos con más de 2 citas</h2>""", unsafe_allow_html=True)

    data = get_stats()

    # Convertir citas por autor a DataFrame, filtrando aquellos con num_citas >= 2
    citas_por_autor_list = []
    for item in data['citas_por_autor']:
        for author, count in item.items():
            if count >= 2:
                citas_por_autor_list.append({'author': author, 'num_citas': count})

    df_citas_por_autor = pd.DataFrame(citas_por_autor_list)

    # Convertir citas por tag a DataFrame, filtrando aquellos con num_citas >= 2
    citas_por_tag_list = []
    for item in data['citas_por_tag']:
        for tag, count in item.items():
            if count >= 2:
                citas_por_tag_list.append({'tag': tag, 'num_citas': count})

    df_citas_por_tag = pd.DataFrame(citas_por_tag_list)

    df_citas_por_autor = df_citas_por_autor.sort_values(by='num_citas', ascending=False)
    df_citas_por_tag = df_citas_por_tag.sort_values(by='num_citas', ascending=False)

    # Crear gráficos de barras con Seaborn
    sns.set_theme(style="white", palette = 'pastel')

    # Gráfico de citas por autor
    fig1, ax1 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='num_citas', y='author', hue = 'author', data=df_citas_por_autor, palette='flare', ax = ax1)
    ax1.set_title('Número de Citas por Autor')
    ax1.set_xlabel('Número de Citas')
    ax1.set_ylabel('Autor')
    st.pyplot(fig1)

    # Gráfico de citas por tag
    fig2, ax2 = plt.subplots(figsize=(12, 8))
    sns.barplot(x='num_citas', y='tag', hue = 'tag', data=df_citas_por_tag, palette='flare', ax = ax2)
    ax2.set_title('Número de Citas por Tag')
    ax2.set_xlabel('Número de Citas')
    ax2.set_ylabel('Tag')
    st.pyplot(fig2)




