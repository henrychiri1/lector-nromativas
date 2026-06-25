import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import base64

# Configuración de página
st.set_page_config(layout="centered", page_title="Plataforma de Ascenso F.D.M.E.R.C.")

# --- LÓGICA DE ADMINISTRADOR ---
# Cambia 'mi_clave_secreta_2026' por tu clave privada
CLAVE_ADMIN = "mi_clave_secreta_2026" 
query_params = st.query_params
es_admin = query_params.get("admin") == CLAVE_ADMIN

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

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)

# Sección QR y AVAL
col1, col2 = st.columns(2)
with col1:
    if os.path.exists("QR.jpeg"):
        st.image("QR.jpeg", caption="Escanea para colaborar con 10 Bs", use_container_width=True)
with col2:
    if os.path.exists("logo.jpeg"):
        st.image("logo.jpeg", use_container_width=True)
        st.markdown("<h4 style='text-align: center; color: #1f77b4;'>Con el aval oficial de la F.D.M.E.R.C.</h4>", unsafe_allow_html=True)

st.markdown("---")

# --- REPRODUCTOR PERSONALIZADO SIN DESCARGA ---
st.subheader("🎧 Reproductor de Audio")
if 'last_audio' in st.session_state and st.session_state.last_audio:
    with open(st.session_state.last_audio, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    
    html_audio = f'''
    <audio controls controlsList="nodownload" style="width: 100%;">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    '''
    st.markdown(html_audio, unsafe_allow_html=True)

    # BOTÓN DE DESCARGA (SOLO PARA ADMIN)
    if es_admin:
        with open(st.session_state.last_audio, "rb") as file:
            st.download_button(
                label="📥 DESCARGAR AUDIO (Solo Admin)",
                data=file,
                file_name="audio_ascenso.mp3",
                mime="audio/mp3"
            )
else:
    st.info("Selecciona un capítulo abajo para comenzar.")

st.markdown("---")

# Lista de libros
ruta_docs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')] if os.path.exists(ruta_docs) else []

for archivo in archivos:
    st.subheader(f"📖 {archivo}")
    ruta_pdf = os.path.join(ruta_docs, archivo)
    doc = fitz.open(ruta_pdf)
    texto_total = "".join([p.get_text() for p in doc])
    secciones = texto_total.split("###")
    lista_ordenada = sorted([(f"Capítulo {i:02d}" if i > 0 else "Prólogo", t) for i, t in enumerate(secciones)])
    
    cols = st.columns(3) 
    for i, (nombre, texto) in enumerate(lista_ordenada):
        with cols[i % 3]:
            if st.button(f"▶️ {nombre}", key=f"{archivo}_{nombre}", use_container_width=True):
                temp_file = "current_audio.mp3"
                with st.spinner("Generando audio..."):
                    async def gen():
                        comunicador = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
                        await comunicador.save(temp_file)
                    asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()

st.sidebar.write(f"📊 Consultas: {st.session_state.visits}")
