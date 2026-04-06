"""Cabeceras, pausas y detección de inmobiliaria compartidos entre scrapers."""

import random
import time
from typing import Dict

import requests
from bs4 import BeautifulSoup

import config

PALABRAS_INMOBILIARIA = [
    "inmobiliaria",
    "asesores",
    "real estate",
    "grupo inmobiliario",
    "gestión inmobiliaria",
    "servicios inmobiliarios",
    "api properties",
    "aproperties",
    "nova finques",
    "cèntric finques",
    "goldmark",
    "signature luxury homes",
    "finques",
    "inmobles",
    "inmob",
    "properties",
    "estate",
    "remax",
    "engel",
    "coldwell",
    "keller williams",
    "century 21",
    "oportunidad",
    "inversión",
    "inversion",
    "promo",
    "promoción",
    "urbanismo",
    "construcción",
    "obras nuevas",
    "obra nueva",
    "entrega",
    "llaves en mano",
    "estrenar",
    "promotor",
    "promotora",
    "desarrollador",
    "desarrolladora",
    "construcciones",
    "grupo",
    "holding",
    "capital",
    "investment",
    "s.l.",
    "sl",
    "sa",
    "ltd",
    "company",
    "corp",
    "corporation",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

REQUEST_TIMEOUT = 25


def pausa_entre_peticiones():
    mn = float(getattr(config, "SCRAPER_PAUSA_MIN", 4.0))
    mx = float(getattr(config, "SCRAPER_PAUSA_MAX", 10.0))
    if mx < mn:
        mx = mn
    time.sleep(random.uniform(mn, mx))


def pausa_entre_fuentes():
    """Entre pisos / fotocasa / DDG para no encadenar ráfagas."""
    mn = float(getattr(config, "PAUSA_ENTRE_FUENTES_MIN", 8.0))
    mx = float(getattr(config, "PAUSA_ENTRE_FUENTES_MAX", 18.0))
    if mx < mn:
        mx = mn
    time.sleep(random.uniform(mn, mx))


def titulo_sugiere_inmobiliaria(titulo: str) -> bool:
    t = titulo.lower()
    for palabra in PALABRAS_INMOBILIARIA:
        if len(palabra) <= 3:
            continue
        if palabra in t:
            return True
    return False


def texto_visible_sin_scripts(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text().lower()


def es_inmobiliaria(
    session: requests.Session, link: str, cache: Dict[str, bool]
) -> bool:
    if link in cache:
        return cache[link]

    try:
        pausa_entre_peticiones()
        response = _get_con_reintento(session, link)

        soup = BeautifulSoup(response.text, "html.parser")
        texto = texto_visible_sin_scripts(soup)

        for palabra in PALABRAS_INMOBILIARIA:
            if palabra in texto:
                cache[link] = True
                return True

        cache[link] = False
        return False

    except (requests.RequestException, OSError):
        cache[link] = False
        return False


def _get_con_reintento(session: requests.Session, url: str) -> requests.Response:
    r = session.get(url, timeout=REQUEST_TIMEOUT)
    if r.status_code == 429:
        espera = random.uniform(50, 100)
        print(f"   (429: esperando {espera:.0f}s…)")
        time.sleep(espera)
        r = session.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    return r


def get_listado(session: requests.Session, url: str) -> requests.Response:
    """GET de página de listado con pausa previa y reintento ante 429."""
    pausa_entre_peticiones()
    return _get_con_reintento(session, url)
