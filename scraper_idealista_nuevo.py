"""Scraper para Idealista (versión mejorada)."""

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT


def buscar_anuncios(zona="sant-cugat-del-valles-barcelona", max_anuncios=None):
    """
    Busca anuncios en Idealista para una zona específica.
    
    Args:
        zona: Zona de búsqueda (slug de Idealista)
        max_anuncios: Límite de anuncios a obtener
    
    Returns:
        Lista de diccionarios con título y link
    """
    anuncios = []
    
    # URL base de Idealista
    base_url = f"https://www.idealista.com/busco/piso-en-barcelona/{zona}/"
    
    print(f"Idealista buscando en: {zona}")
    
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
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar anuncios principales
        items = soup.find_all('article', class_='item')
        
        if not items:
            # Intentar con otros selectores
            items = soup.find_all('div', class_='item')
        
        if not items:
            print("Idealista: No se encontraron anuncios")
            return anuncios
        
        for item in items[:max_anuncios] if max_anuncios else items:
            try:
                # Extraer título
                title_elem = item.find('a', class_='item-link')
                if not title_elem:
                    title_elem = item.find('h3') or item.find('h2')
                
                title = title_elem.get_text(strip=True) if title_elem else "Sin título"
                
                # Extraer enlace
                if title_elem and title_elem.get('href'):
                    link = urljoin("https://www.idealista.com", title_elem.get('href'))
                else:
                    # Buscar enlace en otros elementos
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        link = urljoin("https://www.idealista.com", link_elem.get('href'))
                    else:
                        continue
                
                # Verificar que sea un enlace de anuncio
                if '/inmueble/' not in link:
                    continue
                
                anuncios.append({
                    'titulo': title,
                    'link': link,
                    'fuente': 'Idealista'
                })
                
                # Pausa entre anuncios
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"Error procesando anuncio Idealista: {e}")
                continue
        
        print(f"Idealista encontrados: {len(anuncios)} anuncios")
        
    except Exception as e:
        print(f"Error en Idealista: {e}")
    
    return anuncios
