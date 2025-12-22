#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧠 NEURO-OS GENESIS: MASTER EDITION
===================================
Arquitectura: Single Window / Direct Rendering (Game Loop style)
Estado: 100% Funcional y Estable
"""

import sys
import random
import hashlib
from pathlib import Path

from PySide6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, 
                             QWidget, QFileSystemModel, QTreeView, QHeaderView, QLabel, QHBoxLayout,
                             QFrame, QComboBox, QCheckBox, QGridLayout, QProgressBar, QTextEdit,
                             QTabWidget, QTableWidget, QTableWidgetItem, QMessageBox, QListWidget, QListWidgetItem, QMenu)
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient, QRadialGradient, QPen
from PySide6.QtCore import Qt, QTimer, QPoint, QDir

# Config Manager
from config_manager import ConfigManager

# Web Browser
from web_browser import WebBrowserWindow

# Window Capture
from window_capture import CapturedAppWindow

# ============================================================
# ⚙️ CONFIGURACIÓN Y ESTADOS
# ============================================================
STATE_BOOT = 0
STATE_LOGIN = 1
STATE_DESKTOP = 2

# ============================================================
# 📂 EXPLORADOR DE ARCHIVOS (MODERNO)
# ============================================================
class FileExplorerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window) # Ventana independiente
        self.setWindowTitle("NEURO-FILES")
        self.resize(900, 600)
        self.setStyleSheet("""
            QWidget {
                background: #050510;
                color: cyan;
                font-family: 'Segoe UI', Consolas;
            }
        """)
        self.setStyleSheet("background: rgba(0, 10, 20, 0.95); color: cyan;")
        
        layout = QVBoxLayout(self)
        
        # Ruta del Escritorio del Usuario
        import os
        desktop_path = os.path.normpath(os.path.expanduser("~/Desktop"))
        
        self.model = QFileSystemModel()
        self.model.setRootPath(desktop_path)
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(desktop_path))
        
        # Estilo Futurista para el TreeView
        self.tree.setStyleSheet("""
            QTreeView {
                background: transparent;
                border: 1px solid #004444;
                color: #00ffaa;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QTreeView::item:hover {
                background: rgba(0, 255, 255, 0.2);
                border: 1px solid cyan;
            }
            QTreeView::item:selected {
                background: rgba(0, 255, 255, 0.4);
                color: white;
            }
            QHeaderView::section {
                background: #002233;
                color: cyan;
                padding: 5px;
                border: 1px solid #004455;
            }
        """)
        
        # Columnas
        self.tree.setColumnWidth(0, 350)
        
        layout.addWidget(self.tree)
        
        # StatusBar
        self.status = QLabel("Ready. Connected to Local Storage.")
        self.status.setStyleSheet("color: #00aaaa; font-style: italic; margin-top: 5px;")
        layout.addWidget(self.status)

# ============================================================
# 🖥️ SISTEMA PRINCIPAL
# ============================================================
# ============================================================
# 🖥️ SYSTEM STATUS BAR (TOP BAR)
# ============================================================
class SystemStatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setStyleSheet("background: rgba(0, 10, 20, 0.85); border-bottom: 1px solid #004444;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        
        # --- LEFT: LOGO & MENU ---
        btn_menu = QPushButton("💠 NEURO")
        btn_menu.setStyleSheet("""
            QPushButton { color: cyan; font-weight: bold; border: none; background: transparent; font-size: 14px; }
            QPushButton:hover { color: white; text-shadow: 0 0 10px cyan; }
        """)
        
        # Menú desplegable
        menu = QMenu(btn_menu)
        menu.setStyleSheet("""
            QMenu { background: #001122; border: 1px solid cyan; color: white; }
            QMenu::item:selected { background: #003344; color: cyan; }
        """)
        menu.addAction("📊 System Monitor", lambda: self.run_cmd("taskmgr"))
        menu.addAction("⚙️ Settings", lambda: self.run_cmd("start ms-settings:"))
        menu.addAction("📁 File Explorer", lambda: self.run_cmd("explorer"))
        menu.addSeparator()
        menu.addAction("🔄 Restart", lambda: self.run_cmd("shutdown /r /t 0"))
        menu.addAction("⏻ Shutdown", lambda: self.run_cmd("shutdown /s /t 0"))
        btn_menu.setMenu(menu)
        
        layout.addWidget(btn_menu)
        
        layout.addStretch() # Spacer
        
        # --- CENTER: RESOURCE MONITOR (Lightweight indicator) ---
        self.cpu_lbl = QLabel("CPU: --")
        self.cpu_lbl.setStyleSheet("color: #00ff88; font-family: 'Consolas'; font-size: 11px; margin-right: 10px;")
        layout.addWidget(self.cpu_lbl)
        
        self.ram_lbl = QLabel("RAM: --")
        self.ram_lbl.setStyleSheet("color: #00ff88; font-family: 'Consolas'; font-size: 11px; margin-right: 15px;")
        layout.addWidget(self.ram_lbl)
        
        # --- CENTER: CLOCK ---
        self.clock_lbl = QLabel("--:--")
        self.clock_lbl.setStyleSheet("color: white; font-family: 'Segoe UI'; font-size: 14px; font-weight: bold;")
        layout.addWidget(self.clock_lbl)
        
        layout.addStretch() # Spacer
        
        # --- RIGHT: STATUS ICONS ---
        
        # 1. Bluetooth (Link to Windows Settings)
        btn_bt = QPushButton("🦷")
        btn_bt.setToolTip("Bluetooth Settings")
        btn_bt.clicked.connect(lambda: self.run_cmd("start ms-settings:bluetooth"))
        self.style_icon(btn_bt)
        layout.addWidget(btn_bt)

        # 2. Network (Check status)
        self.net_icon = QPushButton("📶")
        self.net_icon.setToolTip("Network Status")
        self.net_icon.clicked.connect(lambda: self.run_cmd("start ms-settings:network"))
        self.style_icon(self.net_icon)
        layout.addWidget(self.net_icon)

        # 3. Audio (Link to Volume Mixer)
        btn_vol = QPushButton("🔊")
        btn_vol.setToolTip("System Volume")
        btn_vol.clicked.connect(lambda: self.run_cmd("sndvol"))
        self.style_icon(btn_vol)
        layout.addWidget(btn_vol)

        # 4. Battery (Real reading)
        self.bat_lbl = QLabel("🔋 Scanning...")
        self.bat_lbl.setStyleSheet("color: #0f0; margin-left: 10px; font-size: 12px;")
        layout.addWidget(self.bat_lbl)
        
        # 5. User Menu
        btn_user = QPushButton("👤")
        btn_user.setToolTip("User Menu")
        user_menu = QMenu(btn_user)
        user_menu.setStyleSheet("""
            QMenu { background: #001122; border: 1px solid cyan; color: white; }
            QMenu::item:selected { background: #003344; color: cyan; }
        """)
        user_menu.addAction("👤 Profile", lambda: None)  # Placeholder
        user_menu.addAction("🔒 Lock Screen", lambda: self.run_cmd("rundll32 user32.dll,LockWorkStation"))
        user_menu.addSeparator()
        user_menu.addAction("🚪 Logout", lambda: parent.close() if parent else None)
        btn_user.setMenu(user_menu)
        self.style_icon(btn_user)
        layout.addWidget(btn_user)
        
        # Timer para actualizar datos (optimizado a 10s para mínimo consumo)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_status)
        self.timer.start(10000) # Cada 10s - Ultra optimizado
        self.update_status() # Primera ejecución

    def style_icon(self, btn):
        btn.setFixedSize(30, 30)
        btn.setStyleSheet("""
            QPushButton { background: transparent; border: none; font-size: 16px; color: #aaa; }
            QPushButton:hover { color: cyan; background: rgba(255,255,255,0.1); border-radius: 5px; }
        """)

    def run_cmd(self, cmd):
        import os
        os.system(cmd)

    def update_status(self):
        import psutil, datetime
        
        # CPU y RAM (mostrar bajo consumo) - Optimizado sin bloqueo
        try:
            # Usar interval=None para no bloquear (usa valor cacheado)
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory().percent
            
            # Color verde si bajo consumo (<30%), amarillo si medio, rojo si alto
            cpu_color = "#00ff88" if cpu < 30 else ("#ffaa00" if cpu < 60 else "#ff5555")
            ram_color = "#00ff88" if ram < 50 else ("#ffaa00" if ram < 75 else "#ff5555")
            
            self.cpu_lbl.setText(f"CPU: {cpu:.0f}%")
            self.cpu_lbl.setStyleSheet(f"color: {cpu_color}; font-family: 'Consolas'; font-size: 11px; margin-right: 10px;")
            
            self.ram_lbl.setText(f"RAM: {ram:.0f}%")
            self.ram_lbl.setStyleSheet(f"color: {ram_color}; font-family: 'Consolas'; font-size: 11px; margin-right: 15px;")
        except:
            pass
        
        # Hora
        now = datetime.datetime.now().strftime("%H:%M  |  %d %b")
        self.clock_lbl.setText(now)
        
        # Batería
        try:
            bat = psutil.sensors_battery()
            if bat:
                plugged = "⚡" if bat.power_plugged else ""
                self.bat_lbl.setText(f"🔋 {int(bat.percent)}% {plugged}")
                if bat.percent < 20 and not bat.power_plugged:
                    self.bat_lbl.setStyleSheet("color: #ff5555; font-weight: bold;")
                else:
                    self.bat_lbl.setStyleSheet("color: #0f0;")
            else:
                self.bat_lbl.setText("🔌 AC") # Desktop
        except:
             self.bat_lbl.setText("🔌 AC")
             
        # Red (Simple check)
        try:
            net_stats = psutil.net_if_stats()
            # Buscar alguna interfaz 'Up'
            online = any(stats.isup for stats in net_stats.values())
            color = "cyan" if online else "#555"
            self.net_icon.setStyleSheet(f"color: {color}; border: none; background: transparent; font-size: 16px;")
        except: pass

class NeuroMaster(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuro-OS Genesis Elite")
        self.current_state = STATE_BOOT
        
        # --- OPTIMIZACIONES DE RENDIMIENTO ---
        self.setAttribute(Qt.WA_OpaquePaintEvent, True)  # No repintar fondo automáticamente
        self.setAttribute(Qt.WA_NoSystemBackground, True)  # No usar fondo del sistema
        self.setUpdatesEnabled(True)  # Pero permitir updates manuales
        
        # --- CONFIG MANAGER ---
        self.config = ConfigManager()
        
        # --- CARGA DE ASSETS ---
        base_dir = Path(__file__).parent.parent
        assets_dir = base_dir / "activos_generados"
        bg_dir = assets_dir / "obras_originales_protegidas"
        
        # Fondos
        self.bg_images = list(bg_dir.glob("*.png")) if bg_dir.exists() else []
        self.current_bg = QPixmap(str(random.choice(self.bg_images))) if self.bg_images else None
        
        # Assets HUD
        self.pix_frame = QPixmap(str(assets_dir / "hud_frame.png")) if (assets_dir / "hud_frame.png").exists() else None
        
        # Estrellas (para fondo y salvapantallas)
        self.stars = [(random.randint(0, 3000), random.randint(0, 2000), random.randint(100, 255)) for _ in range(500)]
        
        # --- VARIABLES DE ESTADO ---
        # Boot
        self.boot_lines = []
        self.boot_tasks = [
            "Initializing Quantum Kernel...",
            "Loading Neural Neural Networks...",
            "Mounting VFS (Virtual File System)...",
            "Starting Neuro-GFX Engine...",
            "Checking Security Protocols...",
            "System Ready."
        ]
        self.boot_progress = 0
        
        # Login
        self.login_user_text = ""
        self.login_pass_text = ""
        
        # Desktop
        self.user_session = None
        
        # --- UI ELEMENTS (FLOTANTES) ---
        self.init_ui_overlays()
        
        # --- TIMERS ---
        # Game loop deshabilitado (no necesario, solo repinta cuando hay eventos)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.game_loop)
        # self.timer.start(100)
        
        self.boot_timer = QTimer(self)
        self.boot_timer.timeout.connect(self.process_boot)
        self.boot_timer.start(800) # Más lento para reducir CPU

    def init_ui_overlays(self):
        """Inicializa widgets nativos que se superponen al renderizado"""
        
        # --- TOP STATUS BAR ---
        self.status_bar = SystemStatusBar(self)
        self.status_bar.setGeometry(0, 0, self.width(), 40)
        self.status_bar.hide() # Se mostrará al entrar al Desktop
        
        # Layout principal centrado
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(20) # Espacio general entre elementos

        # Contenedor para el formulario (para darle fondo semi-transparente opcional si se quiere)
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setAlignment(Qt.AlignCenter)
        
        # TÍTULO (Más arriba y separado)
        title = QLabel("NEURO-OS GENESIS")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 48px; font-weight: bold; color: cyan; letter-spacing: 5px; margin-bottom: 40px;")
        # Efecto de sombra para el título para que se lea mejor sobre estrellas
        
        form_layout.addWidget(title)
        
        # CAMPOS DE TEXTO
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("USER ID")
        self.user_input.setText("admin") # Auto-fill debug
        self.user_input.setFixedWidth(300)
        self.user_input.setStyleSheet("""
            QLineEdit { 
                padding: 15px; 
                background: rgba(0, 20, 40, 0.8); 
                border: 1px solid cyan; 
                color: white; 
                font-size: 16px; 
                border-radius: 5px;
            }
            QLineEdit:focus { border: 2px solid #00ffaa; }
        """)
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("ACCESS CODE")
        self.pass_input.setText("admin") # Auto-fill debug
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFixedWidth(300)
        self.pass_input.setStyleSheet(self.user_input.styleSheet())
        self.pass_input.returnPressed.connect(self.attempt_login) # Kept original method name
        
        form_layout.addWidget(self.user_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.pass_input)
        
        form_layout.addSpacing(40) # MÁS ESPACIO ANTES DEL BOTÓN
        
        # BOTÓN DE LOGIN
        self.btn_login = QPushButton("INICIAR SESIÓN")
        self.btn_login.setFixedWidth(300)
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.clicked.connect(self.attempt_login) # Kept original method name
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: cyan;
                color: black;
                font-weight: bold;
                font-size: 16px;
                padding: 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ccffff;
                box-shadow: 0 0 15px cyan;
            }
        """)
        
        form_layout.addWidget(self.btn_login)
        
        # Set the form_container as the central widget for the login UI
        # This replaces the old self.login_widget structure
        self.login_widget = form_container # Assign the new container to self.login_widget
        self.login_widget.setParent(self) # Make sure it's a child of NeuroMaster
        self.login_widget.setLayout(form_layout) # Set the layout for the container
        
        # The main_layout is for the QMainWindow, not for the login_widget itself.
        # The login_widget will be positioned by resizeEvent or manually.
        # For now, we just hide it.
        self.login_widget.hide() # Oculto al inicio (BOOT)

        # Contenedor para Dock Inferior (Estilo Mac)
        self.dock_panel = QWidget(self)
        self.dock_height = 80
        self.dock_width = 600
        # Centrar horizontalmente abajo
        dw = (self.width() - self.dock_width) // 2
        dh = self.height() - 100
        self.dock_panel.setGeometry(dw, dh, self.dock_width, self.dock_height)
        
        dock_layout = QHBoxLayout(self.dock_panel)
        dock_layout.setSpacing(15)
        dock_layout.setContentsMargins(20, 10, 20, 10)
        
        # Estilo del contenedor del dock (transparencia y bordes redondeados)
        self.dock_panel.setStyleSheet("""
            QWidget {
                background: rgba(20, 20, 30, 0.7);
                border: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 20px;
            }
        """)

        # Definir botones del dock (Icono + Texto)
        dock_items = [
            ("📁", "FILES", self.open_files),
            ("🌐", "NET", self.open_net),
            ("💻", "TERM", self.open_terminal),
            ("🎵", "MUSIC", self.open_music),
            ("🎨", "GFX", self.open_gfx),
            ("⚙️", "SETTINGS", self.open_settings),
            ("🔌", "OFF", self.close)
        ]
        
        for icon, name, action in dock_items:
            btn = QPushButton(icon)
            btn.setFixedSize(60, 60)
            # Estilo botón dock con efecto hover
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: white;
                    font-size: 30px;
                    border: none;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.2);
                    font-size: 40px; /* Efecto Zoom */
                    margin-bottom: 10px; /* Subir un poco */
                }
            """)
            btn.setToolTip(name)
            if action:
                btn.clicked.connect(action)
            dock_layout.addWidget(btn)
        
        self.dock_panel.hide() # Oculto al inicio

    # --- LÓGICA DE ESTADOS ---
    def process_boot(self):
        if self.current_state != STATE_BOOT: return
        
        if self.boot_progress < len(self.boot_tasks):
            self.boot_lines.append(f"[OK] {self.boot_tasks[self.boot_progress]}")
            self.boot_progress += 1
            self.update() # Forzar repintado
        else:
            self.boot_timer.stop()
            QTimer.singleShot(1000, self.switch_to_login)

    def switch_to_login(self):
        self.current_state = STATE_LOGIN
        self.center_ui(self.login_widget)
        self.login_widget.show()
        if hasattr(self, 'pass_input'): self.pass_input.setFocus()
        self.update()

    def attempt_login(self):
        u = self.user_input.text()
        p = self.pass_input.text()
        # Hardcoded seguro para demo
        if u == "admin" and p == "admin":
            self.user_session = u
            self.switch_to_desktop()
        else:
            self.pass_input.setStyleSheet("background: #300; color: white; border: 1px solid red; padding: 10px; border-radius: 5px;")

    def switch_to_desktop(self):
        self.current_state = STATE_DESKTOP
        self.login_widget.hide()
        self.dock_panel.show()
        if hasattr(self, 'status_bar'): self.status_bar.show()
        self.center_dock()
        self.update()

    # --- GAME LOOP (PAINT EVENT) ---
    def paintEvent(self, event):
        # Solo repintar si es necesario
        if not self.isVisible():
            return
            
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing, False) # Deshabilitar antialiasing para velocidad
        
        # 1. FONDO COMÚN (Estrellas / Espacio)
        self.draw_background(p)
        
        # 2. RENDER SEGÚN ESTADO
        if self.current_state == STATE_BOOT:
            self.draw_boot_screen(p)
        elif self.current_state == STATE_LOGIN:
            self.draw_login_screen(p)
        elif self.current_state == STATE_DESKTOP:
            self.draw_desktop_screen(p)

    def draw_background(self, p):
        # Cachear el fondo para no redibujarlo constantemente
        if not hasattr(self, '_cached_bg') or self._cached_bg.size() != self.size():
            self._cached_bg = QPixmap(self.size())
            bg_painter = QPainter(self._cached_bg)
            
            # Gradiente base
            grad = QLinearGradient(0, 0, 0, self.height())
            grad.setColorAt(0, QColor(2, 5, 20))
            grad.setColorAt(1, QColor(0, 0, 0))
            bg_painter.fillRect(self.rect(), grad)
            
            # Estrellas
            for x, y, b in self.stars:
                sx = int((x / 3000) * self.width())
                sy = int((y / 2000) * self.height())
                
                c = QColor(b, b, b)
                bg_painter.setPen(Qt.NoPen)
                bg_painter.setBrush(c)
                bg_painter.drawEllipse(sx, sy, 2, 2)
            
            bg_painter.end()
        
        # Dibujar el fondo cacheado
        p.drawPixmap(0, 0, self._cached_bg)

    def draw_boot_screen(self, p):
        # Texto terminal verde
        p.setFont(QFont("Consolas", 14))
        p.setPen(QColor(0, 255, 0))
        
        y = 100
        for line in self.boot_lines:
            p.drawText(50, y, line)
            y += 25
            
        # Barra de progreso
        total = len(self.boot_tasks)
        current = self.boot_progress
        width = self.width() - 100
        
        p.setPen(QColor("cyan"))
        p.drawRect(50, self.height() - 100, width, 20)
        p.fillRect(52, self.height() - 98, int((width-4) * (current/total)), 16, QColor("cyan"))

    def draw_login_screen(self, p):
        # Viñeta oscura para dar profundidad
        rad = QRadialGradient(self.width()/2, self.height()/2, self.width()*0.8)
        rad.setColorAt(0, QColor(0,0,0,0))
        rad.setColorAt(1, QColor(0,0,0,200))
        p.fillRect(self.rect(), rad)

    def draw_desktop_screen(self, p):
        # Imagen 4K de Fondo (si existe)
        if self.current_bg:
            scaled = self.current_bg.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            dx = (self.width() - scaled.width()) // 2
            dy = (self.height() - scaled.height()) // 2
            
            # Modo mezcla para que se vean estrellas detrás si la imagen tiene transparencia (o simplemente encima)
            p.drawPixmap(dx, dy, scaled)
            
        # HUD Frame Overlay (DESACTIVADO POR PREFERENCIA DE USUARIO)
        # if self.pix_frame:
        #     frame_scaled = self.pix_frame.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        #     p.setCompositionMode(QPainter.CompositionMode_Screen)
        #     p.drawPixmap(0, 0, frame_scaled)
        #     p.setCompositionMode(QPainter.CompositionMode_SourceOver) # Reset

        # Info Usuario
        p.setPen(QColor("cyan"))
        p.setFont(QFont("Arial", 12))
        p.drawText(self.width() - 250, 30, f"USER: {self.user_session} | CPU: OPTIMAL")

    # --- ACCIONES DEL SISTEMA ---
    def open_files(self):
        print("📂 Abriendo Explorador de Archivos...")
        self.files_app = FileExplorerWindow(self)
        self.files_app.show()

    def open_net(self):
        print("🌐 Abriendo Navegador Integrado...")
        # Usar navegador integrado de Neuro-OS (dentro del desktop)
        self.browser_app = WebBrowserWindow(self)
        self.browser_app.show()
        
        # Feedback visual en Dock
        self.dock_panel.setStyleSheet("background: rgba(0, 100, 255, 0.5); border-radius: 20px;")
        QTimer.singleShot(300, lambda: self.dock_panel.setStyleSheet("background: rgba(20, 20, 30, 0.7); border: 1px solid rgba(0, 255, 255, 0.3); border-radius: 20px;"))

    def open_terminal(self):
        print("💻 Abriendo Terminal...")
        self.term_app = TerminalWindow(self)
        self.term_app.show()

    def open_music(self):
        print("🎵 Abriendo Reproductor Neural...")
        self.music_app = MusicPlayerWindow(self)
        self.music_app.show()

    def open_gfx(self):
        print("🎨 Abriendo Neuro-GFX Optimizer...")
        # Lógica visual de activación
        self.dock_panel.setStyleSheet("""
            QWidget {
                background: rgba(50, 20, 30, 0.8);
                border: 2px solid red;
                border-radius: 20px;
            }
        """)
        QTimer.singleShot(500, lambda: self.dock_panel.setStyleSheet("""
            QWidget {
                background: rgba(20, 20, 30, 0.7);
                border: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 20px;
            }
        """))
        
        # Abrir Monitor Real
        self.gfx_app = GFXOptimizerWindow(self)
        self.gfx_app.show()

    def open_settings(self):
        print("⚙️ Abriendo Configuración...")
        self.settings_app = SettingsWindow(self, self.config)
        self.settings_app.show()

    # --- UTILIDADES ---
    def game_loop(self):
        pass

    def resizeEvent(self, event):
        if hasattr(self, 'status_bar'): self.status_bar.resize(self.width(), 40)
        
        if self.current_state == STATE_LOGIN:
            self.center_ui(self.login_widget)
        elif self.current_state == STATE_DESKTOP:
            self.center_dock()
    
    def center_ui(self, widget):
        cx = (self.width() - widget.width()) // 2
        cy = (self.height() - widget.height()) // 2
        widget.move(cx, cy)

    def center_dock(self):
        # Centrar horizontalmente abajo
        dw = (self.width() - self.dock_width) // 2
        dh = self.height() - 100
        self.dock_panel.move(dw, dh)

# ============================================================
# 📦 APLICACIONES DEL SISTEMA
# ============================================================

# ============================================================
# 🎮 GFX OPTIMIZER (GAME BOOSTER & VIRTUALIZATION)
# ============================================================
class ModeCard(QFrame):
    def __init__(self, title, desc, icon="💠", recommended=False, parent=None, callback=None, mode_id=0):
        super().__init__(parent)
        self.callback = callback
        self.mode_id = mode_id
        self.setFrameShape(QFrame.StyledPanel)
        
        self.default_style = """
            QFrame { background: #111; border: 1px solid #444; border-radius: 8px; }
            QFrame:hover { border: 1px solid #666; background: #1a1a1a; }
            QLabel { color: #aaa; border: none; }
            QLabel#Title { color: #fff; font-weight: bold; font-size: 14px; }
        """
        self.rec_style = """
            QFrame { background: #002200; border: 1px solid #0F0; border-radius: 8px; }
            QLabel { color: #cfc; border: none; }
            QLabel#Title { color: #0F0; font-weight: bold; font-size: 14px; }
        """
        
        self.active_style = """
            QFrame { background: #222; border: 2px solid #00FFCC; border-radius: 8px; } 
            QLabel { color: #FFF; border: none; } 
            QLabel#Title { color: #00FFCC; font-weight: bold; font-size: 14px; }
        """
        
        if recommended:
            self.current_base_style = self.rec_style
        else:
            self.current_base_style = self.default_style
            
        self.setStyleSheet(self.current_base_style)
        
        l = QVBoxLayout()
        t = QLabel(f"{icon} {title}")
        t.setObjectName("Title")
        l.addWidget(t)
        
        d = QLabel(desc)
        d.setWordWrap(True)
        d.setStyleSheet("font-size: 11px;")
        l.addWidget(d)
        
        self.setLayout(l)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if self.callback:
            self.callback(self.mode_id)

    def set_active(self, active):
        if active:
            self.setStyleSheet(self.active_style)
        else:
            self.setStyleSheet(self.current_base_style)

class GFXOptimizerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Neuro-GFX Control Center")
        self.resize(900, 750)
        self.setStyleSheet("background: #050510; color: white; font-family: 'Segoe UI';")
        
        # Layout Principal (Contiene Tabs)
        main_layout = QVBoxLayout(self)
        
        # Header Global
        header = QLabel("NEURO-SYSTEM CONTROL")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: cyan; padding: 5px; border-bottom: 2px solid #004444;")
        main_layout.addWidget(header)
        
        # SISTEMA DE PESTAÑAS
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background: #111; color: #aaa; padding: 8px 20px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #003333; color: cyan; border-bottom: 2px solid cyan; }
            QTabBar::tab:hover { background: #222; }
        """)
        main_layout.addWidget(self.tabs)
        
        # --- TAB 1: GFX ENGINE ---
        self.tab_engine = QWidget()
        self.tabs.addTab(self.tab_engine, "🚀 GFX ENGINE")
        
        # Layout de la pestaña ENGINE (Aquí va todo lo que había antes)
        layout = QVBoxLayout(self.tab_engine) # 'layout' ahora apunta a la pestaña, no a 'self'
        
        # Monitor de Recursos (Engine Tab)
        stats_layout = QHBoxLayout()
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        self.cpu_label.setStyleSheet("color: cyan; font-weight: bold;")
        self.ram_label.setStyleSheet("color: magenta; font-weight: bold;")
        stats_layout.addWidget(self.cpu_label)
        stats_layout.addWidget(self.ram_label)
        layout.addLayout(stats_layout)
        
        # Target Selection
        target_box = QFrame()
        target_box.setStyleSheet("background: #0a0a0a; border: 1px solid #333; border-radius: 5px;")
        tb_l = QHBoxLayout(target_box)
        
        self.txt_path = QLineEdit()
        self.txt_path.setPlaceholderText("Select EXE or Paste Steam URL (steam://rungameid/...)")
        self.txt_path.setStyleSheet("background: #111; color: #00FFCC; border: none; padding: 5px;")
        tb_l.addWidget(self.txt_path)
        
        btn_sel = QPushButton("📂")
        btn_sel.setFixedSize(40, 30)
        btn_sel.setStyleSheet("background: #333; color: white; border: none;")
        btn_sel.clicked.connect(self.select_file)
        tb_l.addWidget(btn_sel)
        
        layout.addWidget(target_box)
        
        
        # MODO CARDS
        cards_layout = QHBoxLayout()
        self.cards = []
        
        c1 = ModeCard("STABILITY", "Passive Mode", "🛡️", recommended=True, callback=self.set_mode, mode_id=0)
        c2 = ModeCard("NEURO HOOK", "Direct Injection", "⚡", callback=self.set_mode, mode_id=1)
        c3 = ModeCard("STREAM", "Virtual Container", "📡", callback=self.set_mode, mode_id=2)
        
        cards_layout.addWidget(c1)
        cards_layout.addWidget(c2)
        cards_layout.addWidget(c3)
        self.cards = [c1, c2, c3]
        layout.addLayout(cards_layout)
        
        self.selected_mode = 0
        self.cards[0].set_active(True)
        
        # --- ADVANCED GRAPHICS SETTINGS ---
        settings_frame = QFrame()
        settings_frame.setStyleSheet("background: #0a0a0a; border: 1px solid #333; border-radius: 5px; margin-top: 10px;")
        sf_layout = QVBoxLayout(settings_frame)
        
        lbl_settings = QLabel("ADVANCED RENDER PARAMETERS")
        lbl_settings.setStyleSheet("color: cyan; font-weight: bold; border: none;")
        sf_layout.addWidget(lbl_settings)
        
        # Grid para controles de Upscaling
        grid = QGridLayout()
        
        # 1. Output Resolution (Lo que ves)
        grid.addWidget(QLabel("📺 Output Resolution (Display):", styleSheet="border:none; color: cyan; font-weight: bold;"), 0, 0)
        self.combo_out_res = QComboBox()
        self.combo_out_res.setEditable(True)
        self.combo_out_res.addItems(["NATIVE (Screen)", "3840x2160 (4K)", "2560x1440 (2K)", "1920x1080 (FHD)"])
        self.combo_out_res.setStyleSheet("background: #111; color: white; border: 1px solid cyan;")
        grid.addWidget(self.combo_out_res, 0, 1)

        # 2. Internal Render Resolution (A lo que procesa la GPU)
        grid.addWidget(QLabel("⚙️ Internal Render (Game Source):", styleSheet="border:none; color: #ff5555; font-weight: bold;"), 1, 0)
        self.combo_render_res = QComboBox()
        self.combo_render_res.setEditable(True)
        self.combo_render_res.addItems(["100% (Native Quality)", "75% (Balanced)", "50% (Performance)", "300x400 (Ultra Low/Pixel Art)", "Custom..."])
        self.combo_render_res.setStyleSheet("background: #220000; color: white; border: 1px solid #ff5555;")
        grid.addWidget(self.combo_render_res, 1, 1)
        
        # FPS Target
        grid.addWidget(QLabel("⏱️ Frame Rate Limit:", styleSheet="border:none; color: #aaa;"), 2, 0)
        self.combo_fps = QComboBox()
        self.combo_fps.addItems(["UNCAPPED (Max Hz)", "144 FPS", "120 FPS", "60 FPS"])
        self.combo_fps.setStyleSheet("background: #222; color: white; border: 1px solid #555;")
        grid.addWidget(self.combo_fps, 2, 1)

        sf_layout.addLayout(grid)
        
        # Sharpness & Upscaling Engine
        self.check_sharp = QCheckBox("✨ Active Neuro-Upscaling (AI Super Resolution)")
        self.check_sharp.setChecked(True)
        self.check_sharp.setStyleSheet("""
            QCheckBox { color: #00FFCC; font-weight: bold; border: none; margin-top: 10px; }
            QCheckBox::indicator { width: 15px; height: 15px; border: 1px solid cyan; }
            QCheckBox::indicator:checked { background: cyan; }
        """)
        sf_layout.addWidget(self.check_sharp)
        
        layout.addWidget(settings_frame)
        
        # --- AUTO DETECT PLATFORMS ---
        platforms_layout = QHBoxLayout()
        platforms_layout.setSpacing(10)
        
        def add_plat_btn(name, icon, path):
            if Path(path).exists() or Path(path.replace(" (x86)", "")).exists():
                btn = QPushButton(f"{icon} {name}")
                btn.setFixedHeight(30)
                btn.setStyleSheet("background: #222; border: 1px solid #555; color: #ccc;")
                btn.clicked.connect(lambda: self.launch_platform(path))
                platforms_layout.addWidget(btn)

        # Rutas comunes
        add_plat_btn("Steam", "🚂", r"C:\Program Files (x86)\Steam\steam.exe")
        add_plat_btn("Epic", "🌑", r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe")
        add_plat_btn("Battle.net", "❄️", r"C:\Program Files (x86)\Battle.net\Battle.net.exe")
        
        layout.addLayout(platforms_layout)
        
        # Terminal Log
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMaximumHeight(80)
        self.log_area.setStyleSheet("background: black; color: #00ff00; font-family: Consolas; font-size: 11px; margin-top: 10px;")
        layout.addWidget(self.log_area)
        
        # Launch Button
        self.btn_launch = QPushButton("🚀 ACTIVATE ENGINE")
        self.btn_launch.setFixedHeight(45)
        self.btn_launch.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #004444, stop:1 #002222);
                color: #00FFCC; 
                border: 1px solid #00FFCC; 
                border-radius: 5px; 
                font-weight: bold; font-size: 14px; 
            }
            QPushButton:hover { background: #006666; }
            QPushButton:pressed { background: #00FFCC; color: black; }
        """)
        self.btn_launch.clicked.connect(self.launch_engine)
        layout.addWidget(self.btn_launch)

        # DISCLAIMER
        lbl_disc = QLabel("⚠️ LEGAL DISCLAIMER: This tool is for educational & optimization purposes only. The creator serves no responsibility for bans in online games when using 'Injection' or 'Hook' modes. Use safe 'Stability' mode for online play.")
        lbl_disc.setWordWrap(True)
        lbl_disc.setAlignment(Qt.AlignCenter)
        lbl_disc.setStyleSheet("color: #777; font-size: 10px; margin-top: 5px; border-top: 1px solid #333; padding-top: 5px;")
        layout.addWidget(lbl_disc)


        
        # Psutil setup y Timer Global
        try:
            import psutil
            self.psutil = psutil
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_stats)
            self.timer.start(2000) # Actualizar cada 2s
            self.log("System Monitor: ONLINE (psutil detected)")
            
            # Auto-Start Radar Service (intervalo muy largo para bajo consumo)
            self.monitor_timer = QTimer(self)
            self.monitor_timer.timeout.connect(self.detect_running_game)
            self.monitor_timer.start(10000) # Scan every 10s - Ultra optimizado
            self.log("🛡️ BACKGROUND RADAR: Active (Low Power Mode)")
        except ImportError:
            self.log("System Monitor: OFFLINE (psutil missing)")

        # --- TAB 2: TASK MANAGER ---
        self.tab_tasks = QWidget()
        self.init_task_manager()
        self.tabs.addTab(self.tab_tasks, "📊 PROCESSES")

    # ==========================
    # TASK MANAGER LOGIC
    # ==========================
    def init_task_manager(self):
        t_layout = QVBoxLayout(self.tab_tasks)
        
        # Controls
        ctrl_layout = QHBoxLayout()
        btn_refresh = QPushButton("🔄 REFRESH LIST")
        btn_refresh.setStyleSheet("background: #222; color: white; border: 1px solid #555; padding: 5px;")
        btn_refresh.clicked.connect(self.refresh_processes)
        ctrl_layout.addWidget(btn_refresh)
        
        btn_kill = QPushButton("💀 KILL SELECTED")
        btn_kill.setStyleSheet("background: #440000; color: #ff5555; border: 1px solid #ff0000; padding: 5px; font-weight: bold;")
        btn_kill.clicked.connect(self.kill_process)
        ctrl_layout.addWidget(btn_kill)
        
        t_layout.addLayout(ctrl_layout)
        
        # Table
        self.proc_table = QTableWidget()
        self.proc_table.setColumnCount(4)
        self.proc_table.setHorizontalHeaderLabels(["PID", "NAME", "CPU %", "RAM (MB)"])
        self.proc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.proc_table.setStyleSheet("""
            QTableWidget { background: #050510; color: #00ff00; gridline-color: #333; font-family: Consolas; }
            QHeaderView::section { background: #111; color: #aaa; padding: 4px; border: 1px solid #333; }
            QTableWidget::item:selected { background: #004400; color: #fff; }
            QTableCornerButton::section { background: #111; }
        """)
        self.proc_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.proc_table.setSortingEnabled(True)
        # Ocultar grid vertical para look más limpio
        self.proc_table.setShowGrid(False)
        self.proc_table.verticalHeader().setVisible(False)
        
        t_layout.addWidget(self.proc_table)
        
        # Llenado inicial
        QTimer.singleShot(500, self.refresh_processes)

    def refresh_processes(self):
        if not hasattr(self, 'psutil'): return
        
        # Guardar scroll
        v_scroll = self.proc_table.verticalScrollBar().value()
        
        self.proc_table.setRowCount(0)
        self.proc_table.setSortingEnabled(False) # Desactivar sorting al insertar para rendimiento
        
        # Iterar procesos (Limitado a 100 para no congelar la UI si hay miles)
        procs = []
        for p in self.psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            procs.append(p)
        
        # Ordenar por uso de memoria por defecto si se quiere, o dejar tal cual
        # procs.sort(key=lambda x: x.info['memory_info'].rss, reverse=True)
        
        row = 0
        for proc in procs:
            try:
                self.proc_table.insertRow(row)
                
                # PID
                pid_item = QTableWidgetItem(str(proc.info['pid']))
                pid_item.setData(Qt.UserRole, proc.info['pid']) # Guardar PID real
                self.proc_table.setItem(row, 0, pid_item)
                
                # Name
                self.proc_table.setItem(row, 1, QTableWidgetItem(proc.info['name']))
                
                # CPU
                cpu = proc.info['cpu_percent'] or 0.0
                self.proc_table.setItem(row, 2, QTableWidgetItem(f"{cpu:.1f}"))
                
                # RAM
                mem = proc.info['memory_info'].rss / (1024 * 1024) # MB
                self.proc_table.setItem(row, 3, QTableWidgetItem(f"{mem:.1f}"))
                
                row += 1
            except (self.psutil.NoSuchProcess, self.psutil.AccessDenied):
                pass
        
        self.proc_table.setSortingEnabled(True)
        self.proc_table.verticalScrollBar().setValue(v_scroll)
    
    def kill_process(self):
        row = self.proc_table.currentRow()
        if row >= 0:
            pid_item = self.proc_table.item(row, 0)
            name_item = self.proc_table.item(row, 1)
            if pid_item:
                pid = int(pid_item.text())
                name = name_item.text()
                
                ret = QMessageBox.warning(self, "TERMINATE PROCESS", f"Are you sure you want to KILL:\n\n{name} (PID: {pid})?\n\nUnsaved data will be lost.", 
                                          QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.Yes:
                    try:
                        p = self.psutil.Process(pid)
                        p.terminate()
                        self.log(f"Process {name} terminated.")
                        QTimer.singleShot(500, self.refresh_processes)
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Could not kill process: {e}")

    # --- EXISTING METHODS ---
    def select_file(self):
        from PySide6.QtWidgets import QFileDialog
        f, _ = QFileDialog.getOpenFileName(self, "Select Executable", "C:/", "Applications (*.exe)")
        if f:
            self.txt_path.setText(f)

    def set_mode(self, mode_id):
        self.selected_mode = mode_id
        for c in self.cards:
            c.set_active(c.mode_id == mode_id)

    def update_stats(self):
        if not hasattr(self, 'psutil'): return
        cpu = self.psutil.cpu_percent()
        ram = self.psutil.virtual_memory().percent
        self.cpu_label.setText(f"CPU: {cpu}%")
        self.ram_label.setText(f"RAM: {ram}%")

    def log(self, text):
        self.log_area.append(f"> {text}")

    def set_mode(self, mode_id):
        """Cambiar modo de optimización"""
        self.selected_mode = mode_id
        mode_names = ["STABILITY", "NEURO HOOK", "STREAM"]
        self.log(f"🔧 Mode changed to: {mode_names[mode_id]}")
        
        # Actualizar visual de las tarjetas
        for i, card in enumerate(self.cards):
            card.set_active(i == mode_id)

    def launch_platform(self, path):
        self.txt_path.setText(path)
        self.log(f"Platform Selected: {Path(path).name}")
        self.launch_engine()

    def start_radar(self):
        self.log("📡 RADAR ACTIVE: Scanning for game process window...")
        self.btn_launch.setText("⏳ SCANNING TARGET...")
        self.btn_launch.setStyleSheet("background: #444400; color: #ff0; border: 1px solid #ff0;")
        
        self.search_retries = 0
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.detect_running_game)
        self.monitor_timer.start(2000) # Check every 2s

    def detect_running_game(self):
        """Servicio constante de detección y optimización de juegos"""
        if not hasattr(self, 'psutil'): return
        if not hasattr(self, 'optimized_pids'): self.optimized_pids = set()
        
        exclude_list = ["explorer.exe", "discord.exe", "chrome.exe", "steam.exe", "python.exe", 
                       "epicgameslauncher.exe", "taskmgr.exe", "searchhost.exe", "svchost.exe", "csrss.exe", 
                       "dwm.exe", "msedge.exe", "ctfmon.exe", "nvcontainer.exe", "firefox.exe",
                       "memcompression", "msmpseng.exe", "vmmemwsl", "antimalware", 
                       "system", "registry", "smss.exe", "wininit.exe", "services.exe", "lsass.exe",
                       "winlogon.exe", "fontdrvhost.exe", "conhost.exe", "runtimebroker.exe",
                       "language_server", "omnisharp", "vscode", "code.exe"]
        
        try:
            # Buscar procesos pesados nuevos
            current_pids = set()
            for p in self.psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    pid = p.info['pid']
                    current_pids.add(pid)
                    
                    if pid in self.optimized_pids: continue # Ya optimizado
                    
                    name = p.info['name'].lower()
                    # Filtro rápido
                    if name in exclude_list: continue
                    if "service" in name or "helper" in name or "host" in name or "nvidia" in name: continue
                    
                    # Heurística: Memoria > 250MB (Juegos gordos)
                    mem_mb = p.info['memory_info'].rss / (1024 * 1024)
                    
                    is_heavy = mem_mb > 250
                    is_target = self.txt_path.text() and Path(self.txt_path.text()).name.lower() in name
                    
                    if is_heavy or is_target:
                        self.log(f"⚡ AUTO-DETECT: {p.info['name']} ({int(mem_mb)}MB)")
                        self.optimize_process(p)
                        self.optimized_pids.add(pid)
                        
                        # Actualizar botón si estábamos esperando
                        if is_target or "SCANNING" in self.btn_launch.text() or "WAITING" in self.btn_launch.text():
                             self.btn_launch.setText(f"✅ RUNNING: {p.info['name']}")
                             self.btn_launch.setStyleSheet("background: #004400; color: #0f0; border: 1px solid #0f0;")

                except (self.psutil.NoSuchProcess, self.psutil.AccessDenied):
                    continue
            
            # Limpiar PIDs muertos del set
            self.optimized_pids.intersection_update(current_pids)
                    
        except Exception: 
            pass

    def optimize_process(self, proc):
        try:
            proc.nice(self.psutil.HIGH_PRIORITY_CLASS)
            self.log(f"⚡ OPTIMIZATION APPLIED: High Priority set for {proc.name()}")
        except Exception as e:
            self.log(f"⚠️ Optimization Error: {e}")

    def launch_engine(self):
        target = self.txt_path.text().strip()
        mode_str = ["PASSIVE", "HOOK", "STREAM"][self.selected_mode]
        out_res = self.combo_out_res.currentText()
        render_res = self.combo_render_res.currentText()
        fps = self.combo_fps.currentText()
        sharp = "ON" if self.check_sharp.isChecked() else "OFF"
        
        self.log(f"Init {mode_str} | Display: {out_res} | Render: {render_res} | FPS: {fps}")
        
        # 1. Optimización del Sistema
        if hasattr(self, 'psutil'):
            try:
                p = self.psutil.Process()
                # p.nice(self.psutil.HIGH_PRIORITY_CLASS) 
                self.log("System Resources Optimized.")
            except: pass
        
        # 2. Lanzar Target
        if target:
            # Caso especial: URL de Steam
            if target.startswith("steam://"):
                 self.log(f"Launching Steam App ID: {target.split('/')[-1]}")
                 self.log("⚠️ Steam apps cannot be captured yet. Opening externally...")
                 import os
                 os.startfile(target)
                 self.log("Steam command sent. Game should start momentarily.")
                 self.start_radar()
                 return

            # Caso normal: Archivo EXE - CAPTURAR DENTRO DE NEURO-OS
            self.log("🪟 Launching in CAPTURE MODE...")
            
            # Extraer nombre de la aplicación
            app_name = Path(target).stem
            
            # Crear ventana de captura
            try:
                self.captured_app = CapturedAppWindow(target, app_name, parent=self)
                self.captured_app.show()
                self.log(f"✅ {app_name} launched in Neuro-OS Container!")
                self.log("📡 Window capture active. App will appear inside Neuro-OS.")
            except Exception as e:
                self.log(f"❌ Capture failed: {e}")
                self.log("Falling back to external launch...")
                
                # Fallback: Lanzar externamente
                import subprocess
                try:
                    subprocess.Popen([target], shell=True, cwd=str(Path(target).parent))
                    self.log("Target launched externally (not captured).")
                except Exception as e2:
                    self.log(f"CRITICAL: Could not launch target. {e2}")
                    QMessageBox.critical(self, "Launch Error", f"Could not start application:\n{e2}")
                    return

        else:
            self.log("No target selected. Running in background monitor mode.")
            
        # Activar radar para detectar el proceso del juego real (Steam lanza, juego aparece después)
        self.start_radar()

# Importar widgets adicionales necesarios para el nuevo layout
from PySide6.QtWidgets import QFileDialog, QFrame, QMessageBox, QComboBox, QCheckBox, QGridLayout

class WebBrowserWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("🌐 Neuro-Net Browser")
        self.resize(1200, 800)
        self.setStyleSheet("background: #0a0a15; color: white;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header con controles
        header = QFrame()
        header.setStyleSheet("background: #111; border-bottom: 2px solid #004444; padding: 5px;")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        # Botones de navegación
        btn_back = QPushButton("◀")
        btn_back.setFixedSize(35, 35)
        btn_back.setStyleSheet("""
            QPushButton { background: #222; color: cyan; border: 1px solid #444; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background: #333; border: 1px solid cyan; }
        """)
        btn_back.setToolTip("Atrás")
        
        btn_forward = QPushButton("▶")
        btn_forward.setFixedSize(35, 35)
        btn_forward.setStyleSheet(btn_back.styleSheet())
        btn_forward.setToolTip("Adelante")
        
        btn_reload = QPushButton("🔄")
        btn_reload.setFixedSize(35, 35)
        btn_reload.setStyleSheet(btn_back.styleSheet())
        btn_reload.setToolTip("Recargar")
        
        # Barra de URL
        self.url_bar = QLineEdit("https://www.google.com")
        self.url_bar.setStyleSheet("""
            QLineEdit { 
                padding: 8px; 
                border-radius: 5px; 
                background: #1a1a2e; 
                color: white; 
                border: 1px solid #333;
                font-size: 13px;
            }
            QLineEdit:focus { border: 1px solid cyan; }
        """)
        self.url_bar.returnPressed.connect(self.navigate)
        
        btn_go = QPushButton("IR")
        btn_go.setFixedSize(50, 35)
        btn_go.clicked.connect(self.navigate)
        btn_go.setStyleSheet("""
            QPushButton { 
                background: #00aacc; 
                color: black; 
                font-weight: bold; 
                padding: 5px 15px; 
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover { background: cyan; }
        """)
        
        header_layout.addWidget(btn_back)
        header_layout.addWidget(btn_forward)
        header_layout.addWidget(btn_reload)
        header_layout.addWidget(self.url_bar)
        header_layout.addWidget(btn_go)
        
        layout.addWidget(header)
        
        # Motor Web
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
            from PySide6.QtCore import QUrl
            
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl("https://www.google.com"))
            layout.addWidget(self.browser)
            
            # Conectar botones
            btn_back.clicked.connect(self.browser.back)
            btn_forward.clicked.connect(self.browser.forward)
            btn_reload.clicked.connect(self.browser.reload)
            
            # Actualizar URL bar cuando cambia la página
            self.browser.urlChanged.connect(lambda url: self.url_bar.setText(url.toString()))
            
            print("✅ Motor WebEngine cargado correctamente.")
            
        except ImportError:
            print("⚠️ WebEngine no encontrado. Usando modo Lite.")
            self.browser = QLabel("⚠️ Módulo QtWebEngine no instalado.\n\nPara navegar en modo completo, instala:\n\npip install PySide6-WebEngine\n\nMientras tanto, puedes usar el navegador del sistema desde el menú NEURO.")
            self.browser.setAlignment(Qt.AlignCenter)
            self.browser.setStyleSheet("color: #ff6666; font-size: 16px; padding: 40px;")
            layout.addWidget(self.browser)
            
            # Deshabilitar controles si no hay motor web
            btn_back.setEnabled(False)
            btn_forward.setEnabled(False)
            btn_reload.setEnabled(False)
            btn_go.setEnabled(False)

    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
            
        try:
            from PySide6.QtCore import QUrl
            if hasattr(self, 'browser') and hasattr(self.browser, 'setUrl'):
                self.browser.setUrl(QUrl(url))
        except:
            pass

class TerminalWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Neuro-Terminal")
        self.resize(800, 600)
        self.setStyleSheet("background: black; color: #0f0; font-family: Consolas; font-size: 14px;")
        
        layout = QVBoxLayout(self)
        
        # Area de salida (Historial)
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("border: none; background: black; color: #0f0;")
        layout.addWidget(self.output_area)
        
        # Input
        input_layout = QHBoxLayout()
        prompt = QLabel("user@neuro-os:~$")
        prompt.setStyleSheet("color: #0f0; font-weight: bold;")
        input_layout.addWidget(prompt)
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("border: none; background: black; color: #0f0;")
        self.input_line.returnPressed.connect(self.run_command)
        input_layout.addWidget(self.input_line)
        
        layout.addLayout(input_layout)
        
        # Mensaje inicial
        self.append_output("Neuro-OS Kernel v4.0. System Ready.")
        
        # Foco inicial
        self.input_line.setFocus()

    def append_output(self, text):
        self.output_area.append(text)
        self.output_area.moveCursor(self.output_area.textCursor().End)

    def run_command(self):
        cmd = self.input_line.text()
        self.append_output(f"user@neuro-os:~$ {cmd}")
        self.input_line.clear()
        
        if not cmd.strip(): return
        
        if cmd == "clear":
            self.output_area.clear()
            return
            
        if cmd == "exit":
            self.close()
            return

        # Ejecutar comando real
        try:
            # Usar subprocess para capturar salida
            import subprocess
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate()
            
            if stdout: self.append_output(stdout)
            if stderr: self.append_output(f"Error: {stderr}")
            
        except Exception as e:
            self.append_output(f"Execution Error: {str(e)}")

# Importar QTextEdit que nos faltaba
from PySide6.QtWidgets import QTextEdit

class MusicPlayerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("Neuro-Beats Media Hub")
        self.resize(550, 750)
        self.setStyleSheet("""
            QWidget { background: #050510; color: #ff00ff; font-family: 'Segoe UI'; }
            QTabWidget::pane { border: 1px solid #330033; }
            QTabBar::tab { background: #111; color: magenta; padding: 10px 20px; }
            QTabBar::tab:selected { background: #330033; color: white; border-bottom: 2px solid magenta; }
            QListWidget { background: #111; border: none; color: #ff88ff; font-size: 14px; }
            QListWidget::item { padding: 8px; }
            QListWidget::item:selected { background: #330033; color: white; }
            QLineEdit { background: #220022; color: white; border: 1px solid magenta; padding: 8px; }
            QPushButton { background: #220022; color: magenta; border: 1px solid magenta; padding: 10px; font-weight: bold; }
            QPushButton:hover { background: magenta; color: black; }
        """)
        
        main_layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("🎵 NEURO MEDIA HUB")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 22px; font-weight: bold; margin: 10px; color: magenta; letter-spacing: 2px;")
        main_layout.addWidget(header)
        
        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # --- TAB 1: LOCAL LIBRARY ---
        self.tab_local = QWidget()
        self.init_local_ui()
        self.tabs.addTab(self.tab_local, "💾 LOCAL FILES")
        
        # --- TAB 2: WEB STREAM (YOUTUBE) ---
        self.tab_web = QWidget()
        self.init_web_ui()
        self.tabs.addTab(self.tab_web, "🌐 YOUTUBE & STREAM")
        
        # Footer Controls (Global)
        footer = QFrame()
        footer.setStyleSheet("background: #111; border-top: 1px solid #333;")
        f_layout = QHBoxLayout(footer)
        
        self.lbl_status = QLabel("Ready")
        self.lbl_status.setStyleSheet("color: #888; border: none;")
        f_layout.addWidget(self.lbl_status)
        
        btn_mixer = QPushButton("🎚️ MIXER")
        btn_mixer.setFixedSize(80, 30)
        btn_mixer.setStyleSheet("font-size: 11px; padding: 5px;")
        btn_mixer.clicked.connect(lambda: os.system("sndvol"))
        f_layout.addWidget(btn_mixer)
        
        main_layout.addWidget(footer)

    def init_local_ui(self):
        layout = QVBoxLayout(self.tab_local)
        
        # Botón recargar
        btn_load = QPushButton("🔄 RESCAN USER MUSIC FOLDER")
        btn_load.clicked.connect(self.load_music)
        layout.addWidget(btn_load)
        
        # Lista
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.play_file)
        layout.addWidget(self.list_widget)
        
        self.load_music()

    def init_web_ui(self):
        layout = QVBoxLayout(self.tab_web)
        
        # YouTube Search
        layout.addWidget(QLabel("🔍 SEARCH YOUTUBE:", styleSheet="color: white; font-weight: bold; border: none;"))
        
        search_layout = QHBoxLayout()
        self.txt_yt = QLineEdit()
        self.txt_yt.setPlaceholderText("Enter song or artist name...")
        self.txt_yt.returnPressed.connect(self.search_youtube)
        search_layout.addWidget(self.txt_yt)
        
        btn_yt = QPushButton("▶ PLAY")
        btn_yt.setFixedSize(60, 40)
        btn_yt.clicked.connect(self.search_youtube)
        search_layout.addWidget(btn_yt)
        layout.addLayout(search_layout)
        
        layout.addSpacing(20)
        
        # Quick Links
        layout.addWidget(QLabel("🚀 QUICK LAUNCHERS:", styleSheet="color: white; font-weight: bold; border: none;"))
        
        q_layout = QGridLayout()
        
        def add_launcher(row, col, name, url, color):
            btn = QPushButton(name)
            btn.setStyleSheet(f"background: {color}; color: white; border: none;")
            btn.clicked.connect(lambda: self.open_url(url))
            q_layout.addWidget(btn, row, col)

        add_launcher(0, 0, "🔴 YouTube Main", "https://www.youtube.com", "#cc0000")
        add_launcher(0, 1, "🎵 YouTube Music", "https://music.youtube.com", "#cc0000")
        add_launcher(1, 0, "🟢 Spotify Web", "https://open.spotify.com", "#1db954")
        add_launcher(1, 1, "☁️ SoundCloud", "https://soundcloud.com", "#ff5500")
        
        layout.addLayout(q_layout)
        layout.addStretch()
        
        info = QLabel("💡 Tip: Searching will open your default browser directly to the video.")
        info.setWordWrap(True)
        info.setStyleSheet("color: #666; font-size: 11px; border: none; margin-top: 10px;")
        layout.addWidget(info)

    def load_music(self):
        import os
        self.list_widget.clear()
        music_dir = os.path.expanduser("~/Music")
        found = False
        if os.path.exists(music_dir):
            for root, dirs, files in os.walk(music_dir):
                for f in files:
                    if f.lower().endswith(('.mp3', '.wav', '.flac', '.m4a')):
                        item = QListWidgetItem(f)
                        item.setData(Qt.UserRole, os.path.join(root, f))
                        self.list_widget.addItem(item)
                        found = True
        
        if not found:
            self.list_widget.addItem("No files found in ~/Music folder.")

    def play_file(self, item):
        path = item.data(Qt.UserRole)
        if path:
            import os
            try:
                os.startfile(path)
                self.lbl_status.setText(f"Playing Local: {item.text()}")
            except Exception as e:
                self.lbl_status.setText(f"Error: {e}")

    def search_youtube(self):
        query = self.txt_yt.text().strip()
        if query:
            import urllib.parse
            import webbrowser
            encoded_query = urllib.parse.quote(query)
            # Truco: "duckduckgo !yt" o directo a youtube results
            url = f"https://www.youtube.com/results?search_query={encoded_query}"
            # O mejor, intentar reproducir el primer resultado (I'm feeling lucky style de YT music no es facil público)
            # Vamos directo a la búsqueda
            webbrowser.open(url)
            self.lbl_status.setText(f"Searching YT: {query}")

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        self.lbl_status.setText(f"Opening: {url}")

class SettingsWindow(QWidget):
    def __init__(self, parent=None, config_manager=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("⚙️ Neuro-Control Panel")
        self.resize(700, 600)
        self.config = config_manager
        
        self.setStyleSheet("""
            QWidget { background: #0a0a15; color: #ddd; font-family: 'Segoe UI'; }
            QLabel { color: #aaa; font-size: 12px; }
            QLabel#SectionTitle { color: cyan; font-weight: bold; font-size: 16px; margin: 10px 0; }
            QPushButton { 
                text-align: center; padding: 10px; 
                background: #1a1a2e; border: 1px solid #444; 
                margin: 5px; border-radius: 5px; font-size: 13px; color: white;
            }
            QPushButton:hover { background: #2a2a3e; border: 1px solid cyan; }
            QPushButton#SaveButton { background: #00aacc; color: black; font-weight: bold; }
            QPushButton#SaveButton:hover { background: cyan; }
            QLineEdit { background: #1a1a2e; color: white; border: 1px solid #444; padding: 8px; border-radius: 5px; }
            QLineEdit:focus { border: 1px solid cyan; }
            QComboBox { background: #1a1a2e; color: white; border: 1px solid #444; padding: 5px; }
            QCheckBox { color: #ddd; }
        """)
        
        main_layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("NEURO-OS CONFIGURATION")
        header.setObjectName("SectionTitle")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-size: 20px; color: cyan; margin-bottom: 20px;")
        main_layout.addWidget(header)
        
        # Tabs para organizar configuraciones
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background: #1a1a2e; color: #aaa; padding: 10px 20px; }
            QTabBar::tab:selected { background: #2a2a3e; color: cyan; border-bottom: 2px solid cyan; }
        """)
        
        # --- TAB 1: NEURO-OS SETTINGS ---
        tab_neuro = QWidget()
        neuro_layout = QVBoxLayout(tab_neuro)
        
        # File Explorer
        lbl_files = QLabel("📁 FILE EXPLORER")
        lbl_files.setObjectName("SectionTitle")
        neuro_layout.addWidget(lbl_files)
        
        lbl_path = QLabel("Default Path:")
        neuro_layout.addWidget(lbl_path)
        
        path_layout = QHBoxLayout()
        self.txt_file_path = QLineEdit(self.config.get("file_explorer.default_path", "~/Desktop") if self.config else "~/Desktop")
        path_layout.addWidget(self.txt_file_path)
        
        btn_browse = QPushButton("📂 Browse")
        btn_browse.clicked.connect(self.browse_folder)
        btn_browse.setFixedWidth(100)
        path_layout.addWidget(btn_browse)
        neuro_layout.addLayout(path_layout)
        
        # Browser
        neuro_layout.addSpacing(20)
        lbl_browser = QLabel("🌐 WEB BROWSER")
        lbl_browser.setObjectName("SectionTitle")
        neuro_layout.addWidget(lbl_browser)
        
        lbl_browser_pref = QLabel("Preferred Browser:")
        neuro_layout.addWidget(lbl_browser_pref)
        
        self.combo_browser = QComboBox()
        self.combo_browser.addItems(["Auto-detect", "Opera", "Chrome", "Edge", "Firefox", "Custom Path"])
        current_browser = self.config.get("browser.preferred", "auto") if self.config else "auto"
        browser_map = {"auto": 0, "opera": 1, "chrome": 2, "edge": 3, "firefox": 4, "custom": 5}
        self.combo_browser.setCurrentIndex(browser_map.get(current_browser, 0))
        neuro_layout.addWidget(self.combo_browser)
        
        lbl_custom = QLabel("Custom Browser Path (if selected above):")
        neuro_layout.addWidget(lbl_custom)
        self.txt_browser_path = QLineEdit(self.config.get("browser.custom_path", "") if self.config else "")
        self.txt_browser_path.setPlaceholderText("C:/Path/To/Browser.exe")
        neuro_layout.addWidget(self.txt_browser_path)
        
        # Performance
        neuro_layout.addSpacing(20)
        lbl_perf = QLabel("⚡ PERFORMANCE")
        lbl_perf.setObjectName("SectionTitle")
        neuro_layout.addWidget(lbl_perf)
        
        self.chk_radar = QCheckBox("Enable Background Game Radar")
        self.chk_radar.setChecked(self.config.get("performance.enable_radar", True) if self.config else True)
        neuro_layout.addWidget(self.chk_radar)
        
        neuro_layout.addStretch()
        tabs.addTab(tab_neuro, "🧠 Neuro-OS")
        
        # --- TAB 2: CUSTOM APPS ---
        tab_apps = QWidget()
        apps_layout = QVBoxLayout(tab_apps)
        
        lbl_apps_title = QLabel("🎮 CUSTOM APPLICATIONS")
        lbl_apps_title.setObjectName("SectionTitle")
        lbl_apps_title.setStyleSheet("font-size: 18px; color: cyan; margin-bottom: 10px;")
        apps_layout.addWidget(lbl_apps_title)
        
        lbl_apps_desc = QLabel("Add external applications to run inside Neuro-OS windows.\nThey will appear as icons on your desktop.")
        lbl_apps_desc.setStyleSheet("color: #888; font-size: 11px; margin-bottom: 15px;")
        apps_layout.addWidget(lbl_apps_desc)
        
        # Lista de apps
        self.apps_list = QListWidget()
        self.apps_list.setStyleSheet("""
            QListWidget { background: #1a1a2e; border: 1px solid #444; color: white; }
            QListWidget::item { padding: 8px; }
            QListWidget::item:selected { background: #2a2a3e; color: cyan; }
        """)
        
        # Cargar apps guardadas
        custom_apps = self.config.get("custom_apps", []) if self.config else []
        for app in custom_apps:
            self.apps_list.addItem(f"{app.get('icon', '📦')} {app.get('name', 'Unknown')} - {app.get('path', '')}")
        
        apps_layout.addWidget(self.apps_list)
        
        # Botones de gestión
        apps_buttons = QHBoxLayout()
        
        btn_add_app = QPushButton("➕ Add Application")
        btn_add_app.clicked.connect(self.add_custom_app)
        apps_buttons.addWidget(btn_add_app)
        
        btn_remove_app = QPushButton("➖ Remove Selected")
        btn_remove_app.clicked.connect(self.remove_custom_app)
        apps_buttons.addWidget(btn_remove_app)
        
        apps_layout.addLayout(apps_buttons)
        
        # Formulario para añadir app
        form_frame = QFrame()
        form_frame.setStyleSheet("background: #1a1a2e; border: 1px solid #444; border-radius: 5px; padding: 10px; margin-top: 10px;")
        form_layout = QVBoxLayout(form_frame)
        
        form_layout.addWidget(QLabel("App Name:"))
        self.txt_app_name = QLineEdit()
        self.txt_app_name.setPlaceholderText("e.g., Photoshop, Discord, VS Code...")
        form_layout.addWidget(self.txt_app_name)
        
        form_layout.addWidget(QLabel("Executable Path:"))
        path_layout_app = QHBoxLayout()
        self.txt_app_path = QLineEdit()
        self.txt_app_path.setPlaceholderText("C:/Path/To/App.exe")
        path_layout_app.addWidget(self.txt_app_path)
        
        btn_browse_app = QPushButton("📂")
        btn_browse_app.setFixedWidth(40)
        btn_browse_app.clicked.connect(self.browse_app_exe)
        path_layout_app.addWidget(btn_browse_app)
        form_layout.addLayout(path_layout_app)
        
        form_layout.addWidget(QLabel("Icon (emoji):"))
        self.txt_app_icon = QLineEdit()
        self.txt_app_icon.setPlaceholderText("🎨")
        self.txt_app_icon.setMaxLength(2)
        form_layout.addWidget(self.txt_app_icon)
        
        apps_layout.addWidget(form_frame)
        apps_layout.addStretch()
        
        tabs.addTab(tab_apps, "🎮 Custom Apps")
        
        # --- TAB 3: WINDOWS SETTINGS ---
        tab_windows = QWidget()
        win_layout = QGridLayout(tab_windows)
        
        win_layout.addWidget(QLabel("WINDOWS SYSTEM CONFIGURATION"), 0, 0, 1, 2)
        
        def add_setting(row, col, name, icon, cmd):
            btn = QPushButton(f"{icon}  {name}")
            btn.clicked.connect(lambda: self.run_cmd(cmd))
            win_layout.addWidget(btn, row, col)

        add_setting(1, 0, "Display & Graphics", "🖥️", "start ms-settings:display")
        add_setting(1, 1, "Sound & Audio", "🔊", "start ms-settings:sound")
        add_setting(2, 0, "Network & Internet", "🌐", "start ms-settings:network")
        add_setting(2, 1, "Bluetooth & Devices", "🦷", "start ms-settings:bluetooth")
        add_setting(3, 0, "Personalization", "🎨", "start ms-settings:personalization")
        add_setting(3, 1, "Apps & Features", "📱", "start ms-settings:appsfeatures")
        add_setting(4, 0, "Windows Update", "🔄", "start ms-settings:windowsupdate")
        add_setting(4, 1, "Task Manager", "📊", "taskmgr")
        
        win_layout.setRowStretch(5, 1)
        tabs.addTab(tab_windows, "🪟 Windows")
        
        main_layout.addWidget(tabs)
        
        # Save Button
        btn_save = QPushButton("💾 SAVE & APPLY CHANGES")
        btn_save.setObjectName("SaveButton")
        btn_save.setFixedHeight(45)
        btn_save.clicked.connect(self.save_settings)
        main_layout.addWidget(btn_save)
    
    def browse_folder(self):
        from PySide6.QtWidgets import QFileDialog
        folder = QFileDialog.getExistingDirectory(self, "Select Default Folder")
        if folder:
            self.txt_file_path.setText(folder)
    
    def browse_app_exe(self):
        from PySide6.QtWidgets import QFileDialog
        exe, _ = QFileDialog.getOpenFileName(self, "Select Application", "", "Executables (*.exe)")
        if exe:
            self.txt_app_path.setText(exe)
            # Auto-fill name if empty
            if not self.txt_app_name.text():
                from pathlib import Path
                self.txt_app_name.setText(Path(exe).stem)
    
    def add_custom_app(self):
        name = self.txt_app_name.text().strip()
        path = self.txt_app_path.text().strip()
        icon = self.txt_app_icon.text().strip() or "📦"
        
        if not name or not path:
            QMessageBox.warning(self, "Error", "Please fill in Name and Path")
            return
        
        from pathlib import Path as PathLib
        if not PathLib(path).exists():
            QMessageBox.warning(self, "Error", f"File not found:\n{path}")
            return
        
        # Añadir a la lista visual
        self.apps_list.addItem(f"{icon} {name} - {path}")
        
        # Limpiar formulario
        self.txt_app_name.clear()
        self.txt_app_path.clear()
        self.txt_app_icon.clear()
        
        QMessageBox.information(self, "Success", f"✅ {name} added!\n\nClick 'SAVE & APPLY' to persist changes.")
    
    def remove_custom_app(self):
        current = self.apps_list.currentRow()
        if current >= 0:
            item = self.apps_list.item(current)
            ret = QMessageBox.question(self, "Confirm", f"Remove:\n{item.text()}?")
            if ret == QMessageBox.Yes:
                self.apps_list.takeItem(current)
    
    def save_settings(self):
        if not self.config:
            QMessageBox.warning(self, "Error", "Config manager not available")
            return
        
        # Guardar configuraciones
        self.config.set("file_explorer.default_path", self.txt_file_path.text())
        
        browser_map = {0: "auto", 1: "opera", 2: "chrome", 3: "edge", 4: "firefox", 5: "custom"}
        self.config.set("browser.preferred", browser_map[self.combo_browser.currentIndex()])
        self.config.set("browser.custom_path", self.txt_browser_path.text())
        self.config.set("performance.enable_radar", self.chk_radar.isChecked())
        
        # Guardar custom apps
        apps_list = []
        for i in range(self.apps_list.count()):
            item_text = self.apps_list.item(i).text()
            # Parse: "icon name - path"
            parts = item_text.split(" - ", 1)
            if len(parts) == 2:
                icon_name = parts[0].strip()
                path = parts[1].strip()
                # Separar icon y name
                icon = icon_name[0] if icon_name else "📦"
                name = icon_name[2:].strip() if len(icon_name) > 2 else "App"
                apps_list.append({"name": name, "path": path, "icon": icon})
        
        self.config.set("custom_apps", apps_list)
        
        QMessageBox.information(self, "Success", "✅ Settings saved successfully!\n\nRestart Neuro-OS for changes to take full effect.")
    
    def run_cmd(self, cmd):
        import os
        os.system(cmd)

if __name__ == "__main__":
    print(">>> LANZANDO NEURO-OS MASTER EDITION...")
    app = QApplication(sys.argv)
    
    app.setFont(QFont("Segoe UI", 10))
    
    master = NeuroMaster()
    master.showFullScreen()
    
    sys.exit(app.exec())
