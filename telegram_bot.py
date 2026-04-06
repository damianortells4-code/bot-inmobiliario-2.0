import os
import threading
import time

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

from telegram_alert import _load_env

# Cargar variables de entorno
_load_env()
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()

def start_command(update: Update, context: CallbackContext) -> None:
    """Handler para /start"""
    update.message.reply_text(
        "🏠 *Bot Inmobiliario 2.0* activo!\n\n"
        "Te enviaré notificaciones de pisos de particulares en:\n"
        "• Rubí\n• Sant Cugat\n• Sabadell\n• Terrassa\n\n"
        "Comandos disponibles:\n"
        "/start - Mensaje de bienvenida\n"
        "/status - Ver estado del bot\n"
        "/help - Ayuda",
        parse_mode='Markdown'
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Handler para /help"""
    update.message.reply_text(
        "🏠 *Bot Inmobiliario 2.0*\n\n"
        "*¿Qué hago?*\n"
        "Busco automáticamente pisos de particulares en varios portales "
        "(pisos.com, fotocasa, idealista) y te los envío por Telegram.\n\n"
        "*Filtros aplicados:*\n"
        "✅ Solo particulares (no agencias)\n"
        "✅ Sin duplicados\n"
        "✅ Enlaces verificados\n\n"
        "*Comandos:*\n"
        "/start - Iniciar bot\n"
        "/status - Estado del bot\n"
        "/help - Esta ayuda\n\n"
        "*Si no recibes mensajes:*\n"
        "• El bot busca cada 5 minutos\n"
        "• Solo envía pisos nuevos\n"
        "• Revisa que no tengas notificaciones silenciadas",
        parse_mode='Markdown'
    )

def status_command(update: Update, context: CallbackContext) -> None:
    """Handler para /status"""
    import config
    update.message.reply_text(
        "📊 *Estado del Bot*\n\n"
        f"🔍 *Búsqueda activa*: Sí\n"
        f"⏱️ *Intervalo*: {config.INTERVALO_SEGUNDOS} segundos\n"
        f"🌐 *Fuentes*: {'✅' if config.USAR_PISOS else '❌'} Pisos.com | "
        f"{'✅' if config.USAR_FOTOCASA else '❌'} Fotocasa | "
        f"{'✅' if config.USAR_IDEALISTA else '❌'} Idealista | "
        f"{'✅' if config.USAR_DUCKDUCKGO else '❌'} DuckDuckGo\n"
        f"🏘️ *Zonas*: Rubí, Sant Cugat, Sabadell, Terrassa\n"
        f"🎯 *Filtro particular*: {'Estricto' if config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO else 'Básico'}\n"
        f"📱 *Estado*: ✅ Activo y buscando",
        parse_mode='Markdown'
    )

def echo_message(update: Update, context: CallbackContext) -> None:
    """Responde a mensajes que no son comandos"""
    update.message.reply_text(
        "🤖 Soy un bot automático. Solo envío notificaciones de pisos.\n\n"
        "Usa /help para ver los comandos disponibles."
    )

def run_telegram_bot():
    """Inicia el bot de Telegram en un hilo separado"""
    if not TOKEN:
        print("❌ No hay TELEGRAM_BOT_TOKEN configurado")
        return
        
    application = Application.builder().token(TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    print("🤖 Bot de Telegram iniciado...")
    application.run_polling()

def start_telegram_thread():
    """Inicia el bot en un hilo para no bloquear el main"""
    bot_thread = threading.Thread(target=run_telegram_bot, daemon=True)
    bot_thread.start()
    return bot_thread
