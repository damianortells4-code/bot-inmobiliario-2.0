#!/usr/bin/env python3
"""
Dashboard visual bonito con estadísticas en tiempo real
Funciona localmente sin necesidad de servidor externo
"""

import time
import sqlite3
import threading
from datetime import datetime, timedelta
import sys
import os

class DashboardVisual:
    """Dashboard visual con estadísticas en tiempo real"""
    
    def __init__(self):
        self.db_path = "anuncios.db"
        self.estadisticas = {
            'total_anuncios': 0,
            'hoy': 0,
            'ayer': 0,
            'ultima_semana': 0,
            'ultimas_24h': 0,
            'mejores_hoy': 0,
            'notificados_hoy': 0,
            'ultima_busqueda': None,
            'estado_actual': 'esperando',
            'ciclos_hoy': 0,
            'promedio_por_ciclo': 0
        }
        
    def limpiar_pantalla(self):
        """Limpiar pantalla para mostrar dashboard"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def obtener_estadisticas(self):
        """Obtener estadísticas de la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de anuncios
            cursor.execute('SELECT COUNT(*) FROM anuncios')
            self.estadisticas['total_anuncios'] = cursor.fetchone()[0]
            
            # Anuncios de hoy
            hoy = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM anuncios WHERE DATE(fecha) = ?', (hoy,))
            self.estadisticas['hoy'] = cursor.fetchone()[0]
            
            # Anuncios de ayer
            ayer = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            cursor.execute('SELECT COUNT(*) FROM anuncios WHERE DATE(fecha) = ?', (ayer,))
            self.estadisticas['ayer'] = cursor.fetchone()[0]
            
            # Últimas 24 horas
            cursor.execute('''
                SELECT COUNT(*) FROM anuncios 
                WHERE fecha > datetime('now', '-24 hours')
            ''')
            self.estadisticas['ultimas_24h'] = cursor.fetchone()[0]
            
            # Última semana
            cursor.execute('''
                SELECT COUNT(*) FROM anuncios 
                WHERE fecha > datetime('now', '-7 days')
            ''')
            self.estadisticas['ultima_semana'] = cursor.fetchone()[0]
            
            # Últimos anuncios con detalles
            cursor.execute('''
                SELECT titulo, fecha FROM anuncios 
                ORDER BY fecha DESC LIMIT 5
            ''')
            ultimos_anuncios = cursor.fetchall()
            
            conn.close()
            return ultimos_anuncios
            
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return []
    
    def dibujar_dashboard(self, estado="esperando", ciclo_info=None):
        """Dibujar dashboard visual"""
        self.limpiar_pantalla()
        
        # Obtener estadísticas
        ultimos_anuncios = self.obtener_estadisticas()
        
        # Header
        print(" " * 60)
        print(" " * 20 + "BOT INMOBILIARIO 2.0")
        print(" " * 25 + "Dashboard Visual")
        print(" " * 60)
        
        # Estado actual con colores
        colores = {
            'buscando': '  BUSCANDO ACTIVAMENTE  ',
            'analizando': '     ANALIZANDO      ',
            'notificando': '   NOTIFICANDO    ',
            'esperando': '     ESPERANDO      ',
            'error': '       ERROR        '
        }
        
        estado_text = colores.get(estado, '     ESPERANDO      ')
        
        # Estado visual
        print(" " * 60)
        print(" " * 15 + f"ESTADO ACTUAL: {estado_text}")
        print(" " * 60)
        print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
        print()
        
        # Estadísticas principales
        print(" " * 60)
        print(" " * 25 + "ESTADÍSTICAS")
        print(" " * 60)
        
        # Cuadro de estadísticas
        print(" " * 10 + "Total anuncios: " + " " * 10 + f"{self.estadisticas['total_anuncios']}")
        print(" " * 10 + "Anuncios hoy:   " + " " * 10 + f"{self.estadisticas['hoy']}")
        print(" " * 10 + "Anuncios ayer:  " + " " * 10 + f"{self.estadisticas['ayer']}")
        print(" " * 10 + "Últimas 24h:    " + " " * 10 + f"{self.estadisticas['ultimas_24h']}")
        print(" " * 10 + "Última semana:  " + " * * 10 + f"{self.estadisticas['ultima_semana']}")
        print()
        
        # Gráfico simple de barras
        print(" " * 60)
        print(" " * 23 + "ACTIVIDAD RECIENTE")
        print(" " * 60)
        
        max_val = max(self.estadisticas['hoy'], self.estadisticas['ayer'], 1)
        
        # Barra de hoy
        bar_hoy = " " * 10 + "Hoy:   " + " " * 2
        bar_hoy += " " * int(20 * self.estadisticas['hoy'] / max_val) + f" {self.estadisticas['hoy']}"
        print(bar_hoy)
        
        # Barra de ayer  
        bar_ayer = " " * 10 + "Ayer:  " + " " * 2
        bar_ayer += " " * int(20 * self.estadisticas['ayer'] / max_val) + f" {self.estadisticas['ayer']}"
        print(bar_ayer)
        
        print()
        
        # Últimos anuncios
        print(" " * 60)
        print(" " * 22 + "ÚLTIMOS ANUNCIOS")
        print(" " * 60)
        
        if ultimos_anuncios:
            for i, (titulo, fecha) in enumerate(ultimos_anuncios, 1):
                fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
                titulo_corto = titulo[:40] + "..." if len(titulo) > 40 else titulo
                print(f" {i}. [{fecha_formateada}] {titulo_corto}")
        else:
            print(" " * 15 + "No hay anuncios recientes")
        
        print()
        
        # Información del ciclo
        if ciclo_info:
            print(" " * 60)
            print(" " * 20 + "INFORMACIÓN DEL CICLO")
            print(" " * 60)
            print(f" Candidatos encontrados: {ciclo_info.get('candidatos', 0)}")
            print(f" Anuncios recientes:    {ciclo_info.get('recientes', 0)}")
            print(f" Mejores anuncios:      {ciclo_info.get('mejores', 0)}")
            print(f" Nuevos notificados:    {ciclo_info.get('nuevos', 0)}")
            print()
        
        # Footer
        print(" " * 60)
        print(" " * 18 + "Actualización automática cada 5 segundos")
        print(" " * 60)
        
    def iniciar_dashboard(self):
        """Iniciar dashboard en segundo plano"""
        def actualizar():
            while True:
                try:
                    # Aquí podríamos obtener estado real del bot
                    # Por ahora mostramos estado simulado
                    self.dibujar_dashboard()
                    time.sleep(5)
                except KeyboardInterrupt:
                    break
        
        thread = threading.Thread(target=actualizar)
        thread.daemon = True
        thread.start()
        return thread

def mostrar_dashboard_simple():
    """Mostrar dashboard simple sin threading"""
    dashboard = DashboardVisual()
    
    try:
        while True:
            dashboard.dibujar_dashboard()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nDashboard detenido.")

if __name__ == "__main__":
    print("Iniciando dashboard visual...")
    print("Presiona Ctrl+C para detener")
    print()
    
    mostrar_dashboard_simple()
