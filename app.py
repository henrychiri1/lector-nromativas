import streamlit as st
import fitz
import edge_tts
import asyncio
import os

# Configuración de página
st.set_page_config(layout="wide", page_title="Plataforma de Ascenso")

# --- INTERFAZ PRINCIPAL CON TEXTO FORZADO A COLOR OSCURO ---
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>📚 Preparación Ascenso 2026</h1>", unsafe_allow_html=True)

# BLOQUE DE COLABORACIÓN: Color de texto forzado a negro (#000000)
st.markdown("""
    <div style='background-color: #fdf2f2; padding: 20px; border-radius: 10px; border: 2px solid #ffcccc; margin-bottom: 20px; color: #000000;'>
        <h3 style='color: #d32f2f; margin-top: 0;'>🤝 ¡Apoya nuestra labor educativa!</h3>
        <p style='font-size: 15px; color: #000000;'>
            Creemos que la educación debe ser accesible para todos. Si este recurso te ayuda, 
            <b>una colaboración voluntaria de 10 Bs</b> nos permite seguir mejorando esta plataforma.
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- CARGA SEGURA DE IMAGEN ---
# Verificamos que el archivo existe antes de intentar mostrarlo
if os.path.exists("QR.jpeg"):
    st.image("QR.jpeg", width=250, caption="Escanea para colaborar")
else:
    st.warning("No se encontró el archivo QR.jpeg. Por favor, verifica que esté en la carpeta raíz.")

st.markdown("---")
# ... (resto de tu código de botones sigue igual)
