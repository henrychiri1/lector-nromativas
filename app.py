import streamlit as st
import os
import base64
import zipfile
import io

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- LÓGICA DE ADMINISTRADOR ---
# Cambia 'mi_clave_secreta_2026' por la que prefieras
CLAVE_ADMIN = "mi_clave_secreta_2026" 
query_params = st.query_params
es_admin = query_params.get("admin") == CLAVE_ADMIN

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_html=True)

if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)

# Sección QR y AVAL
col1, col2 = st.columns(2)
with col1:
    if os.path.exists("QR.jpeg"):
        st.image("QR.jpeg", caption="Escanea para colaborar", use_container_width=True)
with col2:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", use_container_width=True)
        st.markdown("<h4 style='text-align: center; color: #1f77b4;'>Aval oficial F.D.M.E.R.C.</h4>", unsafe_html=True)

st.markdown("---")

# --- LÓGICA DE REPRODUCTOR (Optimizado) ---
st.subheader("🎧 Reproductor de Audio")

if 'audio_a_reproducir' not in st.session_state:
    st.session_state.audio_a_reproducir = None

# Solo intentamos leer si hay algo en el estado y el archivo realmente existe
if st.session_state.audio_a_reproducir and os.path.exists(st.session_state.audio_a_reproducir):
    with open(st.session_state.audio_a_reproducir, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    
    # Reproductor HTML (nodownload oculta la descarga para usuarios normales)
    st.markdown(f'''
        <audio controls controlsList="nodownload" style="width: 100%;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    ''', unsafe_html=True)

    # Botón de descarga solo visible para el Admin
    if es_admin:
        with open(st.session_state.audio_a_reproducir, "rb") as file:
            st.download_button("📥 Descargar este audio (Admin)", data=file, 
                               file_name=os.path.basename(st.session_state.audio_a_reproducir))
else:
    st.info("Selecciona un capítulo de la lista inferior para comenzar.")

st.markdown("---")

# --- LISTA DE AUDIOS (CON PROTECCIÓN DE ERROR) ---
ruta_audios = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios")

if os.path.exists(ruta_audios):
    # Obtenemos lista de archivos mp3
    archivos_mp3 = sorted([f for f in os.listdir(ruta_audios) if f.endswith('.mp3')])
    
    if archivos_mp3:
        st.write("### Selecciona el contenido:")
        cols = st.columns(3)
        for i, archivo in enumerate(archivos_mp3):
            with cols[i % 3]:
                if st.button(f"▶️ {archivo.replace('.mp3', '')}", use_container_width=True):
                    st.session_state.audio_a_reproducir = os.path.join(ruta_audios, archivo)
                    st.rerun()
    else:
        st.warning("La carpeta 'audios' está vacía. Sube archivos .mp3 a GitHub.")
else:
    st.error("⚠️ La carpeta 'audios' no existe en el servidor. Por favor, asegúrate de subir la carpeta 'audios' con contenido a tu repositorio de GitHub.")

# --- PANEL DE ADMINISTRADOR (BARRA LATERAL) ---
if es_admin:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Panel de Administrador")
    
    if st.sidebar.button("📦 Comprimir TODOS los audios"):
        if os.path.exists(ruta_audios):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zf:
                for archivo in os.listdir(ruta_audios):
                    if archivo.endswith(".mp3"):
                        zf.write(os.path.join(ruta_audios, archivo), archivo)
            
            st.sidebar.download_button(
                label="✅ Descargar ZIP (Biblioteca Completa)",
                data=zip_buffer.getvalue(),
                file_name="todos_los_audios.zip",
                mime="application/zip"
            )
        else:
            st.sidebar.error("No se encontró la carpeta 'audios' para comprimir.")
