import requests
from typing import List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class MyCustomLLM(BaseChatModel):
    api_url: str
    api_key: str
    model: str
    temperature: float = 0.8

    @property
    def _llm_type(self) -> str:
        return self.model

    def _generate(
        self,
        messages: List[BaseMessage],
        stop=None,
        run_manager=None,
        **kwargs
    ) -> ChatResult:

        payload = {
            "model": self.model,
            "messages": [
                {"role": m.type, "content": m.content}
                for m in messages
            ],
            "temperature": self.temperature
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        response = requests.post(
            self.api_url,
            json=payload,
            headers=headers,
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        ai_message = AIMessage(content=data["content"])

        return ChatResult(
            generations=[ChatGeneration(message=ai_message)]
        )
