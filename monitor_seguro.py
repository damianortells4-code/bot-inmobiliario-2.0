#!/usr/bin/env python3
"""
Monitor seguro del bot - No interfiere con el bot
"""

import time
import os
import glob
from datetime import datetime

def limpiar_pantalla():
    """Limpiar pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def verificar_bot_activo():
    """Verificar si el bot está activo"""
    try:
        # Buscar procesos Python con main.py
        resultado = os.popen("ps aux | grep 'python.*main.py' | grep -v grep").read()
        return len(resultado.strip()) > 0
    except:
        return False

def contar_archivos_log():
    """Contar archivos de log si existen"""
    try:
        logs = glob.glob('*.log')
        return len(logs)
    except:
        return 0

def mostrar_monitor_seguro():
    """Mostrar monitor que no interfiere"""
    while True:
        limpiar_pantalla()
        
        # Verificar estado
        bot_activo = verificar_bot_activo()
        logs = contar_archivos_log()
        hora_actual = datetime.now().strftime('%H:%M:%S')
        
        print("=" * 60)
        print("🏠 BOT INMOBILIARIO 2.0 - MONITOR SEGURO")
        print("=" * 60)
        print(f"📅 Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"🤖 Bot activo: {'SÍ' if bot_activo else 'NO'}")
        print(f"📁 Archivos log: {logs}")
        print()
        
        # Estado visual
        if bot_activo:
            print("✅ ESTADO: Bot funcionando correctamente")
            print("🔍 El bot está buscando anuncios activamente")
            print("📱 Revisa tu Telegram para las notificaciones")
            print("⏱️  El bot busca cada 2 minutos")
        else:
            print("❌ ESTADO: Bot no detectado")
            print("🚀 Ejecuta: python3 main.py")
            print("📊 O ejecuta el monitor en otra terminal")
        
        print()
        print("📋 INSTRUCCIONES:")
        print("   • Iniciar bot: python3 main.py")
        print("   • Ver logs: tail -f *.log")
        print("   • Detener bot: Ctrl+C en terminal del bot")
        print()
        print("🔄 Actualizando en 15 segundos...")
        print("   Presiona Ctrl+C para salir del monitor")
        print("=" * 60)
        
        time.sleep(15)

if __name__ == "__main__":
    print("Iniciando monitor seguro del bot...")
    print("Este monitor NO interfiere con el bot")
    print()
    
    try:
        mostrar_monitor_seguro()
    except KeyboardInterrupt:
        print("\n¡Monitor detenido!")
