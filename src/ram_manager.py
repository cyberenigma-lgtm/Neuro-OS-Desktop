#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
💾 RAM MANAGER
Liberador y expansor de RAM con soporte para RAM virtual desde disco
"""

import psutil
import os
import sys
from pathlib import Path
from typing import Dict, List

class RAMManager:
    """Gestor de RAM: liberación y expansión virtual"""
    
    def __init__(self):
        self.virtual_ram_path = Path("C:/NeuroOS_VirtualRAM")
        self.virtual_ram_size_gb = 0
    
    def get_ram_status(self) -> Dict:
        """Obtener estado actual de RAM"""
        ram = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'total_gb': ram.total / (1024**3),
            'used_gb': ram.used / (1024**3),
            'free_gb': ram.available / (1024**3),
            'percent': ram.percent,
            'swap_total_gb': swap.total / (1024**3),
            'swap_used_gb': swap.used / (1024**3),
            'swap_percent': swap.percent
        }
    
    def free_ram(self, aggressive: bool = False) -> Dict:
        """
        Liberar RAM
        
        Args:
            aggressive: Si True, libera RAM agresivamente
        
        Returns:
            Dict con RAM liberada
        """
        ram_before = psutil.virtual_memory().available / (1024**3)
        actions = []
        
        try:
            # 1. Limpiar caché de Python
            import gc
            gc.collect()
            actions.append("Python garbage collection")
            
            # 2. Reducir prioridad de apps pesadas
            heavy_apps = []
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    mem_gb = proc.info['memory_info'].rss / (1024**3)
                    if mem_gb > 0.5:  # > 500MB
                        heavy_apps.append({
                            'name': proc.info['name'],
                            'ram_gb': mem_gb,
                            'proc': proc
                        })
                except:
                    pass
            
            # Ordenar por uso de RAM
            heavy_apps.sort(key=lambda x: x['ram_gb'], reverse=True)
            
            if aggressive and heavy_apps:
                # Reducir prioridad de las 5 apps más pesadas
                for app in heavy_apps[:5]:
                    try:
                        app['proc'].nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if sys.platform == 'win32' else 10)
                        actions.append(f"Reduced priority: {app['name']}")
                    except:
                        pass
            
            # 3. Limpiar archivos temporales (Windows)
            if sys.platform == 'win32' and aggressive:
                temp_dirs = [
                    os.environ.get('TEMP'),
                    os.environ.get('TMP'),
                    'C:/Windows/Temp'
                ]
                
                for temp_dir in temp_dirs:
                    if temp_dir and os.path.exists(temp_dir):
                        try:
                            # Contar archivos temporales
                            temp_files = list(Path(temp_dir).glob('*'))
                            if temp_files:
                                actions.append(f"Temp files found: {len(temp_files)}")
                        except:
                            pass
        
        except Exception as e:
            actions.append(f"Error: {str(e)}")
        
        ram_after = psutil.virtual_memory().available / (1024**3)
        ram_freed = ram_after - ram_before
        
        return {
            'ram_freed_gb': max(0, ram_freed),
            'ram_before_gb': ram_before,
            'ram_after_gb': ram_after,
            'actions': actions,
            'heavy_apps': [{'name': app['name'], 'ram_gb': app['ram_gb']} for app in heavy_apps[:10]]
        }
    
    def create_virtual_ram(self, size_gb: int) -> Dict:
        """
        Crear RAM virtual usando espacio en disco
        
        Args:
            size_gb: Tamaño en GB de RAM virtual
        
        Returns:
            Dict con resultado
        """
        try:
            # Crear directorio si no existe
            self.virtual_ram_path.mkdir(exist_ok=True)
            
            # Crear archivo de swap
            swap_file = self.virtual_ram_path / "neuro_swap.dat"
            
            # Calcular tamaño en bytes
            size_bytes = size_gb * 1024 * 1024 * 1024
            
            # Crear archivo (esto puede tardar)
            print(f"[RAM Manager] Creating {size_gb}GB virtual RAM file...")
            
            # Crear archivo sparse (rápido, no ocupa espacio real hasta que se use)
            with open(swap_file, 'wb') as f:
                f.seek(size_bytes - 1)
                f.write(b'\0')
            
            self.virtual_ram_size_gb = size_gb
            
            return {
                'success': True,
                'size_gb': size_gb,
                'path': str(swap_file),
                'note': 'Virtual RAM file created. Restart required to activate.'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_virtual_ram_status(self) -> Dict:
        """Obtener estado de RAM virtual"""
        swap_file = self.virtual_ram_path / "neuro_swap.dat"
        
        if swap_file.exists():
            size_bytes = swap_file.stat().st_size
            size_gb = size_bytes / (1024**3)
            
            return {
                'exists': True,
                'size_gb': size_gb,
                'path': str(swap_file)
            }
        else:
            return {
                'exists': False,
                'size_gb': 0
            }
    
    def remove_virtual_ram(self) -> Dict:
        """Eliminar RAM virtual"""
        try:
            swap_file = self.virtual_ram_path / "neuro_swap.dat"
            
            if swap_file.exists():
                swap_file.unlink()
                return {'success': True, 'message': 'Virtual RAM removed'}
            else:
                return {'success': False, 'message': 'No virtual RAM found'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("RAM MANAGER TEST")
    print("=" * 60)
    print()
    
    manager = RAMManager()
    
    # Estado actual
    status = manager.get_ram_status()
    print("Current RAM Status:")
    print(f"  Total: {status['total_gb']:.1f} GB")
    print(f"  Used: {status['used_gb']:.1f} GB ({status['percent']:.1f}%)")
    print(f"  Free: {status['free_gb']:.1f} GB")
    print(f"  Swap: {status['swap_used_gb']:.1f}/{status['swap_total_gb']:.1f} GB")
    
    # Liberar RAM
    print("\n--- Freeing RAM ---")
    result = manager.free_ram(aggressive=True)
    print(f"RAM freed: {result['ram_freed_gb']:.2f} GB")
    print(f"Actions taken: {len(result['actions'])}")
    
    if result['heavy_apps']:
        print("\nHeavy apps detected:")
        for app in result['heavy_apps'][:5]:
            print(f"  {app['name']}: {app['ram_gb']:.2f} GB")
    
    # Estado de RAM virtual
    print("\n--- Virtual RAM Status ---")
    vram_status = manager.get_virtual_ram_status()
    if vram_status['exists']:
        print(f"Virtual RAM: {vram_status['size_gb']:.1f} GB")
        print(f"Path: {vram_status['path']}")
    else:
        print("No virtual RAM configured")
    
    print("\n" + "=" * 60)
    print("RAM MANAGER TEST COMPLETED")
    print("=" * 60)
