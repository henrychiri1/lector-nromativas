import streamlit as st

# Configuración de la página (esto mantiene tu diseño actual)
st.set_page_config(page_title="Preparación Ascenso 2026", layout="centered")

# --- BLOQUE SUPERIOR: MANTENEMOS TU IDENTIDAD ---
st.title("📚 Preparación Ascenso 2026")
# Aquí puedes agregar tu imagen del logo/banner si la tenías cargada en el repositorio
# st.image("tu_imagen_banner.png") 

st.markdown("""
### ¡APOYA NUESTRA LABOR EDUCATIVA!
*(Aquí puedes poner el texto de tu banner o el código para la imagen del código QR)*
""")
st.markdown("---")

st.header("🎧 Reproductor de Audio")
st.write("Selecciona un capítulo abajo para comenzar.")

# --- LÓGICA DE LA BIBLIOTECA ---
# Definimos tus archivos organizados por libro
libros = {
    "Neurociencia Neuroaprendizaje.pdf": {
        "Capítulo 1": "URL_AQUI",
        "Capítulo 2": "URL_AQUI",
        # ... añade aquí los enlaces de los fragmentos de este libro
    },
    "REGLAMENTO DE FALTAS Y SANCIONES.pdf": {
        "Capítulo 1": "https://archive.org/download/reglamento-de-faltas-y-sanciones-completo/REGLAMENTO%20DE%20FALTAS%20Y%20SANCIONES_completo.mp3",
    },
    "REGLAMENTO DEL ESCALAFÓN NACIONAL DEL SERVICIO DE EDUCACIÓN.pdf": {
        "Capítulo 1": "https://archive.org/download/reglamento-del-escalafo-n-nacional-del-servicio-de-educacio-n-completo/REGLAMENTO%20DEL%20ESCALAF%C3%93N%20NACIONAL%20DEL%20SERVICIO%20DE%20EDUCACI%C3%93N_completo.mp3",
    }
}

# --- GENERACIÓN DE LA INTERFAZ ---
for nombre_libro, capitulos in libros.items():
    st.subheader(f"📖 {nombre_libro}")
    
    # Creamos columnas para organizar los botones como los tenías
    cols = st.columns(3)
    for i, (nombre_cap, url) in enumerate(capitulos.items()):
        if cols[i % 3].button(nombre_cap):
            st.audio(url)
    st.markdown("---")
