"""Listados en fotocasa.es (alquiler y compra) vía HTML estático."""

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

BASE_FOTOCASA = "https://www.fotocasa.es"

PATRON_FICHA = re.compile(
    r"^/es/(?:alquiler|comprar)/vivienda/[^/]+/[^/]+/\d+/d/?$"
)


def _urls_listado(operacion: str) -> list[str]:
    op = operacion if operacion in ("alquiler", "comprar") else "alquiler"
    return [
        f"{BASE_FOTOCASA}/es/{op}/viviendas/{z['fotocasa']}/todas-las-zonas/l"
        for z in config.ZONAS
    ]


def es_url_ficha_fotocasa(href: str) -> bool:
    if not href or href.startswith("#") or "javascript:" in href.lower():
        return False
    path = href.split("?", 1)[0].split("#", 1)[0]
    return bool(PATRON_FICHA.match(path))


def titulo_desde_href_fotocasa(href: str) -> str:
    path = href.split("?", 1)[0].split("#", 1)[0].strip("/")
    parts = path.split("/")
    if len(parts) >= 2 and parts[-1] == "d" and parts[-2].isdigit():
        slug = parts[-3] if len(parts) >= 3 else ""
        return slug.replace("-", " ").strip() or "Anuncio fotocasa"
    return "Anuncio fotocasa"


def extraer_titulo_fotocasa(item) -> str:
    texto = item.get_text(separator=" ", strip=True)
    if len(texto) >= 8:
        return texto.lower()
    titulo_attr = (item.get("title") or item.get("aria-label") or "").strip()
    if len(titulo_attr) >= 8:
        return titulo_attr.lower()
    return titulo_desde_href_fotocasa(item.get("href") or "").lower()


def buscar_anuncios(max_anuncios: Optional[int] = None):
    anuncios = []
    vistos: set[str] = set()
    cache_inmobiliaria: dict[str, bool] = {}
    comprobar_ficha = getattr(config, "COMPROBAR_INMOBILIARIA_EN_FICHA", False)

    limite = max_anuncios
    if limite is None and config.MAX_ANUNCIOS_POR_FUENTE is not None:
        limite = config.MAX_ANUNCIOS_POR_FUENTE

    listados = _urls_listado("alquiler") + _urls_listado("comprar")

    with requests.Session() as session:
        session.headers.update(get_random_headers())

        for i, url_listado in enumerate(listados):
            if limite is not None and len(anuncios) >= limite:
                break

            if i > 0:
                pausa_entre_peticiones()

            print("Fotocasa listado:", url_listado)

            response = get_listado(session, url_listado)

            soup = BeautifulSoup(response.text, "html.parser")

            for item in soup.find_all("a", href=True):
                if limite is not None and len(anuncios) >= limite:
                    break

                href = item.get("href")
                if not es_url_ficha_fotocasa(href):
                    continue

                link = urljoin(BASE_FOTOCASA, href)
                link = link.split("#", 1)[0].split("?", 1)[0]

                if link in vistos:
                    continue
                vistos.add(link)

                titulo = extraer_titulo_fotocasa(item)

                print("Fotocasa →", (titulo[:80] if titulo else link))

                if titulo_sugiere_inmobiliaria(titulo):
                    print("❌ inmobiliaria detectada (título)")
                    cache_inmobiliaria[link] = True
                    continue

                if comprobar_ficha and es_inmobiliaria(session, link, cache_inmobiliaria):
                    print("❌ inmobiliaria detectada")
                    continue

                anuncios.append({"titulo": titulo, "link": link})

    print("Fotocasa anuncios:", len(anuncios))
    return anuncios
