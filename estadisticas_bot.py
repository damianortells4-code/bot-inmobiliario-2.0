"""Sistema de estadísticas y métricas del bot."""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import os


@dataclass
class EstadisticasBot:
    """Clase para almacenar estadísticas del bot."""
    total_anuncios_procesados: int = 0
    anuncios_filtrados: int = 0
    anuncios_notificados: int = 0
    anuncios_por_fuente: Dict[str, int] = None
    anuncios_por_zona: Dict[str, int] = None
    puntuacion_promedio: float = 0.0
    tiempo_ejecucion_promedio: float = 0.0
    ultima_ejecucion: str = ""
    errores_consecutivos: int = 0
    exitos_consecutivos: int = 0
    fecha_inicio: str = ""
    fecha_ultimo_anuncio: str = ""


class GestorEstadisticas:
    """Gestor de estadísticas y métricas del bot."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.stats_db_path = db_path.replace('.db', '_estadisticas.db')
        self._iniciar_base_datos()
    
    def _iniciar_base_datos(self):
        """Inicia la base de datos de estadísticas."""
        conn = sqlite3.connect(self.stats_db_path)
        cursor = conn.cursor()
        
        # Crear tabla de estadísticas si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estadisticas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                total_anuncios_procesados INTEGER DEFAULT 0,
                anuncios_filtrados INTEGER DEFAULT 0,
                anuncios_notificados INTEGER DEFAULT 0,
                anuncios_por_fuente TEXT DEFAULT '{}',
                anuncios_por_zona TEXT DEFAULT '{}',
                puntuacion_promedio REAL DEFAULT 0.0,
                tiempo_ejecucion_promedio REAL DEFAULT 0.0,
                ultima_ejecucion TEXT,
                errores_consecutivos INTEGER DEFAULT 0,
                exitos_consecutivos INTEGER DEFAULT 0,
                fecha_inicio TEXT,
                fecha_ultimo_anuncio TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def registrar_ejecucion(self, 
                        total_procesados: int = 0,
                        filtrados: int = 0,
                        notificados: int = 0,
                        anuncios_por_fuente: Dict[str, int] = None,
                        anuncios_por_zona: Dict[str, int] = None,
                        puntuacion_promedio: float = 0.0,
                        tiempo_ejecucion: float = 0.0,
                        errores: int = 0,
                        exitos: int = 0):
        """Registra las estadísticas de una ejecución del bot."""
        
        conn = sqlite3.connect(self.stats_db_path)
        cursor = conn.cursor()
        
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Obtener estadísticas anteriores
        cursor.execute('SELECT * FROM estadisticas ORDER BY id DESC LIMIT 1')
        stats_anteriores = cursor.fetchone()
        
        if stats_anteriores:
            # Actualizar estadísticas acumuladas
            total_acumulado = stats_anteriores[2] + total_procesados
            filtrados_acumulado = stats_anteriores[3] + filtrados
            notificados_acumulado = stats_anteriores[4] + notificados
            
            # Calcular consecutivos
            if errores > 0:
                errores_consecutivos = stats_anteriores[9] + 1
                exitos_consecutivos = 0
            else:
                errores_consecutivos = 0
                exitos_consecutivos = stats_anteriores[10] + 1
            
            # Actualizar o mantener fecha de inicio
            fecha_inicio = stats_anteriores[12] if stats_anteriores[12] else fecha_actual
            
            # Calcular promedios móviles
            tiempo_promedio = self._calcular_promedio_movil(
                stats_anteriores[8], tiempo_ejecucion, stats_anteriores[11]
            )
            
            cursor.execute('''
                UPDATE estadisticas SET
                    total_anuncios_procesados = ?,
                    anuncios_filtrados = ?,
                    anuncios_notificados = ?,
                    anuncios_por_fuente = ?,
                    anuncios_por_zona = ?,
                    puntuacion_promedio = ?,
                    tiempo_ejecucion_promedio = ?,
                    ultima_ejecucion = ?,
                    errores_consecutivos = ?,
                    exitos_consecutivos = ?,
                    fecha_inicio = ?,
                    fecha_ultimo_anuncio = ?
                WHERE id = ?
            ''', (
                total_acumulado, filtrados_acumulado, notificados_acumulado,
                json.dumps(anuncios_por_fuente) if anuncios_por_fuente else '{}',
                json.dumps(anuncios_por_zona) if anuncios_por_zona else '{}',
                puntuacion_promedio, tiempo_promedio,
                fecha_actual, errores_consecutivos, exitos_consecutivos,
                fecha_inicio, fecha_actual
            ))
        else:
            # Primera ejecución
            cursor.execute('''
                INSERT INTO estadisticas (
                    fecha, total_anuncios_procesados, anuncios_filtrados, anuncios_notificados,
                    anuncios_por_fuente, anuncios_por_zona, puntuacion_promedio, tiempo_ejecucion_promedio,
                    ultima_ejecucion, errores_consecutivos, exitos_consecutivos,
                    fecha_inicio, fecha_ultimo_anuncio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fecha_actual, total_procesados, filtrados, notificados,
                json.dumps(anuncios_por_fuente) if anuncios_por_fuente else '{}',
                json.dumps(anuncios_por_zona) if anuncios_por_zona else '{}',
                puntuacion_promedio, tiempo_ejecucion,
                fecha_actual, errores, exitos,
                fecha_actual, fecha_actual
            ))
        
        conn.commit()
        conn.close()
    
    def _calcular_promedio_movil(self, promedio_anterior: float, nuevo_valor: float, n_muestras: int = 10) -> float:
        """Calcula promedio móvil con número fijo de muestras."""
        if promedio_anterior == 0:
            return nuevo_valor
        
        alpha = 2 / (n_muestras + 1)
        return (alpha * nuevo_valor) + ((1 - alpha) * promedio_anterior)
    
    def obtener_estadisticas_actuales(self) -> Optional[EstadisticasBot]:
        """Obtiene las estadísticas más recientes."""
        conn = sqlite3.connect(self.stats_db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM estadisticas ORDER BY id DESC LIMIT 1')
        stats_row = cursor.fetchone()
        
        conn.close()
        
        if not stats_row:
            return None
        
        return EstadisticasBot(
            total_anuncios_procesados=stats_row[2],
            anuncios_filtrados=stats_row[3],
            anuncios_notificados=stats_row[4],
            anuncios_por_fuente=json.loads(stats_row[5]) if stats_row[5] else {},
            anuncios_por_zona=json.loads(stats_row[6]) if stats_row[6] else {},
            puntuacion_promedio=stats_row[7],
            tiempo_ejecucion_promedio=stats_row[8],
            ultima_ejecucion=stats_row[9],
            errores_consecutivos=stats_row[10],
            exitos_consecutivos=stats_row[11],
            fecha_inicio=stats_row[12],
            fecha_ultimo_anuncio=stats_row[13]
        )
    
    def obtener_historial_estadisticas(self, dias: int = 7) -> List[EstadisticasBot]:
        """Obtiene el historial de estadísticas de los últimos N días."""
        conn = sqlite3.connect(self.stats_db_path)
        cursor = conn.cursor()
        
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            SELECT * FROM estadisticas 
            WHERE fecha >= ? 
            ORDER BY id DESC
        ''', (fecha_limite,))
        
        rows = cursor.fetchall()
        conn.close()
        
        estadisticas = []
        for row in rows:
            estadisticas.append(EstadisticasBot(
                total_anuncios_procesados=row[2],
                anuncios_filtrados=row[3],
                anuncios_notificados=row[4],
                anuncios_por_fuente=json.loads(row[5]) if row[5] else {},
                anuncios_por_zona=json.loads(row[6]) if row[6] else {},
                puntuacion_promedio=row[7],
                tiempo_ejecucion_promedio=row[8],
                ultima_ejecucion=row[9],
                errores_consecutivos=row[10],
                exitos_consecutivos=row[11],
                fecha_inicio=row[12],
                fecha_ultimo_anuncio=row[13]
            ))
        
        return estadisticas
    
    def generar_reporte_rendimiento(self, dias: int = 7) -> str:
        """Genera un reporte de rendimiento del bot."""
        estadisticas = self.obtener_historial_estadisticas(dias)
        
        if not estadisticas:
            return "No hay estadísticas disponibles"
        
        reporte = f"""
