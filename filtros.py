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
    "particular alquila sin comision",
    "dueño alquila sin comision",
    "propietario alquila sin comision",
    "vendo sin comision",
    "alquilo sin comision",
    "particular vende sin comision",
    "dueño vende sin comision",
    "propietario vende sin comision",
    "trato directo con dueño",
    "trato directo con propietario",
    "contacto directo con dueño",
    "contacto directo con propietario",
    "llamar directamente al dueño",
    "llamar directamente al propietario",
    "hablar directamente con dueño",
    "hablar directamente con propietario",
    "sin costes de agencia",
    "sin gastos de agencia",
    "sin comision de agencia",
    "sin comision de inmobiliaria",
    "alquiler directo dueño",
    "alquiler directo propietario",
    "venta directa dueño",
    "venta directa propietario",
    "particular alquila directamente",
    "particular vende directamente",
    "dueño alquila directamente",
    "dueño vende directamente",
    "propietario alquila directamente",
    "propietario vende directamente",
    "sin intermediarios de pago",
    "sin comisiones de intermediacion",
    "contacto particular",
    "contacto dueño",
    "contacto propietario",
    "llamar dueño",
    "llamar propietario",
    "telefono particular",
    "telefono dueño",
    "telefono propietario",
    "móvil particular",
    "móvil dueño",
    "móvil propietario",
    "whatsapp particular",
    "whatsapp dueño",
    "whatsapp propietario",
    "particular no profesional",
    "dueño no profesional",
    "propietario no profesional",
    "particular sin empresa",
    "dueño sin empresa",
    "propietario sin empresa",
    "particular independiente",
    "dueño independiente",
    "propietario independiente",
    "vivienda de particular",
    "piso de particular",
    "chalet de particular",
    "ático de particular",
    "dúplex de particular",
    "estudio de particular",
    "loft de particular",
    "garaje de particular",
    "trastero de particular",
    "local de particular",
    "nave de particular",
    "terreno de particular",
    "solar de particular",
    "finca de particular",
    "parcela de particular",
    "casa de particular",
    "apartamento de particular",
    "vivienda de dueño",
    "piso de dueño",
    "chalet de dueño",
    "ático de dueño",
    "dúplex de dueño",
    "estudio de dueño",
    "loft de dueño",
    "garaje de dueño",
    "trastero de dueño",
    "local de dueño",
    "nave de dueño",
    "terreno de dueño",
    "solar de dueño",
    "finca de dueño",
    "parcela de dueño",
    "casa de dueño",
    "apartamento de dueño",
    "vivienda de propietario",
    "piso de propietario",
    "chalet de propietario",
    "ático de propietario",
    "dúplex de propietario",
    "estudio de propietario",
    "loft de propietario",
    "garaje de propietario",
    "trastero de propietario",
    "local de propietario",
    "nave de propietario",
    "terreno de propietario",
    "solar de propietario",
    "finca de propietario",
    "parcela de propietario",
    "casa de propietario",
    "apartamento de propietario",
]

