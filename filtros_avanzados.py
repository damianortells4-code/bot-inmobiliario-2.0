"""Filtros avanzados para anuncios inmobiliarios."""

import re
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class FiltrosAvanzados:
    """Configuración de filtros avanzados."""
    precio_maximo: float = 1500.0
    precio_minimo: float = 300.0
    puntuacion_minima: float = 70.0
    caracteristicas_requeridas: List[str] = None
    zonas_excluidas: List[str] = None
    fuentes_prioritarias: List[str] = None


class FiltroAvanzado:
    """Filtro avanzado para anuncios basado en precio y características."""
    
    def __init__(self, config: FiltrosAvanzados = None):
        self.config = config or FiltrosAvanzados()
    
    def extraer_precio(self, titulo: str, descripcion: str) -> float:
        """Extrae el precio del anuncio."""
        texto_completo = (titulo + ' ' + descripcion).lower()
        
        # Patrones de precios en euros
        patrones = [
            r'(\d+[.,]?\d{0,3})\s*€',
            r'(\d+)\s*€',
            r'(\d+[.,]?\d{0,3})\s*euros',
            r'(\d+)\s*euros',
        ]
        
        for patron in patrones:
            match = re.search(patron, texto_completo)
            if match:
                try:
                    return float(match.group(1).replace(',', '.'))
                except ValueError:
                    continue
        
        return 0.0
    
    def tiene_caracteristicas_requeridas(self, titulo: str, descripcion: str) -> bool:
        """Verifica si el anuncio tiene características requeridas."""
        if not self.config.caracteristicas_requeridas:
            return True
        
        texto_completo = (titulo + ' ' + descripcion).lower()
        for caracteristica in self.config.caracteristicas_requeridas:
            if caracteristica in texto_completo:
                return True
        
        return False
    
    def esta_en_zona_excluida(self, titulo: str, descripcion: str) -> bool:
        """Verifica si el anuncio está en zona excluida."""
        if not self.config.zonas_excluidas:
            return False
        
        texto_completo = (titulo + ' ' + descripcion).lower()
        for zona in self.config.zonas_excluidas:
            if zona in texto_completo:
                return True
        
        return False
    
    def es_fuente_prioritaria(self, fuente: str) -> bool:
        """Verifica si la fuente es prioritaria."""
        if not self.config.fuentes_prioritarias:
            return True
        
        return fuente.lower() in [f.lower() for f in self.config.fuentes_prioritarias]
    
    def filtrar_anuncios(self, anuncios: List[Dict]) -> List[Dict]:
        """Aplica filtros avanzados a una lista de anuncios."""
        anuncios_filtrados = []
        
        for anuncio in anuncios:
            titulo = anuncio.get('titulo', '')
            descripcion = anuncio.get('descripcion', '')
            fuente = anuncio.get('fuente', '')
            precio = self.extraer_precio(titulo, descripcion)
            
            # Filtro por precio
            if precio > 0 and (
                precio > self.config.precio_maximo or 
                precio < self.config.precio_minimo
            ):
                continue
            
            # Filtro por características requeridas
            if not self.tiene_caracteristicas_requeridas(titulo, descripcion):
                continue
            
            # Filtro por zona excluida
            if self.esta_en_zona_excluida(titulo, descripcion):
                continue
            
            # Filtro por fuente prioritaria
            if not self.es_fuente_prioritaria(fuente):
                continue
            
            anuncios_filtrados.append(anuncio)
        
        return anuncios_filtrados
    
    def configurar_filtro_precio(self, precio_min: float, precio_max: float):
        """Configura el rango de precios."""
        self.config.precio_minimo = precio_min
        self.config.precio_maximo = precio_max
    
    def configurar_caracteristicas_requeridas(self, caracteristicas: List[str]):
        """Configura las características requeridas."""
        self.config.caracteristicas_requeridas = caracteristicas
    
    def configurar_zonas_excluidas(self, zonas: List[str]):
        """Configura las zonas excluidas."""
        self.config.zonas_excluidas = zonas
    
    def configurar_fuentes_prioritarias(self, fuentes: List[str]):
        """Configura las fuentes prioritarias."""
        self.config.fuentes_prioritarias = fuentes


# Instancia global del filtro avanzado
filtro_avanzado = FiltroAvanzado()


def aplicar_filtro_avanzado(anuncios: List[Dict], config: FiltrosAvanzados = None) -> List[Dict]:
    """
    Aplica filtros avanzados a una lista de anuncios.
    
    Args:
        anuncios: Lista de diccionarios con 'titulo', 'link', 'descripcion', 'fuente'
        config: Configuración de filtros avanzados
    
    Returns:
        Lista de anuncios filtrados
    """
    filtro = FiltroAvanzado(config)
    return filtro.filtrar_anuncios(anuncios)


def configurar_filtro_precio(precio_min: float, precio_max: float):
    """Configura el rango de precios del filtro avanzado."""
    filtro_avanzado.configurar_filtro_precio(precio_min, precio_max)


def configurar_caracteristicas_requeridas(caracteristicas: List[str]):
    """Configura las características requeridas del filtro avanzado."""
    filtro_avanzado.configurar_caracteristicas_requeridas(caracteristicas)


def configurar_zonas_excluidas(zonas: List[str]):
    """Configura las zonas excluidas del filtro avanzado."""
    filtro_avanzado.configurar_zonas_excluidas(zonas)


def configurar_fuentes_prioritarias(fuentes: List[str]):
    """Configura las fuentes prioritarias del filtro avanzado."""
    filtro_avanzado.configurar_fuentes_prioritarias(fuentes)
