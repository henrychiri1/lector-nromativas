import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS para hacer los botones y textos más amigables (grandes y claros)
st.markdown("""
    <style>
    .stButton>button {
        height: 4em !important;
        width: 100% !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 10px !important;
    }
    h1 { font-size: 2.5em !important; }
    .css-164nlkn { font-size: 1.2em !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Logo en el encabezado
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", width=120)
with col2:
    st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# Instrucciones claras para los colegas
st.info("Bienvenido. Seleccione un documento a la izquierda, use los botones de navegación para cambiar de página y presione el botón 'Leer página'.")

# 2. Configuración de voces
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {
    "México (Jorge)": "es-MX-JorgeNeural",
    "México (Dalia)": "es-MX-DaliaNeural",
    "España (Alvaro)": "es-ES-AlvaroNeural",
    "Colombia (Gonzalo)": "es-CO-GonzaloNeural"
}
voz_seleccionada = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_seleccionada]

# Definir ruta
ruta_docs = "documentos"
if not os.path.exists(ruta_docs):
    st.error("La carpeta 'documentos' no existe.")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.info("No hay archivos PDF en la carpeta.")
    st.stop()

# 3. Selección y Navegación táctil
archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# Gestión de página en memoria (Session State)
if 'pag_num' not in st.session_state:
    st.session_state.pag_num = 1

doc = fitz.open(ruta_completa)
total_paginas = len(doc)

st.sidebar.markdown("### Navegación")
col_prev, col_next = st.sidebar.columns(2)

if col_prev.button("⬅️ Anterior"):
    if st.session_state.pag_num > 1:
        st.session_state.pag_num -= 1

if col_next.button("Siguiente ➡️"):
    if st.session_state.pag_num < total_paginas:
        st.session_state.pag_num += 1

st.sidebar.write(f"### Página actual: {st.session_state.pag_num} de {total_paginas}")

# 4. Procesamiento de texto
page = doc.load_page(st.session_state.pag_num - 1)
blocks = page.get_text("blocks")
blocks.sort(key=lambda b: b[1])

texto_final = ""
for b in blocks:
    bloque_texto = b[4].strip()
    if len(bloque_texto) < 100:
        texto_final += "\n" + bloque_texto + "\n"
    else:
        texto_final += "\n" + " ".join(bloque_texto.splitlines()) + "\n"

st.write(f"### Leyendo: {archivo_seleccionado}")
st.write(texto_final[:800] + "...")

# 5. Botón de Lectura grande
if st.button("🔊 LEER ESTA PÁGINA"):
    with st.spinner("Generando audio..."):
        try:
            temp_file = "temp_audio.mp3"
            async def generar_final():
                comunicador = edge_tts.Communicate(texto_final, voz_id)
                await comunicador.save(temp_file)
            asyncio.run(generar_final())
            
            with open(temp_file, "rb") as f:
                st.audio(f.read(), format="audio/mp3")
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception as e:
            st.error(f"Error: {e}")
