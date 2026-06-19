import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración inicial de la página
st.set_page_config(layout="wide", page_title="Lector Profesional Cloud")
st.title("📚 Lector Profesional - Administrado")

# 1. Definir ruta y verificar carpeta
ruta_docs = "documentos"

if not os.path.exists(ruta_docs):
    st.error(f"La carpeta '{ruta_docs}' no existe en el repositorio.")
    st.stop()

# Listar archivos PDF
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]

if not archivos:
    st.info("No encontré archivos PDF dentro de la carpeta 'documentos'.")
    st.stop()

# 2. Selección de documento
archivo_seleccionado = st.sidebar.selectbox("Selecciona un libro:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Lectura del PDF
try:
    doc = fitz.open(ruta_completa)
    pag_num = st.sidebar.number_input("Página:", min_value=1, max_value=len(doc), value=1)
    page = doc.load_page(pag_num - 1)
    texto = " ".join(page.get_text().splitlines())
    
    st.write(f"### Leyendo: {archivo_seleccionado} - Pág {pag_num}")
    st.write(texto[:1000] + "...") 
except Exception as e:
    st.error(f"Error al abrir el PDF: {e}")
    st.stop()

# 4. Botón de acción - Versión robusta para la nube
if st.button("🔊 Leer página"):
    if not texto.strip():
        st.warning("La página seleccionada no contiene texto legible.")
    else:
        with st.spinner("Generando narración (esto puede tardar unos segundos)..."):
            try:
                temp_file = "temp_audio.mp3"
                
                # Función para guardar audio
                async def generar_final():
                    comunicador = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
                    await comunicador.save(temp_file)
                
                asyncio.run(generar_final())
                
                # Leer y mostrar
                with open(temp_file, "rb") as f:
                    audio_bytes = f.read()
                
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("Descargar MP3", data=audio_bytes, file_name="lectura.mp3", mime="audio/mp3")
                
                # Limpieza
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            except Exception as e:
                st.error(f"Error técnico al generar audio: {e}")
