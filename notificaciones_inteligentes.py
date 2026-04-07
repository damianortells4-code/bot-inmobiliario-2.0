"""Sistema de notificaciones inteligentes con formato enriquecido."""

import requests
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

import telegram_alert


@dataclass
class NotificacionConfig:
    """Configuración para notificaciones inteligentes."""
    incluir_puntuacion: bool = True
    incluir_detalles: bool = True
    incluir_emoji: bool = True
    formato_html: bool = False
    max_longitud_titulo: int = 60
    mostrar_precio: bool = True
    mostrar_caracteristicas: bool = True
    mostrar_ubicacion: bool = True


class NotificadorInteligente:
    """Generador de notificaciones inteligentes."""
    
    def __init__(self, config: NotificacionConfig = None):
        self.config = config or NotificacionConfig()
    
    def formatear_titulo(self, titulo: str, puntuacion: float = 0) -> str:
        """Formatea el título con truncamiento inteligente."""
        if len(titulo) <= self.config.max_longitud_titulo:
            return titulo
        
        # Truncar con puntos suspensivos
        return titulo[:self.config.max_longitud_titulo-3] + "..."
    
    def generar_resumen_precio(self, precio: float) -> str:
        """Genera un resumen visual del precio."""
        if precio <= 500:
            return "💰 EXCELENTE PRECIO"
        elif precio <= 800:
            return "💵 BUEN PRECIO"
        elif precio <= 1200:
            return "💴 PRECIO NORMAL"
        else:
            return "💸 PRECIO ELEVADO"
    
    def generar_resumen_caracteristicas(self, puntuacion: float) -> str:
        """Genera un resumen visual de las características."""
        if puntuacion >= 85:
            return "🏠 EXCELENTES CARACTERÍSTICAS"
        elif puntuacion >= 70:
            return "🏠 BUENAS CARACTERÍSTICAS"
        elif puntuacion >= 50:
            return "🏠 CARACTERÍSTICAS NORMALES"
        else:
            return "🏠 CARACTERÍSTICAS LIMITADAS"
    
    def generar_resumen_ubicacion(self, puntuacion: float) -> str:
        """Genera un resumen visual de la ubicación."""
        if puntuacion >= 80:
            return "📍 UBICACIÓN EXCELENTE"
        elif puntuacion >= 60:
            return "📍 BUENA UBICACIÓN"
        elif puntuacion >= 40:
            return "📍 UBICACIÓN NORMAL"
        else:
            return "📍 UBICACIÓN A MEJORAR"
    
    def generar_resumen_descripcion(self, puntuacion: float) -> str:
        """Genera un resumen visual de la descripción."""
        if puntuacion >= 80:
            return "📝 DESCRIPCIÓN EXCELENTE"
        elif puntuacion >= 60:
            return "📝 BUENA DESCRIPCIÓN"
        elif puntuacion >= 40:
            return "📝 DESCRIPCIÓN NORMAL"
        else:
            return "📝 DESCRIPCIÓN MEJORAR"
    
    def generar_resumen_reciente(self, puntuacion: float) -> str:
        """Genera un resumen visual de la reciente."""
        if puntuacion >= 80:
            return "🕐 ANUNCIO MUY RECIENTE"
        elif puntuacion >= 60:
            return "🕑 ANUNCIO RECIENTE"
        elif puntuacion >= 40:
            return "🕒 ANUNCIO NORMAL"
        else:
            return "🕓 ANUNCIO ANTIGUO"
    
    def generar_barra_progreso(self, valor: float, maximo: float = 100.0) -> str:
        """Genera una barra de progreso visual."""
        porcentaje = min(valor / maximo, 1.0)
        longitud_barra = 20
        relleno = int(longitud_barra * porcentaje)
        vacio = longitud_barra - relleno
        
        barrita = "█" * relleno + "░" * vacio
        return f"[{barra}] {porcentaje*100:.1f}%"
    
    def generar_notificacion_basica(self, anuncio: Dict) -> str:
        """Genera una notificación básica."""
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        puntuacion = anuncio.get('puntuacion_total', 0)
        
        titulo_formateado = self.formatear_titulo(titulo, puntuacion)
        
        if self.config.incluir_emoji:
            emoji = "🏠" if puntuacion >= 70 else "📋"
            titulo_formateado = f"{emoji} {titulo_formateado}"
        
        mensaje = f"""{titulo_formateado}

⭐ Puntuación: {puntuacion}/100 🌟

🔗 {link}

📅 Enviado: {datetime.now().strftime('%H:%M')}"""
        
        return mensaje
    
    def generar_notificacion_detallada(self, anuncio: Dict) -> str:
        """Genera una notificación detallada con todos los datos."""
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        puntuacion = anuncio.get('puntuacion_total', 0)
        puntuacion_precio = anuncio.get('puntuacion_precio', 0)
        puntuacion_caracteristicas = anuncio.get('puntuacion_caracteristicas', 0)
        puntuacion_ubicacion = anuncio.get('puntuacion_ubicacion', 0)
        puntuacion_descripcion = anuncio.get('puntuacion_descripcion', 0)
        puntuacion_reciente = anuncio.get('puntuacion_reciente', 0)
        fuente = anuncio.get('fuente', 'desconocido')
        
        titulo_formateado = self.formatear_titulo(titulo, puntuacion)
        
        # Generar resúmenes visuales
        resumen_precio = self.generar_resumen_precio(puntuacion_precio) if self.config.mostrar_precio else ""
        resumen_caracteristicas = self.generar_resumen_caracteristicas(puntuacion_caracteristicas) if self.config.mostrar_caracteristicas else ""
        resumen_ubicacion = self.generar_resumen_ubicacion(puntuacion_ubicacion) if self.config.mostrar_ubicacion else ""
        resumen_descripcion = self.generar_resumen_descripcion(puntuacion_descripcion) if self.config.mostrar_descripcion else ""
        resumen_reciente = self.generar_resumen_reciente(puntuacion_reciente) if self.config.incluir_puntuacion else ""
        
        # Generar barras de progreso
        barra_puntuacion = self.generar_barra_progreso(puntuacion) if self.config.incluir_puntuacion else ""
        barra_precio = self.generar_barra_progreso(puntuacion_precio) if self.config.mostrar_precio else ""
        barra_caracteristicas = self.generar_barra_progreso(puntuacion_caracteristicas) if self.config.mostrar_caracteristicas else ""
        barra_ubicacion = self.generar_barra_progreso(puntuacion_ubicacion) if self.config.mostrar_ubicacion else ""
        barra_descripcion = self.generar_barra_progreso(puntuacion_descripcion) if self.config.mostrar_descripcion else ""
        barra_reciente = self.generar_barra_progreso(puntuacion_reciente) if self.config.incluir_puntuacion else ""
        
        mensaje = f"""🏆 ¡ANUNCIO DE ALTA CALIDAD! 🏆

{titulo_formateado}

📊 PUNTUACIÓN GENERAL:
{barra_puntuacion} {puntuacion}/100 🌟

💰 PRECIO: {barra_precio} {puntuacion_precio}/100
{resumen_precio}

🏠 CARACTERÍSTICAS: {barra_caracteristicas} {puntuacion_caracteristicas}/100
{resumen_caracteristicas}

📍 UBICACIÓN: {barra_ubicacion} {puntuacion_ubicacion}/100
{resumen_ubicacion}

📝 DESCRIPCIÓN: {barra_descripcion} {puntuacion_descripcion}/100
{resumen_descripcion}

🕐 RECIENTE: {barra_reciente} {puntuacion_reciente}/100
{resumen_reciente}

🔗 ENLACE DIRECTO:
{link}

📅 FUENTE: {fuente.upper()}
⏰ {datetime.now().strftime('%H:%M %d/%m')}"""
        
        return mensaje
    
    def generar_notificacion_html(self, anuncio: Dict) -> str:
        """Genera una notificación en formato HTML."""
        if not self.config.formato_html:
            return self.generar_notificacion_detallada(anuncio)
        
        # Versión HTML simplificada
        titulo = anuncio.get('titulo', '')
        link = anuncio.get('link', '')
        puntuacion = anuncio.get('puntuacion_total', 0)
        
        html_mensaje = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
                .title {{ font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
                .stats {{ background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0; }}
                .stat-item {{ display: flex; justify-content: space-between; margin: 5px 0; }}
                .progress {{ background: #e9ecef; height: 20px; border-radius: 10px; overflow: hidden; margin: 5px 0; }}
                .progress-bar {{ background: #28a745; height: 100%; transition: width 0.3s; }}
                .link {{ background: #e9ecef; padding: 15px; border-radius: 8px; text-align: center; }}
                .link a {{ color: #007bff; text-decoration: none; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="title">🏆 ANUNCIO DE ALTA CALIDAD</div>
                <div>⭐ Puntuación: {puntuacion}/100</div>
            </div>
            
            <div class="stats">
                <div class="stat-item">
                    <span>💰 Precio:</span>
                    <span>{puntuacion}/100</span>
                </div>
                <div class="stat-item">
                    <span>🏠 Características:</span>
                    <span>{anuncio.get('puntuacion_caracteristicas', 0)}/100</span>
                </div>
                <div class="stat-item">
                    <span>📍 Ubicación:</span>
                    <span>{anuncio.get('puntuacion_ubicacion', 0)}/100</span>
                </div>
                <div class="stat-item">
                    <span>📝 Descripción:</span>
                    <span>{anuncio.get('puntuacion_descripcion', 0)}/100</span>
                </div>
            </div>
            
            <div class="link">
                <a href="{link}">🔗 Ver Anuncio Completo</a>
            </div>
        </body>
        </html>
        """
        
        return html_mensaje
    
    def enviar_notificacion(self, anuncio: Dict) -> bool:
        """Envía la notificación del anuncio."""
        try:
            if self.config.formato_html:
                mensaje = self.generar_notificacion_html(anuncio)
            else:
                mensaje = self.generar_notificacion_detallada(anuncio)
            
            return telegram_alert.enviar_mensaje(mensaje)
        except Exception as e:
            print(f"Error enviando notificación: {e}")
            return False
    
    def enviar_resumen_multiple(self, anuncios: List[Dict]) -> bool:
        """Envía un resumen con múltiples anuncios."""
        if not anuncios:
            return True
        
        titulo = f"📊 {len(anuncios)} ANUNCIOS DE ALTA CALIDAD"
        
        resumen = f"""
🏆 RESUMEN DE ANUNCIOS ({len(anuncios)} encontrados)

"""
        
        for i, anuncio in enumerate(anuncios[:5], 1):
            puntuacion = anuncio.get('puntuacion_total', 0)
            titulo = self.formatear_titulo(anuncio.get('titulo', ''), puntuacion)
            
            resumen += f"""{i}. {titulo}
   ⭐ {puntuacion}/100
   🔗 {anuncio.get('link', '')}
   
"""
        
        if len(anuncios) > 5:
            resumen += f"... y {len(anuncios) - 5} más"
        
        resumen += f"""
📅 {datetime.now().strftime('%H:%M %d/%m')}

🤖 Bot Inmobiliario 2.0
"""
        
        try:
            return telegram_alert.enviar_mensaje(resumen)
        except Exception as e:
            print(f"Error enviando resumen: {e}")
            return False


# Instancia global del notificador
notificador = NotificadorInteligente()


def configurar_notificaciones(config: NotificacionConfig):
    """Configura las notificaciones inteligentes."""
    global notificador
    notificador = NotificadorInteligente(config)


def enviar_notificacion_inteligente(anuncio: Dict) -> bool:
    """Envía una notificación inteligente."""
    return notificador.enviar_notificacion(anuncio)


def enviar_resumen_multiple(anuncios: List[Dict]) -> bool:
    """Envía un resumen con múltiples anuncios."""
    return notificador.enviar_resumen_multiple(anuncios)
