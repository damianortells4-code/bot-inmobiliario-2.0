import subprocess
import sys

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ["requests", "beautifulsoup4", "lxml"]

for package in packages:
    print(f"Instalando {package}...")
    try:
        install_package(package)
        print(f"¡{package} instalado correctamente!")
    except Exception as e:
        print(f"Error instalando {package}: {e}")

print("Instalación completada. Ahora puedes ejecutar python3 main.py")
