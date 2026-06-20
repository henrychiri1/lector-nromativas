import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos para asegurar que todo sea amigable y bloqueado para edición manual
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    /* Evitar que el usuario sienta que puede escribir en los selectores */
    .stSelectbox div[data-baseweb="select"] { cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# 1. Configuración de Voz (Restaurada)
st.sidebar.subheader("⚙️ Configuración de Audio")
voces = {
    "México (Jorge)": "es-MX-JorgeNeural",
    "México (Dalia)": "es-MX-DaliaNeural",
    "Argentina (Tomas)": "es-AR-TomasNeural",
    "España (Alvaro)": "es-ES-AlvaroNeural",
    "Colombia (Gonzalo)": "es-CO-GonzaloNeural"
}
voz_nombre = st.sidebar.selectbox("Elige una voz:", list(voces.keys()))
voz_id = voces[voz_nombre]

# 2. Selección de Documento
ruta_docs = "documentos"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.error("No hay documentos en la carpeta 'documentos'.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)
ruta_indice = ruta_completa + ".idx"

# Marcador fijo para el sistema (ya no es un text_input donde pueden escribir)
MARCADOR_FIJO = "###" 

# 3. Sistema de Indexación (Automático y sin intervención del usuario)
def obtener_indice(ruta_pdf):
    if os.path.exists(ruta_indice):
        with open(ruta_indice, "r") as f:
            return json.load(f)
    
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        if MARCADOR_FIJO in pagina.get_text():
            indices.append(f"Sección {len(indices) + 1} (Pág {i+1})")
    
    if not indices:
        indices = ["Sin secciones marcadas"]
    
    with open(ruta_indice, "w") as f:
        json.dump(indices, f)
    return indices

lista_marcadores = obtener_indice(ruta_completa)

# 4. Selector de Sección (Bloqueado para escritura)
seleccion = st.sidebar.selectbox("Elige la sección a escuchar:", lista_marcadores)

# 5. Lógica de Lectura
if st.button(f"🔊 ESCUCHAR SECCIÓN"):
    if seleccion == "Sin secciones marcadas":
        st.warning("Este documento no contiene marcadores.")
    else:
        with st.spinner("Procesando audio..."):
            try:
                doc = fitz.open(ruta_completa)
                idx_seleccionado = lista_marcadores.index(seleccion)
                texto_total = ""
                capturando = False
                contador = 0
                
                for pagina in doc:
                    texto_pag = pagina.get_text()
                    if MARCADOR_FIJO in texto_pag:
                        if contador == idx_seleccionado:
                            capturando = True
                            texto_pag = texto_pag.split(MARCADOR_FIJO)[-1]
                        else:
                            capturando = False
                        contador += 1
                    
                    if capturando:
                        texto_total += texto_pag
                
                temp_file = "temp_audio.mp3"
                async def generar():
                    comunicador = edge_tts.Communicate(texto_total, voz_id)
                    await comunicador.save(temp_file)
                asyncio.run(generar())
                
                st.audio(temp_file, format="audio/mp3")
                if os.path.exists(temp_file): os.remove(temp_file)
            except Exception as e:
                st.error(f"Error técnico: {e}")

st.write("---")
st.write(f"**Documento activo:** {archivo_seleccionado}")
