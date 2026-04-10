"""Scraper para Idealista Pro (versión profesional)."""

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT


def buscar_anuncios(zona="sant-cugat-del-valles-barcelona", max_anuncios=None):
    """
    Busca anuncios en Idealista Pro para una zona específica.
    
    Args:
        zona: Zona de búsqueda (slug de Idealista)
        max_anuncios: Límite de anuncios a obtener
    
    Returns:
        Lista de diccionarios con título y link
    """
    anuncios = []
    
    # URL base de Idealista Pro
    base_url = f"https://www.idealista.com/busco/piso-en-barcelona/{zona}/"
    
    print(f"Idealista Pro buscando en: {zona}")
    
    try:
        headers = get_random_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        response = requests.get(base_url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar anuncios principales - más selectores específicos
        items = []
        
        # Selectores más específicos para Idealista
        selectores = [
            'article.item',
            'div.item',
            'article.property-item',
            'div.property-item',
            'section.item',
            'div.listing-item',
            'article.listing-item'
        ]
        
        for selector in selectores:
            items = soup.select(selector)
            if items:
                break
        
        if not items:
            print("Idealista Pro: No se encontraron anuncios")
            return anuncios
        
        for item in items[:max_anuncios] if max_anuncios else items:
            try:
                # Extraer título con más selectores
                title_elem = None
                title_selectors = [
                    'a.item-link',
                    'h3 a',
                    'h2 a', 
                    'h4 a',
                    '.title a',
                    '.item-title a',
                    '.property-title a',
                    'a.title'
                ]
                
                for selector in title_selectors:
                    title_elem = item.select_one(selector)
                    if title_elem:
                        break
                
                if not title_elem:
                    # Buscar cualquier enlace con texto largo
                    for link_elem in item.find_all('a'):
                        text = link_elem.get_text(strip=True)
                        if text and len(text) > 10:  # Título mínimo de 10 caracteres
                            title_elem = link_elem
                            break
                
                title = title_elem.get_text(strip=True) if title_elem else "Sin título"
                
                # Extraer enlace
                if title_elem and title_elem.get('href'):
                    link = urljoin("https://www.idealista.com", title_elem.get('href'))
                else:
                    # Buscar enlace principal
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        link = urljoin("https://www.idealista.com", link_elem.get('href'))
                    else:
                        continue
                
                # Verificar que sea un enlace de anuncio
                if '/inmueble/' not in link:
                    continue
                
                # Limpiar título
                title = title.replace('\n', ' ').replace('\t', ' ').strip()
                
                anuncios.append({
                    'titulo': title,
                    'link': link,
                    'fuente': 'Idealista Pro'
                })
                
                # Pausa más larga para evitar bloqueos
                time.sleep(random.uniform(1.0, 2.0))
                
            except Exception as e:
                print(f"Error procesando anuncio Idealista Pro: {e}")
                continue
        
        print(f"Idealista Pro encontrados: {len(anuncios)} anuncios")
        
    except Exception as e:
        print(f"Error en Idealista Pro: {e}")
    
    return anuncios
