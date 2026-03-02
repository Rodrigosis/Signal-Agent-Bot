from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, SystemMessage

from src.infra.llm_proxy import MyCustomLLM

llm = MyCustomLLM()


class RPGState(TypedDict):
    messages: List[BaseMessage]
    iterations: int
    needs_human: bool

# ======================
# NÓ: MESTRE DE RPG
# ======================
def rpg_narrator(state: RPGState) -> RPGState:
    response = llm.invoke(state["messages"])

    state["messages"].append(response)
    state["iterations"] += 1

    # Heurística simples para decisão crítica
    state["needs_human"] = (
        "decisão crítica" in response.content.lower()
        or "escolha difícil" in response.content.lower()
    )

    return state

# ======================
# NÓ: HUMAN IN THE LOOP
# ======================
def human_approval(state: RPGState) -> RPGState:
    print("\n⚠️ DECISÃO CRÍTICA DO MESTRE ⚠️\n")
    print(state["messages"][-1].content)

    user_input = input("\n👉 Supervisor humano (OK ou correção): ")

    if user_input.strip().lower() != "ok":
        state["messages"].append(
            SystemMessage(
                content=f"Correção do supervisor humano: {user_input}"
            )
        )

    state["needs_human"] = False
    return state

# ======================
# ROTEAMENTO
# ======================
def route_after_narration(state: RPGState):
    if state["needs_human"]:
        return "human_approval"
    return END

# ======================
# GRAFO
# ======================
graph = StateGraph(RPGState)

graph.add_node("narrator", rpg_narrator)
graph.add_node("human_approval", human_approval)

graph.set_entry_point("narrator")

graph.add_conditional_edges(
    "narrator",
    route_after_narration,
)

graph.add_edge("human_approval", END)

rpg_master = graph.compile()
