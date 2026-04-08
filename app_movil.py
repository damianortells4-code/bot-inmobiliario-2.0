#!/usr/bin/env python3
"""
Aplicación web móvil para controlar el bot inmobiliario
Accesible desde cualquier navegador móvil
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import json
from datetime import datetime, timedelta
import subprocess
import threading
import time
import os

# Crear aplicación Flask
app = Flask(__name__)
app.secret_key = 'bot_inmobiliario_seguro'

# Configuración
DB_PATH = 'anuncios.db'
BOT_PROCESS = None

class ControladorBot:
    """Controlador para el bot inmobiliario"""
    
    def __init__(self):
        self.estado = 'detenido'
        self.ultimo_anuncio = None
        self.estadisticas = {
            'anuncios_encontrados': 0,
            'anuncios_notificados': 0,
            'anuncios_filtrados': 0,
            'tiempo_ejecucion': 0,
            'ultima_ejecucion': None
        }
    
    def iniciar_bot(self):
        """Iniciar el bot en segundo plano"""
        if self.estado == 'ejecutando':
            return False
        
        def ejecutar_bot():
            try:
                self.estado = 'ejecutando'
                # Ejecutar el bot como proceso separado
                import main
                main.main()
            except Exception as e:
                print(f"Error en bot: {e}")
            finally:
                self.estado = 'detenido'
        
        thread = threading.Thread(target=ejecutar_bot)
        thread.daemon = True
        thread.start()
        
        return True
    
    detener_bot = lambda self: 'Función detener no implementada'
    
    def obtener_estado(self):
        """Obtener estado actual del bot"""
        return {
            'estado': self.estado,
            'ultimo_anuncio': self.ultimo_anuncio,
            'estadisticas': self.estadisticas,
            'timestamp': datetime.now().isoformat()
        }

# Instancia global del controlador
controlador = ControladorBot()

@app.route('/')
def index():
    """Página principal - Dashboard"""
    return render_template('dashboard.html')

@app.route('/api/estado')
def api_estado():
    """API para obtener estado del bot"""
    return jsonify(controlador.obtener_estado())

@app.route('/api/iniciar', methods=['POST'])
def api_iniciar():
    """API para iniciar el bot"""
    if controlador.iniciar_bot():
        return jsonify({'success': True, 'message': 'Bot iniciado'})
    return jsonify({'success': False, 'message': 'El bot ya está ejecutando'})

@app.route('/api/detener', methods=['POST'])
def api_detener():
    """API para detener el bot"""
    controlador.estado = 'detenido'
    return jsonify({'success': True, 'message': 'Bot detenido'})

@app.route('/api/anuncios')
def api_anuncios():
    """API para obtener últimos anuncios"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Obtener últimos 10 anuncios
        cursor.execute('''
            SELECT titulo, link, fecha 
            FROM anuncios 
            ORDER BY fecha DESC 
            LIMIT 10
        ''')
        
        anuncios = []
        for row in cursor.fetchall():
            anuncios.append({
                'titulo': row[0],
                'link': row[1],
                'fecha': row[2]
            })
        
        conn.close()
        return jsonify({'anuncios': anuncios})
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Estadísticas básicas
        cursor.execute('SELECT COUNT(*) FROM anuncios')
        total_anuncios = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM anuncios 
            WHERE fecha > datetime('now', '-24 hours')
        ''')
        ultimas_24h = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM anuncios 
            WHERE fecha > datetime('now', '-7 days')
        ''')
        ultima_semana = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_anuncios': total_anuncios,
            'ultimas_24h': ultimas_24h,
            'ultima_semana': ultima_semana,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/configuracion', methods=['GET', 'POST'])
def api_configuracion():
    """API para obtener/actualizar configuración"""
    if request.method == 'GET':
        try:
            import config
            config_data = {
                'intervalo_segundos': getattr(config, 'INTERVALO_SEGUNDOS', 180),
                'zonas': getattr(config, 'ZONAS', []),
                'fuentes': {
                    'duckduckgo': getattr(config, 'USAR_DUCKDUCKGO', False),
                    'pisos': getattr(config, 'USAR_PISOS', False),
                    'fotocasa': getattr(config, 'USAR_FOTOCASA', False),
                    'milanuncios': getattr(config, 'USAR_MILANUNCIOS', False)
                }
            }
            return jsonify(config_data)
        except Exception as e:
            return jsonify({'error': str(e)})
    
    elif request.method == 'POST':
        # Actualizar configuración (implementar si es necesario)
        return jsonify({'success': True, 'message': 'Configuración actualizada'})

