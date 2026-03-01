import os
import sqlite3
from langchain_core.prompts import ChatPromptTemplate
from src.domain.agent_template_state import RPGState
from src.infra.llm_proxy import MyCustomLLM

llm = MyCustomLLM()

conn = sqlite3.connect("rpg_memory.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS npcs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    status TEXT,
    relationship TEXT,
    notes TEXT
)
""")
conn.commit()

npc_prompt = ChatPromptTemplate.from_messages([
    ("system",
     """Analise a narração e extraia mudanças nos NPCs.
     Retorne no formato JSON:
     [
       { "name": "...", "status": "...", "relationship": "...", "notes": "..." }
     ]
     """),
    ("human", "{narration}")
])

def npc_manager_agent(state: RPGState):
    response = llm.invoke(
        npc_prompt.format_messages(narration=state["narration"])
    )

    import json
    updates = json.loads(response.content)

    for npc in updates:
        cursor.execute("""
        INSERT INTO npcs (name, status, relationship, notes)
        VALUES (?, ?, ?, ?)
        """, (
            npc["name"],
            npc["status"],
            npc["relationship"],
            npc["notes"]
        ))

    conn.commit()
    return {}
