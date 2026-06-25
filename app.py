import streamlit as st
import os
import base64
import zipfile
import io

# --- CONFIGURACIÓN ---
st.set_page_config(layout="centered", page_title="Plataforma FDMERC")

CLAVE_ADMIN = "mi_clave_secreta_2026" 
query_params = st.query_params
es_admin = query_params.get("admin") == CLAVE_ADMIN

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Preparacion Ascenso 2026</h1>", unsafe_allow_html=True)

if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)

st.markdown("---")

# --- LÓGICA DE DIAGNÓSTICO Y LISTADO ---
ruta_audios = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")

# Diagnóstico visual para ti (solo visible para admin)
if es_admin:
    st.sidebar.info(f"Ruta detectada: {ruta_audios}")
    if os.path.exists(ruta_audios):
        archivos_totales = os.listdir(ruta_audios)
        st.sidebar.success(f"Archivos en carpeta: {len(archivos_totales)}")
    else:
        st.sidebar.error("La carpeta 'audios' NO existe en el servidor.")

# --- LÓGICA DE REPRODUCTOR ---
st.subheader("Reproductor de Audio")

if 'audio_a_reproducir' not in st.session_state:
    st.session_state.audio_a_reproducir = None

if st.session_state.audio_a_reproducir and os.path.exists(st.session_state.audio_a_reproducir):
    with open(st.session_state.audio_a_reproducir, "rb") as f:
        b64_audio = base64.b64encode(f.read()).decode()
    
    st.markdown(f'''
    <audio controls controlsList="nodownload" style="width: 100%;">
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
    </audio>
    ''', unsafe_html=True)
else:
    st.info("Selecciona un audio de la lista.")

# --- LISTA DE REPRODUCCIÓN ---
if os.path.exists(ruta_audios):
    archivos = [f for f in os.listdir(ruta_audios) if f.endswith('.mp3')]
    if not archivos:
        st.warning("La carpeta 'audios' está vacía o no contiene archivos .mp3.")
    else:
        for arch in sorted(archivos):
            if st.button(f"Reproducir: {arch.replace('.mp3', '')}", key=arch):
                st.session_state.audio_a_reproducir = os.path.join(ruta_audios, arch)
                st.rerun()

# --- PANEL ADMIN ---
if es_admin:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Panel de Administrador")
    if os.path.exists(ruta_audios):
        if st.sidebar.button("📦 Comprimir y Descargar biblioteca"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for arch in os.listdir(ruta_audios):
                    if arch.endswith(".mp3"):
                        zf.write(os.path.join(ruta_audios, arch), arch)
            
            # Solo descarga si el zip tiene contenido
            if zip_buffer.tell() > 8:
                st.sidebar.download_button("✅ Descargar ZIP", data=zip_buffer.getvalue(), 
                                           file_name="biblioteca.zip", mime="application/zip")
            else:
                st.sidebar.error("El ZIP está vacío. Verifica que haya archivos .mp3 en la carpeta.")
