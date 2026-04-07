"""Sistema de puntuación y ranking de anuncios."""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PuntuacionAnuncio:
    """Clase para almacenar la puntuación de un anuncio."""
    titulo: str
    link: str
    puntuacion_total: float
    puntuacion_precio: float
    puntuacion_caracteristicas: float
    puntuacion_ubicacion: float
    puntuacion_descripcion: float
    detalles: Dict[str, float]
    fecha: str = ""
    fuente: str = ""


class AnalizadorAnuncios:
    """Analizador y puntuador de anuncios inmobiliarios."""
    
    def __init__(self):
        # Pesos para diferentes aspectos
        self.pesos = {
            'precio': 0.30,          # Precio competitivo
            'caracteristicas': 0.25,  # Características deseadas
            'ubicacion': 0.20,          # Buena ubicación
            'descripcion': 0.15,        # Calidad de descripción
            'reciente': 0.10,           # Reciente vs antiguo
        }
    
    def extraer_precio(self, titulo: str, descripcion: str) -> float:
        """Extrae y puntúa el precio del anuncio."""
        # Patrones de precios en euros
        patrones = [
            r'(\d+[.,]?\d{0,3})\s*€',  # 1.234,56€
            r'(\d+)\s*€',                  # 1234€
            r'(\d+[.,]?\d{0,3})\s*euros',  # 1.234,56 euros
            r'(\d+)\s*euros',                # 1234 euros
        ]
        
        puntuacion = 0.0
        
        for patron in patrones:
            match = re.search(patron, descripcion.lower() + ' ' + titulo.lower())
            if match:
                precio = float(match.group(1).replace(',', '.'))
                
                # Puntuación basada en precios competitivos
                if precio <= 500:
                    puntuacion = 100  # Excelente precio
                elif precio <= 800:
                    puntuacion = 85   # Muy bueno
                elif precio <= 1200:
                    puntuacion = 70   # Bueno
                elif precio <= 1800:
                    puntuacion = 50   # Regular
                else:
                    puntuacion = 20   # Caro
                
                return puntuacion
        
        # Si no se encuentra precio, puntuación neutra
        return 50.0
    
    def extraer_caracteristicas(self, titulo: str, descripcion: str) -> float:
        """Extrae y puntúa las características del anuncio."""
        caracteristicas_deseadas = [
            'terraza', 'jardin', 'piscina', 'garaje', 'trastero',
            'ascensor', 'aire acondicionado', 'calefaccion', 'amueblado',
            'exterior', 'balcon', 'vista', 'luminoso', 'reformado',
            'nuevo', 'estrenar', 'moderno', 'cuarto baño', 'suite',
            'planta baja', 'sin muebles', 'cocina equipada', 'sala',
            'dormitorios dobles', 'armarios empotrados', 'hormigon',
        ]
        
        caracteristicas_negativas = [
            'sin ascensor', 'sin exterior', 'necesita reforma', 'antiguo',
            'pequeño', 'oscuro', 'humedad', 'mal estado', 'sin ventana',
            'cuarta planta', 'sin terraza', 'interior', 'sin cocina',
        ]
        
        texto_completo = (titulo + ' ' + descripcion).lower()
        puntuacion = 50.0  # Base
        
        # Características positivas
        for caracteristica in caracteristicas_deseadas:
            if caracteristica in texto_completo:
                puntuacion += 5
        
        # Características negativas
        for caracteristica in caracteristicas_negativas:
            if caracteristica in texto_completo:
                puntuacion -= 3
        
        return min(100, max(0, puntuacion))
    
    def extraer_ubicacion(self, titulo: str, descripcion: str) -> float:
        """Extrae y puntúa la ubicación basada en el texto."""
        zonas_deseadas = [
            'centro', 'casco', 'casco antiguo', 'zona noble', 'ensanche',
            'junto metro', 'cerca metro', 'bien comunicado', 'tranquilo',
            'comercial', 'facultades', 'universidad', 'colegio', 'parque',
            'avenida principal', 'calle principal', 'plaza mayor',
        ]
        
        zonas_negativas = [
            'periferia', 'lejos metro', 'mal comunicado', 'ruidoso',
            'industrial', 'zona industrial', 'sin servicios', 'aislado',
            'callejuela', 'zona oscura', 'dificil acceso',
        ]
        
        texto_completo = (titulo + ' ' + descripcion).lower()
        puntuacion = 50.0  # Base
        
        # Zonas positivas
        for zona in zonas_deseadas:
            if zona in texto_completo:
                puntuacion += 4
        
        # Zonas negativas
        for zona in zonas_negativas:
            if zona in texto_completo:
                puntuacion -= 2
        
        return min(100, max(0, puntuacion))
    
    def extraer_descripcion(self, titulo: str, descripcion: str) -> float:
        """Extrae y puntúa la calidad de la descripción."""
        texto_completo = titulo + ' ' + descripcion
        
        # Indicadores de buena descripción
        indicadores_positivos = [
            len(descripcion) > 100,  # Descripción detallada
            len(descripcion.split()) > 15,  # Frases variadas
            'superficie' in descripcion.lower() or 'm²' in descripcion.lower(),
            'orientación' in descripcion.lower(),
            'certificado' in descripcion.lower(),
            'calificación' in descripcion.lower(),
        ]
        
        # Indicadores de mala descripción
        indicadores_negativos = [
            len(descripcion) < 20,  # Descripción muy corta
            'consultar' in descripcion.lower() or 'información' in descripcion.lower(),
            'sin fotos' in descripcion.lower() or 'sin imágenes' in descripcion.lower(),
            'ver fotos' in descripcion.lower(),
            descripcion.count('!') > 3,  # Demasiado informal
            descripcion.count('?') > 3,  # Demasiadas preguntas
        ]
        
        puntuacion = 50.0  # Base
        
        # Puntuación por indicadores positivos
        for indicador in indicadores_positivos:
            if indicador:
                puntuacion += 3
        
        # Puntuación por indicadores negativos
        for indicador in indicadores_negativos:
            if indicador:
                puntuacion -= 2
        
        return min(100, max(0, puntuacion))
    
    def extraer_reciente(self, titulo: str, descripcion: str) -> float:
        """Extrae y puntúa la reciente del anuncio."""
        texto_completo = (titulo + ' ' + descripcion).lower()
        
        # Indicadores de anuncio reciente
        indicadores_recientes = [
            'hoy', 'publicado hoy', 'reciente', 'último día',
            'esta semana', 'nuevo', 'estrenar', 'disponible inmediato',
            'recién publicado', 'ahora mismo', 'sin demora',
        ]
        
        # Indicadores de anuncio antiguo
        indicadores_antiguos = [
            'hace meses', 'antiguo', 'hace años', 'desde hace',
            'lleva tiempo', 'antigua publicación', 'hace tiempo',
            'renovado hace', 'publicado hace', 'viejo',
        ]
        
        puntuacion = 50.0  # Base
        
        # Puntuación por indicadores recientes
        for indicador in indicadores_recientes:
            if indicador in texto_completo:
                puntuacion += 6
        
        # Puntuación por indicadores antiguos
        for indicador in indicadores_antiguos:
            if indicador in texto_completo:
                puntuacion -= 4
        
        return min(100, max(0, puntuacion))
    
    def analizar_anuncio(self, titulo: str, link: str, descripcion: str = "", fuente: str = "") -> PuntuacionAnuncio:
        """Analiza y puntúa un anuncio completo."""
        
        # Extraer puntuaciones individuales
        puntuacion_precio = self.extraer_precio(titulo, descripcion)
        puntuacion_caracteristicas = self.extraer_caracteristicas(titulo, descripcion)
        puntuacion_ubicacion = self.extraer_ubicacion(titulo, descripcion)
        puntuacion_descripcion = self.extraer_descripcion(titulo, descripcion)
        puntuacion_reciente = self.extraer_reciente(titulo, descripcion)
        
        # Calcular puntuación total ponderada
        puntuacion_total = (
            puntuacion_precio * self.pesos['precio'] +
            puntuacion_caracteristicas * self.pesos['caracteristicas'] +
            puntuacion_ubicacion * self.pesos['ubicacion'] +
            puntuacion_descripcion * self.pesos['descripcion'] +
            puntuacion_reciente * self.pesos['reciente']
        )
        
        # Detalles para debugging
        detalles = {
            'precio': puntuacion_precio,
            'caracteristicas': puntuacion_caracteristicas,
            'ubicacion': puntuacion_ubicacion,
            'descripcion': puntuacion_descripcion,
            'reciente': puntuacion_reciente,
        }
        
        return PuntuacionAnuncio(
            titulo=titulo,
            link=link,
            puntuacion_total=round(puntuacion_total, 2),
            puntuacion_precio=round(puntuacion_precio, 2),
            puntuacion_caracteristicas=round(puntuacion_caracteristicas, 2),
            puntuacion_ubicacion=round(puntuacion_ubicacion, 2),
            puntuacion_descripcion=round(puntuacion_descripcion, 2),
            detalles=detalles,
            fuente=fuente
        )
    
    def ranking_anuncios(self, anuncios: List[PuntuacionAnuncio]) -> List[PuntuacionAnuncio]:
        """Ordena los anuncios por puntuación total de mayor a menor."""
        return sorted(anuncios, key=lambda x: x.puntuacion_total, reverse=True)
    
    def filtrar_por_puntuacion_minima(self, anuncios: List[PuntuacionAnuncio], puntuacion_minima: float = 60.0) -> List[PuntuacionAnuncio]:
        """Filtra anuncios con puntuación mínima."""
        return [anuncio for anuncio in anuncios if anuncio.puntuacion_total >= puntuacion_minima]
    
    def obtener_mejores_anuncios(self, anuncios: List[PuntuacionAnuncio], top_n: int = 5) -> List[PuntuacionAnuncio]:
        """Obtiene los N mejores anuncios."""
        return self.ranking_anuncios(anuncios)[:top_n]
    
    def generar_resumen_puntuacion(self, anuncios: List[PuntuacionAnuncio]) -> str:
        """Genera un resumen formateado de la puntuación de anuncios."""
        if not anuncios:
            return "No hay anuncios para analizar"
        
        anuncios_ordenados = self.ranking_anuncios(anuncios)
        mejor_anuncio = anuncios_ordenados[0] if anuncios_ordenados else None
        
        resumen = f"""
📊 ANÁLISIS DE ANUNCIOS ({len(anuncios)} evaluados)
═══════════════════════════════════════════════════

🏆 MEJOR ANUNCIOS:
{mejor_anuncio.titulo if mejor_anuncio else 'N/A'}
⭐ Puntuación: {mejor_anuncio.puntuacion_total if mejor_anuncio else 'N/A'}/100
💰 Precio: {mejor_anuncio.puntuacion_precio}/100
🏠 Características: {mejor_anuncio.puntuacion_caracteristicas}/100
📍 Ubicación: {mejor_anuncio.puntuacion_ubicacion}/100
📝 Descripción: {mejor_anuncio.puntuacion_descripcion}/100
🕐 Reciente: {mejor_anuncio.puntuacion_reciente}/100
🔗 Fuente: {mejor_anuncio.fuente}

📈 TOP 5 ANUNCIOS:
"""
        
        for i, anuncio in enumerate(anuncios_ordenados[:5], 1):
            resumen += f"""
{i}. {anuncio.titulo[:50]}...
   ⭐ {anuncio.puntuacion_total}/100 | 💰{anuncio.puntuacion_precio} | 🏠{anuncio.puntuacion_caracteristicas} | 📍{anuncio.puntuacion_ubicacion}
"""
        
        resumen += """
═══════════════════════════════════════════════════

🎯 RECOMENDACIONES:
• Enfocarse en anuncios con puntuación > 70
• Priorizar precio y características deseadas
• Considerar ubicación y descripción detallada
"""
        
        return resumen


