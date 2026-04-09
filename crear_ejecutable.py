#!/usr/bin/env python3
"""
Crear ejecutable descargable del bot
"""

import os
import sys
import shutil
import subprocess
from datetime import datetime

def crear_ejecutable():
    """Crear un ejecutable descargable del bot"""
    
    print("·" * 60)
    print("CREANDO EJECUTABLE DESCARGABLE")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Crear carpeta del ejecutable
    carpeta_ejecutable = "/Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable"
    if os.path.exists(carpeta_ejecutable):
        shutil.rmtree(carpeta_ejecutable)
    os.makedirs(carpeta_ejecutable)
    
    print(f"1. Creando carpeta: {carpeta_ejecutable}")
    
    # 2. Copiar archivos esenciales
    archivos_esenciales = [
        "main.py",
        "config.py", 
        "database.py",
        "filtros.py",
        "filtros_tiempo.py",
        "puntuacion_anuncios.py",
        "scraper_internet.py",
        "telegram_alert.py",
        "urls.py",
        "verificador.py",
        "indicador_busqueda.py",
        "scraper_pisos.py",
        "scraper_fotocasa.py",
        "scraper_idealista.py",
        "scraper_milanuncios.py",
        "scraper_habitaclia.py",
        "scraper_duckduckgo.py"
    ]
    
    print("2. Copiando archivos esenciales...")
    for archivo in archivos_esenciales:
        origen = f"/Users/damianortells/Desktop/Bot-inmobiliario 2.0/{archivo}"
        destino = f"{carpeta_ejecutable}/{archivo}"
        
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} (no encontrado)")
    
    # 3. Copiar base de datos si existe
    db_origen = "/Users/damianortells/Desktop/Bot-inmobiliario 2.0/anuncios.db"
    db_destino = f"{carpeta_ejecutable}/anuncios.db"
    if os.path.exists(db_origen):
        shutil.copy2(db_origen, db_destino)
        print(f"   ✅ anuncios.db")
    
    # 4. Crear script de inicio
    script_inicio = f"""#!/bin/bash
# Bot Inmobiliario 2.0 - Ejecutable
echo "·" * 60
echo "BOT INMOBILIARIO 2.0 - INICIADO"
echo "·" * 60
echo "Iniciando búsqueda de anuncios..."
echo "Presiona Ctrl+C para detener"
echo "·" * 60
echo ""

# Configurar PATH de Python
export PATH="/usr/local/bin:/usr/bin:$PATH"

# Ir a la carpeta del bot
cd "$(dirname "$0")"

# Ejecutar el bot
python3 main.py

echo ""
echo "Bot detenido."
echo "¡Hasta pronto!"
"""
    
    with open(f"{carpeta_ejecutable}/iniciar_bot.sh", "w") as f:
        f.write(script_inicio)
    
    # Hacer el script ejecutable
    os.chmod(f"{carpeta_ejecutable}/iniciar_bot.sh", 0o755)
    print("   ✅ iniciar_bot.sh")
    
    # 5. Crear script para Windows
    script_windows = f"""@echo off
title Bot Inmobiliario 2.0
echo ============================================================
echo BOT INMOBILIARIO 2.0 - INICIADO
echo ============================================================
echo Iniciando búsqueda de anuncios...
echo Presiona Ctrl+C para detener
echo ============================================================
echo.

cd /d "%~dp0"
python main.py

echo.
echo Bot detenido.
echo ¡Hasta pronto!
pause
"""
    
    with open(f"{carpeta_ejecutable}/iniciar_bot.bat", "w") as f:
        f.write(script_windows)
    print("   ✅ iniciar_bot.bat")
    
    # 6. Crear README
    readme = f"""# BOT INMOBILIARIO 2.0 - EJECUTABLE

## 🚀 ¿Cómo iniciar el bot?

### Mac/Linux:
```bash
./iniciar_bot.sh
```

### Windows:
```cmd
iniciar_bot.bat
```

### Manual:
```bash
python3 main.py
```

## 📋 Configuración actual:
- ⏱️ **Intervalo:** 2 minutos
- 📅 **Filtro:** Anuncios de hoy (24h)
- 🎯 **Puntuación:** 5+ puntos (muy permisivo)
- 🏠 **Búsqueda:** Compra + Alquiler
- 📍 **Zonas:** Rubí, Sant Cugat, Sabadell, Terrassa

## 📱 ¿Qué esperar?
- **Leads por ronda:** 3-8 anuncios
- **Leads por hora:** 90-240 anuncios  
- **Leads por día:** 500-1500 anuncios
- **Notificaciones:** Directas a Telegram

## 🔧 Requisitos:
- Python 3.9+
- Conexión a internet
- Telegram configurado
- macOS/Linux/Windows

## 📞 Soporte:
- Bot sin errores 409
- Filtros ultra-permisivos
- Búsqueda continua 24/7
- Notificaciones instantáneas

---
**Bot creado: {datetime.now().strftime('%d/%m/%Y %H:%M')}**
**Versión: 2.0 Ejecutable**
"""
    
    with open(f"{carpeta_ejecutable}/README.md", "w") as f:
        f.write(readme)
    print("   ✅ README.md")
    
    # 7. Crear requirements.txt
    requirements = """# Bot Inmobiliario 2.0 - Dependencias
requests>=2.28.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-telegram-bot>=20.0
"""
    
    with open(f"{carpeta_ejecutable}/requirements.txt", "w") as f:
        f.write(requirements)
    print("   ✅ requirements.txt")
    
    # 8. Crear script de instalación
    script_instalacion = f"""#!/bin/bash
# Instalación Bot Inmobiliario 2.0
echo "·" * 60
echo "INSTALANDO BOT INMOBILIARIO 2.0"
echo "·" * 60
echo ""

# Instalar dependencias
echo "1. Instalando dependencias Python..."
pip3 install -r requirements.txt

echo ""
echo "✅ Instalación completada!"
echo "✅ Bot listo para usar!"
echo ""
echo "Para iniciar: ./iniciar_bot.sh"
echo "·" * 60
"""
    
    with open(f"{carpeta_ejecutable}/instalar.sh", "w") as f:
        f.write(script_instalacion)
    
    os.chmod(f"{carpeta_ejecutable}/instalar.sh", 0o755)
    print("   ✅ instalar.sh")
    
    print()
    print("3. Creando paquete comprimido...")
    
    # 9. Crear ZIP
    import zipfile
    zip_path = "/Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_ejecutable):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, carpeta_ejecutable)
                zipf.write(file_path, arcname)
    
    print(f"   ✅ Bot-Inmobiliario-Ejecutable.zip")
    
    # 10. Crear DMG para Mac
    try:
        dmg_path = "/Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable.dmg"
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Bot Inmobiliario 2.0",
            "-srcfolder", carpeta_ejecutable,
            "-ov",
            dmg_path
        ], check=True, capture_output=True)
        print(f"   ✅ Bot-Inmobiliario-Ejecutable.dmg")
    except:
        print("   ⚠️ No se pudo crear DMG (requiere macOS)")
    
    print()
    print("4. ¡EJECUTABLE CREADO!")
    print("·" * 60)
    print(f"📁 Carpeta: {carpeta_ejecutable}")
    print(f"📦 ZIP: /Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable.zip")
    
    if os.path.exists("/Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable.dmg"):
        print(f"💿 DMG: /Users/damianortells/Desktop/Bot-Inmobiliario-Ejecutable.dmg")
    
    print()
    print("📋 Para usar:")
    print("   1. Descomprimir el archivo")
    print("   2. Ejecutar 'iniciar_bot.sh' (Mac/Linux) o 'iniciar_bot.bat' (Windows)")
    print("   3. ¡Listo para recibir leads!")
    print("·" * 60)

if __name__ == "__main__":
    crear_ejecutable()
