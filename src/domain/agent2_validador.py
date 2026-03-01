import os
from langchain_core.prompts import ChatPromptTemplate
from src.domain.agent_template_state import RPGState
from src.infra.llm_proxy import MyCustomLLM

llm = MyCustomLLM()

validator_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """Você é um validador de campanha de RPG.
     Verifique se a resposta do mestre:
     - Está coerente com a campanha
     - Não quebra regras do mundo
     - Não contradiz eventos anteriores

     Responda APENAS com:
     VALIDO ou INVALIDO + explicação curta
     """),
    ("human", "{narration}")
])

def validator_agent(state: RPGState):
    response = llm.invoke(
        validator_prompt.format_messages(narration=state["narration"])
    )

    content = response.content.upper()

    if content.startswith("VALIDO"):
        return {"validated": True}
    else:
        return {
            "validated": False,
            "validation_feedback": response.content
        }
