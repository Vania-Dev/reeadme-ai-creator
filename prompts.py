def construir_prompt(contexto: dict) -> str:
    archivos = contexto['estructura']['archivos']
    estructura_txt = "\n".join([f"- {a['ruta']}" for a in archivos])
    resumenes = contexto.get('resumenes', [])
    resumen_texto = "\n".join([f"{r['ruta']}:\n{r['resumen']}\n" for r in resumenes])

    return f"""
    Eres un experto en documentación de software. Genera un archivo README.md profesional con esta información:

    Lenguaje: {contexto['lenguaje']}
    Dependencias: {contexto.get('dependencias', 'No detectadas')}

    Estructura del proyecto:
    {estructura_txt}

    Resúmenes semánticos de archivos clave:
    {resumen_texto}

    Incluye:
    - Título del proyecto
    - Descripción
    - Cómo instalar
    - Cómo ejecutar
    - Créditos (si aplica)
    - Licencia (si aplica)
    """
