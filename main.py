import os
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters
)
import telegram_bot.handler_telegram as handler_telegram
from config import NGROK_PORT, TELEGRAM_TOKEN

if __name__ == "__main__":
    print("Iniciando Asistente Metro...")

    app = ApplicationBuilder()\
        .token(TELEGRAM_TOKEN)\
        .build()

    app.add_handler(CommandHandler("start", handler_telegram.start))
    app.add_handler(CommandHandler("auth", handler_telegram.auth_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_telegram.handle_message))

    # Registra el webhook
    public_url = handler_telegram.get_public_url()
    webhook_url = f"{public_url}/{TELEGRAM_TOKEN}"

    # Arranca servidor en modo webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=NGROK_PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=webhook_url,
    )

    print("Asistente Metro iniciado correctamente.")
