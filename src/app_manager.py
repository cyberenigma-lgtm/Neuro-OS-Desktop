#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📦 APP MANAGER
Gestiona aplicaciones personalizadas del usuario
Sin escaneo automático - Solo configuración manual
"""

import json
from pathlib import Path
from typing import List, Dict, Optional

class AppManager:
    """Gestor de aplicaciones personalizadas"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = Path(config_file)
        self.apps: List[Dict] = []
        self.load_apps()
    
    def load_apps(self) -> List[Dict]:
        """Cargar apps desde config.json"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.apps = data.get('custom_apps', [])
                    print(f"[AppManager] Loaded {len(self.apps)} apps")
            else:
                # Crear config por defecto
                self.apps = []
                self.save_apps()
                print("[AppManager] Created default config")
        except Exception as e:
            print(f"[AppManager] Error loading apps: {e}")
            self.apps = []
        
        return self.apps
    
    def add_app(self, name: str, path: str, icon: str = "🎮") -> bool:
        """
        Añadir app manualmente
        
        Args:
            name: Nombre de la app
            path: Ruta completa al ejecutable
            icon: Emoji del icono
        
        Returns:
            True si se añadió correctamente
        """
        # Verificar que el archivo existe
        if not Path(path).exists():
            print(f"[AppManager] Error: Path not found: {path}")
            return False
        
        # Verificar que no existe ya
        for app in self.apps:
            if app['path'] == path:
                print(f"[AppManager] App already exists: {name}")
                return False
        
        # Añadir
        new_app = {
            'name': name,
            'path': path,
            'icon': icon
        }
        self.apps.append(new_app)
        self.save_apps()
        
        print(f"[AppManager] Added: {name}")
        return True
    
    def remove_app(self, name: str) -> bool:
        """
        Eliminar app
        
        Args:
            name: Nombre de la app a eliminar
        
        Returns:
            True si se eliminó
        """
        for i, app in enumerate(self.apps):
            if app['name'] == name:
                self.apps.pop(i)
                self.save_apps()
                print(f"[AppManager] Removed: {name}")
                return True
        
        print(f"[AppManager] App not found: {name}")
        return False
    
    def get_apps(self) -> List[Dict]:
        """Obtener lista de apps"""
        return self.apps
    
    def save_apps(self) -> bool:
        """Guardar apps en config.json"""
        try:
            # Cargar config existente o crear nuevo
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Actualizar custom_apps
            config['custom_apps'] = self.apps
            
            # Guardar
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            print(f"[AppManager] Saved {len(self.apps)} apps to {self.config_file}")
            return True
        
        except Exception as e:
            print(f"[AppManager] Error saving apps: {e}")
            return False


if __name__ == "__main__":
    # Test
    print("=== APP MANAGER TEST ===\n")
    
    manager = AppManager("test_config.json")
    
    # Añadir apps de prueba
    manager.add_app("Notepad", "C:/Windows/System32/notepad.exe", "📝")
    manager.add_app("Calculator", "C:/Windows/System32/calc.exe", "🔢")
    
    # Listar
    print("\nApps configuradas:")
    for app in manager.get_apps():
        print(f"  {app['icon']} {app['name']} -> {app['path']}")
    
    # Eliminar
    manager.remove_app("Notepad")
    
    print("\nApps después de eliminar:")
    for app in manager.get_apps():
        print(f"  {app['icon']} {app['name']}")
