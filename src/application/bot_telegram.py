import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from src.domain.ai_agent import rpg_master
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_states = {}

SYSTEM_PROMPT = SystemMessage(
    content="""
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
"""
)

def create_initial_state():
    return {
        "messages": [
            SYSTEM_PROMPT
        ],
        "iterations": 0,
        "needs_human": False,
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # cria novo estado para esse chat
    user_states[chat_id] = create_initial_state()

    # mensagem inicial do jogador
    user_states[chat_id]["messages"].append(
        HumanMessage(content="Inicie a campanha com uma cena épica.")
    )

    result = rpg_master.invoke(user_states[chat_id])

    # atualiza o estado com o retorno do grafo
    user_states[chat_id] = result

    await update.message.reply_text(
        result["messages"][-1].content
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    # se o usuário não deu /start
    if chat_id not in user_states:
        await update.message.reply_text(
            "Use /start para iniciar a campanha 🎲"
        )
        return

    # adiciona fala do jogador no histórico
    user_states[chat_id]["messages"].append(
        HumanMessage(content=text)
    )

    result = rpg_master.invoke(user_states[chat_id])

    # salva estado atualizado
    user_states[chat_id] = result

    await update.message.reply_text(
        result["messages"][-1].content
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

app.run_polling()
