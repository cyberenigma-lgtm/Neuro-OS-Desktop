#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 NEURO-GFX NATIVE MODULE
Módulo de integración para el motor gráfico y virtualización de ventanas.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QFileDialog, QButtonGroup, QMessageBox
)
from PySide6.QtCore import Qt, QProcess
from PySide6.QtGui import QFont

# Intentar importar lógica original si se desea, o reimplementar la UI
# Aquí reimplemento la UI para asegurar integración perfecta sin dependencias raras

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

class NeuroGFXPanel(QMainWindow):
    def __init__(self, parent=None, stand_alone=False):
        super().__init__(parent)
        self.stand_alone = stand_alone
        self.setWindowTitle("Neuro-GFX Control Center")
        if stand_alone:
            self.resize(500, 650)
            
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header = QLabel("NEURO-GFX ENGINE")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("color: #00FFCC; letter-spacing: 2px;")
        layout.addWidget(header)
        
        sub = QLabel("Advanced Window Virtualization Arch.")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #666; font-style: italic;")
        layout.addWidget(sub)
        
        # Target Selection
        target_box = QFrame()
        target_box.setStyleSheet("background: #0a0a0a; border: 1px solid #333; border-radius: 5px;")
        tb_l = QHBoxLayout(target_box)
        
        self.lbl_path = QLabel("Select Target Application...")
        self.lbl_path.setStyleSheet("color: #888;")
        tb_l.addWidget(self.lbl_path)
        
        btn_sel = QPushButton("📂 TARGET")
        btn_sel.setFixedSize(80, 25)
        btn_sel.setStyleSheet("background: #333; color: white; border: none;")
        btn_sel.clicked.connect(self.select_file)
        tb_l.addWidget(btn_sel)
        
        layout.addWidget(target_box)
        
        # Modes
        self.cards = []
        
        c1 = ModeCard("STABILITY CORE", 
                     "Passive Capture (WGC). Max compatibility. Safe for Anti-Cheats.", 
                     "🛡️", recommended=True, callback=self.set_mode, mode_id=0)
        layout.addWidget(c1)
        self.cards.append(c1)
        
        c2 = ModeCard("NEURO HOOK (DX)", 
                     "Direct Injection. Zero Latency. High Performance.", 
                     "⚡", callback=self.set_mode, mode_id=1)
        layout.addWidget(c2)
        self.cards.append(c2)
        
        c3 = ModeCard("QUANTUM LINK", 
                     "Network Stream Offloading. Render remotely.", 
                     "📡", callback=self.set_mode, mode_id=2)
        layout.addWidget(c3)
        self.cards.append(c3)
        
        self.selected_mode = 0
        self.cards[0].set_active(True)
        
        layout.addStretch()
        
        # Launch
        self.btn_launch = QPushButton("🚀 ACTIVATE ENGINE")
        self.btn_launch.setFixedHeight(50)
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
        
        self.file_path = ""
        self.process = None
        
        self.setStyleSheet("background: #050505; color: white; font-family: 'Segoe UI';")

    def select_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Executable", "C:/", "Applications (*.exe)")
        if f:
            self.file_path = f
            self.lbl_path.setText(Path(f).name)
            self.lbl_path.setStyleSheet("color: #00FFCC; font-weight: bold;")

    def set_mode(self, mode_id):
        self.selected_mode = mode_id
        for c in self.cards:
            c.set_active(c.mode_id == mode_id)

    def launch_engine(self):
        import subprocess
        
        mode_str = ["PASSIVE", "HOOK", "STREAM"][self.selected_mode]
        print(f"GFX: Launching {mode_str} mode...")
        
        # Ruta al Launcher Original que movimos a src/modulos/gfx
        base_dir = Path(__file__).parent / "modulos" / "gfx"
        launcher_script = base_dir / "NEURO_GFX_LAUNCHER.py"
        
        if not launcher_script.exists():
            QMessageBox.critical(self, "Error", f"Launcher not found at:\n{launcher_script}")
            return
            
        cmd = [sys.executable, str(launcher_script), "--mode", mode_str]
        if self.file_path:
            cmd.extend(["--target", self.file_path])
            
        try:
            # Lanzar proceso desacoplado
            subprocess.Popen(cmd, cwd=str(base_dir))
            
            if not self.stand_alone:
                # Feedback visual en el SO
                pass 
                
            QMessageBox.information(self, "Engine Started", f"Neuro-GFX running in {mode_str} mode.\nOutput routed to Virtual Display.")
            
        except Exception as e:
            QMessageBox.critical(self, "Launch Error", str(e))

if __name__ == "__main__":
    print("🎮 NEURO-GFX CONTROL CENTER (STANDALONE)")
    app = QApplication(sys.argv)
    win = NeuroGFXPanel(stand_alone=True)
    win.show()
    sys.exit(app.exec())
