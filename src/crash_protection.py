#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ CRASH PROTECTION
Sistema de protección para evitar que Neuro-OS crashee el PC anfitrión
"""

import sys
import psutil
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(
    filename='neuro_os_crash_protection.log',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class CrashProtection:
    """Sistema de protección anti-crash"""
    
    # Límites de seguridad
    MAX_CPU_USAGE = 90  # % máximo de CPU que puede usar Neuro-OS
    MAX_RAM_USAGE = 85  # % máximo de RAM del sistema
    MIN_FREE_RAM_GB = 1.0  # GB mínimos de RAM libre
    MAX_PROCESS_RAM_GB = 4.0  # GB máximos por proceso de Neuro-OS
    
    def __init__(self):
        self.enabled = True
        self.warnings_count = 0
        self.emergency_mode = False
    
    def check_system_health(self) -> dict:
        """Verificar salud del sistema"""
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # RAM
            ram = psutil.virtual_memory()
            ram_percent = ram.percent
            ram_free_gb = ram.available / (1024**3)
            
            # Procesos de Neuro-OS
            neuro_processes = self.get_neuro_processes()
            total_neuro_ram = sum(p.memory_info().rss for p in neuro_processes) / (1024**3)
            
            # Determinar estado
            status = "OK"
            warnings = []
            
            if cpu_percent > self.MAX_CPU_USAGE:
                status = "WARNING"
                warnings.append(f"CPU usage too high: {cpu_percent:.1f}%")
            
            if ram_percent > self.MAX_RAM_USAGE:
                status = "CRITICAL"
                warnings.append(f"RAM usage critical: {ram_percent:.1f}%")
            
            if ram_free_gb < self.MIN_FREE_RAM_GB:
                status = "CRITICAL"
                warnings.append(f"Low free RAM: {ram_free_gb:.2f} GB")
            
            if total_neuro_ram > self.MAX_PROCESS_RAM_GB:
                status = "WARNING"
                warnings.append(f"Neuro-OS using too much RAM: {total_neuro_ram:.2f} GB")
            
            return {
                'status': status,
                'cpu_percent': cpu_percent,
                'ram_percent': ram_percent,
                'ram_free_gb': ram_free_gb,
                'neuro_ram_gb': total_neuro_ram,
                'warnings': warnings
            }
        
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return {'status': 'ERROR', 'warnings': [str(e)]}
    
    def get_neuro_processes(self):
        """Obtener procesos de Neuro-OS"""
        neuro_procs = []
        try:
            current_pid = psutil.Process().pid
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    # Buscar procesos de Python relacionados con Neuro-OS
                    if proc.info['cmdline']:
                        cmdline = ' '.join(proc.info['cmdline']).lower()
                        if 'neuro' in cmdline or proc.info['pid'] == current_pid:
                            neuro_procs.append(proc)
                except:
                    pass
        except:
            pass
        
        return neuro_procs
    
    def apply_emergency_limits(self):
        """Aplicar límites de emergencia"""
        if not self.enabled:
            return
        
        try:
            neuro_procs = self.get_neuro_processes()
            
            for proc in neuro_procs:
                try:
                    # Reducir prioridad
                    proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS if sys.platform == 'win32' else 10)
                    
                    # Limitar afinidad de CPU (usar solo mitad de cores)
                    cpu_count = psutil.cpu_count()
                    if cpu_count > 2:
                        proc.cpu_affinity(list(range(cpu_count // 2)))
                    
                    logging.warning(f"Emergency limits applied to PID {proc.pid}")
                
                except:
                    pass
            
            self.emergency_mode = True
            
        except Exception as e:
            logging.error(f"Failed to apply emergency limits: {e}")
    
    def restore_normal_mode(self):
        """Restaurar modo normal"""
        if not self.emergency_mode:
            return
        
        try:
            neuro_procs = self.get_neuro_processes()
            
            for proc in neuro_procs:
                try:
                    # Restaurar prioridad normal
                    proc.nice(psutil.NORMAL_PRIORITY_CLASS if sys.platform == 'win32' else 0)
                    
                    # Restaurar afinidad completa
                    cpu_count = psutil.cpu_count()
                    proc.cpu_affinity(list(range(cpu_count)))
                    
                except:
                    pass
            
            self.emergency_mode = False
            logging.info("Normal mode restored")
        
        except Exception as e:
            logging.error(f"Failed to restore normal mode: {e}")
    
    def monitor_and_protect(self):
        """Monitorear y proteger (llamar periódicamente)"""
        if not self.enabled:
            return
        
        health = self.check_system_health()
        
        if health['status'] == 'CRITICAL':
            self.warnings_count += 1
            logging.warning(f"CRITICAL: {health['warnings']}")
            
            # Aplicar límites de emergencia
            if self.warnings_count >= 3:
                self.apply_emergency_limits()
        
        elif health['status'] == 'WARNING':
            logging.warning(f"WARNING: {health['warnings']}")
        
        elif health['status'] == 'OK' and self.emergency_mode:
            # Sistema recuperado, restaurar modo normal
            self.warnings_count = 0
            self.restore_normal_mode()
        
        return health
    
    def get_safe_limits(self) -> dict:
        """Obtener límites seguros recomendados"""
        ram = psutil.virtual_memory()
        cpu_count = psutil.cpu_count()
        
        return {
            'max_cpu_percent': self.MAX_CPU_USAGE,
            'max_ram_percent': self.MAX_RAM_USAGE,
            'max_ram_gb': (ram.total / (1024**3)) * (self.MAX_RAM_USAGE / 100),
            'recommended_cpu_cores': max(1, cpu_count // 2),
            'min_free_ram_gb': self.MIN_FREE_RAM_GB
        }


if __name__ == "__main__":
    print("=== CRASH PROTECTION TEST ===\n")
    
    protection = CrashProtection()
    
    # Check system health
    health = protection.check_system_health()
    
    print("System Health:")
    print(f"  Status: {health['status']}")
    print(f"  CPU: {health.get('cpu_percent', 0):.1f}%")
    print(f"  RAM: {health.get('ram_percent', 0):.1f}%")
    print(f"  Free RAM: {health.get('ram_free_gb', 0):.2f} GB")
    print(f"  Neuro-OS RAM: {health.get('neuro_ram_gb', 0):.2f} GB")
    
    if health.get('warnings'):
        print("\nWarnings:")
        for warning in health['warnings']:
            print(f"  - {warning}")
    
    # Safe limits
    limits = protection.get_safe_limits()
    print("\n\nSafe Limits:")
    print(f"  Max CPU: {limits['max_cpu_percent']}%")
    print(f"  Max RAM: {limits['max_ram_percent']}% ({limits['max_ram_gb']:.1f} GB)")
    print(f"  Recommended CPU cores: {limits['recommended_cpu_cores']}")
    print(f"  Min free RAM: {limits['min_free_ram_gb']} GB")
