"""Listados en pisos.com (alquiler) por zonas definidas en config."""

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

BASE_PISOS = "https://www.pisos.com"

PATRON_FICHA = re.compile(r"^/alquilar/.+-\d+_\d+/$")


def _urls_listado_pisos() -> list[str]:
    return [
        f"{BASE_PISOS}/alquiler/pisos-{z['pisos']}/"
        for z in config.ZONAS
    ]


def es_url_ficha_pisos(href: str) -> bool:
    if not href or href.startswith("#") or "javascript:" in href.lower():
        return False
    path = href.split("?", 1)[0]
    return bool(PATRON_FICHA.match(path))


def titulo_desde_href(path: str) -> str:
    m = re.search(r"-(\d+_\d+)/?$", path)
    if not m:
        return "Anuncio alquiler"
    antes = path[: m.start()].rstrip("/")
    if "/alquilar/" not in antes:
        return "Anuncio alquiler"
    resto = antes.split("/alquilar/", 1)[-1]
    if "-" not in resto:
        return resto.replace("_", " ") or "Anuncio alquiler"
    _, zona = resto.split("-", 1)
    return zona.replace("_", " ").strip() or "Anuncio alquiler"


def extraer_titulo_anuncio(item) -> str:
    texto = item.get_text(separator=" ", strip=True)
    if len(texto) >= 8:
        return texto.lower()
    titulo_attr = (item.get("title") or item.get("aria-label") or "").strip()
    if len(titulo_attr) >= 8:
        return titulo_attr.lower()
    href = item.get("href") or ""
    path = href.split("?", 1)[0]
    return titulo_desde_href(path).lower()


def buscar_anuncios(max_anuncios: Optional[int] = None):
    anuncios = []
    vistos: set[str] = set()
    cache_inmobiliaria: dict[str, bool] = {}
    comprobar_ficha = getattr(config, "COMPROBAR_INMOBILIARIA_EN_FICHA", False)

    limite = max_anuncios
    if limite is None and config.MAX_ANUNCIOS_POR_FUENTE is not None:
        limite = config.MAX_ANUNCIOS_POR_FUENTE

    urls_listado = _urls_listado_pisos()

    with requests.Session() as session:
        session.headers.update(get_random_headers())

        for i, url_listado in enumerate(urls_listado):
            if limite is not None and len(anuncios) >= limite:
                break

            if i > 0:
                pausa_entre_peticiones()

            print("Pisos.com listado:", url_listado)

            response = get_listado(session, url_listado)

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.find_all("a", href=True):
                if limite is not None and len(anuncios) >= limite:
                    break

                href = item.get("href")
                if not es_url_ficha_pisos(href):
                    continue

                link = urljoin(BASE_PISOS, href)
                link = link.split("#", 1)[0]

                if link in vistos:
                    continue
                vistos.add(link)

                titulo = extraer_titulo_anuncio(item)

                print("Pisos.com →", titulo[:80] if titulo else link)

                if titulo_sugiere_inmobiliaria(titulo):
                    print("❌ inmobiliaria detectada (título)")
                    cache_inmobiliaria[link] = True
                    continue

                if comprobar_ficha and es_inmobiliaria(session, link, cache_inmobiliaria):
                    print("❌ inmobiliaria detectada")
                    continue

                anuncios.append({"titulo": titulo, "link": link})

        print("Pisos.com anuncios:", len(anuncios))

        return anuncios
