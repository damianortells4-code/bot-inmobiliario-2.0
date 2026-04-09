#!/usr/bin/env python3
"""
Instalador simple con auto-actualizaciones
"""

import os
import sys
import shutil
import subprocess
import json
import urllib.request
from datetime import datetime

def crear_instalador_simple():
    """Crear instalador simple con auto-actualizaciones"""
    
    print("·" * 60)
    print("CREANDO INSTALADOR SIMPLE CON AUTO-ACTUALIZACIONES")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Crear carpeta del instalador
    carpeta_instalador = "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador"
    if os.path.exists(carpeta_instalador):
        shutil.rmtree(carpeta_instalador)
    os.makedirs(carpeta_instalador)
    
    print(f"1. Creando instalador: {carpeta_instalador}")
    
    # 2. Copiar archivos principales
    print("2. Copiando archivos principales...")
    
    archivos_principales = [
        "main.py", "config.py", "database.py", "filtros.py",
        "filtros_tiempo.py", "puntuacion_anuncios.py", "scraper_internet.py",
        "telegram_alert.py", "urls.py", "verificador.py", "indicador_busqueda.py"
    ]
    
    origen_bot = "/Users/damianortells/Desktop/Bot-inmobiliario 2.0"
    
    for archivo in archivos_principales:
        origen = f"{origen_bot}/{archivo}"
        destino = f"{carpeta_instalador}/{archivo}"
        
        if os.path.exists(origen):
            shutil.copy2(origen, destino)
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} (no encontrado)")
    
    # 3. Copiar scrapers
    print("3. Copiando scrapers...")
    
    for archivo in os.listdir(origen_bot):
        if archivo.startswith("scraper_") and archivo.endswith(".py"):
            origen = f"{origen_bot}/{archivo}"
            destino = f"{carpeta_instalador}/{archivo}"
            shutil.copy2(origen, destino)
            print(f"   ✅ {archivo}")
    
    # 4. Copiar base de datos si existe
    db_origen = f"{origen_bot}/anuncios.db"
    db_destino = f"{carpeta_instalador}/anuncios.db"
    if os.path.exists(db_origen):
        shutil.copy2(db_origen, db_destino)
        print(f"   ✅ anuncios.db")
    
    # 5. Crear actualizador simple
    print("4. Creando actualizador...")
    
    actualizador = '''#!/usr/bin/env python3
# Auto-actualizador Bot Inmobiliario 2.0

import os
import json
import urllib.request
import subprocess
from datetime import datetime

VERSION_ACTUAL = "2.0.1"
URL_BASE = "https://raw.githubusercontent.com/damianortells4-code/bot-inmobiliario-2.0/main"

def check_actualizaciones():
    print("🔍 Verificando actualizaciones...")
    try:
        # Obtener versión remota desde GitHub
        with urllib.request.urlopen("https://api.github.com/repos/damianortells4-code/bot-inmobiliario-2.0/releases/latest") as response:
            data = json.loads(response.read().decode())
            version_remota = data["tag_name"].replace("v", "")
        
        print(f"📦 Versión actual: {VERSION_ACTUAL}")
        print(f"📦 Versión remota: {version_remota}")
        
        if version_remota > VERSION_ACTUAL:
            print("✨ ¡Nueva versión disponible!")
            return True
        else:
            print("✅ Estás en la última versión")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando actualizaciones: {e}")
        return False

def descargar_actualizacion():
    print("📥 Descargando actualización...")
    
    archivos_actualizar = [
        "main.py", "config.py", "database.py", "filtros.py",
        "filtros_tiempo.py", "puntuacion_anuncios.py", "scraper_internet.py",
        "telegram_alert.py", "urls.py", "verificador.py", "indicador_busqueda.py"
    ]
    
    # Añadir scrapers
    archivos_actualizar.extend([
        "scraper_pisos.py", "scraper_fotocasa.py", "scraper_idealista.py",
        "scraper_milanuncios.py", "scraper_habitaclia.py"
    ])
    
    for archivo in archivos_actualizar:
        try:
            url = f"{URL_BASE}/{archivo}"
            print(f"   📥 Descargando {archivo}...")
            
            with urllib.request.urlopen(url) as response:
                contenido = response.read().decode()
            
            with open(archivo, "w") as f:
                f.write(contenido)
                
            print(f"   ✅ {archivo} actualizado")
            
        except Exception as e:
            print(f"   ❌ Error actualizando {archivo}: {e}")
    
    print("✅ ¡Actualización completada!")
    print("🔄 Reiniciando bot...")
    
    # Reiniciar el bot
    os.execv(sys.executable, ["python3", "main.py"])

def main():
    print("·" * 60)
    print("ACTUALIZADOR BOT INMOBILIARIO 2.0")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    if check_actualizaciones():
        print("¿Deseas actualizar ahora? (s/n): ", end="")
        respuesta = input().lower().strip()
        
        if respuesta in ["s", "si", "y", "yes"]:
            descargar_actualizacion()
        else:
            print("❌ Actualización cancelada")
    else:
        print("🎯 Bot está actualizado")
    
    print("·" * 60)

if __name__ == "__main__":
    main()
'''
    
    with open(f"{carpeta_instalador}/actualizador.py", "w") as f:
        f.write(actualizador)
    print("   ✅ actualizador.py")
    
    # 6. Crear instalador principal
    print("5. Creando instalador principal...")
    
    instalador = '''#!/usr/bin/env python3
# Instalador Bot Inmobiliario 2.0

import os
import json
from datetime import datetime

def main():
    print("·" * 60)
    print("INSTALADOR BOT INMOBILIARIO 2.0")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    print("🚀 Instalando Bot Inmobiliario 2.0...")
    print()
    
    # Crear configuración
    config = {
        "telegram_bot_token": "",
        "telegram_chat_id": "",
        "intervalo_segundos": 120,
        "puntuacion_minima": 5,
        "filtro_horas": 24,
        "auto_actualizar": True
    }
    
    with open("config_usuario.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ config_usuario.json creado")
    print()
    print("📋 Siguientes pasos:")
    print("   1. Edita config_usuario.json con tus datos de Telegram")
    print("   2. Ejecuta: python3 main.py")
    print("   3. Para actualizar: python3 actualizador.py")
    print()
    print("🎯 Configuración actual:")
    print(f"   - Intervalo: {config['intervalo_segundos']} segundos")
    print(f"   - Puntuación mínima: {config['puntuacion_minima']} puntos")
    print(f"   - Filtro: {config['filtro_horas']} horas")
    print(f"   - Auto-actualizar: {config['auto_actualizar']}")
    print("·" * 60)

if __name__ == "__main__":
    main()
'''
    
    with open(f"{carpeta_instalador}/instalar.py", "w") as f:
        f.write(instalador)
    print("   ✅ instalar.py")
    
    # 7. Crear launcher
    print("6. Creando launcher...")
    
    launcher = '''#!/usr/bin/env python3
# Launcher Bot Inmobiliario 2.0

import os
import json
import subprocess
import sys
from datetime import datetime

def verificar_config():
    if not os.path.exists("config_usuario.json"):
        print("❌ No hay configuración")
        print("📝 Ejecuta primero: python3 instalar.py")
        return False
    
    with open("config_usuario.json", "r") as f:
        config = json.load(f)
    
    if not config.get("telegram_bot_token") or not config.get("telegram_chat_id"):
        print("❌ Configuración incompleta")
        print("📝 Edita config_usuario.json con tu token y chat_id")
        return False
    
    return True

def main():
    print("·" * 60)
    print("BOT INMOBILIARIO 2.0 - LAUNCHER")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    if not verificar_config():
        return
    
    print("🚀 Iniciando Bot Inmobiliario 2.0...")
    print("🔄 Verificando actualizaciones...")
    
    # Verificar actualizaciones
    if os.path.exists("actualizador.py"):
        try:
            subprocess.run([sys.executable, "actualizador.py"], check=True)
        except:
            pass
    
    # Iniciar bot principal
    subprocess.run([sys.executable, "main.py"])

if __name__ == "__main__":
    main()
'''
    
    with open(f"{carpeta_instalador}/launcher.py", "w") as f:
        f.write(launcher)
    print("   ✅ launcher.py")
    
    # 8. Crear README
    print("7. Creando README...")
    
    readme = '''# BOT INMOBILIARIO 2.0 - INSTALADOR

## 🚀 Instalación Rápida

### Paso 1: Instalar
```bash
python3 instalar.py
```

### Paso 2: Configurar
Edita `config_usuario.json` con tus datos de Telegram:
```json
{
  "telegram_bot_token": "TU_TOKEN",
  "telegram_chat_id": "TU_CHAT_ID",
  "intervalo_segundos": 120,
  "puntuacion_minima": 5,
  "filtro_horas": 24,
  "auto_actualizar": true
}
```

### Paso 3: Iniciar
```bash
python3 launcher.py
```

## 🔄 Auto-Actualizaciones

El bot se actualiza automáticamente cada vez que inicia:

1. **Verifica versión** en GitHub
2. **Descarga actualizaciones** si existen
3. **Aplica cambios** automáticamente
4. **Reinicia el bot** con nueva versión

## 📋 Configuración Actual

- ⏱️ **Intervalo:** 2 minutos
- 📅 **Filtro:** Anuncios de hoy (24h)
- 🎯 **Puntuación:** 5+ puntos (muy permisivo)
- 🏠 **Búsqueda:** Compra + Alquiler
- 📍 **Zonas:** Rubí, Sant Cugat, Sabadell, Terrassa
- 🔄 **Auto-actualizar:** Sí

## 📱 Características

✅ **Auto-actualizaciones** desde GitHub
✅ **Configuración fácil** con JSON
✅ **Instalación simple** en 3 pasos
✅ **Verificación automática** de configuración
✅ **Todos los archivos** incluidos
✅ **Multiplataforma** (Mac/Windows/Linux)

---
**Instalador creado: ''' + datetime.now().strftime('%d/%m/%Y %H:%M') + '''
**Versión: 2.0.1 Simple**
'''
    
    with open(f"{carpeta_instalador}/README.md", "w") as f:
        f.write(readme)
    print("   ✅ README.md")
    
    # 9. Crear requirements
    print("8. Creando requirements...")
    
    requirements = """requests>=2.28.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-telegram-bot>=20.0
urllib3>=1.26.0
"""
    
    with open(f"{carpeta_instalador}/requirements.txt", "w") as f:
        f.write(requirements)
    print("   ✅ requirements.txt")
    
    # 10. Hacer scripts ejecutables
    print("9. Creando scripts ejecutables...")
    
    os.chmod(f"{carpeta_instalador}/instalar.py", 0o755)
    os.chmod(f"{carpeta_instalador}/launcher.py", 0o755)
    os.chmod(f"{carpeta_instalador}/actualizador.py", 0o755)
    print("   ✅ Scripts ejecutables")
    
    # 11. Crear ZIP
    print("10. Creando paquete ZIP...")
    
    import zipfile
    zip_path = "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_instalador):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, carpeta_instalador)
                zipf.write(file_path, arcname)
    
    print(f"   ✅ Bot-Inmobiliario-Instalador.zip")
    
    print()
    print("11. ¡INSTALADOR SIMPLE CREADO!")
    print("·" * 60)
    print(f"📁 Carpeta: {carpeta_instalador}")
    print(f"📦 ZIP: /Users/damianortells/Desktop/Bot-Inmobiliario-Instalador.zip")
    print()
    print("🎯 Características del instalador:")
    print("   ✅ Auto-actualizaciones desde GitHub")
    print("   ✅ Instalación simple en 3 pasos")
    print("   ✅ Configuración fácil con JSON")
    print("   ✅ Todos los archivos incluidos")
    print("   ✅ Scripts ejecutables")
    print("   ✅ Multiplataforma (Mac/Windows/Linux)")
    print("   ✅ Launcher inteligente")
    print("   ✅ Verificación de configuración")
    print()
    print("📋 Para usar:")
    print("   1. Descomprimir Bot-Inmobiliario-Instalador.zip")
    print("   2. Ejecutar: python3 instalar.py")
    print("   3. Configurar config_usuario.json")
    print("   4. Iniciar: python3 launcher.py")
    print("   5. ¡Listo para recibir leads con auto-actualizaciones!")
    print("·" * 60)

if __name__ == "__main__":
    crear_instalador_simple()
