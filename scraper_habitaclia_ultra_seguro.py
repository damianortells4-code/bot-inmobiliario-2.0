"""Scraper para Habitaclia con protección ultra anti-bloqueo."""

import time
import random
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from portales_comun import get_random_headers, REQUEST_TIMEOUT, pausa_entre_peticiones, manejar_error_http


def buscar_anuncios(zona="rubi", max_anuncios=None):
    """
    Busca anuncios en Habitaclia con protección ultra anti-bloqueo.
    
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
    
    print(f"Habitaclia Ultra-Seguro buscando en: {zona}")
    
    # Pausa inicial larga antes de empezar
    pausa_inicial = random.uniform(10.0, 20.0)
    print(f"   (pausa inicial Habitaclia: {pausa_inicial:.1f}s)")
    time.sleep(pausa_inicial)
    
    try:
        # Headers específicos para Habitaclia con máxima protección
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': random.choice([
                'es-ES,es;q=0.9,en;q=0.8',
                'es-ES,es;q=0.8,en-GB;q=0.7,en;q=0.6',
                'en-GB,en;q=0.9,es;q=0.8,ca;q=0.7'
            ]),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Sec-GPC': '1',  # Global Privacy Control
            'Sec-CH-UA': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"'
        }
        
        # Timeout más largo para Habitaclia
        timeout_habitaclia = 45
        
        response = requests.get(base_url, headers=headers, timeout=timeout_habitaclia)
        
        # Manejo específico de errores 404/403
        if response.status_code == 404:
            print(f"   [404] Habitaclia: URL no encontrada - probando alternativa")
            # Intentar URL alternativa
            urls_alternativas = [
                f'https://www.habitaclia.com/alquiler-pisos-{zona}.html',
                f'https://www.habitaclia.com/pisos-alquiler-{zona}.html',
                f'https://www.habitaclia.com/buscar/pisos/{zona}'
            ]
            
            for alt_url in urls_alternativas:
                print(f"   Intentando URL alternativa: {alt_url}")
                time.sleep(random.uniform(5.0, 8.0))
                response = requests.get(alt_url, headers=headers, timeout=timeout_habitaclia)
                if response.status_code == 200:
                    print(f"   URL alternativa funcionó: {alt_url}")
                    break
            else:
                # Si ninguna alternativa funciona, registrar error
                manejar_error_http(response, "Habitaclia")
                return anuncios
                
        elif response.status_code == 403:
            print(f"   [403] Habitaclia: Acceso denegado - aplicando contra-medidas")
            # Pausa muy larga y retry con headers diferentes
            time.sleep(random.uniform(180.0, 300.0))  # 3-5 minutos
            
            # Headers completamente diferentes
            headers_alt = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'ca-ES,ca;q=0.9,es;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            response = requests.get(base_url, headers=headers_alt, timeout=timeout_habitaclia)
            if response.status_code != 200:
                manejar_error_http(response, "Habitaclia")
                return anuncios
        
        elif response.status_code == 429:
            print(f"   [429] Habitaclia: Rate limit - pausa extendida")
            time.sleep(random.uniform(120.0, 240.0))  # 2-4 minutos
            response = requests.get(base_url, headers=headers, timeout=timeout_habitaclia)
            if response.status_code != 200:
                manejar_error_http(response, "Habitaclia")
                return anuncios
        
        elif response.status_code not in [200, 202]:
            manejar_error_http(response, "Habitaclia")
            return anuncios
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscar anuncios con múltiples estrategias
        items = []
        
        # Estrategia 1: Selectores principales
        selectores_principales = [
            'div.list-item',
            'article.list-item',
            'div.item',
            'article.item'
        ]
        
        for selector in selectores_principales:
            items = soup.select(selector)
            if items:
                print(f"   Encontrados {len(items)} anuncios con selector: {selector}")
                break
        
        # Estrategia 2: Si no hay resultados, buscar más ampliamente
        if not items:
            print(f"   Buscando con selectores secundarios...")
            selectores_secundarios = [
                'li.list-item',
                'div.ad',
                'article.ad',
                'div[class*="item"]',
                'article[class*="item"]',
                'div[class*="listing"]',
                'article[class*="listing"]'
            ]
            
            for selector in selectores_secundarios:
                items = soup.select(selector)
                if items:
                    print(f"   Encontrados {len(items)} anuncios con selector secundario: {selector}")
                    break
        
        # Estrategia 3: Último recurso - buscar cualquier enlace que parezca anuncio
        if not items:
            print(f"   Búsqueda de último recurso...")
            all_links = soup.find_all('a', href=True)
            items = []
            for link in all_links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                if (len(text) > 15 and 
                    any(palabra in text.lower() for palabra in ['piso', 'habitación', 'alquiler', 'renta', 'euros', 'mes']) and
                    not any(x in href.lower() for x in ['contactar', 'enviar', 'email', 'tel', 'login', 'register'])):
                    # Crear un contenedor artificial para el anuncio
                    parent = link.parent
                    if parent:
                        items.append(parent)
        
        if not items:
            print("Habitaclia Ultra-Seguro: No se encontraron anuncios con ninguna estrategia")
            return anuncios
        
        # Procesar anuncios con pausas más largas
        for i, item in enumerate(items[:max_anuncios] if max_anuncios else items):
            try:
                # Pausa más larga entre anuncios
                if i > 0:  # No pausar en el primer anuncio
                    pausa_anuncio = random.uniform(8.0, 15.0)  # 8-15 segundos
                    if random.random() < 0.2:  # 20% de probabilidad de pausa extra
                        pausa_anuncio += random.uniform(10.0, 20.0)
                    print(f"   (pausa anuncio {i+1}: {pausa_anuncio:.1f}s)")
                    time.sleep(pausa_anuncio)
                
                # Extraer título con múltiples métodos
                title_elem = None
                title_selectors = [
                    'h2 a', 'h3 a', 'h4 a',
                    '.title a', '.ad-title a', 'a.title',
                    'h2', 'h3', 'h4',
                    '.title', '.ad-title'
                ]
                
                for selector in title_selectors:
                    title_elem = item.select_one(selector)
                    if title_elem:
                        break
                
                if not title_elem:
                    # Buscar cualquier enlace con texto largo
                    for link_elem in item.find_all('a'):
                        text = link_elem.get_text(strip=True)
                        if text and len(text) > 10:
                            title_elem = link_elem
                            break
                
                title = title_elem.get_text(strip=True) if title_elem else "Sin título"
                
                # Extraer enlace
                if title_elem and title_elem.get('href'):
                    link = urljoin("https://www.habitaclia.com", title_elem.get('href'))
                else:
                    # Buscar enlace principal
                    link_elem = item.find('a')
                    if link_elem and link_elem.get('href'):
                        link = urljoin("https://www.habitaclia.com", link_elem.get('href'))
                    else:
                        continue
                
                # Verificar que sea un enlace de anuncio
                if any(x in link.lower() for x in ['contactar', 'enviar', 'email', 'tel']):
                    continue
                
                # Verificar que no sea un enlace de navegación
                if any(x in link.lower() for x in ['pagina', 'page', 'siguiente', 'anterior', 'menu']):
                    continue
                
                # Limpiar título
                title = title.replace('\n', ' ').replace('\t', ' ').strip()
                
                anuncios.append({
                    'titulo': title,
                    'link': link,
                    'fuente': 'Habitaclia Ultra-Seguro'
                })
                
                print(f"   Anuncio {i+1}: {title[:50]}...")
                
            except Exception as e:
                print(f"Error procesando anuncio Habitaclia {i+1}: {e}")
                continue
        
        print(f"Habitaclia Ultra-Seguro encontrados: {len(anuncios)} anuncios")
        
        # Pausa final antes de terminar
        pausa_final = random.uniform(5.0, 10.0)
        print(f"   (pausa final Habitaclia: {pausa_final:.1f}s)")
        time.sleep(pausa_final)
        
    except Exception as e:
        print(f"Error en Habitaclia Ultra-Seguro: {e}")
        # Pausa por error general
        time.sleep(random.uniform(30.0, 60.0))
    
    return anuncios
