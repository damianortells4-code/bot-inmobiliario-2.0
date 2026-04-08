#!/usr/bin/env python3
"""
Monitor simple del bot - Muestra estadísticas básicas
"""

import sqlite3
import time
from datetime import datetime
import os

def limpiar_pantalla():
    """Limpiar pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_estadisticas():
    """Obtener estadísticas básicas"""
    try:
        conn = sqlite3.connect('anuncios.db')
        cursor = conn.cursor()
        
        # Total anuncios
        cursor.execute('SELECT COUNT(*) FROM anuncios')
        total = cursor.fetchone()[0]
        
        # Anuncios hoy
        hoy = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM anuncios WHERE DATE(fecha) = ?', (hoy,))
        hoy_count = cursor.fetchone()[0]
        
        # Últimos 5 anuncios
        cursor.execute('SELECT titulo, fecha FROM anuncios ORDER BY fecha DESC LIMIT 5')
        ultimos = cursor.fetchall()
        
        conn.close()
        return total, hoy_count, ultimos
    except:
        return 0, 0, []

def mostrar_monitor():
    """Mostrar monitor simple"""
    while True:
        limpiar_pantalla()
        
        total, hoy, ultimos = obtener_estadisticas()
        
        print("=" * 50)
        print("🏠 BOT INMOBILIARIO 2.0 - MONITOR")
        print("=" * 50)
        print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print()
        print("📊 ESTADÍSTICAS:")
        print(f"   Total anuncios: {total}")
        print(f"   Anuncios hoy: {hoy}")
        print()
        print("📋 ÚLTIMOS ANUNCIOS:")
        
        if ultimos:
            for i, (titulo, fecha) in enumerate(ultimos, 1):
                try:
                    # Quitar milisegundos y T si existe
                    fecha_limpia = fecha.split('.')[0].replace('T', ' ')
                    fecha_formateada = datetime.strptime(fecha_limpia, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                except:
                    fecha_formateada = "??"
                
                titulo_corto = titulo[:45] + "..." if len(titulo) > 45 else titulo
                print(f"   {i}. [{fecha_formateada}] {titulo_corto}")
        else:
            print("   No hay anuncios aún")
        
        print()
        print("🔄 Actualizando en 10 segundos...")
        print("   Presiona Ctrl+C para salir")
        print("=" * 50)
        
        time.sleep(10)

if __name__ == "__main__":
    print("Iniciando monitor del bot...")
    print("Esto muestra estadísticas del bot en tiempo real")
    print()
    
    try:
        mostrar_monitor()
    except KeyboardInterrupt:
        print("\n¡Monitor detenido!")
