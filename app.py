import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import time

# Configuración de página
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# --- Inicialización de Estado ---
if 'puntos' not in st.session_state: st.session_state.puntos = 0
if 'audio_path' not in st.session_state: st.session_state.audio_path = None

# 1. Configuración de Voz
voz_id = st.sidebar.selectbox("Elige una voz:", ["es-MX-JorgeNeural", "es-MX-DaliaNeural", "es-AR-TomasNeural"])

# 2. Selección de Documento
base_path = os.path.dirname(os.path.abspath(__file__))
ruta_docs = os.path.join(base_path, "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

if not archivos:
    st.error("No hay archivos PDF en la carpeta 'documents'.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_pdf = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Indexación basada en ### (Prólogo + Capítulos)
def obtener_indice(ruta):
    doc = fitz.open(ruta)
    texto_total = "".join([p.get_text() for p in doc])
    partes = texto_total.split("###")
    indices = ["Prólogo"] + [f"Capítulo {i}" for i in range(1, len(partes))]
    return indices, partes

lista_nombres, lista_texto = obtener_indice(ruta_pdf)
seleccion = st.sidebar.selectbox("Elige la sección a escuchar:", lista_nombres)
idx_seleccionado = lista_nombres.index(seleccion)

# 4. Generación de Audio Segmentada (Anti-corte)
def generar_audio_robusto(texto, archivo_salida):
    # Dividir en bloques de 2000 caracteres
    segmentos = [texto[i:i+2000] for i in range(0, len(texto), 2000)]
    archivos_temp = []
    
    for i, seg in enumerate(segmentos):
        temp_seg = f"temp_seg_{i}.mp3"
        comunicador = edge_tts.Communicate(seg, voz_id)
        asyncio.run(comunicador.save(temp_seg))
        archivos_temp.append(temp_seg)
    
    # Unir archivos binarios
    with open(archivo_salida, 'wb') as outfile:
        for fname in archivos_temp:
            with open(fname, 'rb') as infile:
                outfile.write(infile.read())
            os.remove(fname)

# 5. Interfaz Principal
col_audio, col_quiz = st.columns([1, 1])

with col_audio:
    if st.button("🔊 ESCUCHAR Y EVALUAR"):
        with st.spinner("Generando audio completo..."):
            texto_a_leer = lista_texto[idx_seleccionado]
            temp_file = os.path.join(base_path, "final_audio.mp3")
            generar_audio_robusto(texto_a_leer, temp_file)
            st.session_state.audio_path = temp_file

    if st.session_state.audio_path and os.path.exists(st.session_state.audio_path):
        st.audio(st.session_state.audio_path, format="audio/mp3")

with col_quiz:
    st.subheader("🏆 Tablero de Desafío")
    st.metric("Puntuación acumulada", st.session_state.puntos)
    st.markdown("---")
    
    with st.form("quiz_form"):
        eleccion = st.radio("¿Qué tema principal se trató en esta sección?", ["Normativa", "Procedimiento", "Sanción"])
        if st.form_submit_button("Verificar respuesta"):
            if eleccion == "Normativa":
                st.session_state.puntos += 10
                st.success("¡Correcto! +10 puntos")
                st.balloons()
            else:
                st.error("Incorrecto. Intenta nuevamente.")

st.write("---")
st.write(f"**Documento activo:** {archivo_seleccionado}")
