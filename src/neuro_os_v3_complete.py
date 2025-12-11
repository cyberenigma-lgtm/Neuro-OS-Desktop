#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NEURO-OS GENESIS V27 (INTEGRATED LAYERS + SMART TRAY)
========================================================
- Arquitectura Jerárquica: MDI incrustado en el Fondo (Garantiza visibilidad).
- Smart Tray Icons: Tooltips dinámicos y Menús Contextuales (Click Derecho).
- Fix definitivo para ventanas invisibles.

Autor: Engineering Team
"""

import sys
import os
import random
import datetime
from pathlib import Path
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEB_ENABLED = True
except ImportError:
    WEB_ENABLED = False

MAX_WINDOWS = 10

# ============================================================
# 📶 SMART TRAY ICON (Iconos Inteligentes V28)
# ============================================================
class NeuroTrayIcon(QPushButton):
    def __init__(self, icon, category, main_window):
        super().__init__(icon, main_window)
        self.category = category
        self.main_win = main_window # Referencia al Kernel
        self.setFixedSize(40, 30)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton { border: none; color: cyan; font-size: 16px; background: transparent; }
            QPushButton:hover { color: white; background: rgba(0, 255, 255, 0.2); border-radius: 5px; }
        """)
        self.update_tooltip()

    def update_tooltip(self):
        if self.category == "WIFI": self.setToolTip("Network: NEURO-LINK_5G\nSignal: 98%")
        elif self.category == "BT": self.setToolTip("Bluetooth: ON\nDevices: 1 Connected")
        elif self.category == "VOL": self.setToolTip("Volume: 80%")
        elif self.category == "PC": self.setToolTip("System: HEALTHY")

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background: rgba(10, 20, 30, 0.98); color: cyan; border: 1px solid cyan; } QMenu::item:selected { background: rgba(0,255,255,0.3); }")
        
        if self.category == "WIFI":
            menu.addAction("📶 Neuro-Link_5G (Active)")
            menu.addSeparator()
            a1 = menu.addAction("🛠️ Network Settings"); a1.triggered.connect(lambda: self.main_win.open_settings("NETWORK"))
            a2 = menu.addAction("🚀 Speed Test"); a2.triggered.connect(lambda: self.main_win.open_app("SPEEDTEST"))
            
        elif self.category == "BT":
            menu.addAction("🎧 Headset V2")
            menu.addSeparator()
            a1 = menu.addAction("⚙️ Bluetooth Settings"); a1.triggered.connect(lambda: self.main_win.open_settings("BLUETOOTH"))
            
        elif self.category == "VOL":
            menu.addAction("🔈 Mute")
            a1 = menu.addAction("🎚️ Audio Mixer"); a1.triggered.connect(lambda: self.main_win.open_settings("AUDIO"))

        menu.exec(event.globalPos())

# ============================================================
# ⚓ SMART DOCK BUTTON (Con lógica de Instancia)
# ============================================================
class NeuroDockBtn(QPushButton):
    def __init__(self, icon, app_id, main_window):
        super().__init__(icon, main_window)
        self.app_id = app_id
        self.main_win = main_window
        self.setFixedSize(90, 90)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.on_click)
        self.setStyleSheet("""
            QPushButton { background: rgba(0,25,40,0.8); border: 2px solid cyan; border-radius: 15px; color: cyan; font-weight: bold; }
            QPushButton:hover { background: rgba(0,255,255,0.2); margin-top: -5px; color: white; }
        """)

    def on_click(self):
        # Lógica: Si ya existe, traer al frente. Si no, abrir.
        self.main_win.launch_app_smart(self.app_id)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background: rgba(10, 20, 30, 0.98); color: white; border: 1px solid cyan; }")
        
        a1 = menu.addAction(f"📄 New Window")
        a1.triggered.connect(lambda: self.main_win.launch_app_smart(self.app_id, force_new=True))
        
        a2 = menu.addAction("❌ Close All")
        a2.triggered.connect(lambda: self.main_win.close_app_family(self.app_id))
        
        menu.exec(event.globalPos())

