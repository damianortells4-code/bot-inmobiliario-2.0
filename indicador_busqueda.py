#!/usr/bin/env python3
"""
Indicador visual en tiempo real para saber si el bot está buscando activamente
"""

import threading
import time
import sys
from datetime import datetime

class IndicadorBusqueda:
    """Indicador visual que muestra si el bot está buscando activamente"""
    
    def __init__(self):
        self.estado = "esperando"
        self.detener = False
        self.hilo = None
        
    def iniciar(self):
        """Iniciar el indicador visual en segundo plano"""
        self.detener = False
        self.hilo = threading.Thread(target=self._mostrar_indicador)
        self.hilo.daemon = True
        self.hilo.start()
        
    def detener(self):
        """Detener el indicador visual"""
        self.detener = True
        if self.hilo:
            self.hilo.join(timeout=1)
            
    def set_estado(self, estado):
        """Cambiar el estado del indicador"""
        self.estado = estado
        
    def _mostrar_indicador(self):
        """Mostrar indicador visual en tiempo real"""
        caracteres = {
            "buscando": "/searching  ",
            "analizando": "analyzing  ",
            "notificando": "notifying  ",
            "esperando": "waiting    ",
            "error": "error      "
        }
        
        colores = {
            "buscando": "\033[93m",  # Amarillo
            "analizando": "\033[94m",  # Azul
            "notificando": "\033[92m",  # Verde
            "esperando": "\033[90m",  # Gris
            "error": "\033[91m"  # Rojo
        }
        
        reset_color = "\033[0m"
        
        while not self.detener:
            estado_actual = self.estado
            caracter = caracteres.get(estado_actual, "waiting    ")
            color = colores.get(estado_actual, "\033[90m")
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Mostrar indicador en una sola línea
            sys.stdout.write(f"\r{color}[{timestamp}] {caracter}{reset_color}")
            sys.stdout.flush()
            
            time.sleep(1)
            
    def limpiar_linea(self):
        """Limpiar la línea del indicador"""
        sys.stdout.write("\r" + " " * 50 + "\r")
        sys.stdout.flush()

# Instancia global del indicador
indicador = IndicadorBusqueda()

def iniciar_indicador():
    """Iniciar el indicador visual"""
    indicador.iniciar()
    
def detener_indicador():
    """Detener el indicador visual"""
    indicador.detener()
    indicador.limpiar_linea()
    
def set_estado_busqueda(estado):
    """Cambiar estado del indicador"""
    indicador.set_estado(estado)

if __name__ == "__main__":
    # Prueba del indicador
    print("Prueba del indicador visual:")
    iniciar_indicador()
    
    estados = ["esperando", "buscando", "analizando", "notificando", "esperando"]
    
    for estado in estados:
        set_estado_busqueda(estado)
        print(f"\nEstado actual: {estado}")
        time.sleep(3)
    
    detener_indicador()
    print("\n¡Indicador detenido!")
