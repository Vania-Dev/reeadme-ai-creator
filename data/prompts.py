def create_prompt(context: dict) -> str:
    files = context['structure']['files']
    txt_structure = "\n".join([f"- {a['route']}" for a in files])
    summaries = context.get('summaries', [])
    text_summary = "\n".join([f"{r['route']}:\n{r['resume']}\n" for r in summaries])

    return f"""
You are a senior software documentation specialist. Based on the following project information, generate a high-quality, professional `README.md` file in Markdown format.

Use the following reference structure as inspiration for the format, tone, and section ordering:

- Project logo and badges at the top
- Centralized project title and description
- Table of contents with collapsible sections
- Sections:
  1. 🏷️ Título del Proyecto
  2. 📖 Acerca del Proyecto
     - Propósito, objetivos, utilidad
  3. 🔧 Construido Con
     - Lenguaje y tecnologías
  4. 🎬 Lista de Videos (si aplica)
  5. ⚙️ Comienza a Usarlo
     - Prerequisitos
     - Instalación
  6. 📁 Descripción de Archivos (opcional si aplica)
  7. 🙌 Contribución
     - Guía paso a paso
  8. 📄 Licencia
  9. 📞 Contacto

Project language: {context['language']}
Detected dependencies: {context.get('dependencies', 'No se encontraron dependencias')}

Project structure:
{txt_structure}

Semantic summaries of key files:
{text_summary}

Instructions:

- Write the entire README in Spanish.
- Use Markdown formatting for a public open-source repository.
- Use emojis in section headers (just like the original).
- Include code blocks, bullet points, and links where appropriate.
- If applicable, add badges, logos or header images at the top using Markdown syntax.
- Be concise, helpful, and professional.

The result should look like a polished, human-written README file for an open-source Python project.
"""
