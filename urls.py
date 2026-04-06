"""Normalización de URLs para comparar y guardar sin duplicados."""

from urllib.parse import urlparse, urlunparse


def normalizar_url_anuncio(url: str) -> str:
    """
    Misma ficha con distinto tracking o con/sin www debe coincidir.
    """
    u = (url or "").strip()
    if not u:
        return ""
    if u.startswith("//"):
        u = "https:" + u
    if not u.startswith("http"):
        u = "https://" + u

    p = urlparse(u)
    host = p.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    path = (p.path or "/").rstrip("/")
    if not path:
        path = "/"

    return urlunparse(("https", host, path, "", "", "")).lower()
