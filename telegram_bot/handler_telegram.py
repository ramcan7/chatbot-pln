# main.py
import os
from telegram import Update
from telegram.ext import ContextTypes
from chatbot_rag.chatbot_rag import cargar_chat_con_memoria
from .auth import is_authenticated, authenticate
import requests
chat_chains = {}

async def auth_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = ctx.args
    if not args:
        return await update.message.reply_text("Usa: /auth <clave_secreta>")

    if authenticate(user_id, args[0]):
        await update.message.reply_text("Autenticación exitosa. Cargando chat...")
        chat_chains[user_id] = cargar_chat_con_memoria()
        await update.message.reply_text("¡Ya puedes chatear!")
    else:
        await update.message.reply_text("Clave incorrecta. Vuelve a intentarlo.")

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Antes de chatear, debes autenticarte con /auth <clave_secreta>."
    )

async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authenticated(user_id):
        return await update.message.reply_text("Debes autenticarte primero con /auth <clave_secreta>")

    chat = chat_chains.get(user_id)
    if chat is None:
        raise RuntimeError("Chat chain no encontrado. Asegúrate de autenticarte primero.")

    await update.message.reply_text("Procesando tu mensaje...")
    respuesta = chat.invoke(update.message.text)["answer"]
    await update.message.reply_text(respuesta)

def get_public_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json().get("tunnels", [])

        for tunnel in tunnels:
            url = tunnel.get("public_url", "")
            if url.startswith("https://"):
                return url

        raise RuntimeError("No se encontró ningún túnel HTTPS en ejecución.")
    except Exception as e:
        raise RuntimeError("Error al consultar ngrok: " + str(e))
