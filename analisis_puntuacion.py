#!/usr/bin/env python3
"""
Análisis de puntuación para ver si es muy alta
"""

import sys
import os
from datetime import datetime

# Configurar automáticamente el entorno para encontrar los paquetes
global_paths = [
    '/Users/damianortells/Library/Python/3.9/lib/python/site-packages',
    '/usr/local/lib/python3.9/site-packages',
    '/usr/lib/python3.9/site-packages'
]

for path in global_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

import config
from filtros_tiempo import filtrar_anuncios_recientes
from scraper_internet import buscar_internet

def analizar_puntuaciones():
    """Analizar las puntuaciones reales de los anuncios"""
    
    print("·" * 60)
    print("ANÁLISIS DE PUNTUACIONES")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Buscar anuncios
    print("1. Buscando anuncios...")
    anuncios = buscar_internet()
    print(f"   Total encontrados: {len(anuncios)}")
    
    # 2. Filtrar por tiempo
    print("\n2. Filtrando por tiempo...")
    anuncios_recientes = filtrar_anuncios_recientes(anuncios, max_minutos=60)
    print(f"   Anuncios recientes: {len(anuncios_recientes)}")
    
    # 3. Analizar puntuaciones con diferentes umbrales
    from puntuacion_anuncios import puntuar_anuncios
    
    anuncios_para_puntuar = []
    for anuncio in anuncios_recientes:
        anuncios_para_puntuar.append({
            'titulo': anuncio['titulo'],
            'link': anuncio['link'],
            'descripcion': anuncio.get('descripcion', ''),
            'fuente': anuncio.get('fuente', 'desconocido')
        })
    
    # Probar diferentes umbrales
    umbrales = [1, 5, 10, 15, 20, 25, 30, 35, 40, 50]
    
    print("\n3. Analizando puntuaciones por umbral:")
    print("Umbral | Anuncios que pasan | % del total")
    print("-" * 50)
    
    for umbral in umbrales:
        try:
            anuncios_puntuados, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=umbral)
            porcentaje = (len(anuncios_puntuados) / len(anuncios_recientes)) * 100 if anuncios_recientes else 0
            print(f"  {umbral:2d}   | {len(anuncios_puntuados):15d} | {porcentaje:5.1f}%")
        except Exception as e:
            print(f"  {umbral:2d}   | ERROR: {e}")
    
    # 4. Analizar distribución de puntuaciones
    print("\n4. Distribución de puntuaciones:")
    print("-" * 50)
    
    try:
        anuncios_puntuados, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=1.0)
        
        if anuncios_puntuados:
            puntuaciones = [a.puntuacion_total for a in anuncios_puntuados]
            puntuaciones.sort()
            
            print(f"   Mínima: {min(puntuaciones):.1f}")
            print(f"   Máxima: {max(puntuaciones):.1f}")
            print(f"   Promedio: {sum(puntuaciones)/len(puntuaciones):.1f}")
            print(f"   Mediana: {puntuaciones[len(puntuaciones)//2]:.1f}")
            
            # Percentiles
            import math
            for p in [25, 50, 75, 90]:
                idx = int(len(puntuaciones) * p / 100)
                print(f"   Percentil {p}%: {puntuaciones[idx]:.1f}")
        
    except Exception as e:
        print(f"   ERROR al analizar distribución: {e}")
    
    # 5. Recomendaciones
    print("\n5. RECOMENDACIONES:")
    print("-" * 50)
    
    try:
        anuncios_puntuados_10, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=10.0)
        anuncios_puntuados_20, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=20.0)
        anuncios_puntuados_30, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=30.0)
        
        total = len(anuncios_recientes)
        
        print(f"• Con umbral 10:  {len(anuncios_puntuados_10)}/{total} ({len(anuncios_puntuados_10)/total*100:.1f}%)")
        print(f"• Con umbral 20:  {len(anuncios_puntuados_20)}/{total} ({len(anuncios_puntuados_20)/total*100:.1f}%)")
        print(f"• Con umbral 30:  {len(anuncios_puntuados_30)}/{total} ({len(anuncios_puntuados_30)/total*100:.1f}%)")
        
        if len(anuncios_puntuados_10) == 0:
            print("• RECOMENDACIÓN: La puntuación es muy alta o hay error en el sistema")
        elif len(anuncios_puntuados_10) < 5:
            print("• RECOMENDACIÓN: Bajar a umbral 5-10 para más leads")
        elif len(anuncios_puntuados_20) < 10:
            print("• RECOMENDACIÓN: Umbral 15-20 es balanceado")
        else:
            print("• RECOMENDACIÓN: Umbral 10-15 es óptimo")
            
    except Exception as e:
        print(f"• ERROR en recomendaciones: {e}")
    
    print("\n" + "·" * 60)

if __name__ == "__main__":
    analizar_puntuaciones()
