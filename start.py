#!/usr/bin/env python3
import os, subprocess, time, requests, signal, sys
from pathlib import Path
from dotenv import load_dotenv

# 1) Carga .env
DOTENV = Path(__file__).parent / '.env'
if DOTENV.exists(): load_dotenv(DOTENV)

NGROK_PORT = os.getenv("NGROK_PORT")

# 2) Inicia ngrok
ngrok = subprocess.Popen(["ngrok", "http", NGROK_PORT], stdout=subprocess.DEVNULL)

def cleanup(sig, frame):
    print("\n🛑 Deteniendo ngrok...")
    ngrok.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

# 3) Espera túnel
print(f"Esperando túnel HTTPS en http://127.0.0.1:4040/api/tunnels...")
public = None
for _ in range(60):
    try:
        data = requests.get('http://127.0.0.1:4040/api/tunnels').json()
        for t in data.get('tunnels', []):
            if t.get('public_url','').startswith('https://'):
                public = t['public_url'].rstrip('/')
                break
    except:
        pass
    if public: break
    time.sleep(0.5)

if not public:
    print("No se encontró túnel HTTPS. Asegúrate de que ngrok esté instalado y accesible.")
    cleanup(None, None)

os.environ['NGROK_URL'] = public
print(f"URL pública: {public}")

# 4) Arranca tu bot
subprocess.run(['python', 'main.py'])
