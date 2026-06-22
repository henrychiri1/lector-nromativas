import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import json

# Configuración inicial
st.set_page_config(layout="wide", page_title="Lector Profesional F.D.M.E.R.C.")

# Estilos CSS
st.markdown("""
    <style>
    .stButton>button { height: 4em !important; width: 100% !important; font-size: 20px !important; font-weight: bold !important; border-radius: 10px !important; }
    .stSelectbox div[data-baseweb="select"] input { caret-color: transparent !important; pointer-events: none !important; }
    .stSelectbox div[data-baseweb="select"] { cursor: pointer !important; }
    </style>
    """, unsafe_ = True)

st.title("📚 Lector Profesional - F.D.M.E.R.C.")

# --- NUEVO: Módulo de Aprendizaje Activo (Lógica) ---
def mostrar_reto_aprendizaje():
    st.subheader("🎯 Reto de 1 minuto: ¡Pon a prueba tu memoria!")
    st.info("Después de escuchar, responde para consolidar el conocimiento.")
    
    # Aquí puedes luego conectar con una IA para generar preguntas dinámicas
    respuesta = st.radio("¿Cuál es el artículo principal tratado en esta sección?", 
                         ["Art. 12 - Clasificación", "Art. 22 - Escalafón", "Art. 45 - Faltas"])
    
    if st.button("Verificar Respuesta"):
        if respuesta == "Art. 22 - Escalafón":
            st.success("¡Excelente! Has retenido la información clave.")
        else:
            st.error("Casi. Te sugiero repasar el minuto 05:00 del audio.")

# [Mantiene tu lógica original de configuración de voz, rutas e indexación...]
# ... (Tu código existente de la sección 1 a la 4 queda intacto) ...

# 5. Lógica de Lectura
if st.button(f"🔊 ESCUCHAR SECCIÓN"):
    if seleccion == "Sin secciones marcadas":
        st.warning("Este documento no contiene marcadores.")
    else:
        with st.spinner("Procesando audio..."):
            try:
                # ... (Tu lógica de extracción de texto original) ...
                
                # Generación de audio (Tu lógica original)
                # ... 
                
                st.audio(temp_file, format="audio/mp3")
                
                # --- NUEVO: Llamada al módulo de aprendizaje ---
                st.markdown("---")
                mostrar_reto_aprendizaje()
                
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    
            except Exception as e:
                st.error(f"Error técnico: {e}")

st.write("---")
