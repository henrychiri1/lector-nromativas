import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración de página
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- LÓGICA DE CONTADOR ---
VISITS_FILE = "visits.txt"
def increment_visits():
    v = 0
    if os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, "r") as f:
            try: v = int(f.read())
            except: v = 0
    with open(VISITS_FILE, "w") as f: f.write(str(v + 1))
    return v + 1

if 'visits' not in st.session_state:
    st.session_state.visits = increment_visits()

# --- INTERFAZ PRINCIPAL ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

# BLOQUE DE COLABORACIÓN (Diseño forzado para modo oscuro/claro)
st.markdown("""
    <div style='background-color: #fdf2f2; padding: 20px; border-radius: 10px; border: 2px solid #ffcccc; margin-bottom: 20px; color: #000000 !important;'>
        <h3 style='color: #d32f2f; margin-top: 0;'>🤝 ¡Apoya nuestra labor educativa!</h3>
        <p style='font-size: 15px; color: #000000 !important;'>
            Creemos que la educación debe ser accesible para todos. Si este recurso te ayuda, 
            <b>una colaboración voluntaria de 10 Bs</b> nos permite seguir mejorando esta plataforma para que más maestros alcancen su ascenso.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Carga de imagen con validación de existencia
if os.path.exists("QR.jpeg"):
    st.image("QR.jpeg", width=250, caption="Escanea para colaborar")
else:
    st.error("Error: La imagen 'QR.jpeg' no está en el servidor. Súbela a la carpeta raíz.")

st.markdown("---")

# Reproductor (Siempre visible)
st.subheader("🎧 Reproductor de Audio")
if 'last_audio' in st.session_state and st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")
else:
    st.info("Selecciona un capítulo abajo para comenzar la reproducción.")

st.markdown("---")

# Lista de libros en rejilla
ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

for archivo in archivos:
    st.subheader(f"📖 {archivo}")
    ruta_pdf = os.path.join(ruta_docs, archivo)
    doc = fitz.open(ruta_pdf)
    texto_total = "".join([p.get_text() for p in doc])
    secciones = texto_total.split("###")
    
    cols = st.columns(3) 
    for i, texto in enumerate(secciones):
        nombre = "Prólogo" if i == 0 else f"Capítulo {i}"
        with cols[i % 3]:
            if st.button(f"▶️ {nombre}", key=f"{archivo}_{i}", use_container_width=True):
                temp_file = "current_audio.mp3"
                with st.spinner("Generando audio..."):
                    async def gen():
                        comunicador = edge_tts.Communicate(texto[:3500], "es-MX-JorgeNeural")
                        await comunicador.save(temp_file)
                    asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()

st.sidebar.write(f"📊 Consultas totales: {st.session_state.visits}")
