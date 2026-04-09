#!/usr/bin/env python3
"""
Crear instalador completo con actualizaciones automáticas
"""

import os
import sys
import shutil
import subprocess
import json
import urllib.request
from datetime import datetime

def crear_instalador_completo():
    """Crear instalador completo con auto-actualizaciones"""
    
    print("·" * 60)
    print("CREANDO INSTALADOR COMPLETO CON AUTO-ACTUALIZACIONES")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Crear carpeta del instalador
    carpeta_instalador = "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo"
    if os.path.exists(carpeta_instalador):
        shutil.rmtree(carpeta_instalador)
    os.makedirs(carpeta_instalador)
    
    print(f"1. Creando instalador: {carpeta_instalador}")
    
    # 2. Copiar TODOS los archivos del bot
    print("2. Copiando TODOS los archivos del bot...")
    
    origen_bot = "/Users/damianortells/Desktop/Bot-inmobiliario 2.0"
    
    for archivo in os.listdir(origen_bot):
        if archivo.endswith('.py') or archivo.endswith('.db') or archivo.endswith('.txt') or archivo.endswith('.md'):
            origen = f"{origen_bot}/{archivo}"
            destino = f"{carpeta_instalador}/{archivo}"
            
            if os.path.isfile(origen):
                shutil.copy2(origen, destino)
                print(f"   ✅ {archivo}")
            elif os.path.isdir(origen) and not archivo.startswith('.'):
                shutil.copytree(origen, destino, dirs_exist_ok=True)
                print(f"   📁 {archivo}/")
    
    # 3. Crear sistema de actualizaciones
    print("3. Creando sistema de auto-actualizaciones...")
    
    actualizador = f"""#!/usr/bin/env python3
# Auto-actualizador Bot Inmobiliario 2.0

import os
import sys
import json
import urllib.request
import subprocess
from datetime import datetime

VERSION_ACTUAL = "2.0.1"
URL_VERSION = "https://api.github.com/repos/damianortells4-code/bot-inmobiliario-2.0/releases/latest"
URL_RAW = "https://raw.githubusercontent.com/damianortells4-code/bot-inmobiliario-2.0/main"

def check_actualizaciones():
    """Verificar si hay actualizaciones disponibles"""
    try:
        print("🔍 Buscando actualizaciones...")
        
        # Obtener versión remota
        with urllib.request.urlopen(URL_VERSION) as response:
            data = json.loads(response.read().decode())
            version_remota = data['tag_name'].replace('v', '')
            
        print(f"📦 Versión actual: {VERSION_ACTUAL}")
        print(f"📦 Versión remota: {version_remota}")
        
        # Comparar versiones
        if version_remota > VERSION_ACTUAL:
            print("✨ ¡Nueva versión disponible!")
            return True, version_remota
        else:
            print("✅ Estás en la última versión")
            return False, version_remota
            
    except Exception as e:
        print(f"❌ Error verificando actualizaciones: {e}")
        return False, VERSION_ACTUAL

def descargar_actualizacion():
    """Descargar y aplicar actualización"""
    try:
        print("📥 Descargando actualización...")
        
        # Archivos a actualizar
        archivos_actualizar = [
            'main.py', 'config.py', 'database.py', 'filtros.py',
            'filtros_tiempo.py', 'puntuacion_anuncios.py',
            'scraper_internet.py', 'telegram_alert.py', 'urls.py',
            'verificador.py', 'indicador_busqueda.py',
            'scraper_pisos.py', 'scraper_fotocasa.py',
            'scraper_idealista.py', 'scraper_milanuncios.py',
            'scraper_habitaclia.py'
        ]
        
        for archivo in archivos_actualizar:
            try:
                url = f"{{URL_RAW}}/{{archivo}}"
                print(f"   📥 Descargando {{archivo}}...")
                
                with urllib.request.urlopen(url) as response:
                    contenido = response.read().decode()
                
                with open(archivo, 'w') as f:
                    f.write(contenido)
                    
                print(f"   ✅ {{archivo}} actualizado")
                
            except Exception as e:
                print(f"   ❌ Error actualizando {{archivo}}: {{e}}")
        
        print("✅ ¡Actualización completada!")
        print("🔄 Reiniciando bot...")
        
        # Reiniciar el bot
        os.execv(sys.executable, ['python3', 'main.py'])
        
    except Exception as e:
        print(f"❌ Error en actualización: {{e}}")

def main():
    """Función principal del actualizador"""
    print("·" * 60)
    print("ACTUALIZADOR BOT INMOBILIARIO 2.0")
    print("·" * 60)
    print(f"Timestamp: {{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}}")
    print()
    
    hay_actualizacion, version_remota = check_actualizaciones()
    
    if hay_actualizacion:
        print("¿Deseas actualizar ahora? (s/n): ", end="")
        respuesta = input().lower().strip()
        
        if respuesta in ['s', 'si', 'y', 'yes']:
            descargar_actualizacion()
        else:
            print("❌ Actualización cancelada")
    else:
        print("🎯 Bot está actualizado")
    
    print("·" * 60)

if __name__ == "__main__":
    main()
"""
    
    with open(f"{carpeta_instalador}/actualizador.py", "w") as f:
        f.write(actualizador)
    print("   ✅ actualizador.py")
    
    # 4. Crear instalador principal
    instalador = f"""#!/usr/bin/env python3
# Instalador Bot Inmobiliario 2.0 - Completo

import os
import sys
import subprocess
import platform
from datetime import datetime

def instalar_dependencias():
    """Instalar dependencias necesarias"""
    print("📦 Instalando dependencias...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "requests"], check=True)
        print("   ✅ requests")
    except:
        print("   ❌ requests (ya instalado o error)")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "beautifulsoup4"], check=True)
        print("   ✅ beautifulsoup4")
    except:
        print("   ❌ beautifulsoup4 (ya instalado o error)")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "lxml"], check=True)
        print("   ✅ lxml")
    except:
        print("   ❌ lxml (ya instalado o error)")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot"], check=True)
        print("   ✅ python-telegram-bot")
    except:
        print("   ❌ python-telegram-bot (ya instalado o error)")

def configurar_bot():
    """Configurar variables de entorno"""
    print("⚙️ Configurando bot...")
    
    # Crear archivo de configuración
    config_usuario = {{
        "telegram_bot_token": "",
        "telegram_chat_id": "",
        "intervalo_segundos": 120,
        "puntuacion_minima": 5,
        "filtro_horas": 24,
        "auto_actualizar": True
    }}
    
    with open("config_usuario.json", "w") as f:
        json.dump(config_usuario, f, indent=2)
    
    print("   ✅ config_usuario.json creado")
    print("   📝 Edítalo con tus datos de Telegram")

def crear_accesos_directos():
    """Crear accesos directos según el sistema"""
    sistema = platform.system().lower()
    
    if sistema == "darwin":  # macOS
        # Crear app para macOS
        app_path = "/Applications/Bot Inmobiliario 2.0.app"
        if not os.path.exists(app_path):
            os.makedirs(f"{{app_path}}/Contents/MacOS")
            os.makedirs(f"{{app_path}}/Contents/Resources")
            
            # Crear ejecutable
            ejecutable = f"""#!/bin/bash
