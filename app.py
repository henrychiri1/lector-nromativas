import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos para accesibilidad
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    h1 { font-size: 2.2em !important; }
    </style>
    """, unsafe_allow_html=True)

# 1. Encabezado
col1, col2 = st.columns([1, 6])
with col1:
    if os.path.exists("logo.jpeg"): st.image("logo.jpeg", width=120)
with col2:
    st.title("📚 Lector Profesional - F.D.M.E.R.C.")

st.info("Escriba el nombre del capítulo o sección (ej: 'Capítulo 1') y presione 'LEER' para procesar automáticamente.")

# 2. Configuración
st.sidebar.subheader("⚙️ Configuración")
voces = {
    "México (Jorge)": "es-MX-JorgeNeural",
    "México (Dalia)": "es-MX-DaliaNeural",
    "Argentina (Tomas)": "es-AR-TomasNeural",
    "España (Alvaro)": "es-ES-AlvaroNeural",
    "Colombia (Gonzalo)": "es-CO-GonzaloNeural"
}
voz_seleccionada = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_seleccionada]

ruta_docs = "documentos"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
archivo_seleccionado = st.sidebar.selectbox("Selecciona documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)

# 3. Buscador Inteligente
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Buscar Capítulo")
titulo_busqueda = st.sidebar.text_input("Nombre del capítulo:", "Capítulo 1")

# 4. Lógica de Lectura Universal
if st.button("🔊 LEER ESTE CAPÍTULO"):
    with st.spinner("Buscando y procesando contenido..."):
        try:
            doc = fitz.open(ruta_completa)
            texto_encontrado = ""
            encontrado = False
            
            for pagina in doc:
                texto_pagina = pagina.get_text()
                
                # Si ya empezamos a leer, buscamos el fin (otro encabezado)
                if encontrado:
                    # Aquí el sistema detecta si hay un nuevo capítulo para detenerse
                    # Buscamos patrones comunes de capítulos
                    if "CAPÍTULO" in texto_pagina.upper() and titulo_busqueda.upper() not in texto_pagina.upper():
                        break
                    texto_encontrado += texto_pagina
                
                # Buscar inicio
                elif titulo_busqueda.upper() in texto_pagina.upper():
                    encontrado = True
                    partes = texto_pagina.split(next((s for s in texto_pagina.splitlines() if titulo_busqueda.upper() in s.upper()), texto_pagina))
                    texto_encontrado += partes[-1] if len(partes) > 1 else texto_pagina

            if not texto_encontrado:
                st.warning("No pude encontrar ese capítulo. Asegúrese de que el nombre esté escrito igual que en el documento.")
            else:
                temp_file = "temp_audio.mp3"
                async def generar():
                    comunicador = edge_tts.Communicate(texto_encontrado, voz_id)
                    await comunicador.save(temp_file)
                asyncio.run(generar())
                
                with open(temp_file, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
                if os.path.exists(temp_file): os.remove(temp_file)
        
        except Exception as e:
            st.error(f"Error técnico: {e}")

st.write("---")
st.write(f"**Documento activo:** {archivo_seleccionado}")
