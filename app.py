import streamlit as st
import fitz
import edge_tts
import asyncio
import os
from PIL import Image

st.set_page_config(layout="wide", page_title="Lector Profesional Cloud")
st.title("📚 Lector Profesional - Administrado")

# 1. Buscar PDFs en la carpeta 'documentos'
ruta_docs = "documentos"
if not os.path.exists(ruta_docs):
    os.makedirs(ruta_docs)
    st.error(f"Por favor, crea la carpeta '{ruta_docs}' y pon tus PDFs ahí.")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.info("No encontré PDFs en la carpeta 'documentos'.")
    st.stop()

# 2. Selección de documento
archivo_seleccionado = st.sidebar.selectbox("Selecciona un libro:", archivos)
ruta_pdf = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Lógica de lectura
doc = fitz.open(ruta_pdf)
pag_num = st.sidebar.number_input("Página:", min_value=1, max_value=len(doc), value=1)
page = doc.load_page(pag_num - 1)
texto = " ".join(page.get_text().splitlines())

st.write(f"### Leyendo: {archivo_seleccionado} - Pág {pag_num}")
st.write(texto[:1000] + "...") 

# 4. Audio con Streamlit nativo (más estable)
if st.button("🔊 Leer página"):
    with st.spinner("Generando narración profesional..."):
        async def generar():
            comm = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
            await comm.save("temp.mp3")
        asyncio.run(generar())
        st.audio("temp.mp3")
        st.download_button("Descargar MP3", data=open("temp.mp3", "rb"), file_name="capitulo.mp3")