# ============================================================
# 🌌 FONDO CÓSMICO (CARRUSEL 4K)
# ============================================================
class StarFieldContainer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_files = []
        self.current_image = None
        self.load_backgrounds()
        
        # Timer de Rotación
        self.bg_timer = QTimer(self)
        self.bg_timer.timeout.connect(self.next_background)
        self.bg_timer.start(60000) # Cambiar cada 60 segundos
        
        # --- CAPA VENTANAS (HIJA DEL FONDO) ---
        self.mdi_area = QMdiArea(self)
        self.mdi_area.setStyleSheet("background: transparent; border: none;")
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def load_backgrounds(self):
        # Ruta detectada
        base_path = Path(r"c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis\activos_generados\obras_originales_protegidas")
        if base_path.exists():
            self.image_files = list(base_path.glob("*.png"))
            
        if not self.image_files:
            print("⚠️ NO SE ENCONTRARON FONDOS CÓSMICOS. USANDO BACKUP.")
            self.current_image = None
        else:
            self.next_background()

    def next_background(self):
        if not self.image_files: return
        img_path = random.choice(self.image_files)
        # Cargar Pixmap Escalado
        try:
            full_pix = QPixmap(str(img_path))
            if not full_pix.isNull():
                self.current_image = full_pix
                self.update() # Forzar repintado
        except Exception as e:
            print(f"Error cargando fondo: {e}")

    def paintEvent(self, event):
        p = QPainter(self)
        # 1. Fondo Negro Base
        p.fillRect(self.rect(), QColor(0, 0, 0))
        
        # 2. Imagen 4K Escalada (AspectFill)
        if self.current_image:
            scaled = self.current_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            # Centrar la imagen
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            p.drawPixmap(x, y, scaled)
            
            # 3. Vinetu Oscuro (Para leer mejor el texto)
            grad = QRadialGradient(self.width()/2, self.height()/2, self.width()*0.8)
            grad.setColorAt(0, QColor(0,0,0,0))
            grad.setColorAt(1, QColor(0,10,20,180)) # Bordes oscuros
            p.fillRect(self.rect(), grad)
        else:
            # Fallback Estrellas simple si no hay imagenes
            p.setPen(Qt.white)
            for _ in range(100):
                p.drawPoint(random.randint(0, self.width()), random.randint(0, self.height()))

    def resizeEvent(self, event):
        self.mdi_area.setGeometry(self.rect())
        super().resizeEvent(event)

