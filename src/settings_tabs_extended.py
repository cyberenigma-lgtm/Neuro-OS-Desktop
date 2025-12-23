    
    def create_system_tab(self):
        """Tab de información del sistema"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        title = QLabel("System Information")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        layout.addWidget(title)
        
        # Info del sistema
        import platform
        try:
            import psutil
            
            # CPU
            group_cpu = QGroupBox("Processor")
            group_cpu.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
            cpu_layout = QVBoxLayout(group_cpu)
            
            cpu_name = platform.processor() or "Unknown CPU"
            cpu_cores = psutil.cpu_count(logical=False)
            cpu_threads = psutil.cpu_count(logical=True)
            
            cpu_layout.addWidget(QLabel(f"Name: {cpu_name}"))
            cpu_layout.addWidget(QLabel(f"Cores: {cpu_cores} | Threads: {cpu_threads}"))
            
            layout.addWidget(group_cpu)
            
            # RAM
            group_ram = QGroupBox("Memory")
            group_ram.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
            ram_layout = QVBoxLayout(group_ram)
            
            ram = psutil.virtual_memory()
            ram_total_gb = ram.total / (1024**3)
            ram_used_gb = ram.used / (1024**3)
            
            ram_layout.addWidget(QLabel(f"Total: {ram_total_gb:.1f} GB"))
            ram_layout.addWidget(QLabel(f"Used: {ram_used_gb:.1f} GB ({ram.percent}%)"))
            
            layout.addWidget(group_ram)
            
            # Storage
            group_storage = QGroupBox("Storage")
            group_storage.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
            storage_layout = QVBoxLayout(group_storage)
            
            disk = psutil.disk_usage('/')
            disk_total_gb = disk.total / (1024**3)
            disk_used_gb = disk.used / (1024**3)
            disk_free_gb = disk.free / (1024**3)
            
            storage_layout.addWidget(QLabel(f"Total: {disk_total_gb:.1f} GB"))
            storage_layout.addWidget(QLabel(f"Used: {disk_used_gb:.1f} GB"))
            storage_layout.addWidget(QLabel(f"Free: {disk_free_gb:.1f} GB"))
            
            layout.addWidget(group_storage)
            
        except ImportError:
            layout.addWidget(QLabel("Install 'psutil' to view system information"))
        
        layout.addStretch()
        return widget
    
    def create_display_tab(self):
        """Tab de configuración de pantalla"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Resolución
        group_res = QGroupBox("Resolution")
        group_res.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        res_layout = QVBoxLayout(group_res)
        
        combo_res = QComboBox()
        combo_res.addItems([
            "1920x1080 (Full HD)",
            "2560x1440 (2K)",
            "3840x2160 (4K)",
            "1366x768",
            "1280x720"
        ])
        res_layout.addWidget(QLabel("Screen Resolution:"))
        res_layout.addWidget(combo_res)
        
        layout.addWidget(group_res)
        
        # Escalado
        group_scale = QGroupBox("Scaling")
        group_scale.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        scale_layout = QVBoxLayout(group_scale)
        
        combo_scale = QComboBox()
        combo_scale.addItems(["100%", "125%", "150%", "175%", "200%"])
        scale_layout.addWidget(QLabel("Display Scaling:"))
        scale_layout.addWidget(combo_scale)
        
        layout.addWidget(group_scale)
        
        # Múltiples monitores
        group_multi = QGroupBox("Multiple Displays")
        group_multi.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        multi_layout = QVBoxLayout(group_multi)
        
        check_extend = QCheckBox("Extend desktop to second monitor")
        multi_layout.addWidget(check_extend)
        
        layout.addWidget(group_multi)
        
        layout.addStretch()
        return widget
    
    def create_sound_tab(self):
        """Tab de configuración de sonido"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Volumen
        group_vol = QGroupBox("Volume")
        group_vol.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        vol_layout = QVBoxLayout(group_vol)
        
        from PySide6.QtWidgets import QSlider
        
        slider_master = QSlider(Qt.Horizontal)
        slider_master.setRange(0, 100)
        slider_master.setValue(50)
        
        vol_layout.addWidget(QLabel("Master Volume:"))
        vol_layout.addWidget(slider_master)
        
        layout.addWidget(group_vol)
        
        # Dispositivos
        group_devices = QGroupBox("Audio Devices")
        group_devices.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        devices_layout = QVBoxLayout(group_devices)
        
        combo_output = QComboBox()
        combo_output.addItems(["Speakers (Default)", "Headphones", "HDMI Audio"])
        devices_layout.addWidget(QLabel("Output Device:"))
        devices_layout.addWidget(combo_output)
        
        combo_input = QComboBox()
        combo_input.addItems(["Microphone (Default)", "Line In"])
        devices_layout.addWidget(QLabel("Input Device:"))
        devices_layout.addWidget(combo_input)
        
        layout.addWidget(group_devices)
        
        layout.addStretch()
        return widget
    
    def create_network_tab(self):
        """Tab de configuración de red"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Estado de conexión
        group_status = QGroupBox("Connection Status")
        group_status.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        status_layout = QVBoxLayout(group_status)
        
        try:
            import psutil
            net_stats = psutil.net_if_stats()
            online = any(stats.isup for stats in net_stats.values())
            status_text = "Connected" if online else "Disconnected"
            status_color = "color: #0f0;" if online else "color: #f00;"
            
            lbl_status = QLabel(f"Status: {status_text}")
            lbl_status.setStyleSheet(status_color + " font-weight: bold;")
            status_layout.addWidget(lbl_status)
        except:
            status_layout.addWidget(QLabel("Status: Unknown"))
        
        layout.addWidget(group_status)
        
        # Wi-Fi
        group_wifi = QGroupBox("Wi-Fi")
        group_wifi.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        wifi_layout = QVBoxLayout(group_wifi)
        
        check_wifi = QCheckBox("Enable Wi-Fi")
        check_wifi.setChecked(True)
        wifi_layout.addWidget(check_wifi)
        
        btn_scan = QPushButton("Scan Networks")
        wifi_layout.addWidget(btn_scan)
        
        layout.addWidget(group_wifi)
        
        # Ethernet
        group_eth = QGroupBox("Ethernet")
        group_eth.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        eth_layout = QVBoxLayout(group_eth)
        
        eth_layout.addWidget(QLabel("Ethernet connection detected"))
        
        layout.addWidget(group_eth)
        
        layout.addStretch()
        return widget
    
    def create_gaming_tab(self):
        """Tab de configuración de gaming"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        title = QLabel("Gaming Optimization")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        layout.addWidget(title)
        
        # Game Mode
        group_mode = QGroupBox("Game Mode")
        group_mode.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        mode_layout = QVBoxLayout(group_mode)
        
        check_game_mode = QCheckBox("Enable Game Mode (Optimize CPU/RAM for games)")
        check_game_mode.setChecked(False)
        mode_layout.addWidget(check_game_mode)
        
        layout.addWidget(group_mode)
        
        # GFX Optimizer
        group_gfx = QGroupBox("GFX Optimizer")
        group_gfx.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        gfx_layout = QVBoxLayout(group_gfx)
        
        gfx_layout.addWidget(QLabel("Upscaling Mode:"))
        combo_upscale = QComboBox()
        combo_upscale.addItems([
            "Disabled",
            "Performance (720p → 4K)",
            "Balanced (1080p → 4K)",
            "Quality (1440p → 4K)"
        ])
        gfx_layout.addWidget(combo_upscale)
        
        check_capture = QCheckBox("Capture game windows with Neuro-OS styling")
        check_capture.setChecked(True)
        gfx_layout.addWidget(check_capture)
        
        layout.addWidget(group_gfx)
        
        # Performance Overlay
        group_overlay = QGroupBox("Performance Overlay")
        group_overlay.setStyleSheet("QGroupBox { color: cyan; font-weight: bold; border: 1px solid #333; padding: 10px; }")
        overlay_layout = QVBoxLayout(group_overlay)
        
        check_fps = QCheckBox("Show FPS counter")
        overlay_layout.addWidget(check_fps)
        
        check_stats = QCheckBox("Show CPU/GPU/RAM stats")
        overlay_layout.addWidget(check_stats)
        
        layout.addWidget(group_overlay)
        
        # Info
        info = QLabel("💡 Tip: Enable Game Mode and GFX Optimizer for best gaming performance")
        info.setStyleSheet("color: #888; font-style: italic; padding: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        return widget
