import sys
import os

# Configurar automáticamente el entorno para encontrar los paquetes
global_paths = [
    '/Users/damianortells/Library/Python/3.9/lib/python/site-packages',
    '/usr/local/lib/python3.9/site-packages',
    '/usr/lib/python3.9/site-packages'
]

for path in global_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

import time
from datetime import datetime
import config
from database import anuncio_existente, guardar_anuncio
from filtros import es_particular
from filtros_tiempo import filtrar_anuncios_recientes
from puntuacion_anuncios import puntuar_anuncios, obtener_mejores_anuncios
from scraper_internet import buscar_internet
from telegram_alert import enviar_mensaje
from urls import normalizar_url_anuncio
from verificador import anuncio_activo
from indicador_busqueda import iniciar_indicador, detener, set_estado_busqueda

# Importar bot interactivo
try:
    from telegram_bot import start_telegram_thread
    TELEGRAM_INTERACTIVE = False  # Desactivado para evitar conflictos 409
except ImportError:
    print("python-telegram-bot no instalado. Solo modo alertas.")
    TELEGRAM_INTERACTIVE = False


def ciclo():
    set_estado_busqueda("buscando")
    print("·" * 60)
    print("BUSCANDO ANUNCIOS DE PARTICULARES")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Fuentes activas: DDG={config.USAR_DUCKDUCKGO} | Pisos={config.USAR_PISOS} | Fotocasa={config.USAR_FOTOCASA} | Idealista={config.USAR_IDEALISTA} | Milanuncios={config.USAR_MILANUNCIOS}")
    print(f"Zonas: {len(config.ZONAS)} configuradas (Rubí, Sant Cugat, Sabadell, Terrassa)")
    print(f"Intervalo: {config.INTERVALO_SEGUNDOS} segundos")
    print(f"Exigir palabra de particular: {config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO}")
    print("Anuncios recientes: últimos 30 minutos")
    if config.MAX_ANUNCIOS_POR_FUENTE is not None:
        print(f"Límite por fuente (pruebas): {config.MAX_ANUNCIOS_POR_FUENTE}")
    print("·" * 60)
    print("Iniciando búsqueda en portales...")
    print()

    anuncios = buscar_internet()
    print("Candidatos tras scrapers:", len(anuncios))

    # Filtrar por tiempo (últimos 30 minutos)
    print("Filtrando anuncios recientes...")
    set_estado_busqueda("analizando")
    anuncios_recientes = filtrar_anuncios_recientes(anuncios, max_minutos=30)
    print(f"Anuncios recientes: {len(anuncios_recientes)}")

    # Convertir anuncios a formato para puntuación
    anuncios_para_puntuar = []
    for anuncio in anuncios_recientes:
        anuncios_para_puntuar.append({
            'titulo': anuncio['titulo'],
            'link': anuncio['link'],
            'descripcion': anuncio.get('descripcion', ''),
            'fuente': anuncio.get('fuente', 'desconocido')
        })

    # Puntuar anuncios
    print("Analizando y puntuando anuncios...")
    anuncios_puntuados, resumen_puntuacion = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=20.0)
    
    # Obtener mejores anuncios
    mejores_anuncios = obtener_mejores_anuncios(anuncios_para_puntuar, top_n=10)
    
    # Mostrar resumen de puntuación
    print(resumen_puntuacion)
    
    print(f"Mejores anuncios encontrados: {len(mejores_anuncios)}")
    if mejores_anuncios:
        print("Top anuncios:")
        for i, anuncio in enumerate(mejores_anuncios[:5], 1):
            print(f"  {i}. {anuncio.titulo[:50]}... (puntuación: {anuncio.puntuacion_total})")
    else:
        print("  No hay anuncios que cumplan los criterios de calidad")
    print()
    
    vistos_ronda: set[str] = set()
    nuevos = 0

    # Procesar solo anuncios de alta calidad
    for anuncio in mejores_anuncios:
        titulo = anuncio.titulo
        link = anuncio.link

        clave = normalizar_url_anuncio(link)
        if not clave:
            continue

        if clave in vistos_ronda:
            continue
        vistos_ronda.add(clave)

        if anuncio_existente(clave):
            continue

        print(f"Nuevo anuncio de particular:")
        print(f"Título: {titulo}")
        print(f"URL: {link}")
        print("Puntuación:", anuncio.puntuacion_total)
        print("Detalles:", anuncio.detalles)

        # Verificar que el anuncio existe y está activo
        if not anuncio_activo(link):
            print("Anuncio inactivo o eliminado, omitiendo.")
            continue

        # Verificar que es de particular
        if not es_particular(titulo, link):
            print("Inmobiliaria filtrada")
            continue

        set_estado_busqueda("notificando")
        mensaje = f"""¡MEJOR ANUNCIO DE PARTICULAR! 

Puntuación: {anuncio.puntuacion_total}/100
Precio: {anuncio.puntuacion_precio}/100
Características: {anuncio.puntuacion_caracteristicas}/100
Ubicación: {anuncio.puntuacion_ubicacion}/100
Descripción: {anuncio.puntuacion_descripcion}/100
Reciente: {anuncio.puntuacion_reciente}/100

{titulo}

{clave}
"""
        enviar_mensaje(mensaje)
        guardar_anuncio(clave, titulo, link)
        nuevos += 1
        set_estado_busqueda("analizando")

    print("·" * 60)
    print(f"Mejores anuncios procesados: {len(mejores_anuncios)}")
    print(f"Nuevos guardados / notificados en esta ronda: {nuevos}")
    
    # Resumen final del ciclo
    print("·" * 60)
    print("CICLO COMPLETADO")
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Total candidatos: {len(anuncios)}")
    print(f"Anuncios recientes: {len(anuncios_recientes)}")
    print(f"Anuncios puntuados: {len(anuncios_puntuados)}")
    print(f"Mejores anuncios: {len(mejores_anuncios)}")
    print(f"Nuevos notificados: {nuevos}")
    print(f"Próxima ronda en {config.INTERVALO_SEGUNDOS} segundos")
    print("·" * 60)
    print()
    
    # Cambiar a estado esperando
    set_estado_busqueda("esperando")


