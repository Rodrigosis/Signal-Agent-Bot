import sqlite3
from deepagents import create_deep_agent
from src.infra.llm_proxy import MyCustomLLM
from src.domain.create_prompt import SYSTEM_PROMPT
from src.domain.history_manager import maybe_summarize
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage

llm = MyCustomLLM()

conn = sqlite3.connect("/app/data/checkpoints.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

rpg_deep_agent = create_deep_agent(
    model=llm,
    system_prompt=SYSTEM_PROMPT.content if hasattr(SYSTEM_PROMPT, "content") else str(SYSTEM_PROMPT),
    tools=[],
    checkpointer=checkpointer,
)


async def chat(user_message: str, chat_id: int) -> str:
    thread_id = f"telegram_rpg_{chat_id}"
    config = {"configurable": {"thread_id": thread_id}}

    # Recupera o estado atual do checkpoint
    state = await rpg_deep_agent.aget_state(config)
    messages = state.values.get("messages", [])

    # ✅ Summariza se necessário, antes de adicionar a nova mensagem
    messages = await maybe_summarize(messages, llm)

    # Adiciona a nova mensagem do usuário
    messages.append(HumanMessage(content=user_message))

    # Atualiza o estado com o histórico compactado
    await rpg_deep_agent.aupdate_state(config, {"messages": messages})

    # Invoca o agente normalmente
    result = await rpg_deep_agent.ainvoke(  # noqa
        {"messages": [HumanMessage(content=user_message)]}, config=config
    )

    return result["messages"][-1].content


def get_or_create_thread(chat_id: int):
    thread_id = f"telegram_rpg_{chat_id}"
    return {"configurable": {"thread_id": thread_id}}
