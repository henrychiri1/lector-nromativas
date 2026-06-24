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
    with open(VISITS_FILE, "r") as f: 
        try: return int(f.read())
        except: return 0

def increment_visits():
    v = get_visits() + 1
    with open(VISITS_FILE, "w") as f: f.write(str(v))
    return v

if 'visits' not in st.session_state:
    st.session_state.visits = increment_visits()

# --- BARRA LATERAL FIJA ---
with st.sidebar:
    st.header("🎧 Panel de Reproducción")
    if 'last_audio' in st.session_state and st.session_state.last_audio:
        st.audio(st.session_state.last_audio, format="audio/mp3")
        st.caption("Tip: Usa los 3 puntos del reproductor para cambiar la velocidad.")
    else:
        st.info("Selecciona un capítulo para comenzar.")
    
    st.markdown("---")
    st.subheader("🤝 Un esfuerzo compartido")
    st.write("Creemos firmemente que la educación debe ser accesible para todos. Con una colaboración voluntaria de 10 Bs, nos ayudas a fortalecer esta comunidad y a construir mejores herramientas para el magisterio.")
    st.image("QR.jpeg", use_container_width=True)
    st.markdown("---")
    st.write(f"📊 Consultas realizadas: {st.session_state.visits}")

# --- CUERPO PRINCIPAL ---
st.markdown("<h1 style='color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

# Instrucciones
st.success("Instrucciones: Selecciona el libro y haz clic en cualquier capítulo. El audio se cargará automáticamente.")

ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

# Contenedor con scroll para los libros
with st.container(height=600):
    for archivo in archivos:
        st.subheader(f"📖 {archivo}")
        ruta_pdf = os.path.join(ruta_docs, archivo)
        doc = fitz.open(ruta_pdf)
        texto_total = "".join([p.get_text() for p in doc])
        secciones = texto_total.split("###")
        
        for i, texto in enumerate(secciones):
            # Lógica de nombre: Prólogo para el primero, Capítulo X para los demás
            nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
            if st.button(f"▶️ {nombre}", key=f"{archivo}_{i}"):
                temp_file = "current_audio.mp3"
                with st.spinner("Generando audio..."):
                    async def gen():
                        # Generación robusta
                        comunicador = edge_tts.Communicate(texto[:3500], "es-MX-JorgeNeural")
                        await comunicador.save(temp_file)
                    asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()
