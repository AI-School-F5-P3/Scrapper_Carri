import streamlit as st
from logging_config import logger
from GUI_screens import change_screen, home_screen, screen_autor, screen_tags, screen_search


# Función para definir una pantalla de login inicial
def login():
    '''
    username se ha dijado como admin y password como 1234 para facilitar las pruebas, pero lo correcto sería externalizar estos datos.
    '''
    pen = "\U0001F58B"
    scroll = "\U0001F4DC"
    

    st.markdown(f"""<h1 style="text-align: center;"> {pen} {scroll} Quotter {scroll} {pen} </h1>""", unsafe_allow_html=True)
    st.markdown("""<h2 style="text-align: center;">Bienvenido/a a la página de gestión de su base de datos.</h2>""", unsafe_allow_html=True)

    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Iniciar sesión"):
        # Verificar las credenciales (simulado)
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            logger.info(f'Se ha iniciado sesión en streamlit')
            st.success("¡Inicio de sesión exitoso!")
        else:
            logger.error(f'Inicio de sesión en Streamlit fallido')
            st.error("Usuario o contraseña incorrectos.")

# Configuración inicial de la página
if 'screen' not in st.session_state:
    st.session_state.screen = 'home'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(layout="wide")

#css para los textos: se definen diferentes fuentes y tamaños para personalizar la interfaz
font_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');

h1, h2 {
    font-family: 'Cinzel', serif;
    text-align: center;
}

.stMarkdown, .stText, .stAlert {
        font-family: 'Great Vibes', cursive;
    }
.great-vibes-text {
        font-family: 'Great Vibes', cursive;
        font-size: 36px;
        text-align: center;
    }
</style>
"""

# Se añade el esitlo css
st.markdown(font_css, unsafe_allow_html=True)

# Banner
custom_html = """
<div class="banner">
    <img src="https://s26162.pcdn.co/wp-content/uploads/2019/07/books.jpg" alt="Banner Image" height="200" width="1000">
</div>
<style>
    .banner {
        width: 100%;
        height: 700px;
        overflow: hidden;
    }
    .banner img {
        width: 100%;
        object-fit: cover;
    }
</style>
"""

def apply_custom_css():
    st.markdown("""
        <style>
        .button-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .stButton button {
            width: 220px;
            height: 60px;
            background-color: #6943ff; /* Purple background */
            color: white; /* Text color */
            border: 1px solid #5227ff; /* Border color */
            border-radius: 8px;
            font-size: 18px; /* Font size */
            margin: 5px;
        }
        .stButton button:hover {
            background-color: #5e3fe0; /* Darker purple on hover */
        }
        /* Streamlit dark theme inspired by Shades of Purple */
        body {
            background-color: #2d2a55; /* Dark purple background */
            color: #e0e0e0; /* Light text */
        }
        .stMarkdown {
            color: #e0e0e0; /* Light text */
        }
        .css-18ni7ap, .css-1d391kg {
            background-color: #2d2a55; /* Dark purple background */
            color: #e0e0e0; /* Light text */
        }
        .css-1d391kg p {
            color: #e0e0e0; /* Light text */
        }
        .css-1v0mbdj a {
            color: #ff9d00; /* Link color */
        }
        .css-1v0mbdj a:hover {
            color: #ff9900; /* Link hover color */
        }
        </style>
    """, unsafe_allow_html=True)

# Mostrar el html customizado donde se han definido los colores para la aplicación
st.components.v1.html(custom_html)
apply_custom_css()

# Renderización del login
if not st.session_state.logged_in:
    login()
else:
    # Selección del menú lateral
    st.sidebar.header("Menú de Navegación")
    if st.sidebar.button("Home"):
        change_screen('home')
    if st.sidebar.button("Citas por autor"):
        change_screen('screen_autor')
    if st.sidebar.button("Citas por etiquetas"):
        change_screen('screen_tags')
    if st.sidebar.button("Buscador de citas"):
        change_screen('screen_search')

    # Renderización de las pantallas
    if st.session_state.screen == 'home':
        home_screen()
    elif st.session_state.screen == 'screen_autor':
        screen_autor()
    elif st.session_state.screen == 'screen_tags':
        screen_tags()
    elif st.session_state.screen == 'screen_search':
        screen_search()