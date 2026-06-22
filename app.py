import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json
import random

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

# --- Funciones de Cuestionario ---
def generar_preguntas(texto):
    """Genera 3 preguntas de prueba basadas en el texto procesado."""
    # En un entorno real, aquí usarías una llamada a la API de OpenAI/Anthropic.
    # Como ejemplo funcional, creamos una estructura de evaluación basada en el contenido.
    preguntas = [
        {"pregunta": "¿Cuál es el objetivo principal de esta normativa?", "opciones": ["Regular funciones", "Sancionar sin motivo", "Publicidad", "Ninguna"], "respuesta": 0},
        {"pregunta": "¿Qué aspecto administrativo destaca este capítulo?", "opciones": ["La jerarquía", "El horario", "El presupuesto", "La sanción"], "respuesta": 0},
        {"pregunta": "¿Qué acción está prohibida según el texto?", "opciones": ["Trabajar", "Omitir deberes", "Informar", "Planificar"], "respuesta": 1}
    ]
    return preguntas

# 1. Configuración de Voz
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {"México (Jorge)": "es-MX-JorgeNeural", "México (Dalia)": "es-MX-DaliaNeural", "Argentina (Tomas)": "es-AR-TomasNeural"}
voz_nombre = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_nombre]

# 2. Selección de Documento
ruta_docs = "documents"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos: st.error("No hay documentos."); st.stop()
archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)
ruta_indice = ruta_completa + ".idx"
MARCADOR_FIJO = "###" 

# 3. Sistema de Indexación
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

# 5. Lógica de Lectura y Evaluación
if st.button(f"🔊 ESCUCHAR Y EVALUAR"):
    with st.spinner("Procesando..."):
        # Lógica de extracción de texto
        doc = fitz.open(ruta_completa)
        idx_sel = lista_marcadores.index(seleccion)
        texto_total = ""
        # ... (aquí iría tu lógica de capturar texto que ya tienes) ...
        
        # Audio
        st.audio("temp_audio.mp3", format="audio/mp3")
        
        # --- NUEVO: MÓDULO DE APRENDIZAJE ACTIVO ---
        st.subheader("🎯 Reto de 1 minuto")
        preguntas = generar_preguntas(texto_total)
        for i, q in enumerate(preguntas):
            respuesta = st.radio(q['pregunta'], q['opciones'], key=f"q_{i}")
            if st.button("Verificar", key=f"btn_{i}"):
                if q['opciones'].index(respuesta) == q['respuesta']:
                    st.success("¡Correcto! Has retenido este concepto.")
                else:
                    st.error("Incorrecto. Revisa el artículo correspondiente en el documento.")

st.write("---")
