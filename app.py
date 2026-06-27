import streamlit as st

# Configuración de página
st.set_page_config(page_title="Preparación Ascenso 2026", layout="centered")

# --- TÍTULO Y BANNER ---
st.title("📚 Preparación Ascenso 2026")
# Si tienes imágenes (QR, logo), asegúrate de que estén en la carpeta de tu repositorio
# st.image("tu_qr.png") 
st.markdown("---")

st.header("🎧 Reproductor de Audio")
st.write("Selecciona un capítulo abajo para comenzar.")

# --- DICCIONARIO DE AUDIOS ---
# Aquí están los 6 enlaces definitivos que me proporcionaste
libros = {
    "Neurociencia Neuroaprendizaje.pdf": {
        "Capítulo 1": "https://archive.org/download/neurociencia-neuroaprendizaje-completo/Neurociencia%20Neuroaprendizaje_completo.mp3",
    },
    "REGLAMENTO DE FALTAS Y SANCIONES.pdf": {
        "Capítulo 1": "https://archive.org/download/reglamento-de-faltas-y-sanciones-completo/REGLAMENTO%20DE%20FALTAS%20Y%20SANCIONES_completo.mp3",
    },
    "REGLAMENTO DEL ESCALAFÓN NACIONAL DEL SERVICIO DE EDUCACIÓN.pdf": {
        "Capítulo 1": "https://archive.org/download/reglamento-del-escalafo-n-nacional-del-servicio-de-educacio-n-completo/REGLAMENTO%20DEL%20ESCALAF%C3%93N%20NACIONAL%20DEL%20SERVICIO%20DE%20EDUCACI%C3%93N_completo.mp3",
    },
    "Ley de las personas con discapacidad": {
        "Capítulo 1": "https://archive.org/download/ley-de-las-personas-con-discapacidad-completo/Ley%20de%20las%20personas%20con%20discapacidad_completo.mp3",
    },
    "Estilos de aprendizaje": {
        "Capítulo 1": "https://archive.org/download/estilos-de-aprendizaje-completo/estilos%20de%20aprendizaje_completo.mp3",
    },
    "Diseño, desarrollo e innovación del currículum": {
        "Capítulo 1": "https://archive.org/download/diseno-desarrollo-e-innovacion-del-curriculum-completo_202606/Dise%C3%B1o%2C%20desarrollo%20e%20innovaci%C3%B3n%20del%20curr%C3%ADculum_completo.mp3",
    }
}

# --- GENERADOR DE BOTONES ---
for nombre_libro, capitulos in libros.items():
    st.subheader(f"📖 {nombre_libro}")
    
    # Organizamos en 3 columnas como en tu imagen
    cols = st.columns(3)
    
    for i, (nombre_cap, url) in enumerate(capitulos.items()):
        # Se añade un 'key' único para evitar el error de duplicados
        unique_key = f"{nombre_libro}_{nombre_cap}"
        
        if cols[i % 3].button(nombre_cap, key=unique_key):
            st.audio(url)
            
    st.markdown("---")
