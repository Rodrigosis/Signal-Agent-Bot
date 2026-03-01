from langgraph.graph import StateGraph, END
from src.domain.agent_template_state import RPGState
from src.domain.agent1_narrador import narrator_agent
from src.domain.agent2_validador import validator_agent
from src.domain.agent3_update_ficha import npc_manager_agent

graph = StateGraph(RPGState)

graph.add_node("narrator", narrator_agent)
graph.add_node("validator", validator_agent)
graph.add_node("npc_manager", npc_manager_agent)

graph.set_entry_point("narrator")

graph.add_edge("narrator", "validator")

def route_after_validation(state: RPGState):
    if state["validated"]:
        return "npc_manager"
    else:
        return "narrator"

graph.add_conditional_edges(
    "validator",
    route_after_validation,
    {
        "npc_manager": "npc_manager",
        "narrator": "narrator"
    }
)

graph.add_edge("npc_manager", END)

rpg_master = graph.compile()
