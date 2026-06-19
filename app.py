import streamlit as st
import fitz
import edge_tts
import asyncio
import os

st.set_page_config(layout="wide", page_title="Lector Profesional Cloud")
st.title("📚 Lector Profesional - Administrado")

ruta_docs = "documentos"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

if not archivos:
    st.info("No encontré archivos PDF en 'documentos'.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un libro:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Lectura inteligente de bloques (respetando estructura de títulos)
try:
    doc = fitz.open(ruta_completa)
    pag_num = st.sidebar.number_input("Página:", min_value=1, max_value=len(doc), value=1)
    page = doc.load_page(pag_num - 1)
    
    # Obtenemos bloques de texto con su información de formato
    blocks = page.get_text("blocks")
    # Ordenamos los bloques verticalmente
    blocks.sort(key=lambda b: b[1])
    
    texto_final = ""
    for b in blocks:
        # b[4] contiene el texto del bloque
        bloque_texto = b[4].strip()
        
        # Detectamos si es probable que sea un título (bloques cortos y aislados)
        if len(bloque_texto) < 100:
            # Es un título/subtítulo: mantiene sus saltos de línea para pausas
            texto_final += "\n" + bloque_texto + "\n"
        else:
            # Es un párrafo: unimos las líneas para que se lea de corrido
            parrafo_limpio = " ".join(bloque_texto.splitlines())
            texto_final += "\n" + parrafo_limpio + "\n"
    
    st.write(f"### Leyendo: {archivo_seleccionado} - Pág {pag_num}")
    st.write(texto_final[:1000] + "...") 
    
except Exception as e:
    st.error(f"Error al procesar el PDF: {e}")
    st.stop()

# 4. Botón de acción con el nuevo texto procesado
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
            if os.path.exists(temp_file): os.remove(temp_file)
        except Exception as e:
            st.error(f"Error: {e}")
