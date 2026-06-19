import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS para botones grandes y legibilidad
st.markdown("""
    <style>
    .stButton>button {
        height: 4em !important;
        width: 100% !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    h1 { font-size: 2.2em !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Logo
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", width=120)
with col2:
    st.title("📚 Lector Profesional - F.D.M.E.R.C.")

st.info("Seleccione el capítulo a la izquierda y presione 'LEER CAPÍTULO COMPLETO' para escuchar.")

# 2. Índice del Escalafón
capitulos = {
    "Prólogo": (1, 1),
    "Capítulo 1 - Concepto, Finalidades y Funciones": (2, 3),
    "Capítulo 2 - Ingreso en el Servicio de Educación": (4, 5),
    "Capítulo 3 - Inscripción en el Escalafón": (6, 7),
    "Capítulo 4 - Jerarquías y Categorías": (8, 9),
    "Capítulo 5 - Calificación de Méritos": (10, 13),
    "Capítulo 6 - Promociones de Categoría": (14, 16),
    "Capítulo 7 - Comisiones Calificadoras": (17, 18),
    "Capítulo 8 - Ascensos de Jerarquía": (19, 20),
    "Capítulo 9 - Provisión de Cargos Docentes": (21, 21),
    "Capítulo 10 - Acumulación de Cargos Docentes": (22, 24),
    "Capítulo 11 - Inamovilidad Docente y Cesantías": (25, 25),
    "Capítulo 12 - Comprobación del Tiempo de Servicios": (26, 26),
    "Disposiciones Generales y Transitorias": (27, 28),
    "Cierre y Firmas Oficiales": (28, 28)
}

# 3. Configuración de voces y archivo
st.sidebar.subheader("⚙️ Configuración")
voces = {
    "México (Jorge)": "es-MX-JorgeNeural",
    "México (Dalia)": "es-MX-DaliaNeural",
    "España (Alvaro)": "es-ES-AlvaroNeural",
    "Colombia (Gonzalo)": "es-CO-GonzaloNeural"
}
voz_seleccionada = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_seleccionada]

ruta_docs = "documentos"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
archivo_seleccionado = st.sidebar.selectbox("Selecciona el documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 4. Navegación por Capítulos
st.sidebar.markdown("---")
st.sidebar.subheader("📖 Índice del Escalafón")
capitulo_seleccionado = st.sidebar.selectbox("Selecciona un capítulo:", list(capitulos.keys()))
inicio, fin = capitulos[capitulo_seleccionado]

doc = fitz.open(ruta_completa)

# 5. Lógica de Lectura
if st.button("🔊 LEER CAPÍTULO COMPLETO"):
    with st.spinner(f"Preparando {capitulo_seleccionado}..."):
        try:
            texto_completo = ""
            for p in range(inicio, fin + 1):
                page = doc.load_page(p - 1)
                texto_completo += page.get_text()
            
            temp_file = "temp_audio.mp3"
            async def generar():
                comunicador = edge_tts.Communicate(texto_completo, voz_id)
                await comunicador.save(temp_file)
            asyncio.run(generar())
            
            with open(temp_file, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            st.error(f"Error técnico: {e}")

# Muestra el rango actual para referencia
st.write(f"### Estás en: {capitulo_seleccionado}")
st.write(f"*(Páginas {inicio} a {fin} del documento)*")
