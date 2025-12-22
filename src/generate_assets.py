#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Assets para Neuro-OS
Crea los archivos PNG faltantes programáticamente
"""

import sys
import random
import math
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QPixmap, QColor, QPen, QRadialGradient, QLinearGradient
from PySide6.QtCore import Qt, QPointF

def create_hud_gauge(size=200):
    """Crea un gauge circular para el HUD"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    center = size / 2
    radius = size / 2 - 10
    
    # Círculo exterior
    pen = QPen(QColor("#00FFFF"), 3)
    painter.setPen(pen)
    painter.drawEllipse(int(center - radius), int(center - radius), 
                       int(radius * 2), int(radius * 2))
    
    # Marcas de tick
    for i in range(0, 360, 30):
        angle_rad = math.radians(i)
        x1 = center + (radius - 10) * math.cos(angle_rad)
        y1 = center + (radius - 10) * math.sin(angle_rad)
        x2 = center + radius * math.cos(angle_rad)
        y2 = center + radius * math.sin(angle_rad)
        painter.drawLine(int(x1), int(y1), int(x2), int(y2))
    
    # Círculo interior
    inner_radius = radius * 0.7
    pen.setWidth(2)
    painter.setPen(pen)
    painter.drawEllipse(int(center - inner_radius), int(center - inner_radius),
                       int(inner_radius * 2), int(inner_radius * 2))
    
    painter.end()
    return pixmap

def create_cosmic_background(width=1920, height=1080, seed=0):
    """Crea un fondo cósmico con estrellas y nebulosa"""
    random.seed(seed)
    pixmap = QPixmap(width, height)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Gradiente de fondo (espacio profundo)
    gradient = QLinearGradient(0, 0, 0, height)
    gradient.setColorAt(0, QColor(5, 10, 30))
    gradient.setColorAt(0.3, QColor(10, 5, 40))
    gradient.setColorAt(0.7, QColor(20, 10, 50))
    gradient.setColorAt(1, QColor(5, 5, 20))
    painter.fillRect(0, 0, width, height, gradient)
    
    # Nebulosas (manchas de color)
    for _ in range(5):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.randint(200, 500)
        
        nebula_gradient = QRadialGradient(QPointF(x, y), radius)
        
        # Colores aleatorios de nebulosa
        colors = [
            (QColor(100, 50, 150, 30), QColor(50, 20, 80, 0)),
            (QColor(50, 100, 200, 30), QColor(20, 50, 100, 0)),
            (QColor(150, 50, 100, 30), QColor(80, 20, 50, 0)),
        ]
        color_pair = random.choice(colors)
        
        nebula_gradient.setColorAt(0, color_pair[0])
        nebula_gradient.setColorAt(1, color_pair[1])
        painter.fillRect(0, 0, width, height, nebula_gradient)
    
    # Estrellas
    painter.setPen(Qt.NoPen)
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        brightness = random.randint(150, 255)
        size = random.choice([1, 1, 1, 2, 2, 3])  # Mayoría pequeñas
        
        color = QColor(brightness, brightness, brightness)
        painter.setBrush(color)
        painter.drawEllipse(x, y, size, size)
    
    # Estrellas brillantes (con glow)
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        
        glow = QRadialGradient(QPointF(x, y), 10)
        glow.setColorAt(0, QColor(255, 255, 255, 200))
        glow.setColorAt(0.5, QColor(200, 220, 255, 100))
        glow.setColorAt(1, QColor(100, 150, 255, 0))
        painter.setBrush(glow)
        painter.drawEllipse(x - 10, y - 10, 20, 20)
    
    painter.end()
    return pixmap

if __name__ == "__main__":
    print("🎨 Generando assets para Neuro-OS...")
    
    app = QApplication(sys.argv)
    
    # Crear directorios
    base_dir = Path(__file__).parent.parent
    assets_dir = base_dir / "activos_generados"
    cosmic_dir = assets_dir / "obras_originales_protegidas"
    
    assets_dir.mkdir(exist_ok=True)
    cosmic_dir.mkdir(exist_ok=True)
    
    # Generar HUD Gauge
    print("📊 Generando hud_gauge.png...")
    gauge = create_hud_gauge(200)
    gauge.save(str(assets_dir / "hud_gauge.png"))
    print("✅ hud_gauge.png creado")
    
    # Generar fondos cósmicos
    for i in range(5):
        print(f"🌌 Generando fondo cósmico {i+1}/5...")
        cosmic = create_cosmic_background(1920, 1080, seed=i)
        cosmic.save(str(cosmic_dir / f"cosmic_bg_{i+1}.png"))
        print(f"✅ cosmic_bg_{i+1}.png creado")
    
    print("\n✨ ¡Todos los assets generados exitosamente!")
    print(f"📁 Ubicación: {assets_dir}")
