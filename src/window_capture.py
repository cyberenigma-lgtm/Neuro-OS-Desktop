#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🪟 NEURO-OS WINDOW CAPTURE
Captura ventanas de aplicaciones externas y las muestra dentro de Neuro-OS
MULTIPLATAFORMA: Windows + Linux
"""

import sys
import subprocess
import time
import platform
from pathlib import Path

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPainter, QPixmap

# Detectar sistema operativo
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"

# Imports específicos de Windows
if IS_WINDOWS:
    import ctypes
    from ctypes import wintypes

class CapturedAppWindow(QWidget):
    """
    Ventana que captura y muestra una aplicación externa dentro de Neuro-OS
    """
    def __init__(self, app_path, app_name="Application", parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle(f"🪟 {app_name} - Neuro-OS")
        self.resize(1200, 800)
        
        # ESTILO NEURO-OS CYBERPUNK
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0a0a15, stop:1 #050510);
                border: 2px solid #00d4ff;
                border-radius: 10px;
            }
        """)
        
        self.app_path = app_path
        self.app_name = app_name
        self.process = None
        self.hwnd = None
        self.captured_image = None
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # CUSTOM TITLE BAR - Estilo Neuro-OS
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1a1a2e, stop:1 #16213e);
                border: none;
                border-bottom: 2px solid #00d4ff;
                border-radius: 0px;
            }
            QPushButton {
                background: #2a2a3e;
                color: #00d4ff;
                border: 1px solid #00d4ff;
                border-radius: 5px;
                font-weight: bold;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background: #3a3a4e;
                border: 2px solid #00ffff;
                color: #00ffff;
            }
            QLabel {
                color: #00d4ff;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
        """)
        
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(15, 5, 15, 5)
        
        # Título
        title_label = QLabel(f"🪟 {app_name}")
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Botones de control
        btn_minimize = QPushButton("_")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.clicked.connect(self.showMinimized)
        title_layout.addWidget(btn_minimize)
        
        btn_maximize = QPushButton("□")
        btn_maximize.setFixedSize(30, 30)
        btn_maximize.clicked.connect(lambda: self.showMaximized() if not self.isMaximized() else self.showNormal())
        title_layout.addWidget(btn_maximize)
        
        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet("""
            QPushButton {
                background: #cc0000;
                color: white;
                border: 1px solid #ff0000;
            }
            QPushButton:hover {
                background: #ff0000;
                border: 2px solid #ff4444;
            }
        """)
        btn_close.clicked.connect(self.close)
        title_layout.addWidget(btn_close)
        
        main_layout.addWidget(title_bar)
        
        # Container para la aplicación capturada
        self.capture_container = QWidget()
        self.capture_container.setStyleSheet("""
            QWidget {
                background: #000000;
                border: 1px solid #004444;
                border-radius: 0px;
            }
        """)
        main_layout.addWidget(self.capture_container)
        
        # Status label (overlay)
        self.status_label = QLabel(f"🚀 Launching {app_name}...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: #00ffff;
                font-size: 16px;
                font-weight: bold;
                padding: 20px;
                background: rgba(10, 10, 21, 0.9);
                border: 2px solid #00d4ff;
                border-radius: 10px;
            }
        """)
        self.status_label.setParent(self.capture_container)
        self.status_label.setGeometry(300, 300, 600, 200)
        
        # Timer para capturar frames
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_frame)
        
        # Lanzar aplicación
        self.launch_app()
    
    def launch_app(self):
        """Lanzar la aplicación externa"""
        try:
            self.process = subprocess.Popen([self.app_path])
            self.status_label.setText(f"Searching for {self.app_name} window...")
            
            # Timer para buscar la ventana
            self.search_timer = QTimer(self)
            self.search_timer.timeout.connect(self.find_window)
            self.search_timer.start(500)  # Buscar cada 500ms
            
        except Exception as e:
            self.status_label.setText(f"❌ Error launching:\n{e}")
    
    def find_window(self):
        """Buscar la ventana de la aplicación por PID"""
        if not self.process:
            return
        
        if IS_WINDOWS:
            self.find_window_windows()
        elif IS_LINUX:
            self.find_window_linux()
        else:
            self.status_label.setText("❌ Platform not supported for window capture")
    
    def find_window_windows(self):
        """Buscar ventana en Windows"""
        user32 = ctypes.windll.user32
        pid = self.process.pid
        found_hwnd = None
        
        @ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        def enum_callback(hwnd, _):
            nonlocal found_hwnd
            window_pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
            
            # Verificar que sea visible y del proceso correcto
            if window_pid.value == pid and user32.IsWindowVisible(hwnd):
                # Obtener título de la ventana
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    found_hwnd = hwnd
                    return False  # Detener enumeración
            return True
        
        user32.EnumWindows(enum_callback, 0)
        
        if found_hwnd:
            self.hwnd = found_hwnd
            self.search_timer.stop()
            self.status_label.setText(f"✅ {self.app_name} captured!")
            
            # Iniciar captura de frames
            self.capture_timer.start(33)  # ~30 FPS
            
            # Ocultar status label
            QTimer.singleShot(1000, lambda: self.status_label.hide())
    
    def find_window_linux(self):
        """Buscar ventana en Linux usando xdotool"""
        try:
            # Buscar ventana por PID
            result = subprocess.run(
                ['xdotool', 'search', '--pid', str(self.process.pid)],
                capture_output=True, text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                self.hwnd = result.stdout.strip().split('\n')[0]  # Primera ventana encontrada
                self.search_timer.stop()
                self.status_label.setText(f"✅ {self.app_name} captured!")
                
                # Iniciar captura de frames
                self.capture_timer.start(33)  # ~30 FPS
                
                # Ocultar status label
                QTimer.singleShot(1000, lambda: self.status_label.hide())
        except FileNotFoundError:
            self.status_label.setText("❌ xdotool not installed. Install: sudo apt install xdotool")
            self.search_timer.stop()
    
    def capture_frame(self):
        """Capturar frame de la ventana"""
        if not self.hwnd:
            return
        
        if IS_WINDOWS:
            self.capture_frame_windows()
        elif IS_LINUX:
            self.capture_frame_linux()
    
    def capture_frame_windows(self):
        """Capturar frame en Windows usando GDI"""
        try:
            user32 = ctypes.windll.user32
            gdi32 = ctypes.windll.gdi32
            
            # Obtener dimensiones de la ventana
            rect = wintypes.RECT()
            user32.GetWindowRect(self.hwnd, ctypes.byref(rect))
            width = rect.right - rect.left
            height = rect.bottom - rect.top
            
            if width <= 0 or height <= 0:
                return
            
            # Capturar ventana
            hwnd_dc = user32.GetWindowDC(self.hwnd)
            mfc_dc = gdi32.CreateCompatibleDC(hwnd_dc)
            save_bitmap = gdi32.CreateCompatibleBitmap(hwnd_dc, width, height)
            gdi32.SelectObject(mfc_dc, save_bitmap)
            
            # Copiar contenido
            gdi32.BitBlt(mfc_dc, 0, 0, width, height, hwnd_dc, 0, 0, 0x00CC0020)  # SRCCOPY
            
            # Crear buffer para los datos de la imagen
            bmp_info = ctypes.create_string_buffer(40)
            ctypes.memmove(bmp_info, ctypes.byref(ctypes.c_int(40)), 4)  # biSize
            ctypes.memmove(ctypes.addressof(bmp_info) + 4, ctypes.byref(ctypes.c_int(width)), 4)  # biWidth
            ctypes.memmove(ctypes.addressof(bmp_info) + 8, ctypes.byref(ctypes.c_int(-height)), 4)  # biHeight (negativo = top-down)
            ctypes.memmove(ctypes.addressof(bmp_info) + 12, ctypes.byref(ctypes.c_short(1)), 2)  # biPlanes
            ctypes.memmove(ctypes.addressof(bmp_info) + 14, ctypes.byref(ctypes.c_short(32)), 2)  # biBitCount (32-bit BGRA)
            
            # Crear buffer para los píxeles
            buffer_size = width * height * 4  # 4 bytes por píxel (BGRA)
            buffer = ctypes.create_string_buffer(buffer_size)
            
            # Obtener los bits del bitmap
            gdi32.GetDIBits(mfc_dc, save_bitmap, 0, height, buffer, bmp_info, 0)  # DIB_RGB_COLORS = 0
            
            # Convertir a QImage
            self.captured_image = QImage(buffer.raw, width, height, width * 4, QImage.Format_RGB32)
            
            # Limpiar
            gdi32.DeleteObject(save_bitmap)
            gdi32.DeleteDC(mfc_dc)
            user32.ReleaseDC(self.hwnd, hwnd_dc)
            
            # Actualizar visualización
            self.update_capture_display()
            
        except Exception as e:
            print(f"Capture error (Windows): {e}")
    
    def capture_frame_linux(self):
        """Capturar frame en Linux usando import (ImageMagick)"""
        try:
            # Capturar ventana usando import de ImageMagick
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                tmp_path = tmp.name
            
            result = subprocess.run(
                ['import', '-window', str(self.hwnd), tmp_path],
                capture_output=True
            )
            
            if result.returncode == 0:
                # Cargar imagen
                self.captured_image = QImage(tmp_path)
                
                # Limpiar archivo temporal
                Path(tmp_path).unlink(missing_ok=True)
                
                # Actualizar visualización
                self.update_capture_display()
        except FileNotFoundError:
            print("ImageMagick not installed. Install: sudo apt install imagemagick")
            self.capture_timer.stop()
        except Exception as e:
            print(f"Capture error (Linux): {e}")
    
    def paintEvent(self, event):
        """Dibujar la ventana capturada"""
        # El paintEvent del container se maneja automáticamente
        # La imagen capturada se dibuja en el update del capture_frame
        pass
    
    def update_capture_display(self):
        """Actualizar la visualización de la captura"""
        if self.captured_image and self.capture_container:
            # Crear un label temporal para mostrar la imagen
            if not hasattr(self, 'image_label'):
                from PySide6.QtWidgets import QLabel
                self.image_label = QLabel(self.capture_container)
                self.image_label.setScaledContents(True)
                self.image_label.setGeometry(self.capture_container.rect())
            
            # Actualizar la imagen
            pixmap = QPixmap.fromImage(self.captured_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.setGeometry(self.capture_container.rect())
    
    def resizeEvent(self, event):
        """Reposicionar elementos al redimensionar"""
        super().resizeEvent(event)
        if hasattr(self, 'status_label') and self.status_label.isVisible():
            # Centrar status label
            w = self.capture_container.width()
            h = self.capture_container.height()
            self.status_label.setGeometry(
                (w - 600) // 2,
                (h - 200) // 2,
                600, 200
            )
        
        if hasattr(self, 'image_label'):
            self.image_label.setGeometry(self.capture_container.rect())
    
    def closeEvent(self, event):
        """Cerrar la aplicación al cerrar la ventana"""
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        event.accept()
