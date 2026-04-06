import requests

import config
from portales_comun import get_random_headers, REQUEST_TIMEOUT


def anuncio_activo(url: str) -> bool:
    if not getattr(config, "VERIFICAR_ENLACE_ACTIVO", True):
        return True

    try:
        r = requests.get(
            url,
            headers=get_random_headers(),
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )
        code = r.status_code
        texto = r.text.lower()

        if code == 404:
            return False

        if code == 200:
            if "no disponible" in texto:
                return False
            if "anuncio eliminado" in texto:
                return False
            if "ya no está disponible" in texto:
                return False
            return True

        # Anti-bot: no podemos leer la ficha; no descartamos el anuncio.
        if code in (403, 429, 503, 502, 401):
            return True

        return False

    except (requests.RequestException, OSError):
        return True
