"""
Parámetros del bot. Ajusta aquí zonas, fuentes y tiempos.

Cada zona define el slug que usa cada portal (no son intercambiables).
"""

# --- Base de datos ---
DB_PATH = "anuncios.db"

# --- Bucle principal (segundos entre rondas de búsqueda) ---
INTERVALO_SEGUNDOS = 120  # 2 minutos (búsqueda de hoy cada 2 min)

# --- Límite por fuente (None = sin límite; útil para pruebas) ---
# Ejemplo: MAX_ANUNCIOS_POR_FUENTE = 20
MAX_ANUNCIOS_POR_FUENTE = None

# --- Ritmo de scraping (más alto = menos bloqueos del portal) ---
SCRAPER_PAUSA_MIN = 6.0  # Más pausa para seguridad con 9 portales
SCRAPER_PAUSA_MAX = 15.0  # Más variación para evitar detección
PAUSA_ENTRE_FUENTES_MIN = 18.0  # Más separación entre portales (9 portales)
PAUSA_ENTRE_FUENTES_MAX = 30.0  # Más tiempo seguro entre fuentes

# Abrir cada anuncio en otra petición para buscar "inmobiliaria" en el HTML.
# True = más fiel y MUCHAS más peticiones (riesgo de bloqueo).
# False = solo heurística por título del listado (recomendado).
COMPROBAR_INMOBILIARIA_EN_FICHA = False

# --- Qué fuentes activar (Idealista requiere: pip install playwright && playwright install chromium) ---
USAR_DUCKDUCKGO = True
USAR_PISOS = True
USAR_FOTOCASA = True
USAR_IDEALISTA = True  # Activado para más anuncios
USAR_HABITACLIA = False  # Desactivado por errores 404
USAR_HABITACLIA_MEJORADO = False  # Desactivado temporalmente por bloqueos
USAR_HABITACLIA_ULTRA_SEGURO = False  # Desactivado por bloqueos
USAR_FOTOCASACOM = False  # Dominio no existe
USAR_PISOSCOM = False  # Sin resultados
USAR_IDEALISTA_PRO = False  # Bloqueo 403
USAR_MILANUNCIOS = True
IDEALISTA_HEADLESS = True

# --- Zonas: mismas áreas en todos los portales ---
# Claves: pisos (segmento URL pisos.com), fotocasa (slug), idealista (sufijo -barcelona)
ZONAS = [
    {
        "pisos": "rubi",
        "fotocasa": "rubi",
        "idealista": "rubi-barcelona",
        "habitaclia": "rubi",
        "habitaclia_mejorado": "rubi",
        "habitaclia_ultra_seguro": "rubi",
        "fotocasacom": "rubi",
        "pisoscom": "rubi",
        "idealista_pro": "rubi-barcelona",
        "milanuncios": "rubi",
    },
    {
        "pisos": "sant_cugat_del_valles",
        "fotocasa": "sant-cugat-del-valles",
        "idealista": "sant-cugat-del-valles-barcelona",
        "habitaclia": "sant_cugat",
        "habitaclia_mejorado": "sant_cugat",
        "habitaclia_ultra_seguro": "sant_cugat",
        "fotocasacom": "sant_cugat",
        "pisoscom": "sant_cugat",
        "idealista_pro": "sant-cugat-del-valles-barcelona",
        "milanuncios": "sant_cugat",
    },
    {
        "pisos": "sabadell",
        "fotocasa": "sabadell",
        "idealista": "sabadell-barcelona",
        "habitaclia": "sabadell",
        "habitaclia_mejorado": "sabadell",
        "habitaclia_ultra_seguro": "sabadell",
        "fotocasacom": "sabadell",
        "pisoscom": "sabadell",
        "idealista_pro": "sabadell-barcelona",
        "milanuncios": "sabadell",
    },
    {
        "pisos": "terrassa",
        "fotocasa": "terrassa",
        "idealista": "terrassa-barcelona",
        "habitaclia": "terrassa",
        "habitaclia_mejorado": "terrassa",
        "habitaclia_ultra_seguro": "terrassa",
        "fotocasacom": "terrassa",
        "pisoscom": "terrassa",
        "idealista_pro": "terrassa-barcelona",
        "milanuncios": "terrassa",
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
EXIGIR_PALABRA_PARTICULAR_EN_TITULO = False

# True: comprobar que la URL siga viva (GET). Si el portal devuelve 403 al bot,
# se asume igualmente activo (no se puede verificar).
VERIFICAR_ENLACE_ACTIVO = True
