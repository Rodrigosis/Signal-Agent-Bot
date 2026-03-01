import os
from langchain.prompts import ChatPromptTemplate

from src.domain.agent_template_state import RPGState
from src.infra.llm_proxy import MyCustomLLM

llm = MyCustomLLM(
    api_url=os.environ["LLM_API_URL"],
    api_key=os.environ["LLM_API_KEY"],
    model=os.environ["LLM_MODEL"],
    temperature=0.8
)

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
