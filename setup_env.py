#!/usr/bin/env python3
import sys
import os
import subprocess

def setup_environment():
    """Configura el entorno e instala dependencias"""
    print("Configurando entorno para el bot inmobiliario...")
    
    # Añadir el path global de Python para que encuentre los paquetes
    global_paths = [
        '/Users/damianortells/Library/Python/3.9/lib/python/site-packages',
        '/usr/local/lib/python3.9/site-packages',
        '/usr/lib/python3.9/site-packages'
    ]
    
    for path in global_paths:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print("Paths de Python configurados")
    
    # Verificar que los paquetes estén disponibles
    try:
        import requests
        import bs4
        import lxml
        print("Todos los paquetes necesarios están disponibles")
        return True
    except ImportError as e:
        print(f"Falta el paquete: {e}")
        print("Instalando paquetes...")
        
        packages = ['requests', 'beautifulsoup4', 'lxml']
        for package in packages:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', package], 
                             check=True, capture_output=True)
                print(f"Paquete {package} instalado")
            except subprocess.CalledProcessError:
                print(f"No se pudo instalar {package}")
        
        return False

if __name__ == "__main__":
    setup_environment()
    print("Entorno configurado. Ahora ejecuta: python3 main.py")
