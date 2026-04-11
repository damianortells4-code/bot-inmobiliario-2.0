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
    "inmob",
    "inmo",
    "inmo.",
    "inmob.",
    "inmobiliaria.",
    "inmobiliarios",
    "inmobiliarias",
    "properties",
    "property",
    "viviendas",
    "vivienda",
    "solar",
    "solares",
    "parcela",
    "parcelas",
    "rustica",
    "rustico",
    "rústica",
    "rústico",
    "urban",
    "urbana",
    "industrial",
    "comercial",
    "residencial",
    "turístico",
    "turistico",
    "turistica",
    "vacacional",
    "segunda mano",
    "segunda mano",
    "turística",
    "turisticas",
    "vacacionales",
    "primera residencia",
    "vivienda habitual",
    "vivienda habitual",
    "vivienda secundaria",
    "vivienda secundaria",
    "uso residencial",
    "uso residencial",
    "uso comercial",
    "uso comercial",
    "uso industrial",
    "uso industrial",
    "uso oficinas",
    "uso oficinas",
    "uso local",
    "uso local",
    "uso nave",
    "uso nave",
    "uso garaje",
    "uso garaje",
    "uso trastero",
    "uso trastero",
    "uso almacen",
    "uso almacen",
    "uso depósito",
    "uso deposito",
    "uso parking",
    "uso parking",
    "suelo urbanizable",
    "suelo urbanizable",
    "suelo urbano",
    "suelo urbano",
    "suelo rústico",
    "suelo rustico",
    "suelo urbanizado",
    "suelo urbanizado",
    "suelo sin urbanizar",
    "suelo sin urbanizar",
    "terreno urbanizable",
    "terreno urbanizable",
    "terreno urbano",
    "terreno urbano",
    "terreno rústico",
    "terreno rustico",
    "terreno urbanizado",
    "terreno urbanizado",
    "terreno sin urbanizar",
    "terreno sin urbanizar",
    "solar urbanizable",
    "solar urbanizable",
    "solar urbano",
    "solar urbano",
    "solar rústico",
    "solar rustico",
    "solar urbanizado",
    "solar urbanizado",
    "solar sin urbanizar",
    "solar sin urbanizar",
    "parcela urbanizable",
    "parcela urbanizable",
    "parcela urbana",
    "parcela urbana",
    "parcela rústica",
    "parcela rustica",
    "parcela urbanizada",
    "parcela urbanizada",
    "parcela sin urbanizar",
    "parcela sin urbanizar",
    "finca urbanizable",
    "finca urbanizable",
    "finca urbana",
    "finca urbana",
    "finca rústica",
    "finca rustica",
    "finca urbanizada",
    "finca urbanizada",
    "finca sin urbanizar",
    "finca sin urbanizar",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
]

