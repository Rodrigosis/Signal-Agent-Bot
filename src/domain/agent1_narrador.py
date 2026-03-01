import os
from langchain_core.prompts import ChatPromptTemplate

from src.domain.agent_template_state import RPGState
from src.infra.llm_proxy import MyCustomLLM

llm = MyCustomLLM()

narrator_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um mestre de RPG de mesa narrativo."),
    ("human", "{input}")
])

def narrator_agent(state: RPGState):
    response = llm.invoke(
        narrator_prompt.format_messages(input=state["user_message"])
    )

    return {
        "narration": response.content
    }
