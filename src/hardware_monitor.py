#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌡️ HARDWARE MONITOR
Monitoreo de temperatura, ventiladores y gestión térmica
"""

import sys
from typing import Dict, List, Optional

class HardwareMonitor:
    """Monitor de hardware (temperatura, ventiladores, etc.)"""
    
    def __init__(self):
        self.sensors_available = self.check_sensors()
    
    def check_sensors(self) -> bool:
        """Verificar si hay sensores disponibles"""
        try:
            import psutil
            # Intentar leer temperaturas
            temps = psutil.sensors_temperatures()
            return len(temps) > 0
        except:
            return False
    
    def get_cpu_temperature(self) -> Optional[float]:
        """Obtener temperatura de CPU en °C"""
        try:
            import psutil
            temps = psutil.sensors_temperatures()
            
            # Buscar sensor de CPU (varía según el sistema)
            for name, entries in temps.items():
                if 'coretemp' in name.lower() or 'cpu' in name.lower():
                    if entries:
                        # Retornar la temperatura más alta
                        return max(entry.current for entry in entries)
            
            # Si no encuentra específico de CPU, retornar el primero disponible
            for name, entries in temps.items():
                if entries:
                    return entries[0].current
            
            return None
        except:
            return None
    
    def get_gpu_temperature(self) -> Optional[float]:
        """Obtener temperatura de GPU en °C"""
        try:
            # Intentar con NVIDIA
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            pynvml.nvmlShutdown()
            return float(temp)
        except:
            pass
        
        try:
            # Intentar con psutil
            import psutil
            temps = psutil.sensors_temperatures()
            for name, entries in temps.items():
                if 'gpu' in name.lower() or 'radeon' in name.lower():
                    if entries:
                        return entries[0].current
        except:
            pass
        
        return None
    
    def get_fan_speeds(self) -> Dict[str, int]:
        """Obtener velocidades de ventiladores en RPM"""
        fans = {}
        
        try:
            import psutil
            fan_data = psutil.sensors_fans()
            
            for name, entries in fan_data.items():
                for i, entry in enumerate(entries):
                    fan_name = f"{name}_{i}" if len(entries) > 1 else name
                    fans[fan_name] = entry.current
        except:
            pass
        
        return fans
    
    def get_thermal_status(self) -> Dict:
        """Obtener estado térmico completo"""
        cpu_temp = self.get_cpu_temperature()
        gpu_temp = self.get_gpu_temperature()
        fans = self.get_fan_speeds()
        
        # Determinar estado térmico
        status = "Normal"
        color = "#0f0"  # Verde
        
        if cpu_temp:
            if cpu_temp > 80:
                status = "Hot"
                color = "#f00"  # Rojo
            elif cpu_temp > 70:
                status = "Warm"
                color = "#ff0"  # Amarillo
        
        return {
            'cpu_temp': cpu_temp,
            'gpu_temp': gpu_temp,
            'fans': fans,
            'status': status,
            'color': color,
            'sensors_available': self.sensors_available
        }
    
    def get_thermal_profile(self, profile_name: str) -> Dict:
        """Obtener perfil térmico"""
        profiles = {
            'Silent': {
                'max_temp': 75,
                'target_temp': 65,
                'fan_curve': 'quiet',
                'description': 'Prioriza silencio, permite temperaturas más altas'
            },
            'Balanced': {
                'max_temp': 70,
                'target_temp': 60,
                'fan_curve': 'balanced',
                'description': 'Balance entre rendimiento y ruido'
            },
            'Performance': {
                'max_temp': 65,
                'target_temp': 55,
                'fan_curve': 'aggressive',
                'description': 'Máximo rendimiento, ventiladores más rápidos'
            },
            'Gaming': {
                'max_temp': 68,
                'target_temp': 58,
                'fan_curve': 'gaming',
                'description': 'Optimizado para gaming, balance performance/temperatura'
            }
        }
        
        return profiles.get(profile_name, profiles['Balanced'])


if __name__ == "__main__":
    print("=== HARDWARE MONITOR TEST ===\n")
    
    monitor = HardwareMonitor()
    
    # Estado térmico
    thermal = monitor.get_thermal_status()
    
    print("Thermal Status:")
    print(f"  CPU Temperature: {thermal['cpu_temp']}°C" if thermal['cpu_temp'] else "  CPU Temperature: N/A")
    print(f"  GPU Temperature: {thermal['gpu_temp']}°C" if thermal['gpu_temp'] else "  GPU Temperature: N/A")
    print(f"  Status: {thermal['status']}")
    
    if thermal['fans']:
        print("\nFan Speeds:")
        for fan_name, rpm in thermal['fans'].items():
            print(f"  {fan_name}: {rpm} RPM")
    else:
        print("\nFan Speeds: N/A")
    
    # Perfiles térmicos
    print("\n\nThermal Profiles:")
    for profile_name in ['Silent', 'Balanced', 'Performance', 'Gaming']:
        profile = monitor.get_thermal_profile(profile_name)
        print(f"\n  {profile_name}:")
        print(f"    Max Temp: {profile['max_temp']}°C")
        print(f"    Target: {profile['target_temp']}°C")
        print(f"    {profile['description']}")
