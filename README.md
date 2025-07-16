# Chatbot PLN con Ollama + RAG

Un bot en Telegram que utiliza un modelo local de Ollama (“llama3.2:3b”) junto con RAG para responder preguntas sobre productos METRO (Perú).

---

## 📋 Prerrequisitos

- **Python 3.10+**  
- **Ollama** instalado y modelo `llama3` disponible (`ollama run llama3`)  
- **ngrok** (o túnel equivalente)  
- Token de Telegram (`TELEGRAM_TOKEN`) obtenido de [@BotFather](https://t.me/BotFather)  
- Clave de acceso privada (`CHATBOT_KEY`) para `/auth`

---

## 🔧 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-org/chatbot-pln.git
cd chatbot-pln

# 2. Crea y activa el entorno virtual
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# .\venv\Scripts\activate   # Windows PowerShell

# 3. Instala dependencias
pip install -r requirements.txt
````

---

## ⚙️ Configuración

En la raíz del proyecto, crea un archivo `.env` con:

```ini
TELEGRAM_TOKEN=123456:ABC-DEF…
BOT_PASSWORD=tuClaveSecreta
PORT=8443
# Opcional: si no usas auto-descubrimiento de ngrok,
# copia aquí la URL HTTPS que te da ngrok
NGROK_URL=https://abcd1234.ngrok-free.app
```

Y asegúrate, en otra terminal, de tener Ollama corriendo:

```bash
ollama run llama3.2:3b
```

---

## 🚀 Ejecución local (Webhook + ngrok)

1. En un terminal, inicia ngrok apuntando al puerto de tu bot:

   ```bash
   ngrok http 8443
   ```
2. En otro terminal, lanza el script de arranque:

   ```bash
   python start.py
   # o bien
   ./start.sh
   ```

   El script:

   * Carga las variables de `.env`
   * Arranca ngrok (si no lo has iniciado manualmente)
   * Espera la URL HTTPS y la exporta a `NGROK_URL`
   * Ejecuta tu bot (`main.py`) en modo webhook

---

## 📝 Uso

1. En Telegram, envía `/start`.
2. Autentícate con `/auth <tu-clave>`.
3. ¡Ya puedes conversar con el bot!

