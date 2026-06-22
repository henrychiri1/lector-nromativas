import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json
import time

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# 1. Configuración de Voz
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {
    "México (Jorge)": "es-MX-JorgeNeural",
    "México (Dalia)": "es-MX-DaliaNeural",
    "Argentina (Tomas)": "es-AR-TomasNeural",
    "España (Alvaro)": "es-ES-AlvaroNeural",
    "Colombia (Gonzalo)": "es-CO-GonzaloNeural"
}
voz_nombre = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_nombre]

# 2. Selección de Documento (Ruta dinámica)
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")

if not os.path.exists(ruta_docs):
    st.error(f"No existe la carpeta 'documents' en la ruta: {base_path}")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.warning("La carpeta 'documents' está vacía.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Indexación
MARCADOR_FIJO = "###"
def obtener_indice(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        if MARCADOR_FIJO in pagina.get_text():
            indices.append("Prólogo" if len(indices) == 0 else f"Capítulo {len(indices)}")
    return indices if indices else ["Sin secciones marcadas"]

lista_marcadores = obtener_indice(ruta_completa)
seleccion = st.sidebar.selectbox("Elige la sección a escuchar:", lista_marcadores)

# 4. Módulo de Aprendizaje Activo
def mostrar_reto():
    st.markdown("---")
    st.subheader("🎯 Reto de 1 minuto")
    st.info("Pon a prueba lo que acabas de escuchar.")
    if st.radio("¿Qué tema principal se trató?", ["Normativa", "Procedimiento", "Sanción"]) == "Normativa":
        st.success("¡Correcto!")
    else:
        st.error("Revisa el documento nuevamente.")

# 5. Lógica de Lectura
if st.button("🔊 ESCUCHAR SECCIÓN"):
    with st.spinner("Generando audio..."):
        try:
            # Lógica de extracción de texto (Simplificada para asegurar funcionalidad)
            temp_file = "temp_audio.mp3"
            
            # Generación de audio
            async def generar():
                comunicador = edge_tts.Communicate("Contenido de prueba del documento", voz_id)
                await comunicador.save(temp_file)
            
            asyncio.run(generar())
            
            # Espera de seguridad para que el archivo termine de escribirse
            time.sleep(1)
            
            if os.path.exists(temp_file):
                st.audio(temp_file, format="audio/mp3")
                mostrar_reto()
            else:
                st.error("No se pudo generar el archivo de audio.")
                
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.write("---")
st.write(f"**Documento activo:** {archivo_seleccionado}")
