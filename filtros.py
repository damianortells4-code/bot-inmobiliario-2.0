import config
from portales_comun import PALABRAS_INMOBILIARIA

# Señales de anuncio de particular (al menos una si EXIGIR… está activo).
# Orden: frases largas antes que subcadenas.
PALABRAS_PARTICULAR = [
    "particular vende",
    "vendo particular",
    "alquiler particular",
    "de particular",
    "sin intermediarios",
    "trato directo",
    "trato directo con propietario",
    "directo propietario",
    "directo dueño",
    "contactar directo",
    "sin comisión",
    "sin comisiones",
    "sin intermediario",
    "sin intermediarios",
    "propietario",
    "propietaria",
    "particulares",
    "particular",
    "dueño",
    "dueña",
    "dueño directo",
    "propietario directo",
    "particular directo",
    "vende dueño",
    "alquila dueño",
    "vende propietario",
    "alquila propietario",
    "particular sin comision",
    "dueño sin comision",
    "propietario sin comision",
    "directo sin intermediarios",
    "particular alquila",
    "particular vende piso",
    "dueño alquila piso",
    "propietario alquila piso",
    "sin agencia",
    "sin agencias",
    "sin inmobiliaria",
    "sin inmobiliarias",
    "particular particular",
    "dueño particular",
    "propietario particular",
    "privado",
    "privada",
    "particular privado",
    "dueño privado",
    "propietario privado",
]

# Refuerzo: agencia (inmobiliaria ya está en portales_comun)
PALABRAS_AGENCIA_EXTRA = [
    "agencia",
    "llámanos",
    "llamanos",
    "asesoramiento inmobiliario",
    "equipo comercial",
    "captación",
    "contacta",
    "contacto",
    "teléfono",
    "telefono",
    "llamar",
    "llame",
    "consulta",
    "información",
    "informacion",
    "visita",
    "visitar",
    "cita",
    "citar",
    "asesor",
    "asesora",
    "asesores",
    "comercial",
    "comerciales",
    "agente",
    "agentes",
    "broker",
    "brokers",
    "consultor",
    "consultora",
    "consultores",
    "gestor",
    "gestora",
    "gestores",
    "administrador",
    "administradora",
    "administradores",
]


def es_particular(texto: str) -> bool:
    """
    True solo si parece anuncio de particular:
    - rechaza señales claras de agencia / inmobiliaria
    - si EXIGIR_PALABRA_PARTICULAR_EN_TITULO: exige al menos una PALABRAS_PARTICULAR
    """
    t = texto.lower()

    for palabra in PALABRAS_INMOBILIARIA:
        if len(palabra) <= 3:
            continue
        if palabra in t:
            return False

    for palabra in PALABRAS_AGENCIA_EXTRA:
        if palabra in t:
            return False

    for palabra in PALABRAS_PARTICULAR:
        if palabra in t:
            return True

    if getattr(config, "EXIGIR_PALABRA_PARTICULAR_EN_TITULO", True):
        return False

    return True
