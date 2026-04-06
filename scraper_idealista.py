"""
Idealista bloquea requests «crudos»; hace falta Chromium vía Playwright.

    pip install playwright && playwright install chromium
"""

import re
from typing import Optional
from urllib.parse import urljoin

import config
from portales_comun import titulo_sugiere_inmobiliaria

BASE_IDEALISTA = "https://www.idealista.com"

PATRON_INMUEBLE = re.compile(r"/inmueble/\d+")

TIMEOUT_MS = 90000


def _urls_idealista() -> list[str]:
    urls = []
    for z in config.ZONAS:
        slug = z["idealista"]
        urls.append(f"{BASE_IDEALISTA}/alquiler-viviendas/{slug}/")
        urls.append(f"{BASE_IDEALISTA}/venta-viviendas/{slug}/")
    return urls


def buscar_anuncios(max_anuncios: Optional[int] = None, headless: bool = True):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Idealista: instala Playwright → pip install playwright && playwright install chromium"
        )
        return []

    limite = max_anuncios
    if limite is None and config.MAX_ANUNCIOS_POR_FUENTE is not None:
        limite = config.MAX_ANUNCIOS_POR_FUENTE

    anuncios = []
    vistos: set[str] = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(
            locale="es-ES",
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            ),
        )

        for url_listado in _urls_idealista():
            if limite is not None and len(anuncios) >= limite:
                break

            print("Idealista listado:", url_listado)
            page = context.new_page()

            try:
                page.goto(
                    url_listado, wait_until="domcontentloaded", timeout=TIMEOUT_MS
                )
                page.wait_for_timeout(4000)
            except Exception as exc:
                print("Idealista (error al cargar):", url_listado, exc)
                page.close()
                continue

            for link_el in page.query_selector_all('a[href*="/inmueble/"]'):
                if limite is not None and len(anuncios) >= limite:
                    break

                href = link_el.get_attribute("href")
                if not PATRON_INMUEBLE.search(href or ""):
                    continue

                full = urljoin(BASE_IDEALISTA, href.split("#")[0].split("?", 1)[0])
                if full in vistos:
                    continue
                vistos.add(full)

                titulo = (link_el.inner_text() or "").strip()
                if len(titulo) < 8:
                    titulo = (link_el.get_attribute("title") or "").strip()
                titulo = titulo.lower() if titulo else "anuncio idealista"

                print("Idealista →", titulo[:80] if titulo else full)

                if titulo_sugiere_inmobiliaria(titulo):
                    print("❌ inmobiliaria detectada (título)")
                    continue

                anuncios.append({"titulo": titulo, "link": full})

            page.close()

        browser.close()

    print("Idealista anuncios:", len(anuncios))
    return anuncios
