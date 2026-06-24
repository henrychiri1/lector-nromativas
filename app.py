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

# Reproductor arriba
st.subheader("🎧 Reproductor de Audio")
if 'last_audio' in st.session_state and st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")
else:
    st.info("Selecciona un capítulo para comenzar.")

# Área de Colaboración
with st.expander("🤝 ¿Cómo apoyar este proyecto?"):
    st.write("Con tu colaboración de 10 Bs, ayudamos a más maestros a alcanzar sus metas.")
    st.image("QR.jpeg", width=250)
    st.write(f"📊 Visitas: {st.session_state.visits}")

st.markdown("---")

# Lista de libros con columnas (Horizontal)
ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

for archivo in archivos:
    st.subheader(f"📖 {archivo}")
    ruta_pdf = os.path.join(ruta_docs, archivo)
    doc = fitz.open(ruta_pdf)
    texto_total = "".join([p.get_text() for p in doc])
    secciones = texto_total.split("###")
    
    # Creamos una rejilla de 3 columnas
    cols = st.columns(3) 
    
    for i, texto in enumerate(secciones):
        nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
        
        # Asignamos el botón a una de las 3 columnas usando el módulo
        with cols[i % 3]:
            if st.button(f"▶️ {nombre}", key=f"{archivo}_{i}", use_container_width=True):
                temp_file = "current_audio.mp3"
                with st.spinner("Cargando..."):
                    async def gen():
                        comunicador = edge_tts.Communicate(texto[:3500], "es-MX-JorgeNeural")
                        await comunicador.save(temp_file)
                    asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()
