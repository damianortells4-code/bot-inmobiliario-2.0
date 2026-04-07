"""Filtros temporales para anuncios recientes."""

import time
import re
from datetime import datetime, timedelta
from typing import Optional

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT


def parse_fecha_texto(fecha_texto: str) -> Optional[datetime]:
    """
    Convierte texto de fecha a datetime.
    Soporta formatos comunes: "hace 10 minutos", "ayer", "hace 2 horas", etc.
    """
    if not fecha_texto:
        return None
    
    fecha_texto = fecha_texto.lower().strip()
    ahora = datetime.now()
    
    # Patrones comunes de tiempo
    patrones = [
        (r'hace (\d+) minutos?', lambda m: ahora - timedelta(minutes=int(m.group(1)))),
        (r'hace (\d+) horas?', lambda m: ahora - timedelta(hours=int(m.group(1)))),
        (r'hace (\d+) días?', lambda m: ahora - timedelta(days=int(m.group(1)))),
        (r'(\d+) minutos?', lambda m: ahora - timedelta(minutes=int(m.group(1)))),
        (r'(\d+) horas?', lambda m: ahora - timedelta(hours=int(m.group(1)))),
        (r'(\d+) días?', lambda m: ahora - timedelta(days=int(m.group(1)))),
        (r'ayer', lambda m: ahora - timedelta(days=1)),
        (r'anteayer', lambda m: ahora - timedelta(days=2)),
        (r'hoy', lambda m: ahora),
        (r'ahora', lambda m: ahora),
        (r'recientemente', lambda m: ahora - timedelta(minutes=30)),
        (r'última hora', lambda m: ahora - timedelta(hours=1)),
        (r'últimas? horas?', lambda m: ahora - timedelta(hours=2)),
        (r'últimos? días?', lambda m: ahora - timedelta(days=1)),
    ]
    
    for patron, parser in patrones:
        match = re.search(patron, fecha_texto)
        if match:
            try:
                return parser(match)
            except:
                continue
    
    # Intentar parsear fechas específicas (DD/MM/YYYY, etc.)
    formatos_fecha = [
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%d/%m/%y',
        '%d-%m-%y',
        '%d de %m de %Y',
        '%d/%m',
        '%d-%m',
    ]
    
    for formato in formatos_fecha:
        try:
            fecha = datetime.strptime(fecha_texto, formato)
            # Si no tiene año, asumir año actual
            if '%Y' not in formato:
                fecha = fecha.replace(year=ahora.year)
                # Si la fecha es futura, asumir año pasado
                if fecha > ahora:
                    fecha = fecha.replace(year=ahora.year - 1)
            return fecha
        except ValueError:
            continue
    
    return None


def es_anuncio_reciente(fecha_texto: str, max_minutos: int = 10) -> bool:
    """
    Determina si un anuncio es reciente (por defecto últimos 10 minutos).
    """
    if not fecha_texto:
        # Si no hay fecha, asumir que es reciente
        return True
    
    fecha = parse_fecha_texto(fecha_texto)
    if not fecha:
        return True
    
    ahora = datetime.now()
    diferencia = ahora - fecha
    
    return diferencia.total_seconds() <= (max_minutos * 60)


def extraer_fecha_anuncio(html_content: str, url: str) -> Optional[str]:
    """
    Extrae información de tiempo del HTML de un anuncio.
    Busca patrones comunes en diferentes portales.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Patrones a buscar en diferentes idiomas
    tiempo_selectores = [
        # Español
        '[class*="tiempo"]', '[class*="time"]', '[class*="fecha"]',
        '[class*="publicado"]', '[class*="actualizado"]',
        '[data-tiempo]', '[data-time]', '[data-date]',
        'time', '.time', '.fecha', '.publicado', '.actualizado',
        '.timestamp', '.date', '.posted', '.updated',
        
        # Inglés
        '[class*="time"]', '[class*="date"]', '[class*="posted"]',
        '[class*="updated"]', '[class*="ago"]', '[class*="recent"]',
        '[datetime]', '[data-time]', '[data-date]',
        '.time-ago', '.date-ago', '.posted-ago', '.updated-ago',
        
        # Atributos comunes
        '[datetime]', '[data-timestamp]', '[data-publish-time]',
        '[data-update-time]', '[data-created-time]',
    ]
    
    for selector in tiempo_selectores:
        elementos = soup.select(selector)
        for elem in elementos:
            # Extraer texto del elemento
            texto = elem.get_text(strip=True)
            if texto:
                # Buscar palabras relacionadas con tiempo
                palabras_tiempo = [
                    'minuto', 'minutos', 'min', 'mins',
                    'hora', 'horas', 'hour', 'hours', 'h',
                    'día', 'días', 'day', 'days', 'd',
                    'ayer', 'anteayer', 'today', 'hoy',
                    'hace', 'ago', 'reciente', 'recientemente',
                    'última', 'ultimo', 'último', 'ultimo',
                    'publicado', 'publicado', 'actualizado', 'actualizado'
                ]
                
                if any(palabra in texto.lower() for palabra in palabras_tiempo):
                    return texto
            
            # Extraer atributos datetime
            for attr in ['datetime', 'data-timestamp', 'data-time', 'data-date']:
                valor = elem.get(attr)
                if valor:
                    return valor
    
    # Buscar patrones de texto en el HTML completo
    patrones_texto = [
        r'hace\s+\d+\s+(minutos?|min|horas?|hour|hours?|días?|days?|d)',
        r'(\d+\s+(minutos?|min|horas?|hour|hours?|días?|days?|d))\s+atrás',
        r'(\d+\s+(minutos?|min|horas?|hour|hours?|días?|days?|d))\s+ago',
        r'(publicado|actualizado)\s+hace\s+\d+\s+(minutos?|horas?|días?)',
        r'(today|hoy|ayer|anteayer)',
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Fechas
        r'(\d{1,2}[/-]\d{1,2})',  # Fechas sin año
    ]
    
    for patron in patrones_texto:
        match = re.search(patron, html_content, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def filtrar_anuncios_recientes(anuncios: list, max_minutos: int = 10) -> list:
    """
    Filtra anuncios para quedarse solo con los más recientes.
    
    Args:
        anuncios: Lista de anuncios con 'titulo' y 'link'
        max_minutos: Máxima antigüedad en minutos (por defecto 10)
    
    Returns:
        Lista de anuncios recientes
    """
    anuncios_recientes = []
    
    for anuncio in anuncios:
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        
        # Si el título ya indica que es reciente, mantenerlo
        if any(palabra in titulo.lower() for palabra in [
            'reciente', 'recién', 'recien', 'última hora', 'ultima hora',
            'hace poco', 'publicado hoy', 'publicado hoy', 'ahora mismo'
        ]):
            anuncios_recientes.append(anuncio)
            continue
        
        # Intentar obtener fecha del portal (requiere petición HTTP)
        try:
            headers = get_random_headers()
            response = requests.get(link, headers=headers, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                fecha_texto = extraer_fecha_anuncio(response.text, link)
                
                if fecha_texto and es_anuncio_reciente(fecha_texto, max_minutos):
                    anuncios_recientes.append(anuncio)
                elif not fecha_texto:
                    # Si no hay fecha, asumir que es reciente
                    anuncios_recientes.append(anuncio)
            else:
                # Si falla la petición, asumir que es reciente
                anuncios_recientes.append(anuncio)
                
        except Exception:
            # Si hay error, asumir que es reciente
            anuncios_recientes.append(anuncio)
    
    return anuncios_recientes
