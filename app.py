import os
import edge_tts
import asyncio
import fitz  # Importa PyMuPDF (instálalo con: pip install pymupdf edge-tts)

# 1. Carpeta donde están tus PDFs
CARPETA_PDFS = "./documentos" 
# 2. Carpeta donde se guardarán los audios (la que luego subirás a GitHub)
CARPETA_AUDIOS = "./audios"

if not os.path.exists(CARPETA_AUDIOS):
    os.makedirs(CARPETA_AUDIOS)

async def generar():
    for archivo in os.listdir(CARPETA_PDFS):
        if archivo.endswith(".pdf"):
            print(f"Procesando: {archivo}...")
            doc = fitz.open(os.path.join(CARPETA_PDFS, archivo))
            
            # Unimos todo el texto del PDF
            texto = ""
            for pagina in doc:
                texto += pagina.get_text()
            
            # Generamos el audio
            nombre_salida = os.path.join(CARPETA_AUDIOS, archivo.replace(".pdf", ".mp3"))
            comunicador = edge_tts.Communicate(texto, "es-MX-JorgeNeural")
            await comunicador.save(nombre_salida)
            print(f"Guardado en: {nombre_salida}")

if __name__ == "__main__":
    asyncio.run(generar())
