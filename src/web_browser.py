#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QFrame, QPushButton, QLineEdit, QLabel
)
from PySide6.QtCore import Qt

# ============================================================
# 🌐 NAVEGADOR WEB INTEGRADO
# ============================================================

class WebBrowserWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("🌐 Neuro Browser")
        self.resize(1400, 900)
        self.setStyleSheet("background: #1a1a1a; color: white;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header con controles
        header = QFrame()
        header.setStyleSheet("""
            QFrame { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #1a1a2e, stop:1 #16213e); 
                border-bottom: 2px solid #00d4ff; 
                padding: 8px;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        header_layout.setSpacing(8)
        
        # Botones de navegación con mejor diseño
        btn_style = """
            QPushButton { 
                background: #2a2a3e; 
                color: #00d4ff; 
                border: 1px solid #00d4ff; 
                border-radius: 8px; 
                font-weight: bold;
                font-size: 16px;
                padding: 5px;
            }
            QPushButton:hover { 
                background: #3a3a4e; 
                border: 2px solid #00ffff;
                color: #00ffff;
            }
            QPushButton:pressed { background: #1a1a2e; }
        """
        
        btn_back = QPushButton("◀")
        btn_back.setFixedSize(40, 40)
        btn_back.setStyleSheet(btn_style)
        btn_back.setToolTip("Atrás")
        
        btn_forward = QPushButton("▶")
        btn_forward.setFixedSize(40, 40)
        btn_forward.setStyleSheet(btn_style)
        btn_forward.setToolTip("Adelante")
        
        btn_reload = QPushButton("⟳")
        btn_reload.setFixedSize(40, 40)
        btn_reload.setStyleSheet(btn_style)
        btn_reload.setToolTip("Recargar")
        
        btn_home = QPushButton("⌂")
        btn_home.setFixedSize(40, 40)
        btn_home.setStyleSheet(btn_style)
        btn_home.setToolTip("Inicio")
        
        # Barra de URL mejorada
        self.url_bar = QLineEdit("https://www.google.com")
        self.url_bar.setStyleSheet("""
            QLineEdit { 
                padding: 12px 15px; 
                border-radius: 20px; 
                background: #0f0f1e; 
                color: white; 
                border: 2px solid #2a2a3e;
                font-size: 14px;
                selection-background-color: #00d4ff;
            }
            QLineEdit:focus { 
                border: 2px solid #00d4ff;
                background: #1a1a2e;
            }
        """)
        self.url_bar.returnPressed.connect(self.navigate)
        
        btn_go = QPushButton("IR")
        btn_go.setFixedSize(60, 40)
        btn_go.clicked.connect(self.navigate)
        btn_go.setStyleSheet("""
            QPushButton { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00aaff, stop:1 #00d4ff); 
                color: black; 
                font-weight: bold; 
                padding: 8px 20px; 
                border-radius: 20px;
                border: none;
                font-size: 13px;
            }
            QPushButton:hover { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #00d4ff, stop:1 #00ffff);
            }
            QPushButton:pressed { background: #0088cc; }
        """)
        
        header_layout.addWidget(btn_back)
        header_layout.addWidget(btn_forward)
        header_layout.addWidget(btn_reload)
        header_layout.addWidget(btn_home)
        header_layout.addWidget(self.url_bar, 1)  # Stretch
        header_layout.addWidget(btn_go)
        
        layout.addWidget(header)
        
        # Motor Web
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView
            from PySide6.QtWebEngineCore import QWebEngineSettings
            from PySide6.QtCore import QUrl
            
            self.browser = QWebEngineView()
            
            # Configurar settings para mejor experiencia
            settings = self.browser.settings()
            settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
            settings.setAttribute(QWebEngineSettings.AutoLoadImages, True)
            
            # Cargar Google
            self.browser.setUrl(QUrl("https://www.google.com"))
            layout.addWidget(self.browser)
            
            # Conectar botones
            btn_back.clicked.connect(self.browser.back)
            btn_forward.clicked.connect(self.browser.forward)
            btn_reload.clicked.connect(self.browser.reload)
            btn_home.clicked.connect(lambda: self.browser.setUrl(QUrl("https://www.google.com")))
            
            # Actualizar URL bar cuando cambia la página
            self.browser.urlChanged.connect(lambda url: self.url_bar.setText(url.toString()))
            
            print("✅ Motor WebEngine cargado correctamente.")
            
        except ImportError:
            print("⚠️ WebEngine no encontrado. Usando modo Lite.")
            self.browser = QLabel(
                "⚠️ Módulo QtWebEngine no instalado.\n\n"
                "Para navegar en modo completo, instala:\n\n"
                "pip install PySide6-WebEngine\n\n"
                "Mientras tanto, puedes usar el navegador del sistema desde el menú NEURO."
            )
            self.browser.setAlignment(Qt.AlignCenter)
            self.browser.setStyleSheet("color: #ff6666; font-size: 16px; padding: 40px;")
            layout.addWidget(self.browser)
            
            # Deshabilitar controles si no hay motor web
            btn_back.setEnabled(False)
            btn_forward.setEnabled(False)
            btn_reload.setEnabled(False)
            btn_go.setEnabled(False)
            btn_home.setEnabled(False)
    
    def navigate(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "https://" + url
        try:
            from PySide6.QtCore import QUrl
            self.browser.setUrl(QUrl(url))
        except:
            pass


# ============================================================
# 🚀 MAIN
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NeuroMaster()
    window.showFullScreen()
    sys.exit(app.exec())
