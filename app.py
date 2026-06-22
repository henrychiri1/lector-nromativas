import streamlit as st
import fitz
import edge_tts
import asyncio
import os
import time

# ... (Configuración de página y estilos se mantienen igual) ...

# 3. Indexación basada ÚNICAMENTE en ###
def obtener_indice(ruta_pdf):
    doc = fitz.open(ruta_pdf)
    indices = []
    for i, pagina in enumerate(doc):
        # Buscamos cuantas veces aparece el marcador en la página
        # Si aparece, añadimos un ítem al índice por cada ocurrencia
        texto_pag = pagina.get_text()
        if MARCADOR in texto_pag:
            # Contamos cuántos marcadores hay en esta página
            cantidad = texto_pag.count(MARCADOR)
            for _ in range(cantidad):
                indices.append(f"Sección {len(indices) + 1}")
    return indices if indices else ["Sin secciones marcadas (falta ###)"]

# 4. Extracción de Texto basada ÚNICAMENTE en ###
def extraer_texto(ruta, indice_seleccionado):
    doc = fitz.open(ruta)
    # Unimos todo el texto del documento para procesarlo como un bloque lineal
    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()
    
    # Dividimos el texto entero usando el marcador como separador
    partes = texto_completo.split(MARCADOR)
    
    # La parte 0 es lo que está antes del primer ###
    # Las partes siguientes son el contenido de cada sección
    if indice_seleccionado + 1 < len(partes):
        return partes[indice_seleccionado + 1]
    return "Contenido no encontrado."

# ... (El resto del código se mantiene igual) ...