# Refuerzo: agencia (inmobiliaria ya está en portales_comun)
PALABRAS_AGENCIA_EXTRA = [
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
    "empresa",
    "empresas",
    "negocio",
    "negocios",
    "profesional",
    "profesionales",
    "servicio",
    "servicios",
    "atención",
    "atencion",
    "cliente",
    "clientes",
    "venta",
    "vendedor",
    "vendedora",
    "vendedores",
    "team",
    "equipo",
    "staff",
    "personal",
    "oficina",
    "oficinas",
    "central",
    "centro",
    "contact",
    "contactar",
    "llamada",
    "llamadas",
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
    "inmobiliario",
    "inmobiliaria.",
    "inmobiliarios",
    "inmobiliarias",
    "real",
    "estate",
    "realstate",
    "real-estate",
    "realestate",
    "properties",
    "property",
    "homes",
    "home",
    "house",
    "houses",
    "apartments",
    "apartment",
    "flats",
    "flat",
    "nueva construcción",
    "nueva construccion",
    "obra nueva",
    "estreno",
    "estrenar",
    "promoción",
    "promocion",
    "promo",
    "promotor",
    "promotora",
    "desarrollador",
    "desarrolladora",
    "constructora",
    "constructor",
    "construcción",
    "construccion",
    "reforma",
    "reformas",
    "reformado",
    "reformada",
    "restaurado",
    "restaurada",
    "restauración",
    "restauracion",
    "diseño",
    "diseño interior",
    "diseño",
    "arquitecto",
    "arquitecta",
    "arquitectos",
    "decorador",
    "decoradora",
    "decoradores",
    "interiorista",
    "interioristas",
    "diseñador",
    "diseñadora",
    "diseñadores",
    "mobiliario",
    "muebles",
    "amueblado",
    "amueblada",
    "sin amueblar",
    "sin amueblar",
    "amueblar",
    "equipado",
    "equipada",
    "sin equipar",
    "sin equipar",
    "equipar",
    "cocina",
    "cocinas",
    "baño",
    "baños",
    "aseos",
    "terraza",
    "terrazas",
    "balcón",
    "balcon",
    "balcones",
    "jardín",
    "jardin",
    "jardines",
    "piscina",
    "piscinas",
    "garaje",
    "garajes",
    "parking",
    "parkings",
    "trastero",
    "trasteros",
    "ascensor",
    "ascensores",
    "calefacción",
    "calefaccion",
    "aire acondicionado",
    "aire",
    "acondicionado",
    "aire acondicionado",
    "gas",
    "gasto",
    "gastos",
    "comunidad",
    "comunidades",
    "ibí",
    "ibi",
    "plusvalía",
    "plusvalia",
    "impuestos",
    "impuesto",
    "tasación",
    "tasacion",
    "valor",
    "valores",
    "precio",
    "precios",
    "coste",
    "costes",
    "inversión",
    "inversion",
    "rentabilidad",
    "renta",
    "rentar",
    "alquilar",
    "alquiler",
    "alquilado",
    "alquilada",
    "arrendar",
    "arrendamiento",
    "arrendado",
    "arrendada",
    "contrato",
    "contratos",
    "fianza",
    "fianzas",
    "depósito",
    "depositos",
    "mensual",
    "mensuales",
    "mes",
    "meses",
    "año",
    "años",
    "día",
    "días",
    "semana",
    "semanas",
    "inmediato",
    "inmediata",
    "urgente",
    "urgentes",
    "rápido",
    "rapida",
    "rápidos",
    "rapidas",
    "inmediato",
    "inmediatos",
    "inmediatas",
    "disponible",
    "disponibles",
    "disponibilidad",
    "libre",
    "libres",
    "ocupado",
    "ocupados",
    "ocupada",
    "ocupadas",
    "vacío",
    "vacio",
    "vacíos",
    "vacios",
    "nuevo",
    "nueva",
    "nuevos",
    "nuevas",
    "antiguo",
    "antigua",
    "antiguos",
    "antiguas",
    "moderno",
    "moderna",
    "modernos",
    "modernas",
    "antiguo",
    "antigua",
    "antiguos",
    "antiguas",
    "reformado",
    "reformada",
    "reformados",
    "reformadas",
    "buen estado",
    "buen estado",
    "muy buen estado",
    "muy buen estado",
    "a estrenar",
    "a estrenar",
    "seminuevo",
    "seminueva",
    "seminuevos",
    "seminuevas",
    "segunda mano",
    "segunda mano",
    "ocasión",
    "ocasion",
    "oportunidad",
    "oportunidades",
    "chollo",
    "chollos",
    "oferta",
    "ofertas",
    "rebaja",
    "rebajas",
    "descuento",
    "descuentos",
    "barato",
    "barata",
    "baratos",
    "baratas",
    "económico",
    "economico",
    "económica",
    "economica",
    "económicos",
    "economicos",
    "económicas",
    "economicas",
    "asequible",
    "asequibles",
    "accesible",
    "accesibles",
    "financiado",
    "financiada",
    "financiados",
    "financiadas",
    "financiación",
    "financiacion",
    "hipoteca",
    "hipotecas",
    "préstamo",
    "prestamo",
    "préstamos",
    "prestamos",
    "banco",
    "bancos",
    "caja",
    "cajas",
    "entidad",
    "entidades",
    "financiera",
    "financieras",
    "financiero",
    "financieros",
    "crédito",
    "credito",
    "créditos",
    "creditos",
    "banca",
    "banca",
    "bancario",
    "bancaria",
    "bancarios",
    "bancarias",
    "financiero",
    "financiera",
    "financieros",
    "financieras",
    "dinero",
    "euros",
    "eur",
    "euro",
    "pesetas",
    "peseta",
    "moneda",
    "monedas",
    "cambio",
    "cambios",
    "tipo",
    "tipos",
    "tasa",
    "tasas",
    "interés",
    "interes",
    "intereses",
    "cuota",
    "cuotas",
    "pago",
    "pagos",
    "pagar",
    "pagado",
    "pagada",
    "pagados",
    "pagadas",
    "abono",
    "abonos",
    "abonado",
    "abonada",
    "abonados",
    "abonadas",
    "ingreso",
    "ingresos",
    "entrada",
    "entradas",
    "inicial",
    "iniciales",
    "reserva",
    "reservas",
    "aparte",
    "apartes",
    "apartar",
    "apartado",
    "apartada",
    "apartados",
    "apartadas",
    "señal",
    "senal",
    "seña",
    "senya",
    "señales",
    "senales",
    "señas",
    "senyas",
    "confirmación",
    "confirmacion",
    "confirmado",
    "confirmada",
    "confirmados",
    "confirmadas",
    "reservado",
    "reservada",
    "reservados",
    "reservadas",
    "anotado",
    "anotada",
    "anotados",
    "anotadas",
    "apuntado",
    "apuntada",
    "apuntados",
    "apuntadas",
    "inscrito",
    "inscrita",
    "inscritos",
    "inscritas",
    "registrado",
    "registrada",
    "registrados",
    "registradas",
    "matriculado",
    "matriculada",
    "matriculados",
    "matriculadas",
    "certificado",
    "certificada",
    "certificados",
    "certificadas",
    "legal",
    "legales",
    "legalizado",
    "legalizada",
    "legalizados",
    "legalizadas",
    "registrado",
    "registrada",
    "registrados",
    "registradas",
    "inscrito",
    "inscrita",
    "inscritos",
    "inscritas",
    "matriculado",
    "matriculada",
    "matriculados",
    "matriculadas",
    "catastro",
    "catastral",
    "catastrales",
    "registro",
    "registral",
    "registrales",
    "notaría",
    "notaria",
    "notario",
    "notaria",
    "notarios",
    "notarias",
    "protocolo",
    "protocolos",
    "escritura",
    "escrituras",
    "título",
    "titulo",
    "títulos",
    "titulos",
    "propiedad",
    "propiedades",
    "propietario",
    "propietaria",
    "propietarios",
    "propietarias",
    "dueño",
    "dueña",
    "dueños",
    "dueñas",
    "titular",
    "titular",
    "titulares",
    "copropietario",
    "copropietaria",
    "copropietarios",
    "copropietarias",
    "comunidad",
    "comunidades",
    "vecinos",
    "vecinas",
    "vecindario",
    "urbanización",
    "urbanizacion",
    "urbanizaciones",
    "polígono",
    "poligono",
    "polígonos",
    "poligonos",
    "parcela",
    "parcelas",
    "solar",
    "solares",
    "terreno",
    "terrenos",
    "suelo",
    "suelos",
    "calle",
    "calles",
    "avenida",
    "avenidas",
    "plaza",
    "plazas",
    "paseo",
    "paseos",
    "ronda",
    "rondas",
    "carrera",
    "carreras",
    "camino",
    "caminos",
    "carretera",
    "carreteras",
    "autopista",
    "autopistas",
    "autovía",
    "autovia",
    "autovías",
    "autovias",
    "nacional",
    "nacionales",
    "comarcal",
    "comarcales",
    "provincial",
    "provinciales",
    "local",
    "locales",
    "municipal",
    "municipales",
    "urbano",
    "urbanos",
    "rústico",
    "rustico",
    "rústicos",
    "rusticos",
    "agrícola",
    "agricola",
    "agrícolas",
    "agricolas",
    "ganadero",
    "ganadera",
    "ganaderos",
    "ganaderas",
    "forestal",
    "forestales",
    "industrial",
    "industriales",
    "comercial",
    "comerciales",
    "residencial",
    "residenciales",
    "turístico",
    "turistico",
    "turísticos",
    "turisticos",
    "turística",
    "turistica",
    "turísticas",
    "turisticas",
    "vacacional",
    "vacacionales",
    "segunda residencia",
    "segunda residencia",
    "primera residencia",
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


def es_particular(texto: str) -> bool:
    """
    True solo si parece anuncio de particular:
    - rechaza señales claras de agencia / inmobiliaria
    - si EXIGIR_PALABRA_PARTICULAR_EN_TITULO: exige al menos una PALABRAS_PARTICULAR
    - ahora también detecta estilo de agencia camuflada
    """
    t = texto.lower()
    
    # 1. Rechazo directo por palabras de agencia/inmobiliaria
    for p in PALABRAS_INMOBILIARIA + PALABRAS_AGENCIA_EXTRA:
        if p in t:
            return False
    
    # 2. Detección de estilo de agencia camuflada
    if _estilo_agencia_camuflada(texto):
        return False
    
    # 3. Si exige palabra particular, verificar que la tenga
    if config.EXIGIR_PALABRA_PARTICULAR_EN_TITULO:
        return any(p in t for p in PALABRAS_PARTICULAR)
    
    # 4. Si no exige palabra particular, aceptar si no es agencia
    return True


def _estilo_agencia_camuflada(texto: str) -> bool:
    """
    Detecta si el texto parece de agencia aunque use palabras de particular.
    Analiza patrones de lenguaje profesional.
    """
    t = texto.lower()
    original = texto
    
    # 1. Demasiada información profesional estructurada
    if _tiene_info_profesional_excesiva(t):
        return True
    
    # 2. Lenguaje demasiado formal o comercial
    if _lenguaje_demasiado_formal(t):
        return True
    
    # 3. Patrones de marketing
    if _contiene_marketing_oculto(t):
        return True
    
    # 4. Estructura muy organizada (como plantilla)
    if _estructura_demasiado_organizada(original):
        return True
    
    # 5. Números y precios muy específicos
    if _precios_demasiado_profesionales(t):
        return True
    
    # 6. Contacto múltiple (señal de profesional)
    if _contacto_multiple_profesional(t):
        return True
    
    return False


def _tiene_info_profesional_excesiva(texto: str) -> bool:
    """Detecta si hay demasiada información profesional."""
    
    # Contar menciones a diferentes tipos de contacto
    contactos = 0
    if any(word in texto for word in ['teléfono', 'telefono', 'phone', 'móvil', 'movil']):
        contactos += 1
    if any(word in texto for word in ['whatsapp', 'wp', 'wsp']):
        contactos += 1
    if any(word in texto for word in ['email', 'mail', 'correo', 'e-mail']):
        contactos += 1
    if any(word in texto for word in ['web', 'página', 'pagina', 'online']):
        contactos += 1
    
    # Si tiene 3+ tipos de contacto, es probablemente profesional
    if contactos >= 3:
        return True
    
    # Menciones a horarios específicos (señal de profesional)
    horarios = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo',
                'mañana', 'tarde', 'noche', '24h', '24 horas', 'horario', 'atención', 'atencion']
    if sum(1 for h in horarios if h in texto) >= 2:
        return True
    
    return False


