import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso")

# --- CONTADOR DE VISITAS (Interno) ---
VISITS_FILE = "visits.txt"
def get_visits():
    if not os.path.exists(VISITS_FILE): return 0
    with open(VISITS_FILE, "r") as f: return int(f.read())

def increment_visits():
    v = get_visits() + 1
    with open(VISITS_FILE, "w") as f: f.write(str(v))
    return v

# --- UI DE BIENVENIDA ---
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>🎓 Plataforma de Preparación para el Ascenso</h1>
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
    <h3 style='color: #2e7d32;'>Instrucciones:</h3>
    <ul>
    <li>Selecciona el libro y haz clic en cualquier capítulo.</li>
    <li>El audio se cargará automáticamente.</li>
    <li><b>¡Plataforma gratuita!</b> Si deseas apoyarnos, una colaboración voluntaria de 10 Bs nos ayuda a mejorar.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# Lógica de carga automática
if 'last_audio' not in st.session_state: st.session_state.last_audio = None
if 'visits_shown' not in st.session_state:
    st.session_state.visits = increment_visits()
    st.session_state.visits_shown = True

st.sidebar.write(f"📊 Visitas: {st.session_state.visits}")

# --- PROCESAMIENTO ---
ruta_docs = os.path.join(os.path.dirname(__file__), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]

for archivo in archivos:
    st.subheader(f"📖 {archivo}")
    ruta_pdf = os.path.join(ruta_docs, archivo)
    doc = fitz.open(ruta_pdf)
    texto_total = "".join([p.get_text() for p in doc])
    secciones = texto_total.split("###")
    
    for i, texto in enumerate(secciones):
        nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
        if st.button(f"▶️ Reproducir {nombre}", key=f"{archivo}_{i}"):
            # Lógica para detener otros (al recargar, el audio anterior se limpia)
            temp_file = "current_audio.mp3"
            async def gen():
                comunicador = edge_tts.Communicate(texto[:3000], "es-MX-JorgeNeural")
                await comunicador.save(temp_file)
            asyncio.run(gen())
            st.session_state.last_audio = temp_file
            st.rerun()

# Reproducción automática
if st.session_state.last_audio and os.path.exists(st.session_state.last_audio):
    st.audio(st.session_state.last_audio, format="audio/mp3")
    st.info("💡 Tip: Haz clic en los tres puntos del reproductor para cambiar la velocidad.")
