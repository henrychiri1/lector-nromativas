import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import io # Añade esta librería

# ... (mantén tu código de selección de archivos igual) ...

if st.button("🔊 Leer página"):
    with st.spinner("Generando narración profesional..."):
        # Usamos un buffer de memoria en lugar de un archivo en disco
        audio_buffer = io.BytesIO()
        
        async def generar():
            comm = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
            # Guardamos directamente en el buffer
            async for chunk in comm.stream():
                if chunk["type"] == "audio":
                    audio_buffer.write(chunk["data"])
        
        asyncio.run(generar())
        
        # Reproducir desde memoria
        st.audio(audio_buffer.getvalue(), format="audio/mp3")
        
        # Botón de descarga
        st.download_button("Descargar MP3", data=audio_buffer.getvalue(), file_name="capitulo.mp3", mime="audio/mp3")
