#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 NEURO-AI SERVICE
Servicio de IA que optimiza en tiempo real automáticamente en segundo plano
"""

import threading
import time
from typing import Optional
from neuro_ai_optimizer import NeuroAI, BottleneckType

class NeuroAIService:
    """Servicio de IA que corre en segundo plano"""
    
    def __init__(self):
        self.ai = NeuroAI()
        self.running = False
        self.thread: Optional[threading.Thread] = None
        
        # Configuración
        self.monitor_interval = 2.0  # Segundos entre análisis
        self.auto_optimize = True
        
        # Estado actual
        self.current_recommendations = None
        self.last_optimization_time = 0
        self.optimization_cooldown = 5.0  # Segundos entre optimizaciones
    
    def start(self):
        """Iniciar servicio de IA en segundo plano"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("[AI Service] Started in background")
    
    def stop(self):
        """Detener servicio de IA"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5.0)
        print("[AI Service] Stopped")
    
    def _monitor_loop(self):
        """Loop de monitoreo en segundo plano"""
        while self.running:
            try:
                # Analizar sistema
                recommendations = self.ai.auto_optimize(current_fps=None)
                self.current_recommendations = recommendations
                
                # Aplicar optimizaciones automáticamente si está habilitado
                if self.auto_optimize:
                    self._apply_optimizations(recommendations)
                
                # Esperar antes del próximo análisis
                time.sleep(self.monitor_interval)
            
            except Exception as e:
                print(f"[AI Service] Error in monitor loop: {e}")
                time.sleep(self.monitor_interval)
    
    def _apply_optimizations(self, recommendations: dict):
        """Aplicar optimizaciones automáticamente"""
        # Verificar cooldown
        current_time = time.time()
        if current_time - self.last_optimization_time < self.optimization_cooldown:
            return
        
        bottleneck = recommendations.get('bottleneck')
        
        # Optimizar RAM si hay cuello de botella
        if bottleneck in ['ram', 'mixed'] and recommendations.get('ram_optimization'):
            ram_opt = recommendations['ram_optimization']
            if ram_opt.get('actions'):
                print(f"[AI Service] Auto-optimizing RAM: {len(ram_opt['actions'])} actions")
                self.last_optimization_time = current_time
        
        # Ajustar resolución si FPS es bajo
        # (Esto se aplicaría al juego activo, por ahora solo registramos)
        preset = recommendations.get('recommended_preset')
        if preset:
            print(f"[AI Service] Recommended preset: {preset}")
    
    def get_status(self) -> dict:
        """Obtener estado actual del servicio"""
        return {
            'running': self.running,
            'auto_optimize': self.auto_optimize,
            'monitor_interval': self.monitor_interval,
            'current_recommendations': self.current_recommendations
        }
    
    def set_auto_optimize(self, enabled: bool):
        """Activar/desactivar optimización automática"""
        self.auto_optimize = enabled
        print(f"[AI Service] Auto-optimize: {enabled}")
    
    def set_monitor_interval(self, seconds: float):
        """Cambiar intervalo de monitoreo"""
        self.monitor_interval = max(1.0, seconds)
        print(f"[AI Service] Monitor interval: {self.monitor_interval}s")


# Instancia global del servicio
_ai_service: Optional[NeuroAIService] = None

def get_ai_service() -> NeuroAIService:
    """Obtener instancia global del servicio de IA"""
    global _ai_service
    if _ai_service is None:
        _ai_service = NeuroAIService()
    return _ai_service

def start_ai_service():
    """Iniciar servicio de IA global"""
    service = get_ai_service()
    service.start()
    return service

def stop_ai_service():
    """Detener servicio de IA global"""
    global _ai_service
    if _ai_service:
        _ai_service.stop()
        _ai_service = None


if __name__ == "__main__":
    print("=" * 60)
    print("NEURO-AI SERVICE TEST")
    print("=" * 60)
    print()
    
    # Iniciar servicio
    service = start_ai_service()
    
    print("AI Service running in background...")
    print("Monitoring system every 2 seconds...")
    print()
    
    # Dejar correr por 10 segundos
    try:
        for i in range(5):
            time.sleep(2)
            status = service.get_status()
            if status['current_recommendations']:
                rec = status['current_recommendations']
                print(f"[{i*2}s] Bottleneck: {rec.get('bottleneck', 'N/A')}, "
                      f"Preset: {rec.get('recommended_preset', 'N/A')}")
    
    except KeyboardInterrupt:
        print("\nStopping...")
    
    # Detener servicio
    stop_ai_service()
    
    print("\n" + "=" * 60)
    print("AI SERVICE TEST COMPLETED")
    print("=" * 60)