def main():
    print("·" * 60)
    print("BOT INMOBILIARIO 2.0 - INICIADO")
    print("·" * 60)
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print(f"Base de datos: {config.DB_PATH}")
    print(f"Intervalo: {config.INTERVALO_SEGUNDOS} segundos")
    print(f"Zonas: {len(config.ZONAS)} configuradas")
    print(f"Fuentes: DDG={config.USAR_DUCKDUCKGO} | Pisos={config.USAR_PISOS} | Fotocasa={config.USAR_FOTOCASA} | Idealista={config.USAR_IDEALISTA} | Milanuncios={config.USAR_MILANUNCIOS}")
    print(f"Puntuación mínima: 40/100")
    print(f"Filtro recientes: 30 minutos")
    print("·" * 60)
    
    # Iniciar bot interactivo de Telegram
    if TELEGRAM_INTERACTIVE:
        print("Iniciando bot interactivo de Telegram...")
        start_telegram_thread()
    else:
        print("Modo alertas Telegram activado")
    
    # Iniciar indicador visual
    print("Iniciando indicador visual de búsqueda...")
    iniciar_indicador()
    
    print("Iniciando modo worker continuo...")
    print("Presiona Ctrl+C para detener el bot")
    print("·" * 60)
    print()
    
    try:
        while True:
            ciclo()
            print(f" Esperando {config.INTERVALO_SEGUNDOS} segundos para próxima búsqueda...")
            time.sleep(config.INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\nBot detenido por el usuario.")
        print("¡Hasta pronto!")
    except Exception as e:
        print(f"Error en ciclo: {e}")
        print("Reiniciando ciclo en 30 segundos...")
        time.sleep(30)
    finally:
        # Detener indicador visual
        detener()
        print("Indicador visual detenido.")


def keep_alive():
    """Función para mantener el proceso vivo en Render"""
    while True:
        time.sleep(3600)  # Dormir 1 hora


if __name__ == "__main__":
    main()