cd "$(dirname "$0")/../../../Resources"
python3 main.py
"""
            with open(f"{{app_path}}/Contents/MacOS/Bot Inmobiliario 2.0", "w") as f:
                f.write(ejecutable)
            os.chmod(f"{{app_path}}/Contents/MacOS/Bot Inmobiliario 2.0", 0o755)
            
            # Crear Info.plist
            info_plist = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Bot Inmobiliario 2.0</string>
    <key>CFBundleIdentifier</key>
    <string>com.botinmobiliario.app</string>
    <key>CFBundleName</key>
    <string>Bot Inmobiliario 2.0</string>
    <key>CFBundleVersion</key>
    <string>2.0.1</string>
</dict>
</plist>'''
            with open(f"{{app_path}}/Contents/Info.plist", "w") as f:
                f.write(info_plist)
            
            print(f"   ✅ App macOS creada: {{app_path}}")
        
        # Crear acceso directo
        desktop_path = os.path.expanduser("~/Desktop/Bot Inmobiliario 2.0.command")
        with open(desktop_path, "w") as f:
            f.write(f"""#!/bin/bash
cd "{os.getcwd()}"
python3 main.py
""")
        os.chmod(desktop_path, 0o755)
        print("   ✅ Acceso directo en Desktop")
        
    elif sistema == "windows":
        # Crear acceso directo para Windows
        desktop_path = os.path.expanduser("~/Desktop/Bot Inmobiliario 2.0.bat")
        with open(desktop_path, "w") as f:
            f.write(f"""@echo off
cd "{os.getcwd()}"
python main.py
pause""")
        print("   ✅ Acceso directo en Desktop")
        
    else:  # Linux
        desktop_path = os.path.expanduser("~/Desktop/bot-inmobiliario-2.0.sh")
        with open(desktop_path, "w") as f:
            f.write(f"""#!/bin/bash
