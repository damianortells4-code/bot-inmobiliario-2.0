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

from portales_comun import HEADERS, pausa_entre_fuentes


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

        time.sleep(random.uniform(2.0, 5.0))

        url = "https://duckduckgo.com/html/?q=" + busqueda.replace(" ", "+")

        r = requests.get(url, headers=HEADERS, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")

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
    ip = config.USAR_PISOS if incluir_pisos is None else incluir_pisos
    ifc = config.USAR_FOTOCASA if incluir_fotocasa is None else incluir_fotocasa
    ii = config.USAR_IDEALISTA if incluir_idealista is None else incluir_idealista
    iddg = config.USAR_DUCKDUCKGO if incluir_duckduckgo is None else incluir_duckduckgo
    ih = (
        config.IDEALISTA_HEADLESS
        if idealista_headless is None
        else idealista_headless
    )

    bloques = []

    if iddg:
        bloques.append(buscar_duckduckgo())

    if ip:
        if bloques:
            pausa_entre_fuentes()
        bloques.append(buscar_pisos())

    if ifc:
        if bloques:
            pausa_entre_fuentes()
        bloques.append(buscar_fotocasa())

    if ii:
        if bloques:
            pausa_entre_fuentes()
        bloques.append(buscar_idealista(headless=ih))

    fusionados = _fusionar_sin_duplicados(*bloques)
    print("Total enlaces únicos (todos los portales):", len(fusionados))
    return fusionados
