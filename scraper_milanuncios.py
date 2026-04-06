"""Listados en milanuncios.com vía HTML estático."""

import re
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import config
from portales_comun import (
    get_random_headers,
    es_inmobiliaria,
    get_listado,
    pausa_entre_peticiones,
    titulo_sugiere_inmobiliaria,
)

BASE_MILANUNCIOS = "https://www.milanuncios.com"

PATRON_FICHA = re.compile(r"^/_\d+\.htm$")

def _urls_listado(tipo: str) -> list[str]:
    """Devuelve URLs de listado para una zona y tipo."""
    urls = []
    for zona_dict in config.ZONAS:
        zona = zona_dict["milanuncios"]
        if tipo == "alquiler":
            urls.append(f"{BASE_MILANUNCIOS}/alquiler-de-pisos-en-{zona}.htm")
        elif tipo == "comprar":
            urls.append(f"{BASE_MILANUNCIOS}/venta-de-pisos-en-{zona}.htm")
    return urls


def _extraer_anuncios(soup: BeautifulSoup, url_base: str) -> list[dict]:
    """Extrae anuncios de una página de Milanuncios."""
    anuncios = []
    for anuncio_div in soup.find_all("div", class_="aditem"):
        titulo_elem = anuncio_div.find("a", class_="aditem-detail-title")
        if not titulo_elem:
            continue

        titulo = titulo_elem.get_text(strip=True)
        href = titulo_elem.get("href", "")
        if not href:
            continue

        if not href.startswith("http"):
            href = urljoin(url_base, href)

        if not PATRON_FICHA.search(href):
            continue

        anuncios.append({"titulo": titulo, "link": href})
    return anuncios


def buscar_anuncios(max_anuncios: Optional[int] = None) -> list[dict]:
    """Busca anuncios en Milanuncios."""
    anuncios = []
    cache_inmobiliaria: dict[str, bool] = {}
    comprobar_ficha = getattr(config, "COMPROBAR_INMOBILIARIA_EN_FICHA", False)

    limite = max_anuncios
    if limite is None and config.MAX_ANUNCIOS_POR_FUENTE is not None:
        limite = config.MAX_ANUNCIOS_POR_FUENTE

    urls_listado = _urls_listado("alquiler") + _urls_listado("comprar")

    with requests.Session() as session:
        session.headers.update(get_random_headers())

        for i, url_listado in enumerate(urls_listado):
            if limite is not None and len(anuncios) >= limite:
                break

            if i > 0:
                pausa_entre_peticiones()

            print("Milanuncios listado:", url_listado)

            try:
                r = get_listado(session, url_listado)
                soup = BeautifulSoup(r.text, "html.parser")
                anuncios_pagina = _extraer_anuncios(soup, url_listado)

                for anuncio in anuncios_pagina:
                    if limite is not None and len(anuncios) >= limite:
                        break

                    titulo = anuncio["titulo"]
                    link = anuncio["link"]

                    # Descartar si parece inmobiliaria por título
                    if titulo_sugiere_inmobiliaria(titulo):
                        print(f"❌ inmobiliaria detectada (título): {titulo[:50]}...")
                        continue

                    # Descartar si ya sabemos que es inmobiliaria
                    if link in cache_inmobiliaria and cache_inmobiliaria[link]:
                        print(f"❌ inmobiliaria cacheada: {titulo[:50]}...")
                        continue

                    if comprobar_ficha and es_inmobiliaria(link):
                        cache_inmobiliaria[link] = True
                        print(f"❌ inmobiliaria detectada (ficha): {titulo[:50]}...")
                        continue

                    cache_inmobiliaria[link] = False
                    anuncios.append(anuncio)
                    print(f"Milanuncios → {titulo}")

            except Exception as e:
                print(f"Error procesando {url_listado}: {e}")
                continue

    return anuncios
