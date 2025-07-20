from pathlib import Path

from pathlib import Path

EXCLUDED_DIRS = {".venv", "__pycache__", ".git", ".pytest_cache"}
EXCLUDED_FILES = {".env", ".gitignore", ".DS_Store"}

def explorar_directorio(path: str) -> dict:
    p = Path(path)

    archivos_info = []
    carpetas = set()

    for file in p.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in file.parts):
            continue
        if file.is_file() and file.name in EXCLUDED_FILES:
            continue
        if file.is_file() and file.name.startswith("."):
            continue

        if file.is_file():
            try:
                content = file.read_text(encoding="utf-8", errors="ignore")
                archivos_info.append({
                    "ruta": str(file.relative_to(p)),
                    "nombre": file.name,
                    "contenido": content[:1000]  # Limitar para no sobrecargar el prompt
                })
            except Exception as e:
                archivos_info.append({
                    "ruta": str(file.relative_to(p)),
                    "nombre": file.name,
                    "contenido": f"(No se pudo leer el archivo: {e})"
                })

        elif file.is_dir():
            carpetas.add(str(file.relative_to(p)))

    return {
        "archivos": archivos_info,
        "carpetas": list(carpetas)
    }


def detectar_stack(archivos: list[str]) -> dict:
    stack = {}
    if "requirements.txt" in archivos:
        stack["lenguaje"] = "Python"
        stack["dependencias"] = "requirements.txt"
    elif "package.json" in archivos:
        stack["lenguaje"] = "JavaScript"
        stack["dependencias"] = "package.json"
    else:
        stack["lenguaje"] = "Desconocido"
    print("Stack detectado:", stack)
    return stack

def escribir_readme(ruta: str, contenido: str):
    print(ruta)
    Path(ruta).joinpath("README.md").write_text(contenido)