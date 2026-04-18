import os
import structlog
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from langchain_core.messages import HumanMessage
from src.domain.ai_agent import rpg_deep_agent, get_or_create_thread

load_dotenv()
logger = structlog.get_logger()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("received_request", model="start")
    chat_id = update.effective_chat.id

    config = get_or_create_thread(chat_id)

    # Mensagem inicial
    input_message = {"messages": [HumanMessage(content="Inicie a campanha do jogo")]}

    # Invoca o Deep Agent
    result = rpg_deep_agent.invoke(input_message, config=config)

    # Pega a última resposta do agente
    last_message = result["messages"][-1]

    await update.message.reply_text(last_message.content)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("received_request", model="echo")
    chat_id = update.effective_chat.id
    text = update.message.text

    config = get_or_create_thread(chat_id)

    # Adiciona a mensagem do jogador
    input_message = {"messages": [HumanMessage(content=text)]}

    try:
        result = rpg_deep_agent.invoke(input_message, config=config)

        # A última mensagem deve ser a resposta do narrador
        last_message = result["messages"][-1]

        await update.message.reply_text(last_message.content)

    except Exception as e:
        logger.error("agent_error", error=str(e))
        await update.message.reply_text("⚠️ Ocorreu um erro ao processar sua ação. Tente novamente.")


# ======================
# Configuração do Bot
# ======================
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

if __name__ == "__main__":
    print("🤖 Bot de RPG iniciado...")
    app.run_polling()
