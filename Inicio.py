import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# ============= CONFIGURACIÓN GENERAL =============
st.set_page_config(
    page_title="BAE Canvas – Cuentos para Bebés",
    page_icon="🧸",
    layout="centered"
)

# ============= ESTILO BAE =============
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #FFF8EA;
    color: #3C3C3C;
    font-family: 'Poppins', sans-serif;
}
.main-title {
    font-size: 2.8rem;
    color: #DD8E6B;
    text-align: center;
    font-weight: 700;
    margin-top: 1rem;
    margin-bottom: 0.3rem;
}
.subtitle {
    font-size: 1.2rem;
    color: #4D797A;
    text-align: center;
    margin-bottom: 2rem;
}
.canvas-container {
    background: #FFFFFF;
    border-radius: 20px;
    border: 2px solid #F0D192;
    padding: 1rem;
    box-shadow: 0 6px 20px rgba(221, 142, 107, 0.15);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #DD8E6B;
    border-bottom: 2px solid #F0D192;
    padding-bottom: 0.3rem;
    margin-bottom: 1rem;
}
.bae-btn button {
    background: linear-gradient(135deg, #F9E79F, #F5CBA7);
    border: none;
    color: #3C3C3C;
    font-weight: 600;
    border-radius: 12px;
    padding: 0.9rem 2rem;
    width: 100%;
    box-shadow: 0 6px 15px rgba(221,142,107,0.25);
    transition: all 0.3s ease;
}
.bae-btn button:hover {
    background: linear-gradient(135deg, #F5CBA7, #FAD7A0);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(221,142,107,0.35);
}
.response-box {
    background: #FFF;
    border-radius: 16px;
    border: 1px solid #F0D192;
    padding: 1.5rem;
    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ============= ESTADO DE SESIÓN =============
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'full_response' not in st.session_state:
    st.session_state.full_response = ""
if 'base64_image' not in st.session_state:
    st.session_state.base64_image = ""

# ============= FUNCIÓN DE CODIFICACIÓN =============
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
            return encoded_image
    except FileNotFoundError:
        return None

# ============= ENCABEZADO PRINCIPAL =============
st.markdown('<div class="main-title">🧸 Canvas de Cuentos BAE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Dibuja libremente y deja que la IA transforme tu arte en un cuento tierno y educativo 💛</div>', unsafe_allow_html=True)

# ============= SIDEBAR BAE =============
with st.sidebar:
    st.image("logo_bae.png", width=140)
    st.markdown("### 🎨 Herramientas de dibujo")
    stroke_width = st.slider('Grosor del trazo', 2, 25, 10)
    stroke_color = st.color_picker('Color del trazo', '#4D797A')

    st.markdown("### 🔑 Clave de OpenAI")
    api_key = st.text_input('Clave API', type="password")

    st.markdown("---")
    st.markdown("**BAE Canvas** crea historias afectivas para bebés a partir de dibujos simples:")
    st.markdown("""
    - 🌈 Imagina un animal o figura  
    - 💭 La IA inventa un cuento tierno  
    - 🧠 Con moraleja y aprendizaje suave  
    - 🎶 Ideal para la hora de dormir
    """)

# ============= PANEL DE DIBUJO =============
st.markdown('<div class="section-title">Tu Dibujo</div>', unsafe_allow_html=True)
st.markdown('<div class="canvas-container">', unsafe_allow_html=True)

canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color="#FFF8EA",
    height=400,
    width=600,
    drawing_mode="freedraw",
    key="canvas"
)
st.markdown('</div>', unsafe_allow_html=True)

# ============= BOTÓN DE ANÁLISIS =============
st.markdown('<div class="bae-btn">', unsafe_allow_html=True)
analyze = st.button("✨ Crear Cuento del Dibujo", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============= PROCESAR EL DIBUJO =============
if analyze:
    if canvas_result.image_data is not None and api_key:
        with st.spinner("💫 Imaginando un cuento dulce para tu dibujo..."):
            # Guardar imagen
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8')).convert('RGBA')
            input_image.save('img.png')
            
            # Convertir a base64
            base64_image = encode_image_to_base64("img.png")
            st.session_state.base64_image = base64_image

            # Prompt adaptado al tono BAE
            prompt_text = """
Eres una inteligencia creativa de BAE, especializada en crear cuentos cortos, tiernos y educativos para bebés.

Observa el dibujo y crea un cuento suave con este formato:

1. 🌟 **Título del cuento**
2. 🧸 **Historia breve (máx. 8 líneas)** – con tono afectivo, ritmo tranquilo y lenguaje simple.
3. 💛 **Mensaje o aprendizaje** – una pequeña moraleja o valor (amistad, ternura, respeto, amor).

Usa un lenguaje cálido, con metáforas visuales dulces, apto para bebés y primera infancia.
"""

            try:
                os.environ['OPENAI_API_KEY'] = api_key
                client = OpenAI(api_key=api_key)

                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt_text},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{base64_image}",
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=500,
                )

                if response.choices[0].message.content:
                    story = response.choices[0].message.content
                    st.session_state.full_response = story
                    st.session_state.analysis_done = True

            except Exception as e:
                st.error(f"❌ Error al generar el cuento: {e}")
    else:
        if not api_key:
            st.warning("🔑 Ingresa tu clave de OpenAI para continuar")
        if canvas_result.image_data is None:
            st.info("🎨 Dibuja algo primero para crear tu cuento")

# ============= MOSTRAR RESULTADO =============
if st.session_state.analysis_done and st.session_state.full_response:
    st.markdown('<div class="section-title">✨ Tu Cuento BAE</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="response-box">{st.session_state.full_response}</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("🌼 *Desarrollado con ternura por BAE — Inteligencia Afectiva para la Primera Infancia* 💛")

