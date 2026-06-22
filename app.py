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

# --- Inicialización de Estado ---
if 'audio_path' not in st.session_state:
    st.session_state.audio_path = None

# 1. Configuración de Voz
voz_id = st.sidebar.selectbox("Elige una voz:", ["es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-AR-TomasNeural"])

# 2. Selección de Documento
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")

if not os.path.exists(ruta_docs):
    st.error(f"Carpeta 'documents' no encontrada en: {base_path}")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.warning("La carpeta 'documents' está vacía.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_pdf = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Indexación
MARCADOR = "###"
def get_idx():
    doc = fitz.open(ruta_pdf)
    items = []
    for i, p in enumerate(doc):
        if MARCADOR in p.get_text():
            items.append(f"Capítulo {len(items) + 1}")
    return items if items else ["Sin secciones"]

lista = get_idx()
seleccion = st.sidebar.selectbox("Elige sección:", lista)

# 4. Lógica de Extracción de Texto REAL
def extraer_texto(ruta, indice):
    doc = fitz.open(ruta)
    texto = ""
    contador = 0
    capturando = False
    for pagina in doc:
        txt = pagina.get_text()
        if MARCADOR in txt:
            if contador == indice:
                capturando = True
                txt = txt.split(MARCADOR)[-1]
            else:
                capturando = False
            contador += 1
        if capturando:
            texto += txt
    return texto

# 5. Interfaz de Audio y Reto
if st.button("🔊 ESCUCHAR SECCIÓN"):
    with st.spinner("Generando audio real..."):
        idx_num = lista.index(seleccion)
        texto_real = extraer_texto(ruta_pdf, idx_num)
        temp_file = "temp_audio.mp3"
        
        async def generar_audio(texto, archivo):
            comunicador = edge_tts.Communicate(texto, voz_id)
            await comunicador.save(archivo)
        
        asyncio.run(generar_audio(texto_real, temp_file))
        time.sleep(1) # Espera de seguridad
        
        if os.path.exists(temp_file):
            st.session_state.audio_path = temp_file
        else:
            st.error("Error al generar el archivo de audio.")

# --- Persistencia del Audio y Reto ---
if st.session_
