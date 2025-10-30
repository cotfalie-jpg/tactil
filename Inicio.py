import os
import streamlit as st
import base64
from openai import OpenAI
import openai
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# -----------------------------------------------------
# CONFIGURACIÓN DE ESTILO BAE
# -----------------------------------------------------
st.set_page_config(page_title="Bae | Tablero Inteligente", page_icon="🍼", layout="centered")

# CSS personalizado con la estética de BAE
st.markdown("""
    <style>
        /* Fondo general */
        .stApp {
            background-color: #FFF8EA;
            color: #3C3C3C;
            font-family: 'Poppins', sans-serif;
        }

        /* Títulos principales */
        h1, h2, h3 {
            color: #DD8E6B;
            font-weight: 700;
        }

        /* Subtítulos */
        .stSidebar h2, .stSidebar h3 {
            color: #DD8E6B !important;
        }

        /* Botones */
        div.stButton > button:first-child {
            background-color: #C6E2E3;
            color: #3C3C3C;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            padding: 0.6em 1.2em;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #DD8E6B;
            color: white;
            transform: scale(1.03);
        }

        /* Barra lateral */
        section[data-testid="stSidebar"] {
            background-color: #FFF2C3;
        }

        /* Inputs */
        input {
            border-radius: 10px !important;
        }

        /* Canvas */
        canvas {
            border-radius: 16px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------
st.title("🍼 Tablero Inteligente de BAE")
st.write("Una herramienta interactiva para explorar cómo la inteligencia artificial puede interpretar los primeros bocetos de ideas creativas.")

with st.sidebar:
    st.subheader("Acerca de esta app")
    st.write("En esta aplicación exploramos la capacidad que ahora tiene una máquina de **interpretar un boceto** y describirlo de forma natural.")
    st.write("Esta versión usa el lenguaje visual y los colores de BAE para mantener una estética cálida y amigable.")
    st.divider()

# Panel de dibujo
st.subheader("Dibuja tu boceto 👶")
st.write("Usa el panel inferior para dibujar tu idea y presiona el botón para analizarla con IA.")

drawing_mode = "freedraw"
stroke_width = st.sidebar.slider('Selecciona el ancho de línea', 1, 30, 5)
stroke_color = "#000000"
bg_color = '#FFF2C3'

canvas_result = st_canvas(
    fill_color="rgba(221,142,107,0.3)",  # tono salmón con transparencia
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=300,
    width=400,
    drawing_mode=drawing_mode,
    key="canvas",
)

ke = st.text_input("🔑 Ingresa tu Clave de API (OpenAI)", type="password")
os.environ["OPENAI_API_KEY"] = ke
api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Botón para análisis
analyze_button = st.button("✨ Analizar imagen", type="secondary")

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return None

# -----------------------------------------------------
# PROCESAMIENTO DE LA IMAGEN
# -----------------------------------------------------
if canvas_result.image_data is not None and api_key and analyze_button:
    with st.spinner("Analizando tu boceto con amor... 💗"):
        input_numpy_array = np.array(canvas_result.image_data)
        input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
        input_image.save('img.png')

        base64_image = encode_image_to_base64("img.png")
        prompt_text = "Describe brevemente en español la imagen que te muestro."

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}},
                    ],
                }],
                max_tokens=500,
            )

            if response.choices[0].message.content:
                st.success("🍼 Análisis completado con éxito:")
                st.markdown(f"**{response.choices[0].message.content}**")

        except Exception as e:
            st.error(f"Ocurrió un error al analizar la imagen: {e}")
else:
    if not api_key:
        st.warning("Por favor, ingresa tu clave de API antes de continuar.")
