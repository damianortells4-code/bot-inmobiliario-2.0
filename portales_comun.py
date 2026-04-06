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
    "administrador",
    "administradora",
    "administradores",
    "fincas",
    "real estate",
    "realstate",
    "inmob",
    "inmo",
    "gestión",
    "gestion",
    "asesor",
    "asesora",
    "asesores",
    "consultor",
    "consultora",
    "consultores",
    "manager",
    "directivo",
    "director",
    "directora",
    "sr",
    "sra",
    "dña",
    "don",
    "profesional",
    "profesionales",
    "empresa",
    "empresas",
    "negocio",
    "negocios",
    "comercial",
    "comerciales",
    "venta",
    "vendedor",
    "vendedora",
    "vendedores",
    "broker",
    "brokers",
    "agent",
    "agents",
    "agente",
    "agentes",
    "team",
    "equipo",
    "staff",
    "personal",
    "oficina",
    "oficinas",
    "central",
    "centro",
    "servicio",
    "servicios",
    "atención",
    "atencion",
    "cliente",
    "clientes",
    "usuario",
    "usuarios",
    "contact",
    "contacto",
    "contactar",
    "llamar",
    "llame",
    "llamen",
    "llamada",
    "llamadas",
    "teléfono",
    "telefono",
    "phone",
    "móvil",
    "movil",
    "móvil",
    "whatsapp",
    "email",
    "mail",
    "correo",
    "web",
    "página",
    "pagina",
    "sitio",
    "online",
    "digital",
    "portal",
    "portales",
    "plataforma",
    "plataformas",
    "redes",
    "social",
    "facebook",
    "instagram",
    "twitter",
    "linkedin",
    "youtube",
    "tiktok",
]

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

def get_random_headers():
    """Genera headers aleatorios para evitar detección"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": random.choice(["es-ES,es;q=0.9,en;q=0.8", "en-US,en;q=0.9,es;q=0.8", "es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7"]),
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
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
    """GET con reintentos y manejo de 403"""
    max_retries = 3
    base_wait = 2
    
    for attempt in range(max_retries):
        try:
            # Usar headers aleatorios en cada intento
            headers = get_random_headers()
            r = session.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
            
            if r.status_code == 429:
                espera = random.uniform(50, 100)
                print(f"   (429: esperando {espera:.0f}s…)")
                time.sleep(espera)
                continue
            elif r.status_code == 403:
                if attempt < max_retries - 1:
                    espera = base_wait * (2 ** attempt) + random.uniform(5, 15)
                    print(f"   (403: reintentando en {espera:.1f}s - intento {attempt + 1}/{max_retries})")
                    time.sleep(espera)
                    continue
                else:
                    print(f"   (403: bloqueado después de {max_retries} intentos)")
                    r.raise_for_status()
            
            r.raise_for_status()
            return r
            
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                espera = base_wait * (2 ** attempt) + random.uniform(1, 3)
                print(f"   (Error {e}: reintentando en {espera:.1f}s - intento {attempt + 1}/{max_retries})")
                time.sleep(espera)
                continue
            else:
                raise


def get_listado(session: requests.Session, url: str) -> requests.Response:
    """GET de página de listado con pausa previa y reintento ante 429."""
    pausa_entre_peticiones()
    return _get_con_reintento(session, url)
