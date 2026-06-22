import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import time

st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""<style>.stButton>button { height: 4em !important; width: 100% !important; }</style>""", unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# Estado
if 'audio_path' not in st.session_state: st.session_state.audio_path = None
if 'puntos' not in st.session_state: st.session_state.puntos = 0

# Configuración
ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []
archivo_sel = st.sidebar.selectbox("Documento:", archivos) if archivos else None

if archivo_sel:
    ruta_pdf = os.path.join(ruta_docs, archivo_sel)
    
    # Lógica de extracción infalible
    def extraer_todo_el_texto(ruta):
        doc = fitz.open(ruta)
        return "\n".join([p.get_text() for p in doc])

    texto_completo = extraer_todo_el_texto(ruta_pdf)
    # Dividimos por el marcador, pero si no hay, devolvemos el texto completo
    partes = texto_completo.split("###")
    
    # Crear índice dinámico
    opciones_indice = [f"Sección {i}" for i in range(len(partes))]
    seleccion = st.sidebar.selectbox("Elige sección:", opciones_indice)
    idx_num = int(seleccion.split(" ")[1])

    # Interfaz
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔊 ESCUCHAR Y EVALUAR"):
            texto_a_leer = partes[idx_num] if len(partes) > idx_num else texto_completo
            temp_file = "temp_audio.mp3"
            
            async def generar():
                comunicador = edge_tts.Communicate(texto_a_leer[:2000], "es-MX-JorgeNeural") # Limitado para evitar bloqueos
                await comunicador.save(temp_file)
            
            asyncio.run(generar())
            time.sleep(1)
            st.session_state.audio_path = temp_file

        if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
            st.audio(st.session_state.audio_path, format="audio/mp3")

    with col2:
        st.subheader("🎯 Reto de 1 minuto")
        with st.form("quiz"):
            respuesta = st.radio("¿Qué tema principal se trató?", ["Normativa", "Procedimiento", "Sanción"])
            if st.form_submit_button("Verificar"):
                st.session_state.puntos += 10
                st.success(f"¡Correcto! Puntos: {st.session_state.puntos}")

else:
    st.error("No se encontraron PDFs en la carpeta 'documents'.")
