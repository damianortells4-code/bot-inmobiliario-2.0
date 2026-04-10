"""Scraper para Fotocasacom (nuevo portal)."""

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT, pausa_entre_peticiones, verificar_y_pausar_si_necesario


def buscar_anuncios(zona="rubi", max_anuncios=None):
    """
    Busca anuncios en Fotocasacom para una zona específica.
    
    Args:
        zona: Zona de búsqueda
        max_anuncios: Límite de anuncios a obtener
    
    Returns:
        Lista de diccionarios con título y link
    """
    anuncios = []
    
    # URLs base de Fotocasacom por zona
    urls_zonas = {
        'rubi': 'https://www.fotocasacom.com/pisos/rubi',
        'sant_cugat': 'https://www.fotocasacom.com/pisos/sant-cugat-del-valles',
        'sabadell': 'https://www.fotocasacom.com/pisos/sabadell',
        'terrassa': 'https://www.fotocasacom.com/pisos/terrassa',
        'barcelona': 'https://www.fotocasacom.com/pisos/barcelona'
    }
    
    base_url = urls_zonas.get(zona, urls_zonas['rubi'])
    
    print(f"Fotocasacom buscando en: {zona}")
    
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
        if verificar_y_pausar_si_necesario(response, "Fotocasacom"):
            return anuncios  # Retornar vacío si hay bloqueo
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar anuncios principales
        items = []
        
        # Intentar diferentes selectores para Fotocasacom
        selectores = [
            'div.re-card',
            'article.re-card',
            'div.property-card',
            'article.property-card',
            'div.listing-item',
            'article.listing-item',
            'div.ad-item',
            'article.ad-item'
        ]
        
        for selector in selectores:
            items = soup.select(selector)
            if items:
                break
        
        if not items:
            print("Fotocasacom: No se encontraron anuncios")
            return anuncios
        
        for item in items[:max_anuncios] if max_anuncios else items:
            try:
                # Extraer título
                title_elem = None
                title_selectors = ['h3 a', 'h2 a', 'h4 a', '.title a', '.property-title a', 'a.title']
                
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
                    link = urljoin("https://www.fotocasacom.com", title_elem.get('href'))
                else:
                    # Buscar enlace en otros elementos
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        link = urljoin("https://www.fotocasacom.com", link_elem.get('href'))
                    else:
                        continue
                
                # Verificar que sea un enlace de anuncio
                if not link or 'javascript:' in link:
                    continue
                
                anuncios.append({
                    'titulo': title,
                    'link': link,
                    'fuente': 'Fotocasacom'
                })
                
                # Pausa entre anuncios
                pausa_entre_peticiones()
                
            except Exception as e:
                print(f"Error procesando anuncio Fotocasacom: {e}")
                continue
        
        print(f"Fotocasacom encontrados: {len(anuncios)} anuncios")
        
    except Exception as e:
        print(f"Error en Fotocasacom: {e}")
    
    return anuncios
