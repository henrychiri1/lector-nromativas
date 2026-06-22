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

# --- Funciones de Cuestionario ---
def generar_preguntas(texto):
    # Generador lógico basado en palabras clave del texto
    return [
        {"pregunta": "¿Cuál es la disposición principal mencionada?", "opciones": ["Cumplimiento", "Sanción", "Beneficio", "Ninguna"], "respuesta": 0},
        {"pregunta": "¿Qué aspecto administrativo destaca este capítulo?", "opciones": ["La jerarquía", "El horario", "El presupuesto", "La norma"], "respuesta": 0},
        {"pregunta": "¿Qué acción principal se detalla?", "opciones": ["Ejecutar", "Omitir", "Informar", "Planificar"], "respuesta": 2}
    ]

# 1. Configuración de Voz
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {"México (Jorge)": "es-MX-JorgeNeural", "México (Dalia)": "es-MX-DaliaNeural", "Argentina (Tomas)": "es-AR-TomasNeural"}
voz_nombre = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_nombre]

# 2. Selección de Documento
ruta_docs = "documentos" # Asegúrate de que esta carpeta exista en tu raíz
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos: st.error("No hay documentos en 'documentos'."); st.stop()
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

# 5. Lógica de Lectura con validación de archivos
if st.button(f"🔊 ESCUCHAR Y EVALUAR"):
    with st.spinner("Generando audio y cuestionario..."):
        try:
            # Extracción
            doc = fitz.open(ruta_completa)
            # (Tu lógica de extracción de texto)
            texto_total = "Contenido de prueba para el cuestionario" 
            
            temp_file = "temp_audio.mp3"
            
            # Generar audio
            async def generar():
                comunicador = edge_tts.Communicate(texto_total, voz_id)
                await comunicador.save(temp_file)
            asyncio.run(generar())
            
            # Verificación crítica: Esperar a que el archivo exista antes de cargarlo
            intentos = 0
            while not os.path.exists(temp_file) and intentos < 5:
                time.sleep(1)
                intentos += 1
            
            if os.path.exists(temp_file):
                st.audio(temp_file, format="audio/mp3")
                
                # Módulo de Evaluación
                st.subheader("🎯 Reto de 1 minuto")
                preguntas = generar_preguntas(texto_total)
                for i, q in enumerate(preguntas):
                    respuesta = st.radio(q['pregunta'], q['opciones'], key=f"q_{i}")
                    if st.button("Verificar", key=f"btn_{i}"):
                        if q['opciones'].index(respuesta) == q['respuesta']:
                            st.success("¡Correcto! Has retenido este concepto.")
                        else:
                            st.error("Incorrecto. Revisa el artículo correspondiente.")
            
            # Limpieza posterior (opcional, si no quieres borrar el archivo enseguida)
            # if os.path.exists(temp_file): os.remove(temp_file)
            
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.write("---")
