import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import time

# Configuración de página
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# --- Inicialización de Estado del Quiz ---
if 'puntos' not in st.session_state:
    st.session_state.puntos = 0
if 'audio_path' not in st.session_state:
    st.session_state.audio_path = None

# 1. Configuración de Voz
voz_id = st.sidebar.selectbox("Elige una voz:", ["es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-AR-TomasNeural"])

# 2. Selección de Documento
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_pdf = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Indexación (Mantiene tu lógica original donde aparece el Prólogo)
MARCADOR = "###"
def obtener_indice(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        if MARCADOR in pagina.get_text():
            indices.append("Prólogo" if len(indices) == 0 else f"Capítulo {len(indices)}")
    return indices if indices else ["Sin secciones marcadas"]

lista_marcadores = obtener_indice(ruta_pdf)
seleccion = st.sidebar.selectbox("Elige la sección a escuchar:", lista_marcadores)

# 4. Extracción de Texto (Tu lógica original intacta)
def extraer_texto(ruta, indice_seleccionado):
    doc = fitz.open(ruta)
    texto_total = ""
    capturando = False
    contador = 0
    for pagina in doc:
        texto_pag = pagina.get_text()
        if MARCADOR in texto_pag:
            if contador == indice_seleccionado:
                capturando = True
                texto_pag = texto_pag.split(MARCADOR)[-1]
            else:
                capturando = False
            contador += 1
        if capturando:
            texto_total += texto_pag
    return texto_total

# 5. Interfaz de Audio y Quiz
col_audio, col_quiz = st.columns([1, 1])

with col_audio:
    if st.button(f"🔊 ESCUCHAR SECCIÓN"):
        idx_idx = lista_marcadores.index(seleccion)
        texto_real = extraer_texto(ruta_pdf, idx_idx)
        temp_file = "temp_audio.mp3"
        async def generar():
            comunicador = edge_tts.Communicate(texto_real, voz_id)
            await comunicador.save(temp_file)
        asyncio.run(generar())
        st.session_state.audio_path = temp_file

    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        st.audio(st.session_state.audio_path, format="audio/mp3")

with col_quiz:
    st.subheader("🏆 Tablero de Desafío")
    st.metric("Puntuación acumulada", st.session_state.puntos)
    
    st.markdown("---")
    st.subheader("🎯 Reto de 1 minuto")
    with st.form("quiz_form"):
        # Pregunta de ejemplo
        pregunta = "¿Cuál es el concepto clave de esta sección según la normativa vigente?"
        opciones = ["A) Procedimiento técnico", "B) Sanción administrativa", "C) Marco normativo"]
        eleccion = st.radio(pregunta, opciones)
        
        if st.form_submit_button("Enviar Respuesta"):
            if eleccion == "C) Marco normativo":
                st.session_state.puntos += 10
                st.success("¡Correcto! +10 puntos")
                st.balloons()
            else:
                st.error("Incorrecto. Intenta nuevamente.")

st.write("---")
st.write(f"**Documento:** {archivo_seleccionado}")
