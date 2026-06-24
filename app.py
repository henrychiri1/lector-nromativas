import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración de página
st.set_page_config(layout="wide", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- CONTADOR DE VISITAS ---
VISITS_FILE = "visits.txt"
def get_visits():
    if not os.path.exists(VISITS_FILE): return 0
    with open(VISITS_FILE, "r") as f: return int(f.read())

def increment_visits():
    v = get_visits() + 1
    with open(VISITS_FILE, "w") as f: f.write(str(v))
    return v

if 'visits' not in st.session_state:
    st.session_state.visits = increment_visits()

# --- BARRA LATERAL FIJA (Audio + Colaboración) ---
with st.sidebar:
    st.header("🎧 Panel de Reproducción")
    if 'last_audio' in st.session_state and st.session_state.last_audio:
        st.audio(st.session_state.last_audio, format="audio/mp3")
        st.caption("Tip: Usa los 3 puntos del reproductor para cambiar la velocidad.")
    else:
        st.info("Selecciona un capítulo para comenzar.")
    
    st.markdown("---")
    st.subheader("🤝 Apoya nuestro proyecto")
    st.write("Creemos firmemente que la educación debe ser accesible para todos. Con una colaboración voluntaria de 10 Bs, nos ayudas a fortalecer esta comunidad.")
    st.image("QR.jpeg", use_container_width=True) # Asegúrate que el archivo esté en la carpeta
    st.markdown("---")
    st.write(f"📊 Consultas: {st.session_state.visits}")

# --- CUERPO PRINCIPAL (Lista de Libros) ---
st.markdown("<h1 style='color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]

# Contenedor con scroll para los libros
with st.container(height=600):
    for archivo in archivos:
        st.subheader(f"📖 {archivo}")
        ruta_pdf = os.path.join(ruta_docs, archivo)
        doc = fitz.open(ruta_pdf)
        texto_total = "".join([p.get_text() for p in doc])
        secciones = texto_total.split("###")
        
        for i, texto in enumerate(secciones):
            nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
            if st.button(f"▶️ {nombre}", key=f"{archivo}_{i}"):
                temp_file = "current_audio.mp3"
                async def gen():
                    comunicador = edge_tts.Communicate(texto[:3000], "es-MX-JorgeNeural")
                    await comunicador.save(temp_file)
                asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()