# ============================================================
# � HUD OVERLAY WIDGET (FUSIÓN INTELIGENTE)
# ============================================================
class HudOverlayWidget(QWidget):
    def __init__(self, parent=None, pixmap=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.setAttribute(Qt.WA_TransparentForMouseEvents) # Clicks pasan a través
        self.setAttribute(Qt.WA_NoSystemBackground) # Sin fondo opaco

    def setPixmap(self, pix):
        self.pixmap = pix
        self.update()

    def paintEvent(self, event):
        if not self.pixmap: return
        p = QPainter(self)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        # ESTA ES LA CLAVE: Modo SCREEN (Negro -> Transparente, Luz -> Brilla)
        p.setCompositionMode(QPainter.CompositionMode_Screen) 
        scaled = self.pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        p.drawPixmap(0, 0, scaled)

# ============================================================
# �🛸 CLASE PRINCIPAL: NEURO-COCKPIT V31 (FIX TRANSPARENCIA)
# ============================================================
class NeuroCockpit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neuro-OS Genesis Elite")
        self.app_registry = {} 
        
        # --- MOTOR GRÁFICO (CAPA 0) ---
        self.engine = StarFieldContainer()
        self.setCentralWidget(self.engine)
        self.mdi = self.engine.mdi_area
        
        # Cargar Assets
        assets = Path(r"c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis\activos_generados")
        self.pix_frame = QPixmap(str(assets / "hud_frame.png"))
        self.pix_gauge = QPixmap(str(assets / "hud_gauge.png"))
        
        # --- UI LAYERS ---
        self.init_hud_overlay()   # Capa 1: HUD (Blending)
        self.init_side_panel()    # Capa 2: Botones
        self.init_gauges()        # Capa 3: Gauges

        # Timer Sensores
        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_sensors_visuals)
        self.stats_timer.start(500)

    def init_hud_overlay(self):
        # Usamos el Widget de Fusión en lugar de QLabel
        self.hud_frame = HudOverlayWidget(self, self.pix_frame)
        self.hud_frame.show()

    def init_side_panel(self):
        self.dock_buttons = []
        btns_def = [
            ("📁 FILES", "FILES"), 
            ("🌐 NET", "NET"), 
            ("💻 TERM", "TERM"), 
            ("⊞ GRID", "GRID")
        ]
        
        base_y = 250
        for i, (txt, app_id) in enumerate(btns_def):
            btn = NeuroDockBtn(txt, app_id, self)
            btn.setFixedSize(140, 50)
            # Estilo Rainmeter Integrado
            btn.setStyleSheet("""
                QPushButton { 
                    background: rgba(0, 30, 60, 0.4); 
                    border-left: 3px solid #00FFFF; 
                    border-right: 1px solid rgba(0,255,255,0.1);
                    color: #00FFFF; font-family: 'Segoe UI'; font-weight: 600; font-size: 13px; text-align: left; padding-left: 20px;
                }
                QPushButton:hover { 
                    background: rgba(0, 255, 255, 0.15); 
                    border-left: 3px solid white; 
                    padding-left: 30px;
                    color: white;
                }
            """)
            btn.move(30, base_y + (i * 70))
            btn.show()
            self.dock_buttons.append(btn)
        
        self.btn_exit = QPushButton("🔌 SHUTDOWN", self)
        self.btn_exit.setFixedSize(140, 40)
        self.btn_exit.clicked.connect(self.close)
        self.btn_exit.setStyleSheet("background: rgba(0,0,0,0.5); color: #FF3333; border: 1px solid #FF3333; font-weight: bold;")
        self.btn_exit.show()

    def init_gauges(self):
        # Gauge CPU con mezcla también
        self.gauge_widget = HudOverlayWidget(self, self.pix_gauge)
        self.gauge_widget.setFixedSize(200, 200)
        self.gauge_widget.show()
        
        self.lbl_cpu_val = QLabel("0%", self.gauge_widget)
        self.lbl_cpu_val.setStyleSheet("color: white; font-size: 22px; font-weight: bold; background: transparent;")
        self.lbl_cpu_val.setAlignment(Qt.AlignCenter)
        self.lbl_cpu_val.resize(200, 200)

    def update_sensors_visuals(self):
        cpu = 0
        if PSUTIL_ENABLED: cpu = psutil.cpu_percent()
        
        transform = QTransform().rotate(cpu * 2.7) # Más dramático
        if not self.pix_gauge.isNull():
            rotated = self.pix_gauge.transformed(transform, Qt.SmoothTransformation)
            self.gauge_widget.setPixmap(rotated)
        self.lbl_cpu_val.setText(f"{int(cpu)}%")

    def resizeEvent(self, event):
        w, h = self.width(), self.height()
        
        # HUD Frame (Full Screen Overlay)
        self.hud_frame.resize(w, h)
        self.hud_frame.raise_()
        
        # CPU Gauge (Derecha)
        self.gauge_widget.move(w - 250, h//2 - 100)
        self.gauge_widget.raise_()
        
        # Botones (Top Z)
        for btn in self.dock_buttons: btn.raise_()
        self.btn_exit.move(30, h - 80); self.btn_exit.raise_()
        
        super().resizeEvent(event)

    # --- WINDOW MANAGER (Controls) ---
    def create_window(self, title, widget):
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setWindowTitle(title)
        sub.setWindowFlags(Qt.SubWindow | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        
        # Styling de Ventana
        sub.setStyleSheet("""
            QMdiSubWindow { background-color: rgba(5,8,10,0.95); border: 1px solid #00FFFF; }
            QMdiSubWindow::title { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #002244, stop:1 #000000); color: cyan; font-weight: bold; height: 28px; }
            QMdiSubWindow::close-button { subcontrol-position: top right; margin: 2px; }
        """)
        
        self.mdi.addSubWindow(sub)
        sub.resize(800, 600)
        sub.show()
        sub.raise_()
        sub.activateWindow()
        
        # Animación entrada simple (Centrar)
        c_x = (self.width() - sub.width()) // 2
        c_y = (self.height() - sub.height()) // 2
        sub.move(c_x, c_y)

    def open_files(self): self.create_window("FILES", AdvancedFileExplorer(r"c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis", self))
    def open_web(self): 
        if WEB_ENABLED: w = QWebEngineView(); w.load(QUrl("https://google.com")); self.create_window("EXTRANET BROWSER", w)
    def open_terminal(self): self.create_window("NEURO COMMAND LINE", NeuroTerminalWidget())
    def tile_windows(self): self.mdi.tileSubWindows()

    # --- ACTIONS --- (Mantener lógica previa)
    def launch_app_smart(self, app_id, force_new=False):
        if app_id == "GRID":
            self.mdi.tileSubWindows()
            return
        
        # Lógica Single Instance
        if not force_new and app_id in self.app_registry and self.app_registry[app_id]:
            win = self.app_registry[app_id][-1]
            try:
                if not win.isVisible(): win.showNormal() # Si estaba minimizada
                win.raise_()
                win.activateWindow()
                return
            except: self.app_registry[app_id].pop()

        widget = None
        title = app_id
        if app_id == "FILES": widget = AdvancedFileExplorer(r"c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis", self)
        elif app_id == "NET": 
            if WEB_ENABLED: widget = QWebEngineView(); widget.load(QUrl("https://google.com"))
        elif app_id == "TERM": widget = NeuroTerminalWidget()
        
        if widget:
            win = self.create_window(title, widget)
            if app_id not in self.app_registry: self.app_registry[app_id] = []
            self.app_registry[app_id].append(win)

    def close_app_family(self, app_id):
        if app_id in self.app_registry:
            for win in self.app_registry[app_id]:
                try: win.close()
                except: pass
            self.app_registry[app_id] = []

    def open_settings(self, category):
        # Placeholder para configuraciones
        self.create_window(f"{category} CONFIG", QLabel(f"SETTINGS for {category}")) # TO-DO: Implementar real


# --- APPS (Dependencias) ---
class NeuroTerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        l = QVBoxLayout(self); l.setContentsMargins(0,0,0,0)
        tabs = QTabWidget()
        tabs.addTab(ConsolePage("WIN", "powershell.exe /c"), "WIN")
        tabs.addTab(ConsolePage("LNX", "wsl.exe"), "LNX")
        l.addWidget(tabs)
        self.tabs = tabs # Exponer tabs para SandboxGatekeeper

class ConsolePage(QWidget):
    def __init__(self, n, p):
        super().__init__()
        self.p=p; l=QVBoxLayout(self)
        self.o=QTextEdit(); self.o.setReadOnly(True); self.o.setStyleSheet("background:black; color:lime; font-family:Consolas; border:none;")
        self.o.append(f"{n} CORE READY."); l.addWidget(self.o)
        self.i=QLineEdit(); self.i.setStyleSheet("background:#111; color:white; border:1px solid #333;"); self.i.returnPressed.connect(self.r); l.addWidget(self.i)
        self.out = self.o 
    
    def r(self):
        c=self.i.text(); self.o.append(f"> {c}"); self.i.clear(); 
        if c: 
            import subprocess
            try: subprocess.Popen(f"{self.p} {c}", shell=True) 
            except: pass

    def run_external(self, cmd):
        # API Pública para que el Gatekeeper inyecte comandos
        self.o.append(f"⚡ INJECTING KERNEL CALL: {cmd}")
        import subprocess
        try: subprocess.Popen(cmd, shell=True)
        except Exception as e: self.o.append(f"KERNEL PANIC: {e}")

# ============================================================
# 🛡️ NEURO-GATEKEEPER (REAL SANDBOX ENGINE)
# ============================================================
class SandboxGatekeeper:
    @staticmethod
    def execute(filepath, cockroach_ref):
        path = Path(filepath)
        ext = path.suffix.lower()
        
        print(f"🛡️ GATEKEEPER REAL EXEC: {path.name} [{ext}]")
        
        if ext in [".exe", ".msi", ".bat", ".cmd"]:
            SandboxGatekeeper.launch_win_container(path, cockroach_ref)
        elif ext in [".apk"]:
            SandboxGatekeeper.launch_android_container(path, cockroach_ref)
        elif ext in [".deb", ".sh", ".rpm", ".bin"]:
            SandboxGatekeeper.launch_linux_container(path, cockroach_ref)
        elif ext in [".py", ".c", ".cpp", ".js", ".html", ".css", ".json", ".md", ".txt"]:
            SandboxGatekeeper.launch_editor(path, cockroach_ref)
        elif ext in [".png", ".jpg", ".jpeg", ".gif"]:
            SandboxGatekeeper.launch_image_viewer(path, cockroach_ref)
        else:
            QMessageBox.warning(cockroach_ref, "Unknown Type", f"Extensions {ext} not supported by any active Sandbox.")

    @staticmethod
    def launch_win_container(path, ctx):
        # 1. Intentar Windows Sandbox (.wsb) para aislamiento total
        try:
            wsb_content = f"""
<Configuration>
  <VGpu>Enable</VGpu>
  <Networking>Enable</Networking>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>{path.parent}</HostFolder>
      <SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Desktop\\Injected</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>C:\\Users\\WDAGUtilityAccount\\Desktop\\Injected\\{path.name}</Command>
  </LogonCommand>
</Configuration>
            """
            wsb_file = path.with_suffix(".wsb")
            wsb_file.write_text(wsb_content)
            
            # Ejecutar Sandbox
            subprocess.Popen(["start", str(wsb_file)], shell=True)
            ctx.create_window(f"SANDBOX: {path.name}", QLabel(f"🚀 LAUNCHING WINDOWS SANDBOX...\nTarget: {path.name}\nIsolation: HIGH"))
            
        except Exception as e:
            # Fallback a ejecución local
            reply = QMessageBox.question(ctx, "Sandbox Error", "Windows Sandbox not available. Run on Host System?", QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                subprocess.Popen(str(path), shell=True)

    @staticmethod
    def launch_android_container(path, ctx):
        # Usar ADB Real
        try:
            # Check devices
            res = subprocess.check_output(["adb", "devices"], text=True)
            if "device" not in res.split("\n")[1]:
                raise Exception("No ADB Device Found")
                
            subprocess.Popen(["adb", "install", "-r", str(path)])
            ctx.create_window(f"ADB: {path.name}", QLabel(f"🤖 INSTALLING APK TO DEVICE...\n{path.name}"))
        except:
            QMessageBox.critical(ctx, "Android Error", "ADB Bridge unreachable. Please start Emulator.")

    @staticmethod
    def launch_linux_container(path, ctx):
        # Usar WSL Real
        cmd = f"wsl.exe -e {path}" if path.suffix != ".sh" else f"wsl.exe -e bash {path}"
        
        term = NeuroTerminalWidget()
        term.tabs.setCurrentIndex(1)
        term.tabs.currentWidget().run_external(cmd)
        ctx.create_window(f"WSL: {path.name}", term)

    @staticmethod
    def launch_editor(path, ctx):
        editor = NeuroCodeEditor(path)
        ctx.create_window(f"CODE: {path.name}", editor)

    @staticmethod
    def launch_image_viewer(path, ctx):
        lbl = QLabel()
        pix = QPixmap(str(path))
        if not pix.isNull():
            lbl.setPixmap(pix.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lbl.setAlignment(Qt.AlignCenter)
            ctx.create_window(f"VIEW: {path.name}", lbl)

# ... (AdvancedFileExplorer se mantiene igual) ...

class NeuroCockpit(QMainWindow):
    # ... (init methods de NeuroCockpit) ...
    # REEMPLAZAR UPDATE_SYSTEM_STATS CON MEDICIÓN REAL
    def update_system_stats(self):
        txt_parts = []
        
        # 1. CPU Real
        if PSUTIL_ENABLED:
            cpu = psutil.cpu_percent(interval=None) # No blocking
            freq = psutil.cpu_freq().current if psutil.cpu_freq() else 0
            txt_parts.append(f"CPU: {cpu}% @ {freq/1000:.1f}GHz")
            
            # 2. RAM Real
            mem = psutil.virtual_memory()
            txt_parts.append(f"RAM: {mem.percent}% ({mem.used/1024**3:.1f}/{mem.total/1024**3:.1f} GB)")
            
            # 3. Batería Real
            batt = psutil.sensors_battery()
            if batt:
                plugged = "⚡" if batt.power_plugged else "🔋"
                txt_parts.append(f"PWR: {plugged} {batt.percent}%")
            else:
                txt_parts.append("PWR: AC")
        else:
            txt_parts.append("SENSORS: OFF")

        # 4. Red Real (Ping) - Ejecutar en Hilo aparte idealmente, aquí simplificado
        # import pythonping could go here, but avoiding blocking.
        # Check connection simply by psutil
        net = "NET: ONLINE" if PSUTIL_ENABLED and psutil.net_if_stats() else "NET: OFFLINE"
        txt_parts.append(net)

        self.lbl_status.setText("  |  ".join(txt_parts))
    # ... (Rest of class) ...

# ============================================================
# 📂 ADVANCED FILE EXPLORER
# ============================================================
class AdvancedFileExplorer(QWidget):
    def __init__(self, start_path, main_window_ref):
        super().__init__()
        self.current_path = Path(start_path)
        self.main_ref = main_window_ref # Referencia para llamar al Gatekeeper
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        
        # 1. Barra de Herramientas
        tool_bar = QFrame(); tool_bar.setStyleSheet("background: #111; border-bottom: 1px solid #333;")
        tb_lay = QHBoxLayout(tool_bar)
        
        btn_up = QPushButton("⬆ UP"); btn_up.clicked.connect(self.go_up)
        btn_up.setStyleSheet("background: #222; color: cyan; padding: 5px;")
        
        self.lbl_path = QLineEdit(str(self.current_path))
        self.lbl_path.setReadOnly(True)
        self.lbl_path.setStyleSheet("background: #000; color: lime; border: 1px solid #333; padding: 5px;")
        
        tb_lay.addWidget(btn_up)
        tb_lay.addWidget(self.lbl_path)
        self.layout.addWidget(tool_bar)
        
        # 2. Tabla de Archivos
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Type", "Size"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setStyleSheet("""
            QTableWidget { background: rgba(0,0,0,0.8); color: cyan; border: none; gridline-color: #333; font-family: Segoe UI; }
            QHeaderView::section { background: #050510; color: white; padding: 5px; border: 1px solid #333; }
            QTableWidget::item:selected { background: rgba(0, 255, 255, 0.3); }
        """)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.itemDoubleClicked.connect(self.on_double_click)
        self.layout.addWidget(self.table)
        
        self.load_directory()

    def go_up(self):
        if self.current_path.parent != self.current_path:
            self.current_path = self.current_path.parent
            self.load_directory()

    def load_directory(self):
        self.lbl_path.setText(str(self.current_path))
        self.table.setRowCount(0)
        
        try:
            # Carpetas primero
            items = sorted(list(self.current_path.iterdir()), key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for f in items:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                # Icono
                icon = "📁" if f.is_dir() else "📄"
                if f.suffix in [".exe", ".msi"]: icon = "📦"
                elif f.suffix in [".py", ".c", ".js"]: icon = "🐍"
                elif f.suffix in [".png", ".jpg"]: icon = "🖼️"
                
                # Nombre
                name_item = QTableWidgetItem(f"{icon}  {f.name}")
                self.table.setItem(row, 0, name_item)
                
                # Tipo
                type_str = "DIR" if f.is_dir() else f.suffix.upper()[1:] + " File"
                self.table.setItem(row, 1, QTableWidgetItem(type_str))
                
                # Tamaño
                size_str = ""
                if f.is_file():
                    sz = f.stat().st_size
                    if sz < 1024: size_str = f"{sz} B"
                    elif sz < 1024**2: size_str = f"{sz/1024:.1f} KB"
                    else: size_str = f"{sz/1024**2:.1f} MB"
                self.table.setItem(row, 2, QTableWidgetItem(size_str))
                
                # Guardar ruta real en el item
                name_item.setData(Qt.UserRole, str(f))
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Access Denied: {e}")

    def on_double_click(self, item):
        # Obtener ruta desde la data del item (Columna 0)
        row = item.row()
        path_str = self.table.item(row, 0).data(Qt.UserRole)
        path = Path(path_str)
        
        if path.is_dir():
            self.current_path = path
            self.load_directory()
        else:
            # CLICK EN ARCHIVO -> LISTO PARA EL GATEKEEPER
            SandboxGatekeeper.execute(path, self.main_ref)

# ============================================================
# 📝 NEURO-CODE EDITOR (Simple)
# ============================================================
class NeuroCodeEditor(QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = Path(path)
        layout = QVBoxLayout(self)
        
        # Toolbar
        btn_save = QPushButton("💾 SAVE")
        btn_save.setStyleSheet("background: #003300; color: lime; border: 1px solid lime;")
        btn_save.clicked.connect(self.save_file)
        layout.addWidget(btn_save)
        
        # Edit Area
        self.editor = QTextEdit()
        self.editor.setStyleSheet("background: #0d1117; color: #c9d1d9; font-family: Consolas; font-size: 13px;")
        try:
            content = self.path.read_text(encoding='utf-8', errors='ignore')
            self.editor.setPlainText(content)
        except:
            self.editor.setPlainText("# Error reading file")
            
        layout.addWidget(self.editor)

    def save_file(self):
        try:
            self.path.write_text(self.editor.toPlainText(), encoding='utf-8')
            QMessageBox.information(self, "Saved", f"File {self.path.name} overwritten successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    win = NeuroCockpit()
    win.showFullScreen()
    sys.exit(app.exec())
