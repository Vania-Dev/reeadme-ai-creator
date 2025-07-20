from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from utils import explorar_directorio, detectar_stack, escribir_readme
from prompts import construir_prompt

model = ChatOllama(model="llama3.2:3b-instruct-q4_K_M", streaming=True)

def analizar_archivo_semantico(codigo: str, llm) -> str:
    prompt = f"""
    Eres un experto desarrollador. Analiza el siguiente fragmento de código y explica brevemente qué hace y su propósito:

    {codigo}

    Resumen:
    """
    respuesta = model.invoke(prompt).content
    print(respuesta)
    return respuesta.strip()

def analizar_contenido(state):
    archivos = state["estructura"]["archivos"]
    res_summaries = []
    for archivo in archivos[:5]:  # Limitar a los primeros 5 archivos para no saturar el prompt
        resumen = analizar_archivo_semantico(archivo["contenido"], model)
        res_summaries.append({
            "ruta": archivo["ruta"],
            "resumen": resumen
        })
    print("Resumenes: ", res_summaries)
    return {**state, "resumenes": res_summaries}

def generar_readme(state):
    contexto = {
        "estructura": state["estructura"],
        "lenguaje": state["lenguaje"],
        "dependencias": state.get("dependencias", None),
    }
    prompt = construir_prompt(contexto)
    respuesta = model.invoke(prompt).content
    print("Readme: ", respuesta)
    return {**state, "readme": respuesta}

def create_graph():
    builder = StateGraph(state_schema=dict)

    builder.add_node("explorar", RunnableLambda(
        lambda state: {**state, "estructura": explorar_directorio(state["ruta"])}
    ))

    builder.add_node("analizar_stack", RunnableLambda(
        lambda state: {**state, **detectar_stack(state["estructura"]["archivos"])}
    ))

    builder.add_node("analizar_contenido", RunnableLambda(analizar_contenido))

    builder.add_node("generar_readme", RunnableLambda(generar_readme))

    builder.add_node("escribir", RunnableLambda(
        lambda state: escribir_readme(state["ruta"], state["readme"]) or state
    ))

    builder.set_entry_point("explorar")
    builder.add_edge("explorar", "analizar_stack")
    builder.add_edge("analizar_stack", "analizar_contenido")
    builder.add_edge("analizar_contenido", "generar_readme")
    builder.add_edge("generar_readme", "escribir")

    return builder.compile()