#!/usr/bin/env python3
"""
Aplicación Multiplataforma con Interfaz Gráfica
Botón de inicio y control total del bot
"""

import os
import sys
import json
import threading
import time
from datetime import datetime
import subprocess

# Importar según plataforma
try:
    if sys.platform == "darwin":  # macOS
        import tkinter as tk
        from tkinter import messagebox, filedialog
        PLATFORM = "macOS"
    elif sys.platform == "win32":  # Windows
        import tkinter as tk
        from tkinter import messagebox, filedialog
        PLATFORM = "Windows"
    else:  # Linux
        import tkinter as tk
        from tkinter import messagebox, filedialog
        PLATFORM = "Linux"
except ImportError:
    print("❌ Error: tkinter no disponible")
    sys.exit(1)

# Importar componentes del bot
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import INTERVALO_SEGUNDOS, ZONAS
    from database import anuncio_existente, guardar_anuncio
    from filtros import es_particular
    from filtros_tiempo import filtrar_anuncios_recientes
    from puntuacion_anuncios import puntuar_anuncios, obtener_mejores_anuncios
    from scraper_internet import buscar_internet
    from telegram_alert import enviar_mensaje
    from urls import normalizar_url_anuncio
    from verificador import anuncio_activo
    from indicador_busqueda import iniciar_indicador, detener, set_estado_busqueda
except ImportError as e:
    print(f"❌ Error importando bot: {e}")
    sys.exit(1)

class BotInmobiliarioApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🏠 Bot Inmobiliario 2.0")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        # Variables de estado
        self.bot_running = False
        self.bot_thread = None
        self.config_file = "config_usuario.json"
        
        # Colores modernos
        self.colors = {
            'bg': '#2c3e50',
            'fg': '#ffffff',
            'button': '#3498db',
            'button_hover': '#2980b9',
            'success': '#28a745',
            'error': '#dc3545',
            'warning': '#f59e0b'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Configurar interfaz gráfica"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🏠 BOT INMOBILIARIO 2.0",
            font=('Arial', 24, 'bold'),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title_label.pack(pady=(0, 20))
        
        # Frame de estado
        status_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(
            status_frame,
            text="🔴 BOT DETENIDO",
            font=('Arial', 14),
            bg=self.colors['bg'],
            fg=self.colors['error']
        )
        self.status_label.pack()
        
        # Frame de configuración
        config_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        config_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Token de Telegram
        token_frame = tk.Frame(config_frame, bg=self.colors['bg'])
        token_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            token_frame,
            text="🔑 Token Telegram:",
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.token_entry = tk.Entry(
            token_frame,
            font=('Arial', 12),
            bg='#34495e',
            fg=self.colors['fg'],
            insertbackground=self.colors['fg'],
            show='*'
        )
        self.token_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Chat ID
        chat_frame = tk.Frame(config_frame, bg=self.colors['bg'])
        chat_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(
            chat_frame,
            text="💬 Chat ID:",
            font=('Arial', 12),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.chat_entry = tk.Entry(
            chat_frame,
            font=('Arial', 12),
            bg='#34495e',
            fg=self.colors['fg'],
            insertbackground=self.colors['fg']
        )
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Frame de control
        control_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        control_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botón principal de INICIO/PARADA
        self.start_button = tk.Button(
            control_frame,
            text="🚀 INICIAR BOT",
            font=('Arial', 16, 'bold'),
            bg=self.colors['button'],
            fg=self.colors['fg'],
            activebackground=self.colors['button_hover'],
            activeforeground=self.colors['fg'],
            relief=tk.RAISED,
            bd=0,
            padx=20,
            pady=15,
            command=self.toggle_bot
        )
        self.start_button.pack(fill=tk.X, pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        stats_frame.pack(fill=tk.X, pady=(20, 0))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="📊 Estadísticas: Esperando inicio...",
            font=('Arial', 11),
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        self.stats_label.pack()
        
        # Frame de logs
        log_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Área de logs
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(
            log_frame,
            height=8,
            font=('Courier', 9),
            bg='#1e1e1e',
            fg=self.colors['fg'],
            yscrollcommand=log_scroll.set
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
        
        # Cargar configuración existente
        self.load_config()
        
        # Actualizar estadísticas cada 5 segundos
        self.update_stats()
        
    def log(self, message, color='fg'):
        """Añadir mensaje al log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
        # Colorear según tipo
        if color == 'success':
            self.log_text.tag_add('success', foreground=self.colors['success'])
        elif color == 'error':
            self.log_text.tag_add('error', foreground=self.colors['error'])
        elif color == 'warning':
            self.log_text.tag_add('warning', foreground=self.colors['warning'])
        else:
            self.log_text.tag_add('normal', foreground=self.colors['fg'])
        
        # Aplicar color a las últimas líneas
        lines = self.log_text.get('1.0', tk.END).split('\n')
        if lines:
            last_line = lines[-1]
            start_idx = f"1.0 linestart {len(lines)-1}"
            end_idx = f"1.0 lineend {len(lines)-1}"
            
            if message.startswith('✅'):
                self.log_text.tag_add('last', foreground=self.colors['success'])
            elif message.startswith('❌'):
                self.log_text.tag_add('last', foreground=self.colors['error'])
            elif message.startswith('⚠️'):
                self.log_text.tag_add('last', foreground=self.colors['warning'])
            else:
                self.log_text.tag_add('last', foreground=self.colors['fg'])
            
            self.log_text.tag_add('last', start=start_idx, end=end_idx)
    
    def load_config(self):
        """Cargar configuración existente"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                self.token_entry.insert(0, config.get('telegram_bot_token', ''))
                self.chat_entry.insert(0, str(config.get('telegram_chat_id', '')))
                
                self.log("✅ Configuración cargada", 'success')
                
            except Exception as e:
                self.log(f"❌ Error cargando configuración: {e}", 'error')
        else:
            self.log("⚠️ No hay configuración guardada", 'warning')
    
    def save_config(self):
        """Guardar configuración actual"""
        config = {
            'telegram_bot_token': self.token_entry.get(),
            'telegram_chat_id': self.chat_entry.get(),
            'intervalo_segundos': 120,
            'puntuacion_minima': 5,
            'filtro_horas': 24,
            'auto_actualizar': True
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.log("✅ Configuración guardada", 'success')
        except Exception as e:
            self.log(f"❌ Error guardando configuración: {e}", 'error')
    
    def toggle_bot(self):
        """Iniciar o detener el bot"""
        if not self.bot_running:
            # Iniciar bot
            self.start_bot()
        else:
            # Detener bot
            self.stop_bot()
    
    def start_bot(self):
        """Iniciar el bot"""
        token = self.token_entry.get().strip()
        chat_id = self.chat_entry.get().strip()
        
        if not token or not chat_id:
            self.log("❌ Token y Chat ID son requeridos", 'error')
            messagebox.showerror("Error", "Debes ingresar Token y Chat ID de Telegram")
            return
        
        # Guardar configuración
        self.save_config()
        
        # Cambiar estado
        self.bot_running = True
        self.start_button.config(
            text="⏸️ DETENER BOT",
            bg=self.colors['error']
        )
        self.status_label.config(
            text="🟢 BOT ACTIVO",
            fg=self.colors['success']
        )
        
        self.log("🚀 Iniciando Bot Inmobiliario 2.0...", 'success')
        
        # Iniciar bot en hilo separado
        self.bot_thread = threading.Thread(target=self.run_bot, args=(token, chat_id))
        self.bot_thread.daemon = True
        self.bot_thread.start()
    
    def stop_bot(self):
        """Detener el bot"""
        self.bot_running = False
        self.start_button.config(
            text="🚀 INICIAR BOT",
            bg=self.colors['button']
        )
        self.status_label.config(
            text="🔴 BOT DETENIDO",
            fg=self.colors['error']
        )
        
        self.log("⏸️ Deteniendo Bot...", 'warning')
        
        # Detener indicador
        try:
            detener()
        except:
            pass
    
    def run_bot(self, token, chat_id):
        """Ejecutar el bot principal"""
        try:
            # Actualizar variables de configuración
            import telegram_alert
            telegram_alert.TELEGRAM_BOT_TOKEN = token
            telegram_alert.TELEGRAM_CHAT_ID = chat_id
            
            # Iniciar indicador
            iniciar_indicador()
            
            self.log("✅ Bot iniciado correctamente", 'success')
            self.log(f"🔍 Buscando en: {len(ZONAS)} zonas", 'normal')
            self.log(f"⏱️ Intervalo: 120 segundos", 'normal')
            self.log(f"🎯 Puntuación mínima: 5 puntos", 'normal')
            self.log(f"📅 Filtro: 24 horas", 'normal')
            
            # Bucle principal del bot
            ciclo_count = 0
            while self.bot_running:
                try:
                    ciclo_count += 1
                    
                    # Buscar anuncios
                    anuncios = buscar_internet()
                    
                    # Filtrar por tiempo
                    anuncios_recientes = filtrar_anuncios_recientes(anuncios, max_minutos=1440)
                    
                    # Puntuar
                    anuncios_para_puntuar = []
                    for anuncio in anuncios_recientes:
                        anuncios_para_puntuar.append({
                            'titulo': anuncio['titulo'],
                            'link': anuncio['link'],
                            'descripcion': anuncio.get('descripcion', ''),
                            'fuente': anuncio.get('fuente', 'desconocido')
                        })
                    
                    anuncios_puntuados, _ = puntuar_anuncios(anuncios_para_puntuar, puntuacion_minima=5.0)
                    
                    # Procesar primeros 10
                    nuevos = 0
                    for anuncio in anuncios_puntuados[:10]:
                        titulo = anuncio.titulo
                        link = anuncio.link
                        
                        clave = normalizar_url_anuncio(link)
                        if not clave or anuncio_existente(clave):
                            continue
                        
                        # Verificar si es particular
                        if not es_particular(titulo):
                            continue
                        
                        # Verificar si está activo
                        if not anuncio_activo(link):
                            continue
                        
                        # Enviar a Telegram
                        mensaje = f"""🏠 NUEVO ANUNCIO DE PARTICULAR!

{titulo}

💰 Puntuación: {anuncio.puntuacion_total}/100

🔗 Ver anuncio: {link}

🤖 Bot Inmobiliario 2.0
⏰ {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}
"""
                        
                        if enviar_mensaje(mensaje):
                            guardar_anuncio(link, titulo)
                            nuevos += 1
                            self.log(f"✅ Nuevo anuncio: {titulo[:30]}...", 'success')
                    
                    # Actualizar estadísticas
                    self.stats_label.config(
                        text=f"📊 Ciclo #{ciclo_count} | Encontrados: {len(anuncios)} | Recientes: {len(anuncios_recientes)} | Notificados: {nuevos}"
                    )
                    
                    # Esperar para siguiente ciclo
                    time.sleep(120)
                    
                except Exception as e:
                    self.log(f"❌ Error en ciclo: {e}", 'error')
                    time.sleep(10)
                    
        except Exception as e:
            self.log(f"❌ Error fatal del bot: {e}", 'error')
            self.stop_bot()
    
    def update_stats(self):
        """Actualizar estadísticas periódicamente"""
        if self.bot_running:
            # Aquí podrías agregar más estadísticas
            pass
        
        # Programar siguiente actualización
        self.root.after(5000, self.update_stats)
    
    def on_closing(self):
        """Al cerrar la aplicación"""
        if self.bot_running:
            self.stop_bot()
        
        self.root.destroy()
    
    def run(self):
        """Iniciar la aplicación"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    """Función principal"""
    print("·" * 60)
    print("BOT INMOBILIARIO 2.0 - APLICACIÓN MULTIPLATAFORMA")
    print("·" * 60)
    print(f"Plataforma: {PLATFORM}")
    print(f"Timestamp: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}")
    print()
    
    # Crear y ejecutar aplicación
    app = BotInmobiliarioApp()
    app.run()

if __name__ == "__main__":
    main()
