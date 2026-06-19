import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import io

st.set_page_config(layout="wide", page_title="Lector Profesional Cloud")
st.title("📚 Lector Profesional - Administrado")

# 1. Ajustamos la ruta para que busque dentro de la carpeta 'documentos'
ruta_docs = "documentos"

# Verificamos que la carpeta exista
if not os.path.exists(ruta_docs):
    st.error(f"La carpeta '{ruta_docs}' no existe en el repositorio.")
    st.stop()

# Listamos solo los archivos .pdf dentro de la carpeta 'documentos'
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]

if not archivos:
    st.info("No encontré archivos PDF dentro de la carpeta 'documentos'.")
    st.stop()

# 2. Selección de documento
archivo_seleccionado = st.sidebar.selectbox("Selecciona un libro:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Lógica de lectura
doc = fitz.open(ruta_completa)
pag_num = st.sidebar.number_input("Página:", min_value=1, max_value=len(doc), value=1)
page = doc.load_page(pag_num - 1)
texto = " ".join(page.get_text().splitlines())

st.write(f"### Leyendo: {archivo_seleccionado} - Pág {pag_num}")
st.write(texto[:1000] + "...") 

# 4. Botón de acción
if st.button("🔊 Leer página"):
    with st.spinner("Generando narración profesional..."):
        try:
            audio_buffer = io.BytesIO()
            async def generar_audio(texto_a_leer):
                comm = edge_tts.Communicate(texto_a_leer, "es-MX-JorgeNeural")
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.write(chunk["data"])
            
            asyncio.run(generar_audio(texto))
            st.audio(audio_buffer.getvalue(), format="audio/mp3")
            st.download_button("Descargar MP3", data=audio_buffer.getvalue(), file_name="capitulo.mp3", mime="audio/mp3")
        except Exception as e:
            st.error(f"Error al generar el audio: {e}")
