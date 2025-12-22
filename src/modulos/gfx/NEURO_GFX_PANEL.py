#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎛️ NEURO-GFX CONTROL PANEL
--------------------------
Interfaz de mando para seleccionar el motor de ejecución.
"""

import sys
import os
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QFileDialog, QRadioButton, QButtonGroup, QStackedWidget)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor, QPalette

class ModeCard(QFrame):
    def __init__(self, title, desc, icon="💠", recommended=False, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        if recommended:
            self.setStyleSheet("""
                QFrame { background: #002200; border: 1px solid #0F0; border-radius: 8px; }
                QLabel { color: #cfc; border: none; }
                QLabel#Title { color: #0F0; font-weight: bold; font-size: 14px; }
            """)
        else:
            self.setStyleSheet("""
                QFrame { background: #111; border: 1px solid #444; border-radius: 8px; }
                QFrame:hover { border: 1px solid #666; background: #1a1a1a; }
                QLabel { color: #aaa; border: none; }
                QLabel#Title { color: #fff; font-weight: bold; font-size: 14px; }
            """)
        
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

class GFXPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEURO-GFX | ENGINE SELECTOR")
        self.resize(500, 600)
        self.setStyleSheet("background-color: #050505; color: #EEE; font-family: 'Segoe UI', sans-serif;")
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # HEADER
        header = QLabel("NEURO-GFX ENGINE")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setStyleSheet("color: #00FFCC; margin-bottom: 5px;")
        main_layout.addWidget(header)
        
        sub = QLabel("Select Visualization Architecture")
        sub.setAlignment(Qt.AlignCenter)
        sub.setStyleSheet("color: #666; margin-bottom: 10px;")
        main_layout.addWidget(sub)
        
        # --- TARGET SELECTION ---
        target_box = QFrame()
        target_box.setStyleSheet("background: #111; border-radius: 5px;")
        tb_l = QHBoxLayout(target_box)
        
        self.lbl_path = QLabel("No Executable Selected...")
        self.lbl_path.setStyleSheet("color: #888; font-style: italic;")
        tb_l.addWidget(self.lbl_path)
        
        btn_sel = QPushButton("📂 SELECT EXE")
        btn_sel.setFixedSize(100, 30)
        btn_sel.setStyleSheet("background: #333; color: #FFF; border: none; border-radius: 4px;")
        btn_sel.clicked.connect(self.select_file)
        tb_l.addWidget(btn_sel)
        
        main_layout.addWidget(target_box)
        
        # --- MODE SELECTION ---
        self.mode_group = QButtonGroup(self)
        
        # MODE A
        self.card_a = ModeCard("STABILITY CORE", 
                             "Passive Capture (WGC/InputMapper). Best for demos, anti-cheat compatibility, and system stability.",
                             "🛡️", recommended=True)
        self.card_a.mousePressEvent = lambda e: self.set_mode(0)
        main_layout.addWidget(self.card_a)
        
        # MODE B
        self.card_b = ModeCard("NEURO HOOK (DIRECTX)", 
                             "Internal Injection (DLL). Zero latency, max performance. Requires hooking. (Experimental)",
                             "⚡")
        self.card_b.mousePressEvent = lambda e: self.set_mode(1)
        main_layout.addWidget(self.card_b)
        
        # MODE C
        self.card_c = ModeCard("QUANTUM LINK", 
                             "Local Network Streaming. Offload rendering to this PC and play on another device.",
                             "📡")
        self.card_c.mousePressEvent = lambda e: self.set_mode(2)
        main_layout.addWidget(self.card_c)
        
        self.selected_mode = 0
        
        main_layout.addStretch()
        
        # LAUNCH BUTTON
        self.btn_launch = QPushButton("🚀 INITIALIZE ENGINE")
        self.btn_launch.setFixedHeight(50)
        self.btn_launch.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_launch.setStyleSheet("""
            QPushButton { background: #004444; color: #00FFCC; border: 1px solid #00FFCC; border-radius: 5px; }
            QPushButton:hover { background: #006666; }
            QPushButton:pressed { background: #003333; }
        """)
        self.btn_launch.clicked.connect(self.launch_engine)
        main_layout.addWidget(self.btn_launch)
        
        self.file_path = ""
        self.setLayout(main_layout)

    def select_file(self):
        f, _ = QFileDialog.getOpenFileName(self, "Select Game", "C:/", "Exes (*.exe)")
        if f:
            self.file_path = f
            self.lbl_path.setText(os.path.basename(f))
            self.lbl_path.setStyleSheet("color: #FFF; font-weight: bold;")

    def set_mode(self, mode):
        self.selected_mode = mode
        # Visual feedback reset
        def reset_style(card, rec=False):
            if rec: card.setStyleSheet("QFrame { background: #002200; border: 1px solid #0F0; border-radius: 8px; } QLabel { color: #cfc; border: none; } QLabel#Title { color: #0F0; font-weight: bold; font-size: 14px; }")
            else: card.setStyleSheet("QFrame { background: #111; border: 1px solid #444; border-radius: 8px; } QLabel { color: #aaa; border: none; } QLabel#Title { color: #fff; font-weight: bold; font-size: 14px; }")
            
        reset_style(self.card_a, True)
        reset_style(self.card_b)
        reset_style(self.card_c)
        
        # Highlight selected
        sel_style = "QFrame { background: #222; border: 2px solid #00FFCC; border-radius: 8px; } QLabel { color: #FFF; border: none; } QLabel#Title { color: #00FFCC; font-weight: bold; font-size: 14px; }"
        
        if mode == 0: self.card_a.setStyleSheet(sel_style)
        elif mode == 1: self.card_b.setStyleSheet(sel_style)
        elif mode == 2: self.card_c.setStyleSheet(sel_style)

    def launch_engine(self):
        # Allow launching without path to use internal "Cartridge Select"
        target = self.file_path if self.file_path else "" 
            
        import subprocess
        
        mode_str = ["PASSIVE", "HOOK", "STREAM"][self.selected_mode]
        print(f"Launching {mode_str} mode...")
        
        # Lanzar el NEURO_GFX_LAUNCHER pasando argumentos
        launcher_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "NEURO_GFX_LAUNCHER.py")
        cmd = [sys.executable, launcher_script, "--mode", mode_str]
        
        if target:
            cmd.extend(["--target", target])
        
        print(f"DEBUG: Executing -> {cmd}")
        # Usar Popen para no bloquear el panel
        try:
            subprocess.Popen(cmd, cwd=os.path.dirname(launcher_script))
        except Exception as e:
            print(f"CRITICAL LAUNCH ERROR: {e}")
            self.lbl_path.setText(f"❌ ERROR: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = GFXPanel()
    ui.show()
    sys.exit(app.exec())
