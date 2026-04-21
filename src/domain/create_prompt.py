import os
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv
import requests

load_dotenv()

response = requests.get(
    url=f'https://raw.githubusercontent.com/{os.getenv("GITHUB_PROMPT_FILE")}',
    headers={"Authorization": os.getenv("GITHUB_TOKEN")}
)

SYSTEM_PROMPT = SystemMessage(
    content=f"""
Você é um Mestre de RPG experiente.
Seu papel é:
- Narrar o mundo e os acontecimentos
- Interpretar NPCs
- Reagir às escolhas do jogador
- Criar consequências interessantes
- Manter consistência narrativa

Regras:
- Nunca controle as ações do jogador
- Faça perguntas claras sobre decisões
- Crie uma história envolvente
- Use descrições sensoriais
- Quando uma decisão for crítica, sinalize claramente


----------------------- O JOGO ----------------------- 
{response.content}
"""
)
