if st.button("🔊 Leer página"):
    with st.spinner("Generando narración profesional..."):
        try:
            # Usamos un buffer de memoria
            audio_buffer = io.BytesIO()
            
            # Definimos la función pasando el texto como argumento explícito
            async def generar_audio(texto_a_leer):
                comm = edge_tts.Communicate(texto_a_leer, "es-MX-JorgeNeural")
                async for chunk in comm.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.write(chunk["data"])
            
            # Ejecutamos el bucle de forma segura
            asyncio.run(generar_audio(texto))
            
            # Reproducir desde memoria
            st.audio(audio_buffer.getvalue(), format="audio/mp3")
            
            # Botón de descarga
            st.download_button(
                label="Descargar MP3", 
                data=audio_buffer.getvalue(), 
                file_name="capitulo.mp3", 
                mime="audio/mp3"
            )
        except Exception as e:
            st.error(f"Ocurrió un error al generar el audio: {e}")
