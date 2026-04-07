"""Agrega DuckDuckGo y listados directos (pisos, fotocasa, idealista)."""

import random
import time
from urllib.parse import parse_qs, unquote, urlparse

import requests
from bs4 import BeautifulSoup

import config
from urls import normalizar_url_anuncio
from scraper_fotocasa import buscar_anuncios as buscar_fotocasa
from scraper_idealista import buscar_anuncios as buscar_idealista
from scraper_pisos import buscar_anuncios as buscar_pisos
from scraper_habitaclia import buscar_anuncios as buscar_habitaclia
from scraper_milanuncios import buscar_anuncios as buscar_milanuncios

from portales_comun import get_random_headers, pausa_entre_fuentes


def _url_real_desde_duckduckgo(href: str) -> str:
    """DDG devuelve enlaces a //duckduckgo.com/l/?uddg=https%3A%2F%2F... — extraemos la URL final."""
    if not href:
        return href
    h = href.strip()
    if h.startswith("//"):
        h = "https:" + h
    if "duckduckgo.com" not in h.lower():
        return h
    try:
        q = parse_qs(urlparse(h).query)
        if "uddg" in q and q["uddg"]:
            return unquote(q["uddg"][0])
    except (ValueError, IndexError):
        pass
    return h


def _fusionar_sin_duplicados(*colecciones) -> list:
    vistos: set[str] = set()
    resultado = []
    for col in colecciones:
        for item in col:
            clave = normalizar_url_anuncio(item.get("link", ""))
            if not clave or clave in vistos:
                continue
            vistos.add(clave)
            resultado.append(item)
    return resultado


def buscar_duckduckgo() -> list:
    anuncios = []

    for busqueda in config.BUSQUEDAS_DUCKDUCKGO:
        print("DuckDuckGo buscando:", busqueda)

        time.sleep(random.uniform(1.0, 2.5))  # Tiempo seguro para evitar detección

        url = "https://duckduckgo.com/html/?q=" + busqueda.replace(" ", "+")

        try:
            r = requests.get(url, headers=get_random_headers(), timeout=25)
            r.raise_for_status()
            
            # Intentar diferentes parsers si hay error
            try:
                soup = BeautifulSoup(r.text, "html.parser")
            except Exception:
                try:
                    soup = BeautifulSoup(r.text, "lxml")
                except Exception:
                    soup = BeautifulSoup(r.text, "html5lib")
                    
        except Exception as e:
            print(f"Error en DuckDuckGo: {e}")
            continue

        resultados = soup.find_all("a", class_="result__a")
        if not resultados:
            resultados = soup.select(".web-result a.result__a")

        if not resultados and r.status_code != 200:
            print(
                "DuckDuckGo HTTP",
                r.status_code,
                "sin resultados parseables —",
                busqueda[:40],
            )
            continue

        for res in resultados:
            link_crudo = res.get("href")
            titulo = res.get_text(strip=True)

            if not link_crudo:
                continue

            link = _url_real_desde_duckduckgo(link_crudo)
            hay_portal = any(
                p in link_crudo.lower() or p in link.lower()
                for p in config.PORTALES_DUCKDUCKGO
            )
            if not hay_portal:
                continue

            anuncios.append({"titulo": titulo or link, "link": link})

    print("DuckDuckGo enlaces:", len(anuncios))
    return anuncios


def buscar_internet(
    incluir_pisos=None,
    incluir_fotocasa=None,
    incluir_idealista=None,
    incluir_duckduckgo=None,
    idealista_headless=None,
):
    """
    Junta fuentes y elimina URLs duplicadas.
    Si un argumento es None, se usa el valor en config.py.
    """
    bloques = []

    if config.USAR_DUCKDUCKGO:
        bloques.append(buscar_duckduckgo())

    if config.USAR_PISOS:
        bloques.append(buscar_pisos())

    if config.USAR_FOTOCASA:
        bloques.append(buscar_fotocasa())

    if config.USAR_IDEALISTA:
        bloques.append(buscar_idealista())

    if config.USAR_HABITACLIA:
        bloques.append(buscar_habitaclia())

    if config.USAR_MILANUNCIOS:
        bloques.append(buscar_milanuncios())

    # Unir y eliminar duplicados por URL normalizada
    vistos: set[str] = set()
    unicos = []

    for bloque in bloques:
        pausa_entre_fuentes()
        for anuncio in bloque:
            clave = normalizar_url_anuncio(anuncio["link"])
            if clave and clave not in vistos:
                vistos.add(clave)
                unicos.append(anuncio)

    return unicos