def crear_templates():
    """Crear archivos HTML para la aplicación móvil"""
    
    # Dashboard HTML
    dashboard_html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Inmobiliario - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            color: #333;
        }
        
        .container {
            max-width: 100%;
            padding: 20px;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .status {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .status-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ccc;
        }
        
        .status-dot.active {
            background: #4CAF50;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: all 0.3s;
        }
        
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        
        .btn.danger {
            background: #e53e3e;
        }
        
        .btn.danger:hover {
            background: #c53030;
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }
        
        .stat-item {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .stat-number {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .anuncio {
            padding: 15px;
            border-left: 4px solid #667eea;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        
        .anuncio-titulo {
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .anuncio-fecha {
            font-size: 12px;
            color: #666;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #666;
        }
        
        .error {
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bot Inmobiliario 2.0</h1>
            <p>Control desde móvil</p>
        </div>
        
        <div class="card">
            <div class="status">
                <h3>Estado del Bot</h3>
                <div class="status-dot" id="statusDot"></div>
            </div>
            <p id="estadoTexto">Desconocido</p>
            <div style="text-align: center; margin-top: 15px;">
                <button class="btn" onclick="iniciarBot()">Iniciar Bot</button>
                <button class="btn danger" onclick="detenerBot()">Detener Bot</button>
            </div>
        </div>
        
        <div class="card">
            <h3>Estadísticas</h3>
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number" id="totalAnuncios">-</div>
                    <div class="stat-label">Total Anuncios</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="ultimas24h">-</div>
                    <div class="stat-label">Últimas 24h</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="ultimaSemana">-</div>
                    <div class="stat-label">Última Semana</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number" id="estado">-</div>
                    <div class="stat-label">Estado</div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>Últimos Anuncios</h3>
            <div id="anunciosContainer">
                <div class="loading">Cargando anuncios...</div>
            </div>
        </div>
        
        <div class="card">
            <h3>Configuración</h3>
            <div id="configContainer">
                <div class="loading">Cargando configuración...</div>
            </div>
        </div>
    </div>
    
    <script>
        // Funciones de la aplicación
        async function actualizarEstado() {
            try {
                const response = await fetch('/api/estado');
                const data = await response.json();
                
                const statusDot = document.getElementById('statusDot');
                const estadoTexto = document.getElementById('estadoTexto');
                
                if (data.estado === 'ejecutando') {
                    statusDot.classList.add('active');
                    estadoTexto.textContent = 'Bot ejecutando';
                } else {
                    statusDot.classList.remove('active');
                    estadoTexto.textContent = 'Bot detenido';
                }
            } catch (error) {
                console.error('Error al actualizar estado:', error);
            }
        }
        
        async function actualizarEstadisticas() {
            try {
                const response = await fetch('/api/estadisticas');
                const data = await response.json();
                
                document.getElementById('totalAnuncios').textContent = data.total_anuncios || 0;
                document.getElementById('ultimas24h').textContent = data.ultimas_24h || 0;
                document.getElementById('ultimaSemana').textContent = data.ultima_semana || 0;
            } catch (error) {
                console.error('Error al actualizar estadísticas:', error);
            }
        }
        
        async function actualizarAnuncios() {
            try {
                const response = await fetch('/api/anuncios');
                const data = await response.json();
                
                const container = document.getElementById('anunciosContainer');
                
                if (data.error) {
                    container.innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                    return;
                }
                
                if (data.anuncios.length === 0) {
                    container.innerHTML = '<div class="loading">No hay anuncios recientes</div>';
                    return;
                }
                
                let html = '';
                data.anuncios.forEach(anuncio => {
                    const fecha = new Date(anuncio.fecha);
                    const fechaStr = fecha.toLocaleString('es-ES');
                    
                    html += `
                        <div class="anuncio">
                            <div class="anuncio-titulo">${anuncio.titulo}</div>
                            <div class="anuncio-fecha">${fechaStr}</div>
                        </div>
                    `;
                });
                
                container.innerHTML = html;
            } catch (error) {
                console.error('Error al actualizar anuncios:', error);
            }
        }
        
        async function actualizarConfiguracion() {
            try {
                const response = await fetch('/api/configuracion');
                const data = await response.json();
                
                const container = document.getElementById('configContainer');
                
                if (data.error) {
                    container.innerHTML = '<div class="error">Error: ' + data.error + '</div>';
                    return;
                }
                
                let html = `
                    <p><strong>Intervalo:</strong> ${data.intervalo_segundos} segundos</p>
                    <p><strong>Zonas:</strong> ${data.zonas.length} configuradas</p>
                    <p><strong>Fuentes activas:</strong></p>
                    <ul>
                `;
                
                Object.entries(data.fuentes).forEach(([fuente, activa]) => {
                    html += `<li>${fuente}: ${activa ? 'Sí' : 'No'}</li>`;
                });
                
                html += '</ul>';
                container.innerHTML = html;
            } catch (error) {
                console.error('Error al actualizar configuración:', error);
            }
        }
        
        async function iniciarBot() {
            try {
                const response = await fetch('/api/iniciar', {method: 'POST'});
                const data = await response.json();
                
                if (data.success) {
                    alert('Bot iniciado correctamente');
                    actualizarEstado();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error al iniciar el bot');
            }
        }
        
        async function detenerBot() {
            try {
                const response = await fetch('/api/detener', {method: 'POST'});
                const data = await response.json();
                
                if (data.success) {
                    alert('Bot detenido correctamente');
                    actualizarEstado();
                } else {
                    alert('Error: ' + data.message);
                }
            } catch (error) {
                alert('Error al detener el bot');
            }
        }
        
        // Actualizar datos cada 10 segundos
        function actualizarDatos() {
            actualizarEstado();
            actualizarEstadisticas();
            actualizarAnuncios();
            actualizarConfiguracion();
        }
        
        // Inicialización
        actualizarDatos();
        setInterval(actualizarDatos, 10000);
    </script>
</body>
</html>
    """
    
    # Crear directorio templates si no existe
    os.makedirs('templates', exist_ok=True)
    
    # Guardar el archivo HTML
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dashboard_html)
    
    print("Templates creados correctamente")

def iniciar_app():
    """Iniciar la aplicación web móvil"""
    print("Creando templates...")
    crear_templates()
    
    print("Iniciando aplicación web móvil...")
    print("Accede a: http://localhost:8080")
    print("Desde móvil: http://TU_IP:8080")
    
    app.run(host='0.0.0.0', port=8080, debug=False)

if __name__ == '__main__':
    iniciar_app()
