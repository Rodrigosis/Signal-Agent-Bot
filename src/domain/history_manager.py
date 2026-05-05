from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from typing import List

MAX_MESSAGES = 10          # dispara summarização acima disso
KEEP_RECENT = 4            # mantém as N últimas mensagens intactas após resumir

SUMMARY_PROMPT = """Você é um assistente de RPG. Resuma a sessão abaixo em um parágrafo compacto, preservando:
- Nome e raça/classe do personagem
- Localização atual e objetivo principal
- Itens, aliados e inimigos relevantes
- Decisões e eventos importantes

Seja conciso mas completo. Responda apenas com o resumo, sem preâmbulo."""


async def maybe_summarize(messages: List[BaseMessage], llm) -> List[BaseMessage]:
    """
    Se o histórico for longo demais, resume as mensagens antigas com o LLM
    e retorna uma lista compacta: [SystemMessage(resumo)] + msgs recentes.
    """
    # Separa system message(s) do restante
    system_msgs = [m for m in messages if isinstance(m, SystemMessage)]
    chat_msgs   = [m for m in messages if not isinstance(m, SystemMessage)]

    if len(chat_msgs) <= MAX_MESSAGES:
        return messages  # ainda dentro do limite, não faz nada

    to_summarize = chat_msgs[:-KEEP_RECENT]
    recent       = chat_msgs[-KEEP_RECENT:]

    # Monta o contexto para o LLM resumir
    history_text = "\n".join(
        f"{'Usuário' if isinstance(m, HumanMessage) else 'Assistente'}: {m.content}"
        for m in to_summarize
    )

    summary_response = await llm.ainvoke([
        SystemMessage(content=SUMMARY_PROMPT),
        HumanMessage(content=history_text),
    ])

    summary_text = (
        summary_response.content
        if hasattr(summary_response, "content")
        else str(summary_response)
    )

    summary_msg = SystemMessage(
        content=f"[RESUMO DA SESSÃO ANTERIOR]\n{summary_text}"
    )

    return system_msgs + [summary_msg] + recent
