"""Scraper para Habitaclia (versión mejorada)."""

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT, pausa_entre_peticiones


def buscar_anuncios(zona="rubi", max_anuncios=None):
    """
    Busca anuncios en Habitaclia para una zona específica.
    
    Args:
        zona: Zona de búsqueda
        max_anuncios: Límite de anuncios a obtener
    
    Returns:
        Lista de diccionarios con título y link
    """
    anuncios = []
    
    # URLs base de Habitaclia por zona
    urls_zonas = {
        'rubi': 'https://www.habitaclia.com/pisos-en-rubi.html',
        'sant_cugat': 'https://www.habitaclia.com/pisos-en-sant-cugat-del-valles.html',
        'sabadell': 'https://www.habitaclia.com/pisos-en-sabadell.html',
        'terrassa': 'https://www.habitaclia.com/pisos-en-terrassa.html',
        'barcelona': 'https://www.habitaclia.com/pisos-en-barcelona.html'
    }
    
    base_url = urls_zonas.get(zona, urls_zonas['rubi'])
    
    print(f"Habitaclia buscando en: {zona}")
    
    try:
        headers = get_random_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        response = requests.get(base_url, headers=headers, timeout=REQUEST_TIMEOUT)
        
        # Verificar si hay bloqueo
        from portales_comun import verificar_y_pausar_si_necesario
        if verificar_y_pausar_si_necesario(response, "Habitaclia"):
            return anuncios  # Retornar vacío si hay bloqueo
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar anuncios principales - varios selectores posibles
        items = []
        
        # Intentar diferentes selectores para Habitaclia
        selectores = [
            'div.list-item',
            'article.list-item',
            'div.item',
            'article.item',
            'li.list-item',
            'div.ad',
            'article.ad'
        ]
        
        for selector in selectores:
            items = soup.select(selector)
            if items:
                break
        
        if not items:
            print("Habitaclia: No se encontraron anuncios con selectores conocidos")
            # Intentar búsqueda más amplia
            items = soup.find_all(['div', 'article'], class_=lambda x: x and ('item' in str(x).lower() or 'ad' in str(x).lower() or 'list' in str(x).lower()))
        
        if not items:
            print("Habitaclia: No se encontraron anuncios")
            return anuncios
        
        for item in items[:max_anuncios] if max_anuncios else items:
            try:
                # Extraer título
                title_elem = None
                title_selectors = ['h2 a', 'h3 a', 'h4 a', '.title a', '.ad-title a', 'a.title']
                
                for selector in title_selectors:
                    title_elem = item.select_one(selector)
                    if title_elem:
                        break
                
                if not title_elem:
                    # Buscar cualquier enlace con texto
                    title_elem = item.find('a')
                
                title = title_elem.get_text(strip=True) if title_elem else "Sin título"
                
                # Extraer enlace
                if title_elem and title_elem.get('href'):
                    link = urljoin("https://www.habitaclia.com", title_elem.get('href'))
                else:
                    # Buscar enlace en otros elementos
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        link = urljoin("https://www.habitaclia.com", link_elem.get('href'))
                    else:
                        continue
                
                # Verificar que sea un enlace de anuncio
                if any(x in link.lower() for x in ['contactar', 'enviar', 'email', 'tel']):
                    continue
                
                anuncios.append({
                    'titulo': title,
                    'link': link,
                    'fuente': 'Habitaclia'
                })
                
                # Pausa entre anuncios
                pausa_entre_peticiones()
                
            except Exception as e:
                print(f"Error procesando anuncio Habitaclia: {e}")
                continue
        
        print(f"Habitaclia encontrados: {len(anuncios)} anuncios")
        
    except Exception as e:
        print(f"Error en Habitaclia: {e}")
    
    return anuncios
