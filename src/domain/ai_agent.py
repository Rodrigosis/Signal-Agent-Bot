import sqlite3
from deepagents import create_deep_agent
# from langgraph.checkpoint.memory import MemorySaver
# from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.infra.llm_proxy import MyCustomLLM
from src.domain.create_prompt import SYSTEM_PROMPT
from langgraph.checkpoint.sqlite import SqliteSaver

# ======================
# Inicializa o Deep Agent (uma vez só)
# ======================
llm = MyCustomLLM()  # LLM customizada

conn = sqlite3.connect("/app/data/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
# checkpointer = MemorySaver()

rpg_deep_agent = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT.content if hasattr(SYSTEM_PROMPT, "content") else str(SYSTEM_PROMPT),
    tools=[],                    # adicione ferramentas depois se quiser (buscar lore, rolar dados, etc.)
    checkpointer=checkpointer,
    # interrupt_on={}            # você pode configurar aqui se usar ferramentas que precisam de aprovação
)

def get_or_create_thread(chat_id: int):
    """Cria ou recupera o thread (conversa) por chat_id"""
    thread_id = f"telegram_rpg_{chat_id}"
    config = {"configurable": {"thread_id": thread_id}}
    return config
