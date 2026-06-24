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

# BLOQUE DE COLABORACIÓN: Imagen de alto impacto
if os.path.exists("mensaje logo.png"):
    st.image("mensaje logo.png", use_container_width=True)
else:
    st.error("Error: La imagen 'mensaje logo.png' no está en el servidor.")

# QR (Debajo de la imagen)
if os.path.exists("QR.jpeg"):
    st.image("QR.jpeg", width=250, caption="Escanea para colaborar con 10 Bs")
else:
    st.warning("Imagen 'QR.jpeg' no encontrada.")

st.markdown("---")

# Reproductor
st.subheader("🎧 Reproductor de Audio")
if 'last_audio' in st.session_state and st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3")
else:
    st.info("Selecciona un capítulo abajo para comenzar.")

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
    
    # --- ORDENAMIENTO DE BOTONES PARA EVITAR EL DESORDEN EN CELULARES ---
    lista_ordenada = []
    for i, texto in enumerate(secciones):
        # Usamos formato numérico :02d para que 10 sea mayor que 02 y se ordenen bien
        nombre = "Prólogo" if i == 0 else f"Capítulo {i:02d}"
        lista_ordenada.append((nombre, texto))
    
    # Ordenamos alfabéticamente
    lista_ordenada.sort()
    
    cols = st.columns(3) 
    for i, (nombre, texto) in enumerate(lista_ordenada):
        with cols[i % 3]:
            # Convertimos el nombre para mostrarlo bonito (quitando el 0 del 01)
            display_name = nombre.replace("Capítulo 0", "Capítulo ").replace("Capítulo ", "Capítulo ")
            if st.button(f"▶️ {display_name}", key=f"{archivo}_{nombre}", use_container_width=True):
                temp_file = "current_audio.mp3"
                with st.spinner("Generando audio..."):
                    async def gen():
                        comunicador = edge_tts.Communicate(texto[:3500], "es-MX-JorgeNeural")
                        await comunicador.save(temp_file)
                    asyncio.run(gen())
                st.session_state.last_audio = temp_file
                st.rerun()

st.sidebar.write(f"📊 Consultas totales: {st.session_state.visits}")
