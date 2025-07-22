def create_prompt(context: dict) -> str:
    files = context['structure']['files']
    txt_structure = "\n".join([f"- {a['route']}" for a in files])
    summaries = context.get('summaries', [])
    text_summary = "\n".join([f"{r['route']}:\n{r['resume']}\n" for r in summaries])

    return f"""
    Eres un experto en documentación de software. Genera un archivo README.md profesional con esta información:

    Lenguaje: {context['language']}
    Dependencias: {context.get('dependencies', 'No hay dependencias detectadas')}

    Estructura del proyecto:
    {txt_structure}

    Resúmenes semánticos de files clave:
    {text_summary}

    Incluye:
    - Título del proyecto
    - Descripción
    - Cómo instalar
    - Cómo ejecutar
    - Créditos (si aplica)
    - Licencia (si aplica)
    """
