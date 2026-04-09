#!/usr/bin/env python3
"""
DEBUG TOTAL - Diagnóstico completo de todos los problemas
"""

import sys
import os
import traceback
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

def debug_paso_a_paso():
    """Debug paso a paso de todo el proceso"""
    
    print("·" * 60)
    print("DEBUG TOTAL - DIAGNÓSTICO COMPLETO")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # 1. Importaciones
    print("1. IMPORTACIONES...")
    try:
        import config
        print("   config.py: OK")
    except Exception as e:
        print(f"   config.py: ERROR - {e}")
        return
    
    try:
        from database import anuncio_existente, guardar_anuncio
        print("   database.py: OK")
    except Exception as e:
        print(f"   database.py: ERROR - {e}")
        return
    
    try:
        from filtros import es_particular
        print("   filtros.py: OK")
    except Exception as e:
        print(f"   filtros.py: ERROR - {e}")
        return
    
    try:
        from filtros_tiempo import filtrar_anuncios_recientes
        print("   filtros_tiempo.py: OK")
    except Exception as e:
        print(f"   filtros_tiempo.py: ERROR - {e}")
        return
    
    try:
        from puntuacion_anuncios import puntuar_anuncios, obtener_mejores_anuncios
        print("   puntuacion_anuncios.py: OK")
    except Exception as e:
        print(f"   puntuacion_anuncios.py: ERROR - {e}")
        return
    
    try:
        from scraper_internet import buscar_internet
        print("   scraper_internet.py: OK")
    except Exception as e:
        print(f"   scraper_internet.py: ERROR - {e}")
        return
    
    try:
        from urls import normalizar_url_anuncio
        print("   urls.py: OK")
    except Exception as e:
        print(f"   urls.py: ERROR - {e}")
        return
    
    try:
        from verificador import anuncio_activo
        print("   verificador.py: OK")
    except Exception as e:
        print(f"   verificador.py: ERROR - {e}")
        return
    
    print()
    
    # 2. Configuración
    print("2. CONFIGURACIÓN...")
    print(f"   DB_PATH: {config.DB_PATH}")
    print(f"   INTERVALO_SEGUNDOS: {config.INTERVALO_SEGUNDOS}")
    print(f"   ZONAS: {len(config.ZONAS)}")
    print(f"   USAR_DUCKDUCKGO: {config.USAR_DUCKDUCKGO}")
    print(f"   USAR_PISOS: {config.USAR_PISOS}")
    print(f"   USAR_FOTOCASA: {config.USAR_FOTOCASA}")
    print(f"   USAR_IDEALISTA: {config.USAR_IDEALISTA}")
    print(f"   USAR_MILANUNCIOS: {config.USAR_MILANUNCIOS}")
    print()
    
    # 3. Base de datos
    print("3. BASE DE DATOS...")
    try:
        if os.path.exists(config.DB_PATH):
            print(f"   Base de datos: EXISTE ({os.path.getsize(config.DB_PATH)} bytes)")
        else:
            print(f"   Base de datos: NO EXISTE")
    except Exception as e:
        print(f"   Base de datos: ERROR - {e}")
    print()
    
    # 4. Scraper
    print("4. SCRAPER - Buscando anuncios...")
    try:
        anuncios = buscar_internet()
        print(f"   Anuncios encontrados: {len(anuncios)}")
        
        if len(anuncios) == 0:
            print("   ADVERTENCIA: No se encontraron anuncios")
            return
        
        # Mostrar primeros 3 anuncios
        print("   Primeros 3 anuncios:")
        for i, anuncio in enumerate(anuncios[:3], 1):
            print(f"     {i}. {anuncio['titulo'][:50]}...")
            print(f"        Fuente: {anuncio.get('fuente', 'desconocido')}")
            print(f"        Link: {anuncio['link'][:50]}...")
        
    except Exception as e:
        print(f"   Scraper: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 5. Filtro tiempo
    print("5. FILTRO TIEMPO...")
    try:
        anuncios_recientes = filtrar_anuncios_recientes(anuncios, max_minutos=60)
        print(f"   Anuncios recientes: {len(anuncios_recientes)}")
        
        if len(anuncios_recientes) == 0:
            print("   ADVERTENCIA: No hay anuncios recientes")
            return
            
    except Exception as e:
        print(f"   Filtro tiempo: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 6. Puntuación
    print("6. PUNTUACIÓN...")
    try:
        anuncios_para_puntuar = []
        for anuncio in anuncios_recientes:
            anuncios_para_puntuar.append({
                'titulo': anuncio['titulo'],
                'link': anuncio['link'],
                'descripcion': anuncio.get('descripcion', ''),
                'fuente': anuncio.get('fuente', 'desconocido')
            })
        
        # Probar con umbral muy bajo
        anuncios_puntuados, resumen = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=1.0)
        print(f"   Con umbral 1: {len(anuncios_puntuados)} anuncios")
        
        if len(anuncios_puntuados) == 0:
            print("   ADVERTENCIA: Ningún anuncio pasa la puntuación")
            return
        
        # Mostrar puntuaciones
        print("   Puntuaciones de los primeros 3:")
        for i, anuncio in enumerate(anuncios_puntuados[:3], 1):
            print(f"     {i}. {anuncio.titulo[:30]}... - {anuncio.puntuacion_total} pts")
            
    except Exception as e:
        print(f"   Puntuación: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 7. Verificador
    print("7. VERIFICADOR...")
    try:
        # Probar con el primer anuncio
        primer_anuncio = anuncios_recientes[0]
        link = primer_anuncio['link']
        
        print(f"   Probando verificador con: {link[:50]}...")
        activo = anuncio_activo(link)
        print(f"   Está activo: {'SÍ' if activo else 'NO'}")
        
    except Exception as e:
        print(f"   Verificador: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 8. Filtro particulares
    print("8. FILTRO PARTICULARES...")
    try:
        # Probar con el primer anuncio
        titulo = primer_anuncio['titulo']
        print(f"   Probando es_particular con: {titulo[:50]}...")
        
        es_part = es_particular(titulo)
        print(f"   Es particular: {'SÍ' if es_part else 'NO'}")
        
    except Exception as e:
        print(f"   Filtro particulares: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 9. Base de datos - guardar
    print("9. BASE DE DATOS - Guardar...")
    try:
        clave = normalizar_url_anuncio(primer_anuncio['link'])
        print(f"   Clave normalizada: {clave[:50]}...")
        
        existe = anuncio_existente(clave)
        print(f"   Ya existe: {'SÍ' if existe else 'NO'}")
        
        if not existe:
            guardar_anuncio(clave, primer_anuncio['titulo'], primer_anuncio['link'])
            print("   Guardado: OK")
        
    except Exception as e:
        print(f"   Base de datos - guardar: ERROR - {e}")
        traceback.print_exc()
        return
    
    print()
    
    # 10. Telegram
    print("10. TELEGRAM...")
    try:
        from telegram_alert import enviar_mensaje
        
        mensaje_test = f"DEBUG TEST - {datetime.now().strftime('%H:%M:%S')}"
        enviado = enviar_mensaje(mensaje_test)
        print(f"   Telegram: {'OK' if enviado else 'ERROR'}")
        
    except Exception as e:
        print(f"   Telegram: ERROR - {e}")
        traceback.print_exc()
    
    print()
    print("·" * 60)
    print("DIAGNÓSTICO COMPLETADO")
    print("·" * 60)

if __name__ == "__main__":
    debug_paso_a_paso()
