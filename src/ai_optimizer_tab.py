    
    def create_ai_optimizer_tab(self):
        """Tab de configuración de IA Optimizer"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Título
        title = QLabel("AI Optimization Engine")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title.setStyleSheet("color: cyan;")
        layout.addWidget(title)
        
        desc = QLabel("Intelligent system that auto-manages RAM, detects bottlenecks, and scales resolution")
        desc.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(desc)
        
        # Enable AI
        group_enable = QGroupBox("AI Optimization")
        enable_layout = QVBoxLayout(group_enable)
        
        check_ai = QCheckBox("Enable AI Optimizer (Automatic optimization)")
        check_ai.setChecked(True)
        enable_layout.addWidget(check_ai)
        
        layout.addWidget(group_enable)
        
        # Target FPS
        group_fps = QGroupBox("Performance Target")
        fps_layout = QVBoxLayout(group_fps)
        
        lbl_target_fps = QLabel("Target FPS:")
        fps_layout.addWidget(lbl_target_fps)
        
        combo_fps = QComboBox()
        combo_fps.addItems(["30 FPS (Minimum)", "60 FPS (Recommended)", "120 FPS (High-end)", "144 FPS (Competitive)"])
        combo_fps.setCurrentIndex(1)  # 60 FPS por defecto
        fps_layout.addWidget(combo_fps)
        
        layout.addWidget(group_fps)
        
        # Resolution Scaling
        group_scaling = QGroupBox("Auto Resolution Scaling")
        scaling_layout = QVBoxLayout(group_scaling)
        
        lbl_scaling_info = QLabel("AI automatically adjusts render resolution based on FPS:")
        lbl_scaling_info.setStyleSheet("color: #888; font-style: italic;")
        scaling_layout.addWidget(lbl_scaling_info)
        
        # Presets
        from PySide6.QtWidgets import QRadioButton, QButtonGroup
        
        self.scaling_group = QButtonGroup()
        
        radio_auto = QRadioButton("Auto (AI decides)")
        radio_auto.setChecked(True)
        self.scaling_group.addButton(radio_auto, 0)
        scaling_layout.addWidget(radio_auto)
        
        radio_ultra = QRadioButton("Ultra Performance (720p → 4K)")
        self.scaling_group.addButton(radio_ultra, 1)
        scaling_layout.addWidget(radio_ultra)
        
        radio_perf = QRadioButton("Performance (1080p → 4K)")
        self.scaling_group.addButton(radio_perf, 2)
        scaling_layout.addWidget(radio_perf)
        
        radio_balanced = QRadioButton("Balanced (1440p → 4K)")
        self.scaling_group.addButton(radio_balanced, 3)
        scaling_layout.addWidget(radio_balanced)
        
        radio_quality = QRadioButton("Quality (Native 4K)")
        self.scaling_group.addButton(radio_quality, 4)
        scaling_layout.addWidget(radio_quality)
        
        layout.addWidget(group_scaling)
        
        # Bottleneck Detection
        group_bottleneck = QGroupBox("Bottleneck Detection")
        bottleneck_layout = QVBoxLayout(group_bottleneck)
        
        check_cpu = QCheckBox("Monitor CPU bottleneck")
        check_cpu.setChecked(True)
        bottleneck_layout.addWidget(check_cpu)
        
        check_ram = QCheckBox("Monitor RAM bottleneck")
        check_ram.setChecked(True)
        bottleneck_layout.addWidget(check_ram)
        
        check_gpu = QCheckBox("Monitor GPU bottleneck")
        check_gpu.setChecked(True)
        bottleneck_layout.addWidget(check_gpu)
        
        layout.addWidget(group_bottleneck)
        
        # RAM Optimization
        group_ram_opt = QGroupBox("RAM Optimization")
        ram_opt_layout = QVBoxLayout(group_ram_opt)
        
        check_auto_ram = QCheckBox("Auto-optimize RAM when bottleneck detected")
        check_auto_ram.setChecked(True)
        ram_opt_layout.addWidget(check_auto_ram)
        
        check_aggressive = QCheckBox("Aggressive RAM freeing (may close background apps)")
        ram_opt_layout.addWidget(check_aggressive)
        
        layout.addWidget(group_ram_opt)
        
        # Test AI button
        btn_test_ai = QPushButton("🧪 Test AI Optimizer")
        btn_test_ai.clicked.connect(self.test_ai_optimizer)
        layout.addWidget(btn_test_ai)
        
        self.lbl_ai_result = QLabel("")
        self.lbl_ai_result.setStyleSheet("color: cyan; font-weight: bold;")
        layout.addWidget(self.lbl_ai_result)
        
        # Info
        info = QLabel("💡 Tip: AI Optimizer learns from your usage and adapts automatically")
        info.setStyleSheet("color: #888; font-style: italic; padding: 10px;")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        return widget
    
    def test_ai_optimizer(self):
        """Probar AI Optimizer"""
        self.lbl_ai_result.setText("Testing AI Optimizer...")
        QApplication.processEvents()
        
        try:
            from neuro_ai_optimizer import NeuroAI
            
            ai = NeuroAI()
            
            # Simular FPS bajo
            recommendations = ai.auto_optimize(current_fps=25)
            
            # Mostrar resultado
            bottleneck = recommendations['bottleneck']
            preset = recommendations['recommended_preset']
            render_res = recommendations['render_resolution']
            output_res = recommendations['output_resolution']
            
            result_text = (
                f"AI Test Results:\n"
                f"Bottleneck: {bottleneck.upper()}\n"
                f"Recommended: {preset}\n"
                f"Resolution: {render_res[0]}x{render_res[1]} → {output_res[0]}x{output_res[1]}"
            )
            
            self.lbl_ai_result.setText(result_text)
            
            # Mostrar diálogo
            QMessageBox.information(
                self,
                "AI Optimizer Test",
                f"AI Optimization Test (25 FPS scenario):\n\n"
                f"🔍 Bottleneck Detected: {bottleneck.upper()}\n"
                f"🎮 Recommended Preset: {preset}\n"
                f"📐 Resolution Scaling:\n"
                f"   Render: {render_res[0]}x{render_res[1]}\n"
                f"   Output: {output_res[0]}x{output_res[1]}\n\n"
                f"⚡ Expected FPS Boost: ~4x"
            )
        
        except Exception as e:
            self.lbl_ai_result.setText(f"Test failed: {str(e)}")
            QMessageBox.warning(self, "AI Test Error", f"Could not test AI:\n{str(e)}")
