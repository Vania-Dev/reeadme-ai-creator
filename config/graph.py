from langgraph.graph import StateGraph
from langchain_ollama import ChatOllama
from langchain_core.runnables import RunnableLambda
from utils.utils import explore_directory, detect_stack, write_readme
from data.prompts import create_prompt

model = ChatOllama(model="llama3.2:3b-instruct-q4_K_M", streaming=True)


def analyze_semantic_file(code: str) -> str:
    prompt = f"""
    Eres un experto desarrollador. Analiza el siguiente fragmento de código y explica brevemente qué hace y su propósito:ß
    {code}
    Resumen:
    """
    response = model.invoke(prompt).content
    return response.strip()


def analize_content(state):
    files = state["structure"]["files"]
    res_summaries = []
    for file in files[:5]:  # Limitar a los primeros 5 files para no saturar el prompt
        resume = analyze_semantic_file(file["content"])
        res_summaries.append({
            "route": file["route"],
            "resume": resume
        })
    return {**state, "summaries": res_summaries}


def create_readme(state):
    context = {
        "structure": state["structure"],
        "language": state["language"],
        "dependencies": state.get("dependencies", None),
    }
    prompt = create_prompt(context)
    response = model.invoke(prompt).content
    return {**state, "readme": response}


def create_graph():
    builder = StateGraph(state_schema=dict)

    builder.add_node("explore", RunnableLambda(
        lambda state: {**state, "structure": explore_directory(state["route"])}
    ))

    builder.add_node("analize_stack", RunnableLambda(
        lambda state: {**state, **detect_stack(state["structure"]["files"])}
    ))

    builder.add_node("analize_content", RunnableLambda(analize_content))

    builder.add_node("create_readme", RunnableLambda(create_readme))

    builder.add_node("write", RunnableLambda(
        lambda state: write_readme(state["route"], state["readme"]) or state
    ))

    builder.set_entry_point("explore")
    builder.add_edge("explore", "analize_stack")
    builder.add_edge("analize_stack", "analize_content")
    builder.add_edge("analize_content", "create_readme")
    builder.add_edge("create_readme", "write")

    return builder.compile()