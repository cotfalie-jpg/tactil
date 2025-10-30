import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# -----------------------------------------------------
# CONFIGURACIÓN DE ESTILO VISUAL BAE
# -----------------------------------------------------
st.set_page_config(page_title="BAE | Análisis de Sentimiento", page_icon="🍼", layout="centered")

# CSS personalizado (estética BAE)
st.markdown("""
    <style>
        /* Fondo general */
        .stApp {
            background-color: #FFF8EA;
            color: #3C3C3C;
            font-family: 'Poppins', sans-serif;
        }

        /* Títulos */
        h1, h2, h3 {
            color: #DD8E6B;
            font-weight: 700;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #FFF2C3;
            border-right: 2px solid #DD8E6B20;
        }

        /* Botones */
        div.stButton > button:first-child {
            background-color: #C6E2E3;
            color: #3C3C3C;
            border: none;
            border-radius: 10px;
            font-weight: 600;
            padding: 0.5em 1em;
            transition: all 0.3s ease;
        }
        div.stButton > button:first-child:hover {
            background-color: #DD8E6B;
            color: white;
            transform: scale(1.03);
        }

        /* Expander */
        [data-testid="stExpander"] {
            border: 1px solid #C6E2E3;
            border-radius: 12px;
            background-color: #FFFDF5;
        }
        [data-testid="stExpander"] summary {
            color: #DD8E6B !important;
            font-weight: 600;
        }

        /* Campos de texto */
        textarea, input {
            border-radius: 10px !important;
            border: 1px solid #DD8E6B40 !important;
            background-color: #FFFFFF !important;
        }

        /* Texto del sidebar */
        .stSidebar p, .stSidebar div, .stSidebar span {
            font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------
translator = Translator()
st.title("🍼 Análisis de Sentimiento con BAE")
st.write("Una herramienta que interpreta el tono emocional de tus textos y sugiere correcciones con ayuda de **IA afectiva**.")

with st.sidebar:
    st.subheader("Polaridad y Subjetividad")
    st.write("""
    **Polaridad:** Mide si el sentimiento es positivo, negativo o neutral.
    -1 (muy negativo) → 0 (neutral) → 1 (muy positivo)

    **Subjetividad:** Evalúa cuánto del texto es **opinión** o **hecho**.  
    0 = objetivo | 1 = muy subjetivo.
    """)

# -----------------------------------------------------
# ANÁLISIS DE POLARIDAD Y SUBJETIVIDAD
# -----------------------------------------------------
with st.expander("💬 Analizar Polaridad y Subjetividad en un texto"):
    text1 = st.text_area("✏️ Escribe por favor tu texto:", placeholder="Ejemplo: Me encanta aprender cosas nuevas con mi bebé 💕")
    
    if text1:
        translation = translator.translate(text1, src="es", dest="en")
        blob = TextBlob(translation.text)
        
        st.markdown(f"**Polarity:** {round(blob.sentiment.polarity, 2)}")
        st.markdown(f"**Subjectivity:** {round(blob.sentiment.subjectivity, 2)}")
        
        x = round(blob.sentiment.polarity, 2)
        if x >= 0.5:
            st.success("✨ Es un sentimiento **Positivo**.")
        elif x <= -0.5:
            st.error("😔 Es un sentimiento **Negativo**.")
        else:
            st.info("😐 Es un sentimiento **Neutral**.")

# -----------------------------------------------------
# CORRECCIÓN EN INGLÉS
# -----------------------------------------------------
with st.expander("🧠 Corrección en inglés"):
    text2 = st.text_area("✏️ Escribe una frase en inglés:", key="4", placeholder="Example: I has a great idea for my baby app.")
    
    if text2:
        blob2 = TextBlob(text2)
        corrected_text = blob2.correct()
        st.markdown(f"✅ **Texto corregido:** {corrected_text}")
