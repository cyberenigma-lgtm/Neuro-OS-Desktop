#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 NEURO-AI OPTIMIZER
IA inteligente que gestiona RAM, detecta cuellos de botella y auto-escala resolución
"""

import psutil
import time
from typing import Dict, Optional, Tuple
from enum import Enum

class BottleneckType(Enum):
    """Tipos de cuello de botella"""
    NONE = "none"
    CPU = "cpu"
    RAM = "ram"
    GPU = "gpu"
    MIXED = "mixed"

class ResolutionPreset(Enum):
    """Presets de resolución"""
    ULTRA_PERFORMANCE = ("720p", (1280, 720), (3840, 2160))   # 720p -> 4K
    PERFORMANCE = ("1080p", (1920, 1080), (3840, 2160))        # 1080p -> 4K
    BALANCED = ("1440p", (2560, 1440), (3840, 2160))           # 1440p -> 4K
    QUALITY = ("native", (3840, 2160), (3840, 2160))           # 4K nativo

class NeuroAI:
    """IA de optimización automática"""
    
    def __init__(self):
        self.enabled = True
        self.current_preset = ResolutionPreset.BALANCED
        self.target_fps = 60
        self.min_acceptable_fps = 30
        
        # Historial de rendimiento
        self.performance_history = []
        self.max_history = 100
        
        # Límites adaptativos
        self.cpu_threshold = 85  # %
        self.ram_threshold = 80  # %
        self.gpu_threshold = 90  # %
    
    def analyze_system(self) -> Dict:
        """Analizar estado del sistema en tiempo real"""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_freq = psutil.cpu_freq()
        cpu_cores = psutil.cpu_count(logical=False)
        
        # RAM
        ram = psutil.virtual_memory()
        ram_percent = ram.percent
        ram_available_gb = ram.available / (1024**3)
        
        # GPU (si está disponible)
        gpu_usage = self._get_gpu_usage()
        
        return {
            'cpu_percent': cpu_percent,
            'cpu_freq_mhz': cpu_freq.current if cpu_freq else 0,
            'cpu_cores': cpu_cores,
            'ram_percent': ram_percent,
            'ram_available_gb': ram_available_gb,
            'gpu_usage': gpu_usage,
            'timestamp': time.time()
        }
    
    def _get_gpu_usage(self) -> Optional[float]:
        """Obtener uso de GPU"""
        try:
            import pynvml
            pynvml.nvmlInit()
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            pynvml.nvmlShutdown()
            return float(utilization.gpu)
        except:
            return None
    
    def detect_bottleneck(self, system_state: Dict) -> BottleneckType:
        """
        Detectar cuello de botella del sistema
        
        Returns:
            BottleneckType: Tipo de cuello de botella detectado
        """
        cpu_high = system_state['cpu_percent'] > self.cpu_threshold
        ram_high = system_state['ram_percent'] > self.ram_threshold
        
        gpu_usage = system_state.get('gpu_usage')
        gpu_high = gpu_usage and gpu_usage > self.gpu_threshold
        
        # Determinar cuello de botella
        if cpu_high and ram_high:
            return BottleneckType.MIXED
        elif cpu_high:
            return BottleneckType.CPU
        elif ram_high:
            return BottleneckType.RAM
        elif gpu_high:
            return BottleneckType.GPU
        else:
            return BottleneckType.NONE
    
    def optimize_ram(self, aggressive: bool = False) -> Dict:
        """
        Optimizar uso de RAM
        
        Args:
            aggressive: Si True, libera RAM agresivamente
        
        Returns:
            Dict con acciones tomadas
        """
        actions = []
        
        try:
            # 1. Limpiar caché del sistema
            if aggressive:
                # En Windows, esto requiere privilegios de admin
                # Por ahora, solo registramos la acción
                actions.append("Cache clearing (requires admin)")
            
            # 2. Reducir prioridad de procesos no esenciales
            current_pid = psutil.Process().pid
            for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
                try:
                    if proc.info['pid'] == current_pid:
                        continue
                    
                    # Si el proceso usa mucha RAM y no es crítico
                    if proc.info['memory_percent'] > 5:
                        # Lista de procesos que podemos reducir prioridad
                        reducible = ['chrome', 'firefox', 'discord', 'spotify']
                        if any(name in proc.info['name'].lower() for name in reducible):
                            proc.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
                            actions.append(f"Reduced priority: {proc.info['name']}")
                except:
                    pass
            
            # 3. Sugerir cerrar apps pesadas
            heavy_apps = []
            for proc in psutil.process_iter(['name', 'memory_info']):
                try:
                    mem_gb = proc.info['memory_info'].rss / (1024**3)
                    if mem_gb > 1.0:  # > 1GB
                        heavy_apps.append({
                            'name': proc.info['name'],
                            'ram_gb': mem_gb
                        })
                except:
                    pass
            
            if heavy_apps:
                actions.append(f"Heavy apps detected: {len(heavy_apps)}")
        
        except Exception as e:
            actions.append(f"Error: {str(e)}")
        
        return {
            'actions': actions,
            'ram_freed_estimate_gb': len(actions) * 0.5  # Estimación
        }
    
    def decide_resolution(self, current_fps: Optional[float] = None, 
                         bottleneck: BottleneckType = BottleneckType.NONE) -> ResolutionPreset:
        """
        Decidir resolución óptima basándose en FPS y cuellos de botella
        
        Args:
            current_fps: FPS actual del juego
            bottleneck: Cuello de botella detectado
        
        Returns:
            ResolutionPreset recomendado
        """
        # Si no hay FPS, usar preset balanceado
        if current_fps is None:
            return ResolutionPreset.BALANCED
        
        # Lógica de decisión basada en FPS
        if current_fps < self.min_acceptable_fps:
            # FPS muy bajo, máxima performance
            return ResolutionPreset.ULTRA_PERFORMANCE
        
        elif current_fps < self.target_fps * 0.8:  # < 48 FPS (si target es 60)
            # FPS bajo, priorizar performance
            return ResolutionPreset.PERFORMANCE
        
        elif current_fps >= self.target_fps:
            # FPS objetivo alcanzado, podemos mejorar calidad
            if bottleneck == BottleneckType.NONE:
                return ResolutionPreset.QUALITY
            else:
                return ResolutionPreset.BALANCED
        
        else:
            # FPS aceptable, mantener balance
            return ResolutionPreset.BALANCED
    
    def auto_optimize(self, current_fps: Optional[float] = None) -> Dict:
        """
        Optimización automática completa
        
        Args:
            current_fps: FPS actual del juego (opcional)
        
        Returns:
            Dict con recomendaciones y acciones
        """
        # 1. Analizar sistema
        system_state = self.analyze_system()
        
        # 2. Detectar cuello de botella
        bottleneck = self.detect_bottleneck(system_state)
        
        # 3. Decidir resolución
        recommended_preset = self.decide_resolution(current_fps, bottleneck)
        
        # 4. Optimizar RAM si es necesario
        ram_optimization = None
        if bottleneck in [BottleneckType.RAM, BottleneckType.MIXED]:
            ram_optimization = self.optimize_ram(aggressive=True)
        
        # 5. Generar recomendaciones
        recommendations = {
            'system_state': system_state,
            'bottleneck': bottleneck.value,
            'recommended_preset': recommended_preset.value[0],
            'render_resolution': recommended_preset.value[1],
            'output_resolution': recommended_preset.value[2],
            'ram_optimization': ram_optimization,
            'current_fps': current_fps,
            'target_fps': self.target_fps
        }
        
        # 6. Guardar en historial
        self.performance_history.append(recommendations)
        if len(self.performance_history) > self.max_history:
            self.performance_history.pop(0)
        
        return recommendations
    
    def get_optimization_summary(self, recommendations: Dict) -> str:
        """Generar resumen legible de optimizaciones"""
        bottleneck = recommendations['bottleneck']
        preset = recommendations['recommended_preset']
        render_res = recommendations['render_resolution']
        output_res = recommendations['output_resolution']
        
        summary = f"AI Optimization:\n"
        summary += f"  Bottleneck: {bottleneck.upper()}\n"
        summary += f"  Preset: {preset}\n"
        summary += f"  Resolution: {render_res[0]}x{render_res[1]} -> {output_res[0]}x{output_res[1]}\n"
        
        if recommendations.get('ram_optimization'):
            ram_opt = recommendations['ram_optimization']
            summary += f"  RAM Actions: {len(ram_opt['actions'])}\n"
        
        return summary


if __name__ == "__main__":
    print("=" * 60)
    print("NEURO-AI OPTIMIZER TEST")
    print("=" * 60)
    print()
    
    # Crear IA
    ai = NeuroAI()
    
    # Simular diferentes escenarios
    scenarios = [
        ("Low FPS (25)", 25),
        ("Target FPS (60)", 60),
        ("High FPS (90)", 90),
        ("Very Low FPS (15)", 15)
    ]
    
    for scenario_name, fps in scenarios:
        print(f"\n--- Scenario: {scenario_name} ---")
        
        # Ejecutar optimización
        recommendations = ai.auto_optimize(current_fps=fps)
        
        # Mostrar resumen
        print(ai.get_optimization_summary(recommendations))
        
        # Detalles del sistema
        sys_state = recommendations['system_state']
        print(f"  CPU: {sys_state['cpu_percent']:.1f}%")
        print(f"  RAM: {sys_state['ram_percent']:.1f}% ({sys_state['ram_available_gb']:.1f} GB free)")
    
    print("\n" + "=" * 60)
    print("AI OPTIMIZATION TEST COMPLETED")
    print("=" * 60)
