import os
import threading
import time

import requests

from telegram_alert import _load_env

# Cargar variables de entorno
_load_env()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

def send_message_to_telegram(text: str) -> bool:
    """Envía mensaje usando requests simple"""
    if not TOKEN or not CHAT_ID:
        return False
        
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        r = requests.post(
            url,
            data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"},
            timeout=30,
        )
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Error enviando mensaje: {e}")
        return False

def process_telegram_update(update: dict) -> None:
    """Procesa una actualización de Telegram"""
    message = update.get("message", {})
    text = message.get("text", "")
    chat_id = message.get("chat", {}).get("id")
    
    if chat_id != int(CHAT_ID):
        return
        
    if text == "/start":
        response = """🏠 *Bot Inmobiliario 2.0* activo!

Te enviaré notificaciones de pisos de particulares en:
• Rubí
• Sant Cugat  
• Sabadell
• Terrassa

Comandos disponibles:
/start - Mensaje de bienvenida
/status - Ver estado del bot
/help - Ayuda"""
        
    elif text == "/help":
        response = """🏠 *Bot Inmobiliario 2.0*

*¿Qué hago?*
Busco automáticamente pisos de particulares en varios portales (pisos.com, fotocasa, idealista) y te los envío por Telegram.

*Filtros aplicados:*
✅ Solo particulares (no agencias)
✅ Sin duplicados
✅ Enlaces verificados

*Comandos:*
/start - Iniciar bot
/status - Estado del bot
/help - Esta ayuda

*Si no recibes mensajes:*
• El bot busca cada 5 minutos
• Solo envía pisos nuevos
• Revisa que no tengas notificaciones silenciadas"""
        
    elif text == "/status":
        import config
        response = f"""📊 *Estado del Bot*

🔍 *Búsqueda activa*: Sí
⏱️ *Intervalo*: {config.INTERVALO_SEGUNDOS} segundos
🌐 *Fuentes*: {'✅' if config.USAR_PISOS else '❌'} Pisos.com | {'✅' if config.USAR_FOTOCASA else '❌'} Fotocasa | {'✅' if config.USAR_IDEALISTA else '❌'} Idealista | {'✅' if config.USAR_DUCKDUCKGO else '❌'} DuckDuckGo
🏘️ *Zonas*: Rubí, Sant Cugat, Sabadell, Terrassa
🎯 *Filtro particular*: {'Estricto' if config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO else 'Básico'}
📱 *Estado*: ✅ Activo y buscando"""
        
    else:
        response = """🤖 Soy un bot automático. Solo envío notificaciones de pisos.

Usa /help para ver los comandos disponibles."""
    
    send_message_to_telegram(response)

def check_telegram_updates():
    """Revisa actualizaciones de Telegram periódicamente"""
    if not TOKEN:
        return
        
    last_update_id = 0
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={last_update_id + 1}"
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            
            data = r.json()
            if data.get("ok"):
                for update in data.get("result", []):
                    process_telegram_update(update)
                    last_update_id = update.get("update_id", last_update_id)
                    
        except Exception as e:
            print(f"Error revisando actualizaciones: {e}")
            
        time.sleep(5)  # Revisar cada 5 segundos

def start_telegram_thread():
    """Inicia el bot en un hilo separado"""
    if not TOKEN or not CHAT_ID:
        print("❌ No hay TELEGRAM_BOT_TOKEN o TELEGRAM_CHAT_ID configurado")
        return None
        
    print("🤖 Iniciando bot interactivo de Telegram...")
    bot_thread = threading.Thread(target=check_telegram_updates, daemon=True)
    bot_thread.start()
    
    # Enviar mensaje de inicio
    send_message_to_telegram("🏠 *Bot Inmobiliario 2.0* reiniciado y activo\n\nUsa /help para ver comandos")
    
    return bot_thread
