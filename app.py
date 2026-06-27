import streamlit as st

# Configuración de página
st.set_page_config(page_title="Preparación Ascenso 2026", layout="centered")

# --- TÍTULO Y ELEMENTOS GRÁFICOS ---
st.title("📚 Preparación Ascenso 2026")

# Reinsertamos tus elementos gráficos (Asegúrate de que los archivos estén en tu repo)
# st.image("tu_banner_principal.png") 
# st.image("tu_qr.png") 
# st.image("tu_logo_fdmerc.png")

st.markdown("---")

st.header("🎧 Reproductor de Audio")
st.write("Selecciona un audio completo abajo para comenzar.")

# --- DICCIONARIO DE AUDIOS COMPLETOS ---
libros = {
    "Neurociencia Neuroaprendizaje completo": "https://archive.org/download/neurociencia-neuroaprendizaje-completo/Neurociencia%20Neuroaprendizaje_completo.mp3",
    "REGLAMENTO DE FALTAS Y SANCIONES completo": "https://archive.org/download/reglamento-de-faltas-y-sanciones-completo/REGLAMENTO%20DE%20FALTAS%20Y%20SANCIONES_completo.mp3",
    "REGLAMENTO DEL ESCALAFÓN NACIONAL DEL SERVICIO DE EDUCACIÓN completo": "https://archive.org/download/reglamento-del-escalafo-n-nacional-del-servicio-de-educacio-n-completo/REGLAMENTO%20DEL%20ESCALAF%C3%93N%20NACIONAL%20DEL%20SERVICIO%20DE%20EDUCACI%C3%93N_completo.mp3",
    "Ley de las personas con discapacidad completo": "https://archive.org/download/ley-de-las-personas-con-discapacidad-completo/Ley%20de%20las%20personas%20con%20discapacidad_completo.mp3",
    "Estilos de aprendizaje completo": "https://archive.org/download/estilos-de-aprendizaje-completo/estilos%20de%20aprendizaje_completo.mp3",
    "Diseño, desarrollo e innovación del currículum completo": "https://archive.org/download/diseno-desarrollo-e-innovacion-del-curriculum-completo_202606/Dise%C3%B1o%2C%20desarrollo%20e%20innovaci%C3%B3n%20del%20curr%C3%ADculum_completo.mp3"
}

# --- GENERADOR DE BOTONES ---
# Ahora cada botón carga directamente el audio completo
for titulo, url in libros.items():
    # Usamos el título completo como etiqueta del botón y como llave única
    if st.button(titulo, key=titulo):
        st.audio(url)
    st.markdown("---")
