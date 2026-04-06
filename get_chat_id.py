import os
import sys
import json

try:
    import requests
except ImportError:
    print("Instala requests: pip install requests")
    sys.exit(1)

def _parse_env(path):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

proj = os.path.dirname(__file__)
secrets_path = os.path.join(proj, "secrets", ".env")

env = _parse_env(secrets_path)
token = env.get("TELEGRAM_BOT_TOKEN") or env.get("TELEGRAM_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")

if not token:
    print("No se ha encontrado token. Añádelo a secrets/.env como TELEGRAM_TOKEN o TELEGRAM_BOT_TOKEN.")
    sys.exit(1)

print("Usando token (no se muestra). Si no has enviado /start al bot, hazlo ahora y espera 10-20s.\n")

url = f"https://api.telegram.org/bot{token}/getUpdates"
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
except Exception as e:
    print("Error llamando a la API de Telegram:", e)
    sys.exit(1)

data = r.json()
if not data.get("ok"):
    print("Respuesta no OK de Telegram:", json.dumps(data, indent=2))
    sys.exit(1)

results = data.get("result", [])
if not results:
    print("No hay updates. Envía /start al bot desde TU cuenta y vuelve a ejecutar este script.")
    sys.exit(0)

found = {}
for u in results:
    msg = u.get("message") or u.get("edited_message") or u.get("channel_post") or {}
    if not msg:
        continue
    chat = msg.get("chat", {})
    cid = chat.get("id")
    if cid is None:
        continue
    username = chat.get("username") or chat.get("first_name") or ""
    text = (msg.get("text") or "")[:200]
    found.setdefault(cid, []).append({"username": username, "text": text})

print("Chat IDs encontrados:")
for cid, msgs in found.items():
    print("-", cid)
    for m in msgs[-3:]:
        print("   >", (m["username"] or "<sin-username>"), ":", m["text"])
print("\nCopia el número que necesites y pégalo en secrets/.env como TELEGRAM_CHAT_ID=EL_NUMERO")