#!/usr/bin/env python3
"""
Test de Telegram para verificar que funciona el envío
"""

import os
import sys

# Configurar automáticamente el entorno para encontrar los paquetes
global_paths = [
    '/Users/damianortells/Library/Python/3.9/lib/python/site-packages',
    '/usr/local/lib/python3.9/site-packages',
    '/usr/lib/python3.9/site-packages'
]

for path in global_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

from telegram_alert import enviar_mensaje

def test_telegram():
    """Enviar mensaje de prueba a Telegram"""
    
    mensaje_prueba = """¡TEST DEL BOT INMOBILIARIO! 

Este es un mensaje de prueba para verificar que:
- El bot funciona correctamente
- Las notificaciones llegan bien
- El sistema está operativo

Cuando encuentre pisos reales, te llegarán mensajes como este pero con:
- Título del piso
- Puntuación
- Link al anuncio
- Ubicación

El bot está buscando ahora mismo...
Próximo lead esperado: 30-60 minutos

¡Bot listo y funcionando!"""

    print("Enviando mensaje de prueba a Telegram...")
    
    if enviar_mensaje(mensaje_prueba):
        print("¡MENSAJE ENVIADO CORRECTAMENTE!")
        print("Revisa tu Telegram ahora mismo.")
        print("Si lo recibiste, el bot funciona perfectamente.")
    else:
        print("ERROR: No se pudo enviar el mensaje.")
        print("Revisa la configuración de Telegram.")

if __name__ == "__main__":
    test_telegram()