cd "{os.getcwd()}"
python3 main.py""")
        os.chmod(desktop_path, 0o755)
        print("   ✅ Acceso directo en Desktop")

def main():
    """Función principal del instalador"""
    print("·" * 60)
    print("INSTALADOR BOT INMOBILIARIO 2.0 - COMPLETO")
    print("·" * 60)
    print(f"Timestamp: {{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}}")
    print(f"Sistema: {{platform.system()}} {{platform.release()}}")
    print()
    
    print("🚀 Iniciando instalación completa...")
    print()
    
    # 1. Instalar dependencias
    instalar_dependencias()
    print()
    
    # 2. Configurar bot
    configurar_bot()
    print()
    
    # 3. Crear accesos directos
    crear_accesos_directos()
    print()
    
    print("✅ ¡Instalación completada!")
    print()
    print("📋 Siguientes pasos:")
    print("   1. Edita 'config_usuario.json' con tu token de Telegram")
    print("   2. Ejecuta 'Bot Inmobiliario 2.0' desde Desktop")
    print("   3. ¡Listo para recibir leads!")
    print()
    print("🔄 Para actualizar: ejecuta 'actualizador.py'")
    print("·" * 60)

if __name__ == "__main__":
    main()
"""
    
    with open(f"{carpeta_instalador}/instalar.py", "w") as f:
        f.write(instalador)
    print("   ✅ instalar.py")
    
    # 5. Crear launcher principal
    launcher = f"""#!/usr/bin/env python3
# Launcher principal Bot Inmobiliario 2.0

import os
import sys
import subprocess
import json
from datetime import datetime

def verificar_configuracion():
    """Verificar configuración de Telegram"""
    if os.path.exists("config_usuario.json"):
        with open("config_usuario.json", "r") as f:
            config = json.load(f)
        
        if not config.get("telegram_bot_token") or not config.get("telegram_chat_id"):
            print("❌ Configuración incompleta")
            print("📝 Edita 'config_usuario.json' con:")
            print("   - telegram_bot_token: TU_TOKEN")
            print("   - telegram_chat_id: TU_CHAT_ID")
            return False
        
        return True
    else:
        print("❌ No hay configuración")
        print("📝 Ejecuta 'instalar.py' primero")
        return False

def iniciar_bot():
    """Iniciar el bot principal"""
    if not verificar_configuracion():
        return
    
    print("🚀 Iniciando Bot Inmobiliario 2.0...")
    print("·" * 60)
    
    # Verificar actualizaciones
    if os.path.exists("actualizador.py"):
        try:
            subprocess.run([sys.executable, "actualizador.py"], check=True)
        except:
            pass  # Si hay error, continuar con el bot normal
    
    # Iniciar bot principal
    subprocess.run([sys.executable, "main.py"])

def main():
    """Función principal"""
    print("·" * 60)
    print("BOT INMOBILIARIO 2.0 - LAUNCHER")
    print("·" * 60)
    print(f"Timestamp: {{datetime.now().strftime('%H:%M:%S %d/%m/%Y')}}")
    print()
    
    iniciar_bot()

if __name__ == "__main__":
    main()
"""
    
    with open(f"{carpeta_instalador}/launcher.py", "w") as f:
        f.write(launcher)
    print("   ✅ launcher.py")
    
    # 6. Crear scripts de sistema
    print("4. Creando scripts de sistema...")
    
    # Script de instalación global
    script_global = f"""#!/bin/bash
# Instalador global Bot Inmobiliario 2.0

INSTALL_DIR="/usr/local/bin/bot-inmobiliario-2.0"
APP_DIR="/Applications/Bot Inmobiliario 2.0.app"

echo "🚀 Instalando Bot Inmobiliario 2.0 globalmente..."

# Crear directorio de instalación
sudo mkdir -p "$INSTALL_DIR"

# Copiar archivos
sudo cp -r "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo/"* "$INSTALL_DIR/"

# Crear app para macOS
if [ ! -d "$APP_DIR" ]; then
    sudo mkdir -p "$APP_DIR/Contents/MacOS"
    sudo mkdir -p "$APP_DIR/Contents/Resources"
    
    sudo cp "$INSTALL_DIR/launcher.py" "$APP_DIR/Contents/MacOS/Bot Inmobiliario 2.0"
    sudo chmod +x "$APP_DIR/Contents/MacOS/Bot Inmobiliario 2.0"
fi

# Crear comando global
echo '#!/bin/bash' | sudo tee /usr/local/bin/bot-inmobiliario > /dev/null
echo 'cd "$INSTALL_DIR" && python3 launcher.py' | sudo tee -a /usr/local/bin/bot-inmobiliario > /dev/null
sudo chmod +x /usr/local/bin/bot-inmobiliario

echo "✅ ¡Instalación global completada!"
echo "🚀 Ejecuta: bot-inmobiliario"
echo "📱 O abre la app desde Applications"
"""
    
    with open(f"{carpeta_instalador}/install_global.sh", "w") as f:
        f.write(script_global)
    print("   ✅ install_global.sh")
    
    # 7. Crear README completo
    readme_completo = f"""# BOT INMOBILIARIO 2.0 - INSTALADOR COMPLETO

## 🚀 Instalación Rápida

### Opción 1: Instalador Automático
```bash
python3 instalar.py
```

### Opción 2: Instalación Global
```bash
sudo ./install_global.sh
```

### Opción 3: Inicio Rápido
```bash
python3 launcher.py
```

## 🔄 Auto-Actualizaciones

El bot se actualiza automáticamente cada vez que se inicia:

1. **Verifica versión** en GitHub
2. **Descarga actualizaciones** si existen
3. **Aplica cambios** automáticamente
4. **Reinicia el bot** con nueva versión

## ⚙️ Configuración

Edita `config_usuario.json`:

```json
{{
  "telegram_bot_token": "TU_TOKEN_AQUI",
  "telegram_chat_id": "TU_CHAT_ID_AQUI",
  "intervalo_segundos": 120,
  "puntuacion_minima": 5,
  "filtro_horas": 24,
  "auto_actualizar": true
}}
```

## 📱 Accesos Directos

- **macOS:** Applications → Bot Inmobiliario 2.0.app
- **Windows:** Desktop → Bot Inmobiliario 2.0.bat
- **Linux:** Desktop → bot-inmobiliario-2.0.sh

## 🎯 Características

✅ **Auto-actualizaciones** desde GitHub
✅ **Instalación global** en el sistema
✅ **Accesos directos** en Desktop/Applications
✅ **Configuración fácil** con JSON
✅ **Todos los archivos** incluidos
✅ **Multiplataforma** (Mac/Windows/Linux)

## 📊 Configuración Actual

- ⏱️ **Intervalo:** 2 minutos
- 📅 **Filtro:** Anuncios de hoy (24h)
- 🎯 **Puntuación:** 5+ puntos (muy permisivo)
- 🏠 **Búsqueda:** Compra + Alquiler
- 📍 **Zonas:** Rubí, Sant Cugat, Sabadell, Terrassa
- 🔄 **Auto-actualizar:** Sí

---
**Instalador creado: {datetime.now().strftime('%d/%m/%Y %H:%M')}**
**Versión: 2.0.1 Completo**
"""
    
    with open(f"{carpeta_instalador}/README.md", "w") as f:
        f.write(readme_completo)
    print("   ✅ README.md completo")
    
    # 8. Crear requirements completo
    requirements_completo = """# Bot Inmobiliario 2.0 - Dependencias Completas
requests>=2.28.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
python-telegram-bot>=20.0
urllib3>=1.26.0
certifi>=2022.12.7
"""
    
    with open(f"{carpeta_instalador}/requirements.txt", "w") as f:
        f.write(requirements_completo)
    print("   ✅ requirements.txt completo")
    
    print()
    print("5. Creando paquetes de distribución...")
    
    # 9. Crear instalador comprimido
    import zipfile
    zip_path = "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_instalador):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, carpeta_instalador)
                zipf.write(file_path, arcname)
    
    print(f"   ✅ Bot-Inmobiliario-Instalador-Completo.zip")
    
    # 10. Crear DMG para Mac
    try:
        dmg_path = "/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo.dmg"
        subprocess.run([
            "hdiutil", "create",
            "-volname", "Bot Inmobiliario 2.0 - Instalador",
            "-srcfolder", carpeta_instalador,
            "-ov",
            dmg_path
        ], check=True, capture_output=True)
        print(f"   ✅ Bot-Inmobiliario-Instalador-Completo.dmg")
    except:
        print("   ⚠️ No se pudo crear DMG (requiere macOS)")
    
    print()
    print("6. ¡INSTALADOR COMPLETO CREADO!")
    print("·" * 60)
    print(f"📁 Carpeta: {carpeta_instalador}")
    print(f"📦 ZIP: /Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo.zip")
    
    if os.path.exists("/Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo.dmg"):
        print(f"💿 DMG: /Users/damianortells/Desktop/Bot-Inmobiliario-Instalador-Completo.dmg")
    
    print()
    print("🎯 Características del instalador:")
    print("   ✅ Auto-actualizaciones desde GitHub")
    print("   ✅ Instalación global en el sistema")
    print("   ✅ Accesos directos automáticos")
    print("   ✅ Configuración fácil con JSON")
    print("   ✅ Todos los archivos incluidos")
    print("   ✅ Multiplataforma (Mac/Windows/Linux)")
    print("   ✅ Launcher inteligente")
    print("   ✅ Verificación de configuración")
    print()
    print("📋 Para usar:")
    print("   1. Descomprimir el instalador")
    print("   2. Ejecutar 'python3 instalar.py'")
    print("   3. Configurar Telegram en config_usuario.json")
    print("   4. ¡Listo para recibir leads con auto-actualizaciones!")
    print("·" * 60)

if __name__ == "__main__":
    crear_instalador_completo()
