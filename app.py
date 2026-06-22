import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json
import time

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    .stSelectbox div[data-baseweb="select"] input { caret-color: transparent !important; pointer-events: none !important; }
    .stSelectbox div[data-baseweb="select"] { cursor: pointer !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# 1. Configuración de Voz
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {"México (Jorge)": "es-MX-JorgeNeural", "México (Dalia)": "es-MX-DaliaNeural", "Argentina (Tomas)": "es-AR-TomasNeural"}
voz_id = st.sidebar.selectbox("Elige una voz:", list(voces.keys()), format_func=lambda x: x)
voz_id = voces[voz_id]

# 2. Selección de Documento con Ruta Absoluta
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")

if not os.path.exists(ruta_docs):
    st.error(f"Error: No se encuentra la carpeta 'documents' en {base_path}")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.warning("La carpeta 'documents' está vacía o no tiene archivos PDF.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)
ruta_indice = ruta_completa + ".idx"
MARCADOR_FIJO = "###" 

# 3. Sistema de Indexación (Auto-regenerable)
def obtener_indice(ruta_pdf):
    if os.path.exists(ruta_indice): os.remove(ruta_indice)
    
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        if MARCADOR_FIJO in pagina.get_text():
            indices.append("Prólogo" if len(indices) == 0 else f"Capítulo {len(indices)}")
    
    if not indices: indices = ["Sin secciones marcadas"]
    with open(ruta_indice, "w") as f: json.dump(indices, f)
    return indices

lista_marcadores = obtener_indice(ruta_completa)
seleccion = st.sidebar.selectbox("Elige la sección a escuchar:", lista_marcadores)

# 4. Lógica de Reproducción y Evaluación
if st.button(f"🔊 ESCUCHAR Y EVALUAR"):
    with st.spinner("Procesando audio..."):
        try:
            # Aquí iría la lógica de extracción de texto que ya tienes
            temp_file = "temp_audio.mp3"
            
            # (El código de generación de edge-tts iría aquí)
            
            if os.path.exists(temp_file):
                st.audio(temp_file, format="audio/mp3")
                
                # Módulo de Evaluación (Active Recall)
                st.subheader("🎯 Reto de 1 minuto")
                st.info("Responde para reforzar tu memoria:")
                if st.radio("¿Qué tema principal se trató en esta sección?", ["Normativa", "Sanción", "Procedimiento"]) == "Normativa":
                    st.success("¡Correcto!")
                else:
                    st.error("Revisa el documento nuevamente.")
            else:
                st.warning("El audio se está generando, intenta de nuevo en un segundo.")
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")
st.write(f"**Documento activo:** {archivo_seleccionado}")
