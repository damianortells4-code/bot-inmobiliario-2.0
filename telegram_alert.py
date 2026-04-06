import os
import sys

import requests

def _load_env():
    """Load environment variables from .env file if it exists."""
    env_path = os.path.join(os.path.dirname(__file__), "secrets", ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

_load_env()

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

_AVISO_TOKEN = False


def enviar_mensaje(texto: str) -> bool:
    """
    Envía un mensaje por Telegram.
    Configura variables de entorno TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID.
    """
    global _AVISO_TOKEN

    if not TOKEN or not CHAT_ID:
        if not _AVISO_TOKEN:
            print(
                "[Telegram] Sin TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID en el entorno; "
                "no se envían mensajes.",
                file=sys.stderr,
            )
            _AVISO_TOKEN = True
        return False

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": texto},
            timeout=30,
        )
        r.raise_for_status()
        return True
    except (requests.RequestException, OSError) as exc:
        print(f"[Telegram] Error al enviar: {exc}", file=sys.stderr)
        return False
