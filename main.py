import sys
import time
import os

import config
from database import anuncio_existente, guardar_anuncio
from filtros import es_particular
from scraper_internet import buscar_internet
from telegram_alert import enviar_mensaje
from urls import normalizar_url_anuncio
from verificador import anuncio_activo


def ciclo():
    print("─" * 60)
    print("Buscando anuncios de particulares (filtro + sin duplicar por URL)…")
    print(
        f"Fuentes: DDG={config.USAR_DUCKDUCKGO} pisos={config.USAR_PISOS} "
        f"fotocasa={config.USAR_FOTOCASA} idealista={config.USAR_IDEALISTA}"
    )
    print(
        f"Exigir palabra de particular en título: "
        f"{config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO}"
    )
    if config.MAX_ANUNCIOS_POR_FUENTE is not None:
        print(f"Límite por fuente (pruebas): {config.MAX_ANUNCIOS_POR_FUENTE}")

    anuncios = buscar_internet()

    print("Candidatos tras scrapers:", len(anuncios))

    vistos_ronda: set[str] = set()
    nuevos = 0

    for anuncio in anuncios:
        titulo = anuncio["titulo"]
        link = anuncio["link"]

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

        print("🏠", titulo)
        print("🔗", clave)

        mensaje = f"""🏠 {titulo}

🔗 {clave}
"""
        enviar_mensaje(mensaje)

    print(f"Nuevos guardados / notificados en esta ronda: {nuevos}")
    print(f"Próxima ronda en {config.INTERVALO_SEGUNDOS} s\n")


def main():
    print("Bot inmobiliario — Ctrl+C para salir")
    print(f"Base de datos: {config.DB_PATH}")
    
    # En Render, solo ejecutar una vez y salir
    if os.environ.get("RENDER"):
        print("Ejecutando en Render - modo single run")
        ciclo()
        print("Bot finalizado. Render reiniciará según su configuración.")
        return

    while True:
        try:
            ciclo()
            time.sleep(config.INTERVALO_SEGUNDOS)
        except KeyboardInterrupt:
            print("\nDetenido por el usuario.")
            sys.exit(0)


if __name__ == "__main__":
    main()
