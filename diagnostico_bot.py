#!/usr/bin/env python3
"""
Diagnóstico del bot para ver qué está pasando
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
from database import anuncio_existente, guardar_anuncio
from filtros import es_particular
from filtros_tiempo import filtrar_anuncios_recientes
from puntuacion_anuncios import puntuar_anuncios, obtener_mejores_anuncios
from scraper_internet import buscar_internet
from urls import normalizar_url_anuncio
from verificador import anuncio_activo

def diagnostico_completo():
    """Diagnóstico completo del bot"""
    
    print("·" * 60)
    print("DIAGNÓSTICO COMPLETO DEL BOT")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Buscar anuncios
    print("1. BUSCANDO ANUNCIOS...")
    anuncios = buscar_internet()
    print(f"   Total encontrados: {len(anuncios)}")
    
    if not anuncios:
        print("   ERROR: No se encontraron anuncios")
        return
    
    # 2. Filtrar por tiempo
    print("\n2. FILTRANDO POR TIEMPO...")
    anuncios_recientes = filtrar_anuncios_recientes(anuncios, max_minutos=60)  # 1 hora
    print(f"   Anuncios recientes (1 hora): {len(anuncios_recientes)}")
    
    # 3. Analizar primeros 10 anuncios
    print("\n3. ANALIZANDO PRIMEROS 10 ANUNCIOS...")
    for i, anuncio in enumerate(anuncios_recientes[:10], 1):
        titulo = anuncio['titulo']
        link = anuncio['link']
        fuente = anuncio.get('fuente', 'desconocido')
        
        print(f"\n   Anuncio {i}:")
        print(f"   Título: {titulo[:60]}...")
        print(f"   Fuente: {fuente}")
        print(f"   Link: {link[:50]}...")
        
        # Verificar si es particular
        es_part = es_particular(titulo)
        print(f"   ¿Es particular?: {'SÍ' if es_part else 'NO'}")
        
        # Verificar si está activo
        try:
            activo = anuncio_activo(link)
            print(f"   ¿Está activo?: {'SÍ' if activo else 'NO'}")
        except:
            print(f"   ¿Está activo?: ERROR al verificar")
        
        # Verificar si ya existe
        clave = normalizar_url_anuncio(link)
        if clave:
            existe = anuncio_existente(clave)
            print(f"   ¿Ya existe en BD?: {'SÍ' if existe else 'NO'}")
    
    # 4. Probar puntuación con umbral bajo
    print("\n4. PROBANDO PUNTUACIÓN...")
    anuncios_para_puntuar = []
    for anuncio in anuncios_recientes:
        anuncios_para_puntuar.append({
            'titulo': anuncio['titulo'],
            'link': anuncio['link'],
            'descripcion': anuncio.get('descripcion', ''),
            'fuente': anuncio.get('fuente', 'desconocido')
        })
    
    # Probar con puntuación muy baja
    anuncios_puntuados_bajo, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=1.0)
    print(f"   Con puntuación mínima 1: {len(anuncios_puntuados_bajo)} anuncios")
    
    # Probar con puntuación actual (30)
    anuncios_puntuados_actual, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=30.0)
    print(f"   Con puntuación mínima 30: {len(anuncios_puntuados_actual)} anuncios")
    
    # 5. Resumen
    print("\n" + "·" * 60)
    print("RESUMEN DEL DIAGNÓSTICO:")
    print(f"Total anuncios: {len(anuncios)}")
    print(f"Anuncios recientes: {len(anuncios_recientes)}")
    print(f"Anuncios con puntuación > 1: {len(anuncios_puntuados_bajo)}")
    print(f"Anuncios con puntuación > 30: {len(anuncios_puntuados_actual)}")
    print()
    
    # 6. Recomendaciones
    print("RECOMENDACIONES:")
    if len(anuncios) == 0:
        print("- ERROR: El scraper no encuentra nada")
    elif len(anuncios_recientes) == 0:
        print("- ERROR: Todos los anuncios son viejos (>60 min)")
    elif len(anuncios_puntuados_bajo) == 0:
        print("- ERROR: La puntuación no funciona")
    elif len(anuncios_puntuados_actual) == 0:
        print("- SOLUCIÓN: Bajar puntuación mínima a 10-15")
    else:
        print("- El bot funciona, solo es cuestión de tiempo")
    
    print("·" * 60)

if __name__ == "__main__":
    diagnostico_completo()
