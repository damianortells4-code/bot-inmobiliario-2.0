import sys
import time
import os

import config
from database import anuncio_existente, guardar_anuncio
from filtros import es_particular
from filtros_tiempo import filtrar_anuncios_recientes
from puntuacion_anuncios import puntuar_anuncios, obtener_mejores_anuncios
from scraper_internet import buscar_internet
from telegram_alert import enviar_mensaje
from urls import normalizar_url_anuncio
from verificador import anuncio_activo

# Importar bot interactivo
try:
    from telegram_bot import start_telegram_thread
    TELEGRAM_INTERACTIVE = True
except ImportError:
    print("⚠️ python-telegram-bot no instalado. Solo modo alertas.")
    TELEGRAM_INTERACTIVE = False


def ciclo():
    print("·" * 60)
    print("Buscando anuncios de particulares (filtro + sin duplicar por URL)...")
    print(
        f"Fuentes: DDG={config.USAR_DUCKDUCKGO} pisos={config.USAR_PISOS} "
        f"fotocasa={config.USAR_FOTOCASA} idealista={config.USAR_IDEALISTA} "
        f"habitaclia={config.USAR_HABITACLIA} milanuncios={config.USAR_MILANUNCIOS}"
    )
    print(
        f"Exigir palabra de particular en título: "
        f"{config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO}"
    )
    print(f"Anuncios recientes: últimos 30 minutos")
    if config.MAX_ANUNCIOS_POR_FUENTE is not None:
        print(f"Límite por fuente (pruebas): {config.MAX_ANUNCIOS_POR_FUENTE}")

    anuncios = buscar_internet()
    print("Candidatos tras scrapers:", len(anuncios))

    # Filtrar por tiempo (últimos 30 minutos)
    print("Filtrando anuncios recientes...")
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
    anuncios_puntuados, resumen_puntuacion = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=65.0)
    
    # Obtener mejores anuncios
    mejores_anuncios = obtener_mejores_anuncios(anuncios_para_puntuar, top_n=3)
    
    # Mostrar resumen de puntuación
    print(resumen_puntuacion)
    
    vistos_ronda: set[str] = set()
    nuevos = 0

    # Procesar solo anuncios de alta calidad
    for anuncio in mejores_anuncios:
        titulo = anuncio['titulo']
        link = anuncio['link']

        clave = normalizar_url_anuncio(link)
        if not clave:
            continue

        if clave in vistos_ronda:
            continue
        vistos_ronda.add(clave)

        if anuncio_existente(link):
            continue

        if not anuncio_activo(link):
            continue

        if not es_particular(titulo):
            continue

        guardar_anuncio(link, titulo)
        nuevos += 1

        print("·" * 60)
        print("🏆 ¡MEJOR ANUNCIO ENCONTRADO!")
        print("Título:", titulo)
        print("URL:", clave)
        print("Puntuación:", anuncio['puntuacion_total'])
        print("Detalles:", anuncio.get('detalles', {}))

        mensaje = f"""🏆 ¡MEJOR ANUNCIO DE PARTICULAR! 🏆

⭐ Puntuación: {anuncio['puntuacion_total']}/100
💰 Precio: {anuncio['puntuacion_precio']}/100
🏠 Características: {anuncio['puntuacion_caracteristicas']}/100
📍 Ubicación: {anuncio['puntuacion_ubicacion']}/100
📝 Descripción: {anuncio['puntuacion_descripcion']}/100
🕐 Reciente: {anuncio['puntuacion_reciente']}/100

{titulo}

{clave}
"""
        enviar_mensaje(mensaje)

    print("·" * 60)
    print(f"Mejores anuncios procesados: {len(mejores_anuncios)}")
    print(f"Nuevos guardados / notificados en esta ronda: {nuevos}")
    print(f"Próxima ronda en {config.INTERVALO_SEGUNDOS} s\n")


def main():
    print("Bot inmobiliario iniciado...")
    print(f"Base de datos: {config.DB_PATH}")
    
    # Iniciar bot interactivo de Telegram
    if TELEGRAM_INTERACTIVE:
        print("🤖 Iniciando bot interactivo de Telegram...")
        start_telegram_thread()
    
    # Ejecutar indefinidamente como worker (tanto en local como en Render)
    print("🔄 Iniciando modo worker continuo...")
    print("📝 Presiona Ctrl+C para detener el bot")
    
    while True:
        try:
            ciclo()
            print(f"⏳ Esperando {config.INTERVALO_SEGUNDOS} segundos para próxima búsqueda...")
            time.sleep(config.INTERVALO_SEGUNDOS)
        except KeyboardInterrupt:
            print("\n🛑 Bot detenido por el usuario.")
            print("👋 ¡Hasta pronto!")
            break
        except Exception as e:
            print(f"❌ Error en ciclo: {e}")
            print("🔄 Reiniciando ciclo en 30 segundos...")
            time.sleep(30)


def keep_alive():
    """Función para mantener el proceso vivo en Render"""
    while True:
        time.sleep(3600)  # Dormir 1 hora


if __name__ == "__main__":
    main()