def _lenguaje_demasiado_formal(texto: str) -> bool:
    """Detecta lenguaje demasiado formal o comercial."""
    
    # Palabras formales/comerciales
    palabras_formales = [
        'exclusivo', 'exclusiva', 'exclusivos', 'exclusivas',
        'privilegio', 'privilegios', 'oportunidad única', 'oportunidad única',
        'inversión', 'inversion', 'rentabilidad', 'renta',
        'financiado', 'financiada', 'financiamiento',
        'promoción', 'promocion', 'oferta especial', 'oferta especial',
        'servicio', 'servicios', 'atención', 'atencion', 'cliente',
        'profesional', 'profesionales', 'calidad', 'garantía', 'garantia',
        'excelente', 'excelentes', 'excepcional', 'excepcionales',
        'inmejorable', 'inmejorables', 'único', 'unica', 'únicos', 'unicas',
        'premium', 'lujo', 'deluxe', 'high-end', 'vip',
        'estratégico', 'estrategica', 'estratégicos', 'estrategicas',
        'ubicación privilegiada', 'ubicacion privilegiada',
        'zona exclusiva', 'zonas exclusivas', 'área premium'
    ]
    
    # Si tiene 3+ palabras formales, es sospechoso
    count = sum(1 for word in palabras_formales if word in texto)
    if count >= 3:
        return True
    
    # Uso de abreviaturas profesionales
    abreviaturas = ['s.l.', 'sl', 'sa', 'ltd', 'ltd.', 'cif', 'nif', 'dni']
    if any(abr in texto for abr in abreviaturas):
        return True
    
    return False


