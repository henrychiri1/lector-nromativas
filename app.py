import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración de página
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- CONTADOR DE VISITAS ---
VISITS_FILE = "visits.txt"
def get_visits():
    if not os.path.exists(VISITS_FILE): return 0
    with open(VISITS_FILE, "r") as f: 
        try: return int(f.read())
        except: return 0

def increment_visits():
    v = get_visits() + 1
    with open(VISITS_FILE, "w") as f: f.write(str(v))
    return v

if 'visits' not in st.session_state:
    st.session_state.visits = increment_visits()

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

# 1. Reproductor en el centro y arriba
st.subheader("🎧 Reproductor de Audio")
if 'last_audio' in st.session_state and st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")
else:
    st.info("Selecciona un capítulo abajo para cargar el audio.")

# 2. Área de Colaboración (Visible y clara)
with st.expander("🤝 ¿Cómo apoyar este proyecto? (Haz clic aquí)"):
    st.write("Creemos en una educación accesible. Con una colaboración voluntaria de 10 Bs, nos ayudas a mejorar.")
    st.image("QR.jpeg", width=250)
    st.write(f"📊 Consultas realizadas: {st.session_state.visits}")

st.markdown("---")

# 3. Lista de libros
ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

st.subheader("📖 Selecciona un capítulo para escuchar:")
for archivo in archivos:
    st.write(f"**{archivo}**")
    ruta_pdf = os.path.join(ruta_docs, archivo)
    doc = fitz.open(ruta_pdf)
    texto_total = "".join([p.get_text() for p in doc])
    secciones = texto_total.split("###")
    
    # Creamos botones más grandes y legibles
    for i, texto in enumerate(secciones):
        nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
        if st.button(f"▶️ {nombre}", key=f"{archivo}_{i}"):
            temp_file = "current_audio.mp3"
            with st.spinner("Cargando audio..."):
                async def gen():
                    comunicador = edge_tts.Communicate(texto[:3500], "es-MX-JorgeNeural")
                    await comunicador.save(temp_file)
                asyncio.run(gen())
            st.session_state.last_audio = temp_file
            st.rerun()