def get_random_headers():
    """Genera headers aleatorios para evitar detección"""
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice([
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8"
        ]),
        "Accept-Language": random.choice([
            "es-ES,es;q=0.9,en;q=0.8",
            "en-US,en;q=0.9,es;q=0.8", 
            "es-ES,es;q=0.9,en-GB;q=0.8,en;q=0.7",
            "es-ES,es;q=0.8,en;q=0.5",
            "en-GB,en;q=0.9,es;q=0.8"
        ]),
        "Accept-Encoding": random.choice([
            "gzip, deflate, br",
            "gzip, deflate",
            "gzip, deflate, br, zstd"
        ]),
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": random.choice([
            "max-age=0",
            "no-cache",
            "no-store, max-age=0"
        ])
    }
    
    # Añadir headers opcionales aleatoriamente
    if random.random() < 0.3:  # 30% de probabilidad
        headers["Sec-GPC"] = "1"  # Global Privacy Control
    
    if random.random() < 0.2:  # 20% de probabilidad
        headers["Sec-CH-UA"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
        headers["Sec-CH-UA-Mobile"] = "?0"
        headers["Sec-CH-UA-Platform"] = random.choice(['"Windows"', '"macOS"', '"Linux"'])
    
    return headers

REQUEST_TIMEOUT = 25


def pausa_entre_peticiones():
    """Pausa aleatoria entre peticiones para evitar detección."""
    # Pausa más larga y aleatoria para simular comportamiento humano
    pausa = random.uniform(config.SCRAPER_PAUSA_MIN, config.SCRAPER_PAUSA_MAX)
    
    # Añadir variación extra para evitar patrones
    if random.random() < 0.4:  # 40% de probabilidad de pausa extra
        pausa += random.uniform(2.0, 4.0)
    
    # 15% de probabilidad de pausa muy larga (simulación de lectura)
    if random.random() < 0.15:
        pausa += random.uniform(5.0, 8.0)
    
    print(f"   (pausa {pausa:.1f}s)")
    time.sleep(pausa)


def pausa_entre_fuentes():
    """Entre portales para no encadenar ráfagas."""
    mn = float(getattr(config, "PAUSA_ENTRE_FUENTES_MIN", 18.0))
    mx = float(getattr(config, "PAUSA_ENTRE_FUENTES_MAX", 30.0))
    if mx < mn:
        mx = mn
    
    # Pausa base con variación extra
    pausa = random.uniform(mn, mx)
    
    # 35% de probabilidad de pausa extra larga
    if random.random() < 0.35:
        pausa += random.uniform(3.0, 7.0)
    
    # 10% de probabilidad de pausa muy larga (simulación de cambio de portal)
    if random.random() < 0.10:
        pausa += random.uniform(8.0, 12.0)
    
    print(f"   (pausa entre fuentes {pausa:.1f}s)")
    time.sleep(pausa)


def pausa_larga_aleatoria():
    """Pausa larga aleatoria para evitar detección prolongada."""
    # Pausa de 30-90 segundos aleatoria
    pausa = random.uniform(30.0, 90.0)
    
    print(f"   (pausa larga anti-bloqueo {pausa:.1f}s)")
    time.sleep(pausa)


def verificar_y_pausar_si_necesario(respuesta, portal_nombre=""):
    """Verifica si hay respuesta de bloqueo y pausa si es necesario."""
    
    # Verificar códigos de bloqueo comunes
    bloqueo_codes = [429, 403, 503, 502, 418, 404]  # Añadir 404
    
    if respuesta.status_code in bloqueo_codes:
        if respuesta.status_code == 404:
            print(f"   (!) Error 404 en {portal_nombre} - página no encontrada (posible bloqueo)")
        elif respuesta.status_code == 403:
            print(f"   (!) Error 403 en {portal_nombre} - acceso prohibido (bloqueo activo)")
        else:
            print(f"   (!) Posible bloqueo en {portal_nombre} (código {respuesta.status_code})")
        
        pausa_larga_aleatoria()
        return True
    
    # Verificar texto de bloqueo en respuesta
    texto_bloqueo = [
        "too many requests",
        "rate limit",
        "blocked",
        "captcha",
        "access denied",
        "forbidden",
        "service unavailable",
        "demasiadas solicitudes",
        "bloqueado",
        "captcha",
        "not found",
        "page not found",
        "acceso denegado",
        "prohibido",
        "restringido"
    ]
    
    if any(palabra in respuesta.text.lower() for palabra in texto_bloqueo):
        print(f"   (!) Texto de bloqueo detectado en {portal_nombre}")
        pausa_larga_aleatoria()
        return True
    
    return False


def manejar_error_http(respuesta, portal_nombre=""):
    """Maneja específicamente errores HTTP comunes."""
    
    if respuesta.status_code == 404:
        print(f"   [404] {portal_nombre}: Página no encontrada - posible cambio de URL o bloqueo")
        # Pausa más larga para 404
        pausa = random.uniform(60.0, 120.0)  # 1-2 minutos
        print(f"   (pausa por 404: {pausa:.1f}s)")
        time.sleep(pausa)
        return "bloqueo_temporal"
    
    elif respuesta.status_code == 403:
        print(f"   [403] {portal_nombre}: Acceso prohibido - bloqueo activo")
        # Pausa muy larga para 403
        pausa = random.uniform(120.0, 300.0)  # 2-5 minutos
        print(f"   (pausa por 403: {pausa:.1f}s)")
        time.sleep(pausa)
        return "bloqueo_fuerte"
    
    elif respuesta.status_code == 429:
        print(f"   [429] {portal_nombre}: Demasiadas peticiones - rate limit")
        # Pausa estándar para 429
        pausa_larga_aleatoria()
        return "rate_limit"
    
    elif respuesta.status_code in [500, 502, 503]:
        print(f"   [{respuesta.status_code}] {portal_nombre}: Error del servidor")
        # Pausa moderada para errores de servidor
        pausa = random.uniform(30.0, 60.0)  # 30-60 segundos
        print(f"   (pausa por error {respuesta.status_code}: {pausa:.1f}s)")
        time.sleep(pausa)
        return "error_servidor"
    
    return None


# Sistema de desactivación temporal de portales
PORTALES_ERROR_COUNT = {}
PORTALES_DESACTIVADOS_TEMP = {}
MAX_ERRORES_PORTAL = 3  # Máximo de errores antes de desactivar
TIEMPO_DESACTIVACION = 1800  # 30 minutos en segundos


def registrar_error_portal(portal_nombre: str, tipo_error: str):
    """Registra errores de un portal y desactiva si hay demasiados."""
    
    # Incrementar contador de errores
    PORTALES_ERROR_COUNT[portal_nombre] = PORTALES_ERROR_COUNT.get(portal_nombre, 0) + 1
    
    print(f"   [ERROR] {portal_nombre}: {tipo_error} (total: {PORTALES_ERROR_COUNT[portal_nombre]})")
    
    # Verificar si se debe desactivar temporalmente
    if PORTALES_ERROR_COUNT[portal_nombre] >= MAX_ERRORES_PORTAL:
        print(f"   [DESACTIVADO] {portal_nombre}: Demasiados errores ({PORTALES_ERROR_COUNT[portal_nombre]})")
        print(f"   [DESACTIVADO] {portal_nombre}: Desactivado por 30 minutos")
        
        # Desactivar temporalmente
        PORTALES_DESACTIVADOS_TEMP[portal_nombre] = time.time() + TIEMPO_DESACTIVACION
        
        # Resetear contador
        PORTALES_ERROR_COUNT[portal_nombre] = 0
        
        return True  # Portal desactivado
    
    return False  # Portal sigue activo


def esta_portal_desactivado(portal_nombre: str) -> bool:
    """Verifica si un portal está desactivado temporalmente."""
    
    if portal_nombre not in PORTALES_DESACTIVADOS_TEMP:
        return False
    
    # Verificar si ya pasó el tiempo de desactivación
    tiempo_reactivacion = PORTALES_DESACTIVADOS_TEMP[portal_nombre]
    
    if time.time() >= tiempo_reactivacion:
        # Reactivar portal
        print(f"   [REACTIVADO] {portal_nombre}: Reactivado después de 30 minutos")
        del PORTALES_DESACTIVADOS_TEMP[portal_nombre]
        PORTALES_ERROR_COUNT[portal_nombre] = 0  # Resetear contador
        return False
    
    return True  # Sigue desactivado


def limpiar_portales_desactivados():
    """Limpia portales cuyo tiempo de desactivación ha expirado."""
    
    portales_a_eliminar = []
    tiempo_actual = time.time()
    
    for portal, tiempo_reactivacion in PORTALES_DESACTIVADOS_TEMP.items():
        if tiempo_actual >= tiempo_reactivacion:
            portales_a_eliminar.append(portal)
            print(f"   [REACTIVADO] {portal}: Reactivado automáticamente")
            PORTALES_ERROR_COUNT[portal] = 0
    
    for portal in portales_a_eliminar:
        del PORTALES_DESACTIVADOS_TEMP[portal]


def titulo_sugiere_inmobiliaria(titulo: str) -> bool:
    """
    Filtro ultra restrictivo para detectar SOLO inmobiliarias reales.
    Máxima prioridad: NO filtrar particulares NUNCA.
    """
    t = titulo.lower().strip()
    
    # === DEBUG: Mostrar qué se está analizando ===
    print(f"   [DEBUG] Analizando título: '{titulo}'")
    
    # === PALABRAS QUE INDICAN INMOBILIARIA 100% SEGURO ===
    palabras_inmobiliaria_seguras = {
        'inmobiliaria', 'inmobiliarias', 'inmob', 'inmo', 'inmo.', 'inmob.',
        'remax', 'remax ', 'engel & volkers', 'engel', 'coldwell banker',
        'keller williams', 'century 21', 'nova finques', 'cèntric finques',
        'aproperties', 'api properties', 'goldmark', 'signature luxury homes',
        'finques', 'real estate', 'properties', 'property', 'realstate',
        'estate', 'estate agency', 'estate agents', 'realty', 'realty group',
        'tas'  # Término específico de tasación inmobiliaria
    }
    
    # === PALABRAS QUE INDICAN EMPRESA/NEGOCIO ===
    palabras_empresa = {
        'asesores', 'asesor', 'asesora', 'gestión', 'gestion', 'grupo',
        'holding', 'empresa', 'empresas', 'corporation', 'corp', 'ltd',
        'company', 'sl', 'sa', 's.l.', 'investment', 'capital',
        'oportunidad', 'inversión', 'inversion', 'promo', 'promoción',
        'urbanismo', 'construcción', 'obras nuevas', 'obra nueva',
        'promotor', 'promotora', 'desarrollador', 'desarrolladora',
        'negocio', 'negocios', 'comercial', 'comerciales', 'broker', 'brokers',
        'agent', 'agents', 'agente', 'agentes', 'team', 'equipo',
        'staff', 'personal', 'central', 'centro', 'servicio', 'servicios',
        'administrador', 'administradora', 'administradores',
        'consultor', 'consultora', 'consultores', 'manager',
        'directivo', 'director', 'directora', 'profesional',
        'profesionales', 'sr', 'sra', 'dña', 'don',
        # Términos adicionales que podrían usar inmobiliarias
        'asesoría', 'asesoramiento', 'consultoría', 'consultoría',
        'inmobiliario', 'inmobiliaria', 'finca raíz', 'finca urbana',
        'promoción inmobiliaria', 'promociones inmobiliarias',
        'construcción nueva', 'construcciones nuevas', 'obra en construcción',
        'desarrollo inmobiliario', 'desarrollos inmobiliarios',
        'marketing inmobiliario', 'marketing inmobiliario',
        'publicidad inmobiliaria', 'publicidad inmobiliaria',
        'servicios inmobiliarios', 'servicio inmobiliario',
        'gestión inmobiliaria', 'gestión del patrimonio',
        'administración de fincas', 'administración de inmuebles',
        'correduría', 'corredor', 'corredores',
        'intermediación', 'intermediario', 'intermediarios',
        'comisión', 'comisiones', 'fee', 'fees',
        'honorarios', 'honorario', 'costes', 'costes de gestión',
        'tasación', 'tasador', 'tasadores', 'valoración',
        'perito', 'peritos', 'peritaje', 'informe pericial',
        'certificación', 'certificado', 'registro', 'registral',
        'notaría', 'notario', 'notarial', 'escritura',
        'propiedad horizontal', 'comunidad de vecinos', 'comunidad de propietarios',
        'urbanizable', 'urbanizable', 'suelo urbanizable',
        'licencia', 'licencia de obra', 'licencia de actividad',
        'permiso', 'permisos', 'permiso de construcción',
        'calificación energética', 'certificado energético',
        'reforma', 'reformas', 'rehabilitación', 'rehabilitación de edificios',
        'restauración', 'restauración de inmuebles',
        'conservación', 'conservación de patrimonio',
        'patrimonio', 'patrimonio histórico', 'patrimonio cultural',
        'expropiación', 'expropiación de inmuebles', 'desahucio',
        'alquiler', 'arrendamiento', 'arrendador', 'arrendadora',
        'contrato', 'contratos', 'contrato de arrendamiento',
        'fianza', 'fianzas', 'depósito', 'depósitos',
        'garantía', 'garantías', 'aval', 'avales',
        'subasta', 'subastas', 'subasta judicial', 'subasta notarial',
        'remate', 'remates', 'remate judicial',
        'desalojo', 'desahucio', 'desalojo forzoso',
        'ocupación', 'ocupación ilegal', 'desalojo',
        'reivindicación', 'reivindicaciones', 'deslinde',
        'servidumbre', 'servidumbres', 'cargas', 'cargas reales',
        'gravamen', 'gravámenes', 'anotación', 'anotaciones registrales',
        'hipoteca', 'hipotecas', 'préstamo', 'préstamos',
        'crédito', 'créditos', 'financiación', 'financiera',
        'banco', 'banca', 'entidad bancaria', 'caja',
        'seguro', 'seguros', 'póliza', 'pólizas',
        'impuesto', 'impuestos', 'ibi', 'plusvalía', 'iplusvalía',
        'municipal', 'autonómica', 'estatal', 'gobierno',
        'ayuntamiento', 'ayuntamiento', 'consistorio', 'diputación',
        'comunidad autónoma', 'generalitat', 'gobierno regional',
        'urbanismo', 'planeamiento', 'planeamiento urbanístico',
        'pgou', 'plan general', 'plan parcial',
        'normativa', 'normativa urbanística', 'reglamento',
        'ley', 'leyes', 'código civil', 'legislación',
        'jurídico', 'jurídica', 'abogado', 'abogados',
        'bufete', 'bufetes', 'despacho', 'despachos',
        'procurador', 'procuradores', 'procuradoría',
        'mandato', 'mandatos', 'representación', 'representante',
        'poder', 'poderes', 'poder notarial',
        'sucesión', 'sucesiones', 'herencia', 'herencias',
        'donación', 'donaciones', 'donante', 'donatario',
        'compraventa', 'compraventa de inmuebles',
        'permuta', 'permutas', 'permuta de viviendas',
        'cesión', 'cesiones', 'cesión de derechos',
        'usufructo', 'usufructos', 'nuda propiedad',
        'uso', 'derecho de uso', 'habitación', 'derecho de habitación'
    }
    
    # === CONTEXTOS QUE INDICAN 100% PARTICULAR ===
    contextos_particular_definitivos = {
        'particular', 'particulares', 'propietario', 'dueño', 'dueña',
        'directo', 'sin comisión', 'sin comision', 'sin intermediario',
        'particular a particular', 'de particular', 'por particular',
        'propietario directo', 'dueño directo', 'sin agencia',
        'sin inmobiliaria', 'sin tasación', 'sin gastos de agencia',
        'trato directo', 'contacto directo', 'llamar al dueño',
        'llamar al propietario', 'particular vende', 'particular alquila'
    }
    
    # === FRASES COMPLETAS DE PARTICULARES ===
    frases_particular_definitivas = [
        'vendo particular', 'alquilo particular', 'particular vende',
        'particular alquila', 'dueño vende', 'dueño alquila',
        'propietario vende', 'propietario alquila', 'sin intermediarios',
        'sin comisiones', 'compra directa', 'venta directa',
        'alquiler directo', 'contacto con propietario'
    ]
    
    # === TIPOS DE PROPIEDAD (NUNCA FILTRAR) ===
    tipos_propiedad = {
        'finca', 'fincas', 'piso', 'pisos', 'chalet', 'chalets', 
        'ático', 'aticos', 'dúplex', 'duplex', 'estudio', 'estudios',
        'loft', 'lofts', 'garaje', 'garajes', 'trastero', 'trasteros',
        'local', 'locales', 'oficina', 'oficinas', 'nave', 'naves',
        'terreno', 'terrenos', 'solar', 'solares', 'parcela', 'parcelas',
        'rustica', 'rustico', 'rústica', 'rústico', 'casa', 'casas',
        'apartamento', 'apartamentos', 'villa', 'villas', 'masia', 'masias',
        'bungalow', 'bungalows', 'estudio', 'estudios', 'loft', 'lofts'
    }
    
    # === VERIFICACIÓN ULTRA restrictiva ===
    
    # PASO 1: Si hay contexto definitivo de particular, NUNCA filtrar
    for contexto in contextos_particular_definitivos:
        if contexto in t:
            print(f"   [DEBUG] Contexto particular encontrado: '{contexto}' -> NO FILTRAR")
            return False
    
    # PASO 2: Si hay frase definitiva de particular, NUNCA filtrar
    for frase in frases_particular_definitivas:
        if frase in t:
            print(f"   [DEBUG] Frase particular encontrada: '{frase}' -> NO FILTRAR")
            return False
    
    # PASO 3: Si es SOLO tipo de propiedad, NUNCA filtrar
    palabras_titulo = t.split()
    if len(palabras_titulo) <= 4:  # Títulos cortos
        solo_tipos_propiedad = True
        for palabra in palabras_titulo:
            if palabra not in tipos_propiedad:
                solo_tipos_propiedad = False
                break
        
        if solo_tipos_propiedad:
            print(f"   [DEBUG] Solo tipos de propiedad -> NO FILTRAR")
            return False
    
    # PASO 4: Palabras seguras de inmobiliaria (100% filtrar)
    for palabra in palabras_inmobiliaria_seguras:
        if palabra in t:
            print(f"   [DEBUG] Palabra inmobiliaria segura: '{palabra}' -> FILTRAR")
            return True
    
    # PASO 5: Palabras de empresa (con verificación estricta)
    for palabra in palabras_empresa:
        if len(palabra) <= 3:
            continue
            
        if palabra in t:
            # Verificación estricta: no debe haber contexto de particular
            for contexto in contextos_particular_definitivos:
                if contexto in t:
                    print(f"   [DEBUG] Palabra empresa '{palabra}' con contexto particular '{contexto}' -> NO FILTRAR")
                    return False
            
            # Verificación estricta: no debe ser solo tipo de propiedad
            if palabra in tipos_propiedad:
                print(f"   [DEBUG] Palabra empresa '{palabra}' es tipo de propiedad -> NO FILTRAR")
                return False
            
            print(f"   [DEBUG] Palabra empresa detectada: '{palabra}' -> FILTRAR")
            return True
    
    print(f"   [DEBUG] Sin criterios de filtrado -> NO FILTRAR")
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
    """
    Realiza petición GET con reintentos y manejo de 403/429.
    """
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
    """
    GET de página de listado con pausa previa y reintento ante 429.
    """
    pausa_entre_peticiones()
    return _get_con_reintento(session, url)
