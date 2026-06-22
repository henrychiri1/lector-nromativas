def extraer_texto(ruta, indice_seleccionado):
    doc = fitz.open(ruta)
    texto_total = ""
    capturando = False
    contador = 0
    
    # Lista de posibles títulos de capítulos para detección automática
    # Esto elimina la dependencia exclusiva de ###
    for pagina in doc:
        texto_pag = pagina.get_text()
        
        # Detecta si esta página contiene el inicio de un capítulo
        # Buscamos la estructura "CAPÍTULO" o tu marcador "###"
        es_inicio_capitulo = ("CAPÍTULO" in texto_pag.upper() or MARCADOR in texto_pag)
        
        if es_inicio_capitulo:
            if contador == indice_seleccionado:
                capturando = True
                # Limpiamos el texto para que empiece desde el título del capítulo
                texto_pag = texto_pag.split("CAPÍTULO" if "CAPÍTULO" in texto_pag.upper() else MARCADOR)[-1]
            else:
                # Si encontramos un NUEVO capítulo, dejamos de capturar el anterior
                capturando = False
                contador += 1
        
        if capturando:
            texto_total += texto_pag + "\n" # Asegura que los artículos no se peguen
            
    return texto_total
