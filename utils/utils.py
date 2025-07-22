from pathlib import Path

EXCLUDED_DIRS = {".venv", "__pycache__", ".git", ".pytest_cache"}
EXCLUDED_FILES = {".env", ".gitignore", ".DS_Store"}


def explore_directory(path: str) -> dict:
    p = Path(path)

    files_info = []
    folders = set()

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
                files_info.append({
                    "route": str(file.relative_to(p)),
                    "name": file.name,
                    "content": content[:1000]  # Limitar para no sobrecargar el prompt
                })
            except Exception as e:
                files_info.append({
                    "route": str(file.relative_to(p)),
                    "name": file.name,
                    "content": f"(No se pudo leer el archivo: {e})"
                })

        elif file.is_dir():
            folders.add(str(file.relative_to(p)))

    return {
        "files": files_info,
        "folders": list(folders)
    }


def detect_stack(files: list[str]) -> dict:
    stack = {}
    project_files = [file["route"] for file in files]

    if "requirements.txt" in project_files:
        stack["language"] = "Python"
        stack["dependencies"] = "requirements.txt"
    elif "package.json" in project_files:
        stack["language"] = "JavaScript"
        stack["dependencies"] = "package.json"
    else:
        stack["language"] = "Desconocido"
    print("Stack detectado:", stack)
    return stack


def write_readme(route: str, content: str):
    Path(route).joinpath("README.md").write_text(content)