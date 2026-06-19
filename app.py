import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# 1. Logo en el encabezado (Opción 2: Logo junto al título)
col1, col2 = st.columns([1, 6]) # Columna pequeña para logo, grande para título
with col1:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", width=120)
    else:
        st.warning("Logo no encontrado.")
with col2:
    st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# Definir ruta y verificar carpeta
ruta_docs = "documentos"
if not os.path.exists(ruta_docs):
    st.error(f"La carpeta '{ruta_docs}' no existe.")
    st.stop()

# Listar archivos PDF
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.info("No encontré archivos PDF en la carpeta 'documentos'.")
    st.stop()

# 2. Selección de documento
archivo_seleccionado = st.sidebar.selectbox("Selecciona un libro:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Lectura inteligente de bloques
try:
    doc = fitz.open(ruta_completa)
    pag_num = st.sidebar.number_input("Página:", min_value=1, max_value=len(doc), value=1)
    page = doc.load_page(pag_num - 1)
    
    blocks = page.get_text("blocks")
    blocks.sort(key=lambda b: b[1])
    
    texto_final = ""
    for b in blocks:
        bloque_texto = b[4].strip()
        if len(bloque_texto) < 100:
            texto_final += "\n" + bloque_texto + "\n"
        else:
            parrafo_limpio = " ".join(bloque_texto.splitlines())
            texto_final += "\n" + parrafo_limpio + "\n"
    
    st.write(f"### Leyendo: {archivo_seleccionado} - Pág {pag_num}")
    st.write(texto_final[:1000] + "...") 
    
except Exception as e:
    st.error(f"Error al procesar el PDF: {e}")
    st.stop()

# 4. Botón de acción robusto
if st.button("🔊 Leer página"):
    with st.spinner("Generando narración profesional..."):
        try:
            temp_file = "temp_audio.mp3"
            async def generar_final():
                comunicador = edge_tts.Communicate(texto_final, "es-MX-JorgeNeural")
                await comunicador.save(temp_file)
            
            asyncio.run(generar_final())
            
            with open(temp_file, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button("Descargar MP3", data=audio_bytes, file_name="lectura.mp3", mime="audio/mp3")
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            st.error(f"Error técnico: {e}")
