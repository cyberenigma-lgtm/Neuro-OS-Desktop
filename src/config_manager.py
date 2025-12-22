#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔧 NEURO-OS CONFIG MANAGER
Gestiona la configuración persistente del sistema
"""

import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = Path(__file__).parent / config_file
        self.config = self.load_config()
    
    def load_config(self):
        """Cargar configuración desde JSON"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.get_default_config()
        else:
            # Crear config por defecto
            config = self.get_default_config()
            self.save_config(config)
            return config
    
    def save_config(self, config=None):
        """Guardar configuración a JSON"""
        if config is None:
            config = self.config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_default_config(self):
        """Configuración por defecto"""
        import os
        return {
            "file_explorer": {
                "default_path": os.path.expanduser("~/Desktop"),
                "show_hidden": False
            },
            "browser": {
                "preferred": "auto",  # auto, opera, chrome, edge, firefox
                "custom_path": ""
            },
            "performance": {
                "enable_radar": True,
                "radar_interval_ms": 3000,
                "memory_threshold_mb": 250
            },
            "ui": {
                "theme": "dark",
                "animations": True
            }
        }
    
    def get(self, key_path, default=None):
        """Obtener valor de configuración usando path (ej: 'browser.preferred')"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value
    
    def set(self, key_path, value):
        """Establecer valor de configuración"""
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save_config()