def _contiene_marketing_oculto(texto: str) -> bool:
    """Detecta patrones de marketing ocultos."""
    
    # Frases de marketing
    frases_marketing = [
        'no te quedes sin', 'última oportunidad', 'últimas unidades',
        'precio rebajado', 'precio reducido', 'super oferta',
        'oferta limitada', 'plazas limitadas', 'oportunidad única',
        'inversión segura', 'inversion segura', 'rentabilidad asegurada',
        'no te arrepentirás', 'no te arrepentiras', 'decisión acertada',
        'elección perfecta', 'eleccion perfecta', 'no encontrarás mejor',
        'no encontraras mejor', 'la mejor opción', 'la mejor opcion',
        'calidad precio', 'relacion calidad', 'calidad-precio',
        'más por menos', 'mas por menos', 'ahorra dinero',
        'ahorra comprando', 'compra inteligente', 'inversión inteligente',
        'negocio seguro', 'negocio seguro', 'inversión segura',
        'oportunidad de oro', 'oportunidad de oro', 'gangas',
        'chollo', 'chollos', 'rebaja', 'rebajas', 'liquidación',
        'liquidacion', 'stock limitado', 'unidades limitadas'
    ]
    
    if any(frase in texto for frase in frases_marketing):
        return True
    
    # Emojis excesivos (señal de marketing)
    emoji_count = sum(1 for char in texto if char in ['!', '¡', '?', '¿', '*', '·', '·', '°', 'º', 'ª'])
    if emoji_count >= 5:
        return True
    
    return False


