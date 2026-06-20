import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json

st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional con Índice Permanente")

# Configuración
marcador = st.sidebar.text_input("Marcador de inicio:", "###")
ruta_docs = "documentos"
archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
archivo_seleccionado = st.sidebar.selectbox("Selecciona documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)
ruta_indice = ruta_completa + ".idx"

# 1. Sistema de Indexación (Se ejecuta solo si es necesario)
def obtener_o_crear_indice(ruta_pdf, marcador):
    if os.path.exists(ruta_indice):
        with open(ruta_indice, "r") as f:
            return json.load(f)
    
    # Si no existe, escaneamos (solo se hace la primera vez)
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        if marcador in pagina.get_text():
            indices.append(f"Sección {len(indices) + 1} (Pág {i+1})")
    
    with open(ruta_indice, "w") as f:
        json.dump(indices, f)
    return indices

lista_marcadores = obtener_o_crear_indice(ruta_completa, marcador)

# 2. Selector
seleccion = st.sidebar.selectbox("Elige la sección:", lista_marcadores)
idx_seleccionado = lista_marcadores.index(seleccion)

# 3. Lógica de Lectura
if st.button(f"🔊 LEER {seleccion.upper()}"):
    with st.spinner("Cargando sección desde índice..."):
        try:
            doc = fitz.open(ruta_completa)
            texto_total = ""
            capturando = False
            contador = 0
            
            for pagina in doc:
                texto_pag = pagina.get_text()
                if marcador in texto_pag:
                    if contador == idx_seleccionado:
                        capturando = True
                        texto_pag = texto_pag.split(marcador)[-1]
                    else:
                        capturando = False
                    contador += 1
                
                if capturando:
                    texto_total += texto_pag
            
            # Generación de audio
            temp_file = "temp_audio.mp3"
            async def generar():
                comunicador = edge_tts.Communicate(texto_total, "es-MX-JorgeNeural")
                await comunicador.save(temp_file)
            asyncio.run(generar())
            
            st.audio(temp_file, format="audio/mp3")
            if os.path.exists(temp_file): os.remove(temp_file)
        except Exception as e:
            st.error(f"Error: {e}")
