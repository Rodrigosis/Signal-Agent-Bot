import os
import structlog
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from langchain_core.messages import HumanMessage
from src.domain.ai_agent import rpg_master
from src.domain.create_prompt import SYSTEM_PROMPT

load_dotenv()
logger = structlog.get_logger()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
user_states = {}


def create_initial_state():
    return {
        "messages": [
            SYSTEM_PROMPT
        ],
        "iterations": 0,
        "needs_human": False,
    }

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("received_request", model="start")
    chat_id = update.effective_chat.id

    # cria novo estado para esse chat
    user_states[chat_id] = create_initial_state()

    # mensagem inicial do jogador
    user_states[chat_id]["messages"].append(
        HumanMessage(content="Inicie a campanha do jogo")
    )

    result = rpg_master.invoke(user_states[chat_id])

    # atualiza o estado com o retorno do grafo
    user_states[chat_id] = result

    await update.message.reply_text(
        result["messages"][-1].content
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("received_request", model="echo")
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
