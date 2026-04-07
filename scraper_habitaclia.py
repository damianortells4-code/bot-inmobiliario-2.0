"""Listados en habitaclia.com vía HTML estático."""

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

BASE_HABITACLIA = "https://www.habitaclia.com"

PATRON_FICHA = re.compile(r"^/vivienda/\d+/")

def _urls_listado(tipo: str) -> list[str]:
    """Devuelve URLs de listado para una zona y tipo."""
    urls = []
    for zona_dict in config.ZONAS:
        zona = zona_dict["habitaclia"]
        if tipo == "alquiler":
            urls.append(f"{BASE_HABITACLIA}/alquiler-de-pisos-y-lofts-{zona}.htm")
        elif tipo == "comprar":
            urls.append(f"{BASE_HABITACLIA}/compra-de-pisos-y-lofts-{zona}.htm")
    return urls


def _extraer_anuncios_ficha(soup: BeautifulSoup, url_base: str) -> list[dict]:
    """Extrae anuncios de una página de ficha (detalles)."""
    anuncios = []
    for articulo in soup.find_all("article", class_="ad"):
        titulo_elem = articulo.find("h2")
        if not titulo_elem:
            continue

        titulo = titulo_elem.get_text(strip=True)
        link_elem = articulo.find("a")
        if not link_elem or not link_elem.get("href"):
            continue

        href = link_elem["href"]
        if not href.startswith("http"):
            href = urljoin(url_base, href)

        if not PATRON_FICHA.search(href):
            continue

        anuncios.append({"titulo": titulo, "link": href})
    return anuncios


def _extraer_anuncios_listado(soup: BeautifulSoup, url_base: str) -> list[dict]:
    """Extrae anuncios de una página de listado."""
    anuncios = []
    for articulo in soup.find_all("div", class_="ad"):
        titulo_elem = articulo.find("h3")
        if not titulo_elem:
            continue

        titulo = titulo_elem.get_text(strip=True)
        link_elem = articulo.find("a")
        if not link_elem or not link_elem.get("href"):
            continue

        href = link_elem["href"]
        if not href.startswith("http"):
            href = urljoin(url_base, href)

        if not PATRON_FICHA.search(href):
            continue

        anuncios.append({"titulo": titulo, "link": href})
    return anuncios


def buscar_anuncios(max_anuncios: Optional[int] = None) -> list[dict]:
    """Busca anuncios en Habitaclia."""
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

            print("Habitaclia listado:", url_listado)

            try:
                r = get_listado(session, url_listado)
                soup = BeautifulSoup(r.text, "html.parser")

                # Intentar extraer de listado
                anuncios_pagina = _extraer_anuncios_listado(soup, url_listado)

                if not anuncios_pagina:
                    # Si no hay, intentar de ficha
                    anuncios_pagina = _extraer_anuncios_ficha(soup, url_listado)

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
                        print(f"   (inmobiliaria filtrada)")
                        continue

                    if comprobar_ficha and es_inmobiliaria(link):
                        cache_inmobiliaria[link] = True
                        print(f"   (inmobiliaria filtrada)")
                        continue

                    cache_inmobiliaria[link] = False
                    anuncios.append(anuncio)
                    print(f"Habitaclia → {titulo}")

            except Exception as e:
                print(f"Error procesando {url_listado}: {e}")
                continue

    return anuncios
