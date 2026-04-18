from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.infra.llm_proxy import MyCustomLLM
from src.domain.create_prompt import SYSTEM_PROMPT

# ======================
# Inicializa o Deep Agent (uma vez só)
# ======================
llm = MyCustomLLM()  # sua LLM customizada continua funcionando perfeitamente

checkpointer = MemorySaver()

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