📊 REPORTE DE RENDIMIENTO - ÚLTIMOS {dias} DÍAS
══════════════════════════════════════════════════

📈 MÉTRICAS PRINCIPALES:
"""
        
        if len(estadisticas) >= 2:
            stats_actual = estadisticas[0]
            stats_anterior = estadisticas[1]
            
            # Calcular tendencias
            tendencia_procesados = stats_actual.total_anuncios_procesados - stats_anterior.total_anuncios_procesados
            tendencia_notificados = stats_actual.anuncios_notificados - stats_anterior.anuncios_notificados
            tendencia_filtrados = stats_actual.anuncios_filtrados - stats_anterior.anuncios_filtrados
            
            reporte += f"""
   📊 Total Procesados: {stats_actual.total_anuncios_procesados} ({tendencia_procesados:+d})
   📋 Notificados: {stats_actual.anuncios_notificados} ({tendencia_notificados:+d})
   🚫 Filtrados: {stats_actual.anuncios_filtrados} ({tendencia_filtrados:+d})
   📈 Puntuación Promedio: {stats_actual.puntuacion_promedio:.1f}
   ⏱ Tiempo Promedio: {stats_actual.tiempo_ejecucion_promedio:.1f}s
"""
        
        # Top fuentes
        if stats_actual.anuncios_por_fuente:
            reporte += f"""
