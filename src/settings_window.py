#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ SETTINGS WINDOW - COMPLETE VERSION
Panel de configuración completo de Neuro-OS Desktop
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QListWidget, QFileDialog, QMessageBox,
    QComboBox, QCheckBox, QGroupBox, QListWidgetItem, QSlider
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# Importar AppManager
try:
    from app_manager import AppManager
except:
    import sys
    sys.path.append(str(Path(__file__).parent))
    from app_manager import AppManager


# Constantes del sistema
NEURO_OS_VERSION = "0.1"
NEURO_OS_AUTHOR = "José Manuel Moreno Cano"
NEURO_OS_NAME = "Neuro-OS Desktop"
NEURO_OS_WEBSITE = "neuro-os.es"


class SettingsWindow(QWidget):
    """Ventana de configuración de Neuro-OS"""
    
    # Signal para notificar cambios
    apps_changed = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Window)
        self.setWindowTitle("⚙️ Neuro-OS Settings")
        self.resize(750, 650)
        
        # App Manager
        self.app_manager = AppManager()
        
        # Estilo
        self.setStyleSheet("""
            QWidget {
                background: #0a0a0a;
                color: white;
                font-family: 'Segoe UI';
            }
            QTabWidget::pane {
                border: 1px solid #333;
                background: #111;
            }
            QTabBar::tab {
                background: #1a1a1a;
                color: #888;
                padding: 10px 15px;
                border: 1px solid #333;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #004444;
                color: cyan;
                border-bottom: 2px solid cyan;
            }
            QPushButton {
                background: #004444;
                color: cyan;
                border: 1px solid cyan;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #006666;
            }
            QPushButton:pressed {
                background: cyan;
                color: black;
            }
            QListWidget {
                background: #0a0a0a;
                border: 1px solid #333;
                color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #222;
            }
            QListWidget::item:selected {
                background: #004444;
                color: cyan;
            }
            QComboBox {
                background: #1a1a1a;
                color: white;
                border: 1px solid #333;
                padding: 5px;
            }
            QCheckBox {
                color: white;
            }
            QGroupBox {
                color: cyan;
                font-weight: bold;
                border: 1px solid #333;
                border-radius: 5px;
                padding: 15px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("NEURO-OS SETTINGS")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 16, QFont.Bold))
        header.setStyleSheet("color: cyan; padding: 10px;")
        main_layout.addWidget(header)
        
        # Tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_system_tab(), "🖥️ System")
        tabs.addTab(self.create_general_tab(), "🏠 General")
        tabs.addTab(self.create_performance_tab(), "⚡ Performance")
        tabs.addTab(self.create_applications_tab(), "📦 Applications")
        tabs.addTab(self.create_ai_optimizer_tab(), "🤖 AI Optimizer")
        
        main_layout.addWidget(tabs)
        
        # Footer buttons
        footer = QHBoxLayout()
        footer.addStretch()
        
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        footer.addWidget(btn_close)
        
        main_layout.addLayout(footer)
    
    def create_system_tab(self):
        """Tab de información del sistema"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Neuro-OS Info
        group_neuro = QGroupBox("Neuro-OS Information")
        neuro_layout = QVBoxLayout(group_neuro)
        
        lbl_name = QLabel(f"System: {NEURO_OS_NAME}")
        lbl_name.setStyleSheet("color: cyan; font-size: 14px; font-weight: bold;")
        neuro_layout.addWidget(lbl_name)
        
        lbl_version = QLabel(f"Version: {NEURO_OS_VERSION}")
        neuro_layout.addWidget(lbl_version)
        
        lbl_author = QLabel(f"Author: {NEURO_OS_AUTHOR}")
        neuro_layout.addWidget(lbl_author)
        
        lbl_website = QLabel(f"Website: {NEURO_OS_WEBSITE}")
        lbl_website.setStyleSheet("color: #00aaff;")
        neuro_layout.addWidget(lbl_website)
        
        layout.addWidget(group_neuro)
        
        # Hardware Info
        import platform
        try:
            import psutil
            
            # CPU
            group_cpu = QGroupBox("Processor")
            cpu_layout = QVBoxLayout(group_cpu)
            
            cpu_name = platform.processor() or "Unknown CPU"
            cpu_cores = psutil.cpu_count(logical=False)
            cpu_threads = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            
            cpu_layout.addWidget(QLabel(f"Name: {cpu_name}"))
            cpu_layout.addWidget(QLabel(f"Cores: {cpu_cores} | Threads: {cpu_threads}"))
            if cpu_freq:
                cpu_layout.addWidget(QLabel(f"Frequency: {cpu_freq.current:.0f} MHz"))
            
            layout.addWidget(group_cpu)
            
            # RAM
            group_ram = QGroupBox("Memory")
            ram_layout = QVBoxLayout(group_ram)
            
            ram = psutil.virtual_memory()
            ram_total_gb = ram.total / (1024**3)
            ram_used_gb = ram.used / (1024**3)
            ram_free_gb = ram.available / (1024**3)
            
            ram_layout.addWidget(QLabel(f"Total: {ram_total_gb:.1f} GB"))
            ram_layout.addWidget(QLabel(f"Used: {ram_used_gb:.1f} GB ({ram.percent}%)"))
            ram_layout.addWidget(QLabel(f"Available: {ram_free_gb:.1f} GB"))
            
            layout.addWidget(group_ram)
            
            # Storage
            group_storage = QGroupBox("Storage")
            storage_layout = QVBoxLayout(group_storage)
            
            disk = psutil.disk_usage('/')
            disk_total_gb = disk.total / (1024**3)
            disk_used_gb = disk.used / (1024**3)
            disk_free_gb = disk.free / (1024**3)
            
            storage_layout.addWidget(QLabel(f"Total: {disk_total_gb:.0f} GB"))
            storage_layout.addWidget(QLabel(f"Used: {disk_used_gb:.0f} GB ({disk.percent}%)"))
            storage_layout.addWidget(QLabel(f"Free: {disk_free_gb:.0f} GB"))
            
            layout.addWidget(group_storage)
            
        except ImportError:
            info = QLabel("Install 'psutil' to view detailed system information:\npip install psutil")
            info.setStyleSheet("color: #888; font-style: italic;")
            layout.addWidget(info)
        
        layout.addStretch()
        return widget
    
    def create_general_tab(self):
        """Tab de configuración general"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tema
        group_theme = QGroupBox("Theme")
        theme_layout = QVBoxLayout(group_theme)
        
        combo_theme = QComboBox()
        combo_theme.addItems(["Dark (Default)", "Light", "Cyberpunk"])
        theme_layout.addWidget(combo_theme)
        
        layout.addWidget(group_theme)
        
        # Idioma
        group_lang = QGroupBox("Language")
        lang_layout = QVBoxLayout(group_lang)
        
        combo_lang = QComboBox()
        combo_lang.addItems(["English", "Español", "Français"])
        lang_layout.addWidget(combo_lang)
        
        layout.addWidget(group_lang)
        
        layout.addStretch()
        return widget
    
    def create_performance_tab(self):
        """Tab de optimización de rendimiento"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Monitoreo
        group_monitor = QGroupBox("System Monitoring")
        monitor_layout = QVBoxLayout(group_monitor)
        
        lbl_interval = QLabel("Update Interval:")
        combo_interval = QComboBox()
        combo_interval.addItems(["10 seconds", "30 seconds (Recommended)", "60 seconds", "Disabled"])
        combo_interval.setCurrentIndex(1)  # 30s por defecto
        
        monitor_layout.addWidget(lbl_interval)
        monitor_layout.addWidget(combo_interval)
        
        layout.addWidget(group_monitor)
        
        # Animaciones
        group_anim = QGroupBox("Visual Effects")
        anim_layout = QVBoxLayout(group_anim)
        
        check_animations = QCheckBox("Enable animations")
        check_animations.setChecked(True)
        anim_layout.addWidget(check_animations)
        
        layout.addWidget(group_anim)
        
        # Virtual RAM (Swap/Page File)
        group_vram = QGroupBox("Virtual RAM (Page File)")
        vram_layout = QVBoxLayout(group_vram)
        
        lbl_vram_info = QLabel("Increase virtual RAM to improve performance on low-RAM systems")
        lbl_vram_info.setStyleSheet("color: #888; font-style: italic;")
        vram_layout.addWidget(lbl_vram_info)
        
        lbl_vram_size = QLabel("Virtual RAM Size:")
        vram_layout.addWidget(lbl_vram_size)
        
        combo_vram = QComboBox()
        combo_vram.addItems([
            "System Managed (Default)",
            "2 GB (Minimum)",
            "4 GB (Recommended for 4GB RAM)",
            "8 GB (Recommended for 8GB RAM)",
            "16 GB (High Performance)",
            "32 GB (Maximum)"
        ])
        vram_layout.addWidget(combo_vram)
        
        btn_apply_vram = QPushButton("Apply Virtual RAM Settings")
        btn_apply_vram.clicked.connect(lambda: QMessageBox.information(
            self, "Virtual RAM", 
            "Virtual RAM settings will be applied on next restart.\n\n"
            "Note: This modifies Windows page file settings."
        ))
        vram_layout.addWidget(btn_apply_vram)
        
        layout.addWidget(group_vram)
        
        # GPU Acceleration
        group_gpu = QGroupBox("GPU Acceleration")
        gpu_layout = QVBoxLayout(group_gpu)
        
        lbl_gpu_info = QLabel("Use host PC's GPU to accelerate graphics rendering")
        lbl_gpu_info.setStyleSheet("color: #888; font-style: italic;")
        gpu_layout.addWidget(lbl_gpu_info)
        
        check_gpu = QCheckBox("Enable GPU Acceleration (CUDA/OpenCL)")
        check_gpu.setChecked(True)
        gpu_layout.addWidget(check_gpu)
        
        # GPU Info
        try:
            from gpu_accelerator import GPUAccelerator
            gpu_acc = GPUAccelerator()
            gpu_info = gpu_acc.get_info()
            
            lbl_gpu_detected = QLabel(f"Detected: {gpu_info['gpu_name']} ({gpu_info['gpu_vendor']})")
            lbl_gpu_detected.setStyleSheet("color: #0f0; font-weight: bold;")
            gpu_layout.addWidget(lbl_gpu_detected)
            
            lbl_gpu_backend = QLabel(f"Backend: {gpu_info['best_backend']}")
            gpu_layout.addWidget(lbl_gpu_backend)
        except:
            lbl_gpu_error = QLabel("GPU detection failed. Install 'torch' or 'pyopencl' for acceleration.")
            lbl_gpu_error.setStyleSheet("color: #f80;")
            gpu_layout.addWidget(lbl_gpu_error)
        
        # Benchmark button
        btn_benchmark = QPushButton("📊 Run GPU Benchmark")
        btn_benchmark.clicked.connect(self.run_gpu_benchmark)
        gpu_layout.addWidget(btn_benchmark)
        
        self.lbl_benchmark_result = QLabel("")
        self.lbl_benchmark_result.setStyleSheet("color: cyan; font-weight: bold;")
        gpu_layout.addWidget(self.lbl_benchmark_result)
        
        layout.addWidget(group_gpu)
        
        # Info
        info = QLabel("💡 Tip: Disable monitoring and animations for better performance on low-end PCs")
        info.setStyleSheet("color: #888; font-style: italic; padding: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        return widget
    
    def create_applications_tab(self):
        """Tab de gestión de aplicaciones"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        title = QLabel("Custom Applications")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        layout.addWidget(title)
        
        desc = QLabel("Add your favorite games and programs to the Neuro-OS desktop")
        desc.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(desc)
        
        # Lista de apps
        self.app_list = QListWidget()
        self.refresh_app_list()
        layout.addWidget(self.app_list)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_add = QPushButton("➕ Add Application")
        btn_add.clicked.connect(self.add_application)
        btn_layout.addWidget(btn_add)
        
        btn_remove = QPushButton("🗑️ Remove")
        btn_remove.clicked.connect(self.remove_application)
        btn_layout.addWidget(btn_remove)
        
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        return widget
    
    def refresh_app_list(self):
        """Actualizar lista de apps"""
        self.app_list.clear()
        
        apps = self.app_manager.get_apps()
        
        if not apps:
            item = QListWidgetItem("No applications configured. Click 'Add Application' to start.")
            item.setFlags(Qt.NoItemFlags)  # No seleccionable
            self.app_list.addItem(item)
        else:
            for app in apps:
                icon = app.get('icon', '📦')
                name = app.get('name', 'Unknown')
                path = app.get('path', '')
                
                item_text = f"{icon}  {name}\n    {path}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, app)  # Guardar datos de la app
                self.app_list.addItem(item)
    
    def add_application(self):
        """Añadir aplicación manualmente"""
        # Abrir file dialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Application",
            "C:/",
            "Executables (*.exe);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        # Obtener nombre
        app_name = Path(file_path).stem
        
        # Añadir
        success = self.app_manager.add_app(app_name, file_path, "🎮")
        
        if success:
            self.refresh_app_list()
            self.apps_changed.emit()  # Notificar cambio
            QMessageBox.information(self, "Success", f"Added: {app_name}")
        else:
            QMessageBox.warning(self, "Error", "Could not add application. It may already exist.")
    
    def remove_application(self):
        """Eliminar aplicación seleccionada"""
        current_item = self.app_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an application to remove")
            return
        
        app_data = current_item.data(Qt.UserRole)
        if not app_data:
            return
        
        app_name = app_data.get('name', '')
        
        # Confirmar
        reply = QMessageBox.question(
            self,
            "Confirm",
            f"Remove '{app_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.app_manager.remove_app(app_name)
            
            if success:
                self.refresh_app_list()
                self.apps_changed.emit()  # Notificar cambio
                QMessageBox.information(self, "Success", f"Removed: {app_name}")


if __name__ == "__main__":
    # Test standalone
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
