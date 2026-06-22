import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import time

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# 1. Configuración de Voz
voz_id = st.sidebar.selectbox("Elige una voz:", ["es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-AR-TomasNeural"])

# 2. Selección de Documento
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
archivo_sel = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_pdf = os.path.join(ruta_docs, archivo_sel)

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
def extraer_texto_seccion(ruta, indice_seleccionado):
    doc = fitz.open(ruta)
    texto_seccion = ""
    contador = 0
    capturando = False
    
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
            texto_seccion += texto_pag
    return texto_seccion

# 5. Lógica de Reproducción
if st.button("🔊 ESCUCHAR SECCIÓN"):
    with st.spinner("Generando audio real..."):
        # Extraer texto real del PDF
        idx_num = lista.index(seleccion)
        texto_real = extraer_texto_seccion(ruta_pdf, idx_num)
        
        temp_file = "temp_audio.mp3"
        
        # Generar audio con el texto real
        async def generar_audio(texto, archivo_salida):
            comunicador = edge_tts.Communicate(texto, voz_id)
            await comunicador.save(archivo_salida)
        
        asyncio.run(generar_audio(texto_real, temp_file))
        time.sleep(1)
        
        if os.path.exists(temp_file):
            st.audio(temp_file, format="audio/mp3")
            st.subheader("🎯 Reto de 1 minuto")
            st.info("Responde para consolidar tu conocimiento.")
