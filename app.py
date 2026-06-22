import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS - CORREGIDO: ahora es 'unsafe_allow_html=True'
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# --- Módulo de Aprendizaje Activo ---
def mostrar_reto_aprendizaje():
    st.subheader("🎯 Reto de 1 minuto")
    st.info("Responde para reforzar tu memoria:")
    respuesta = st.radio("¿Qué concepto clave se abordó?", ["Opción A", "Opción B", "Opción C"])
    if st.button("Verificar"):
        st.success("¡Muy bien!")

# --- Lógica de Archivos ---
ruta_docs = "documents" # Asegúrate de que la carpeta se llame 'documents' en tu proyecto

if not os.path.exists(ruta_docs):
    st.error(f"No encuentro la carpeta '{ruta_docs}'.")
    st.stop()

archivos = [f for f in os.listdir(ruta_docs) if f.endswith('.pdf')]
if not archivos:
    st.warning("No hay archivos PDF en la carpeta.")
    st.stop()

archivo_seleccionado = st.sidebar.selectbox("Selecciona un documento:", archivos)
ruta_completa = os.path.join(ruta_docs, archivo_seleccionado)
MARCADOR_FIJO = "###" 

# --- Indexación ---
def obtener_indice(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    indices = ["Prólogo"]
    for i, pagina in enumerate(doc):
        if MARCADOR_FIJO in pagina.get_text():
            indices.append(f"Capítulo {len(indices)}")
    return indices

lista_marcadores = obtener_indice(ruta_completa)
seleccion = st.sidebar.selectbox("Elige la sección:", lista_marcadores)

# --- Lógica de Reproducción ---
if st.button("🔊 ESCUCHAR SECCIÓN"):
    with st.spinner("Procesando..."):
        try:
            # Aquí va tu lógica de extracción de texto
            temp_file = "temp_audio.mp3"
            
            # (Asegúrate de que tu lógica de edge-tts guarde aquí)
            
            if os.path.exists(temp_file):
                st.audio(temp_file, format="audio/mp3")
                mostrar_reto_aprendizaje() # Llamamos al reto aquí
            else:
                st.error("No se generó el audio.")
        except Exception as e:
            st.error(f"Error: {e}")
