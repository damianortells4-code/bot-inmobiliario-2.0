"""
Parámetros del bot. Ajusta aquí zonas, fuentes y tiempos.

Cada zona define el slug que usa cada portal (no son intercambiables).
"""

# --- Base de datos ---
DB_PATH = "anuncios.db"

# --- Bucle principal (segundos entre rondas de búsqueda) ---
INTERVALO_SEGUNDOS = 300

# --- Límite por fuente (None = sin límite; útil para pruebas) ---
# Ejemplo: MAX_ANUNCIOS_POR_FUENTE = 20
MAX_ANUNCIOS_POR_FUENTE = None

# --- Ritmo de scraping (más alto = menos bloqueos del portal) ---
SCRAPER_PAUSA_MIN = 6.0
SCRAPER_PAUSA_MAX = 15.0
PAUSA_ENTRE_FUENTES_MIN = 15.0
PAUSA_ENTRE_FUENTES_MAX = 30.0

# Abrir cada anuncio en otra petición para buscar "inmobiliaria" en el HTML.
# True = más fiel y MUCHAS más peticiones (riesgo de bloqueo).
# False = solo heurística por título del listado (recomendado).
COMPROBAR_INMOBILIARIA_EN_FICHA = False

# --- Qué fuentes activar (Idealista requiere: pip install playwright && playwright install chromium) ---
USAR_DUCKDUCKGO = True
USAR_PISOS = True
USAR_FOTOCASA = True
USAR_IDEALISTA = True
IDEALISTA_HEADLESS = True

# --- Zonas: mismas áreas en todos los portales ---
# Claves: pisos (segmento URL pisos.com), fotocasa (slug), idealista (sufijo -barcelona)
ZONAS = [
    {
        "pisos": "rubi",
        "fotocasa": "rubi",
        "idealista": "rubi-barcelona",
    },
    {
        "pisos": "sant_cugat_del_valles",
        "fotocasa": "sant-cugat-del-valles",
        "idealista": "sant-cugat-del-valles-barcelona",
    },
    {
        "pisos": "sabadell",
        "fotocasa": "sabadell",
        "idealista": "sabadell-barcelona",
    },
    {
        "pisos": "terrassa",
        "fotocasa": "terrassa",
        "idealista": "terrassa-barcelona",
    },
]

# --- Búsquedas en DuckDuckGo (orientadas a particulares) ---
BUSQUEDAS_DUCKDUCKGO = [
    "alquiler piso sant cugat particular",
    "piso alquiler rubi particular",
    "piso terrassa alquiler propietario",
    "vendo piso sabadell particular",
]

# Dominios que aceptamos en resultados DDG
PORTALES_DUCKDUCKGO = [
    "idealista",
    "fotocasa",
    "pisos.com",
    "habitaclia",
    "milanuncios",
]

# --- Solo anuncios de particulares ---
# True: el título debe incluir alguna palabra de particulares (particular, propietario, dueño…).
# False: solo se descartan textos que parezcan agencia (más resultados, menos fiable).
EXIGIR_PALABRA_PARTICULAR_EN_TITULO = True

# True: comprobar que la URL siga viva (GET). Si el portal devuelve 403 al bot,
# se asume igualmente activo (no se puede verificar).
VERIFICAR_ENLACE_ACTIVO = True
