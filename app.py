import streamlit as st
import os
import base64
import zipfile
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="centered", page_title="Plataforma FDMERC")

# --- LÓGICA DE ADMINISTRADOR ---
CLAVE_ADMIN = "mi_clave_secreta_2026" 
query_params = st.query_params
es_admin = query_params.get("admin") == CLAVE_ADMIN

# --- INTERFAZ ---
# Título limpio sin caracteres complejos
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Preparacion Ascenso 2026</h1>", unsafe_allow_html=True)

if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)

st.markdown("---")

# --- LÓGICA DE REPRODUCTOR (Mejorada para ocultar descarga) ---
st.subheader("Reproductor de Audio")

if 'audio_a_reproducir' not in st.session_state:
    st.session_state.audio_a_reproducir = None

if st.session_state.audio_a_reproducir and os.path.exists(st.session_state.audio_a_reproducir):
    with open(st.session_state.audio_a_reproducir, "rb") as f:
        audio_data = f.read()
        b64_audio = base64.b64encode(audio_data).decode()
    
    # HTML puro para el reproductor con controles limitados
    html_player = f'''
    <audio controls controlsList="nodownload" style="width: 100%;">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>
    '''
    st.markdown(html_player, unsafe_allow_html=True)

    # Botón exclusivo para el administrador
    if es_admin:
        with open(st.session_state.audio_a_reproducir, "rb") as file:
            st.download_button("Descargar este audio (Admin)", data=file, 
                               file_name=os.path.basename(st.session_state.audio_a_reproducir))
else:
    st.info("Selecciona un audio de la lista.")

st.markdown("---")

# --- LISTA DE AUDIOS ---
ruta_audios = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")

if os.path.exists(ruta_audios):
    archivos = [f for f in os.listdir(ruta_audios) if f.endswith('.mp3')]
    for arch in sorted(archivos):
        if st.button(f"Reproducir: {arch.replace('.mp3', '')}", key=arch):
            st.session_state.audio_a_reproducir = os.path.join(ruta_audios, arch)
            st.rerun()
else:
    st.warning("Carpeta 'audios' no encontrada.")

# --- PANEL ADMIN ---
if es_admin:
    st.sidebar.subheader("Panel Admin")
    if st.sidebar.button("Comprimir biblioteca"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for arch in os.listdir(ruta_audios):
                if arch.endswith(".mp3"):
                    zf.write(os.path.join(ruta_audios, arch), arch)
        st.sidebar.download_button("Descargar ZIP", data=zip_buffer.getvalue(), 
                                   file_name="biblioteca.zip", mime="application/zip")