📈 TOP FUENTES:
"""
            fuentes_ordenadas = sorted(
                stats_actual.anuncios_por_fuente.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for fuente, count in fuentes_ordenadas[:5]:
                reporte += f"   • {fuente}: {count} anuncios\n"
        
        # Top zonas
        if stats_actual.anuncios_por_zona:
            reporte += f"""
📍 TOP ZONAS:
"""
            zonas_ordenadas = sorted(
                stats_actual.anuncios_por_zona.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            for zona, count in zonas_ordenadas[:5]:
                reporte += f"   • {zona}: {count} anuncios\n"
        
        # Estado del sistema
        reporte += f"""
🤖 ESTADO DEL SISTEMA:
   ✅ Éxitos Consecutivos: {stats_actual.exitos_consecutivos}
   ❌ Errores Consecutivos: {stats_actual.errores_consecutivos}
   📅 Última Ejecución: {stats_actual.ultima_ejecucion}
   📅 Inicio Operación: {stats_actual.fecha_inicio}
   📈 Último Anuncio: {stats_actual.fecha_ultimo_anuncio}

════════════════════════════════════════════════
"""
        
        return reporte
    
    def limpiar_estadisticas_antiguas(self, dias: int = 30):
        """Limpia estadísticas antiguas para mantener la base de datos ligera."""
        conn = sqlite3.connect(self.stats_db_path)
        cursor = conn.cursor()
        
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('DELETE FROM estadisticas WHERE fecha < ?', (fecha_limite,))
        
        eliminados = cursor.rowcount
        conn.commit()
        conn.close()
        
        return f"🧹 Eliminadas {eliminadas} estadísticas antiguas (más de {dias} días)"


# Instancia global del gestor de estadísticas
gestor_estadisticas = None


def iniciar_gestor_estadisticas(db_path: str):
    """Inicia el gestor de estadísticas."""
    global gestor_estadisticas
    gestor_estadisticas = GestorEstadisticas(db_path)


def registrar_estadisticas_ejecucion(**kwargs):
    """Registra las estadísticas de una ejecución del bot."""
    if gestor_estadisticas:
        return gestor_estadisticas.registrar_ejecucion(**kwargs)
    return False


def obtener_estadisticas_actuales():
    """Obtiene las estadísticas actuales del bot."""
    if gestor_estadisticas:
        return gestor_estadisticas.obtener_estadisticas_actuales()
    return None


def generar_reporte_rendimiento(dias: int = 7):
    """Genera un reporte de rendimiento del bot."""
    if gestor_estadisticas:
        return gestor_estadisticas.generar_reporte_rendimiento(dias)
    return "Gestor de estadísticas no iniciado"


def limpiar_estadisticas_antiguas(dias: int = 30):
    """Limpia estadísticas antiguas."""
    if gestor_estadisticas:
        return gestor_estadisticas.limpiar_estadisticas_antiguas(dias)
    return "Gestor de estadísticas no iniciado"