# Instancia global del analizador
analizador = AnalizadorAnuncios()


def puntuar_anuncios(anuncios: List[Dict], puntuacion_minima: float = 60.0) -> Tuple[List[PuntuacionAnuncio], str]:
    """
    Función principal para puntuar una lista de anuncios.
    
    Args:
        anuncios: Lista de diccionarios con 'titulo', 'link', 'descripcion'
        puntuacion_minima: Puntuación mínima para considerar un anuncio
    
    Returns:
        Tuple con (anuncios_puntuados, resumen)
    """
    anuncios_puntuados = []
    
    for anuncio in anuncios:
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        descripcion = anuncio.get('descripcion', '')
        fuente = anuncio.get('fuente', '')
        
        # Analizar y puntuar
        anuncio_puntuado = analizador.analizar_anuncio(titulo, link, descripcion, fuente)
        anuncios_puntuados.append(anuncio_puntuado)
    
    # Filtrar por puntuación mínima
    anuncios_filtrados = analizador.filtrar_por_puntuacion_minima(anuncios_puntuados, puntuacion_minima)
    
    # Generar resumen
    resumen = analizador.generar_resumen_puntuacion(anuncios_filtrados)
    
    return anuncios_filtrados, resumen


def obtener_mejores_anuncios(anuncios: List[Dict], top_n: int = 5) -> List[PuntuacionAnuncio]:
    """
    Obtiene los mejores N anuncios basados en puntuación.
    """
    anuncios_puntuados = []
    
    for anuncio in anuncios:
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        descripcion = anuncio.get('descripcion', '')
        fuente = anuncio.get('fuente', '')
        
        anuncio_puntuado = analizador.analizar_anuncio(titulo, link, descripcion, fuente)
        anuncios_puntuados.append(anuncio_puntuado)
    
    return analizador.obtener_mejores_anuncios(anuncios_puntuados, top_n)
