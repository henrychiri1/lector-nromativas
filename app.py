import streamlit as st
import os
import streamlit.components.v1 as components

# --- METADATOS PARA LA VISTA PREVIA EN WHATSAPP ---
metadatos = """
<head>
    <meta property="og:title" content="Preparación Ascenso 2026 - F.D.M.E.R.C." />
    <meta property="og:description" content="Accede a los audios de estudio para tu ascenso de categoría." />
    <meta property="og:image" content="https://ascensodecategoria.streamlit.app/~/+/media/cd872257da279b732bc171798951cc54.jpg" />
</head>
"""
components.html(metadatos, height=0)

# Configuración de página
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- LÓGICA DE CONTADOR ---
VISITS_FILE = "visits.txt"
def increment_visits():
    v = 0
    if os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, "r") as f:
            try: v = int(f.read())
            except: v = 0
    with open(VISITS_FILE, "w") as f: f.write(str(v + 1))
    return v + 1

if 'visits' not in st.session_state:
    st.session_state.visits = increment_visits()

# --- INTERFAZ GRÁFICA ORIGINAL ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

# Imagen portada
if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)

# Sección QR y Logo lateral
col1, col2 = st.columns(2)
with col1:
    if os.path.exists("QR.jpeg"):
        st.image("QR.jpeg", caption="Escanea para colaborar con 10 Bs", use_container_width=True)
with col2:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", use_container_width=True)
        st.markdown("<h4 style='text-align: center; color: #1f77b4;'>Con el aval oficial de la F.D.M.E.R.C.</h4>", unsafe_allow_html=True)

st.markdown("---")

st.header("🎧 Reproductor de Audio")
st.write("Selecciona un audio completo abajo para comenzar.")

# --- DICCIONARIO DE AUDIOS ---
audios = {
    "Neurociencia Neuroaprendizaje completo": "https://archive.org/download/neurociencia-neuroaprendizaje-completo/Neurociencia%20Neuroaprendizaje_completo.mp3",
    "REGLAMENTO DE FALTAS Y SANCIONES completo": "https://archive.org/download/reglamento-de-faltas-y-sanciones-completo/REGLAMENTO%20DE%20FALTAS%20Y%20SANCIONES_completo.mp3",
    "REGLAMENTO DEL ESCALAFÓN NACIONAL DEL SERVICIO DE EDUCACIÓN completo": "https://archive.org/download/reglamento-del-escalafo-n-nacional-del-servicio-de-educacio-n-completo/REGLAMENTO%20DEL%20ESCALAF%C3%93N%20NACIONAL%20DEL%20SERVICIO%20DE%20EDUCACI%C3%93N_completo.mp3",
    "Ley de las personas con discapacidad completo": "https://archive.org/download/ley-de-las-personas-con-discapacidad-completo/Ley%20de%20las%20personas%20con%20discapacidad_completo.mp3",
    "Estilos de aprendizaje completo": "https://archive.org/download/estilos-de-aprendizaje-completo/estilos%20de%20aprendizaje_completo.mp3",
    "Diseño, desarrollo e innovación del currículum completo": "https://archive.org/download/diseno-desarrollo-e-innovacion-del-curriculum-completo_202606/Dise%C3%B1o%2C%20desarrollo%20e%20innovaci%C3%B3n%20del%20curr%C3%ADculum_completo.mp3"
}

# --- GENERACIÓN DE BOTONES CON REPRODUCTOR ABAJO ---
for titulo, url in audios.items():
    st.subheader(f"📖 {titulo}")
    # Cada botón es único gracias al key
    if st.button("Reproducir Audio", key=f"btn_{titulo}", use_container_width=True):
        st.audio(url, format="audio/mp3")
    st.markdown("---")

# Contador en barra lateral
st.sidebar.write(f"📊 Consultas totales: {st.session_state.visits}")