def _estructura_demasiado_organizada(texto: str) -> bool:
    """Detecta si el texto está demasiado estructurado (plantilla)."""
    
    # Muchas líneas separadas por guiones o puntos
    lineas = texto.split('\n')
    lineas_con_formato = 0
    
    for linea in lineas:
        linea_limpia = linea.strip()
        if not linea_limpia:
            continue
            
        # Si empieza con viñetas o números
        if any(linea_limpia.startswith(pref) for pref in ['-', '·', '·', '°', 'º', 'ª', '1.', '2.', '3.', '4.', '5.', 'a)', 'b)', 'c)']):
            lineas_con_formato += 1
        
        # Si tiene muchos dos puntos (descripciones)
        if linea_limpia.count(':') >= 2:
            lineas_con_formato += 1
    
    # Si hay 3+ líneas con formato, es sospechoso
    if lineas_con_formato >= 3:
        return True
    
    # Texto muy largo con mucha puntuación organizada
    if len(texto) > 300 and texto.count('.') >= 10:
        return True
    
    return False


def _precios_demasiado_profesionales(texto: str) -> bool:
    """Detecta precios muy específicos o profesionales."""
    
    import re
    
    # Buscar patrones de precios muy específicos
    patrones_precio = [
        r'\d+[.,]\d{3}[.,]\d{2}',  # 1.234,56
        r'\d{3}[.,]\d{2}',         # 123,45
        r'\d{4}[.,]\d{2}',         # 1234,56
        r'\d{5}[.,]\d{2}',         # 12345,56
    ]
    
    count_precios = 0
    for patron in patrones_precio:
        matches = re.findall(patron, texto)
        count_precios += len(matches)
    
    # Si hay 2+ precios detallados, es profesional
    if count_precios >= 2:
        return True
    
    # Menciones a financiación, hipotecas, etc.
    if any(word in texto for word in ['hipoteca', 'hipotecas', 'financiar', 'financiacion', 'préstamo', 'prestamo', 'cuota', 'cuotas']):
        return True
    
    return False


def _contacto_multiple_profesional(texto: str) -> bool:
    """Detecta múltiples formas de contacto (señal de profesional)."""
    
    # Buscar diferentes formatos de teléfono
    telefonos = 0
    import re
    
    # Patrones de teléfono
    patrones_tel = [
        r'\d{3}[-.\s]\d{3}[-.\s]\d{3}',  # 123-456-789
        r'\d{3}[-.\s]\d{2}[-.\s]\d{2}[-.\s]\d{2}',  # 123-45-67-89
        r'\d{9}',                         # 123456789
        r'\d{3}\s\d{6}',                  # 123 456789
        r'\+34\s\d{9}',                   # +34 123456789
    ]
    
    for patron in patrones_tel:
        matches = re.findall(patron, texto)
        telefonos += len(matches)
    
    # Si hay 2+ teléfonos, es profesional
    if telefonos >= 2:
        return True
    
    # Email + teléfono
    if telefonos >= 1 and any(word in texto for word in ['@', 'email', 'mail', 'correo']):
        return True
    
    return False
