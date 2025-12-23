#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 NEURO-OS BENCHMARK SUITE
Sistema de benchmarking veraz para medir mejoras reales de rendimiento
"""

import time
import json
import psutil
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List

class NeuroBenchmark:
    """Suite de benchmarks para Neuro-OS Desktop"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.get_system_info(),
            'benchmarks': {}
        }
    
    def get_system_info(self) -> Dict:
        """Obtener información del sistema"""
        import platform
        
        return {
            'os': platform.system(),
            'os_version': platform.version(),
            'cpu': platform.processor(),
            'cpu_cores': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'ram_total_gb': psutil.virtual_memory().total / (1024**3),
            'python_version': platform.python_version()
        }
    
    def benchmark_cpu_usage(self, duration_seconds: int = 10) -> Dict:
        """
        Benchmark de uso de CPU
        Mide CPU idle vs con Neuro-OS activo
        """
        print(f"[Benchmark] CPU Usage Test ({duration_seconds}s)...")
        
        cpu_samples = []
        start_time = time.time()
        
        while time.time() - start_time < duration_seconds:
            cpu_samples.append(psutil.cpu_percent(interval=0.5))
        
        return {
            'avg_cpu_percent': np.mean(cpu_samples),
            'max_cpu_percent': np.max(cpu_samples),
            'min_cpu_percent': np.min(cpu_samples),
            'std_cpu_percent': np.std(cpu_samples)
        }
    
    def benchmark_ram_usage(self) -> Dict:
        """
        Benchmark de uso de RAM
        Mide consumo de memoria de Neuro-OS
        """
        print("[Benchmark] RAM Usage Test...")
        
        ram = psutil.virtual_memory()
        
        # Obtener procesos de Neuro-OS
        neuro_ram = 0
        try:
            current_process = psutil.Process()
            neuro_ram = current_process.memory_info().rss / (1024**3)
        except:
            pass
        
        return {
            'total_ram_gb': ram.total / (1024**3),
            'used_ram_gb': ram.used / (1024**3),
            'free_ram_gb': ram.available / (1024**3),
            'ram_percent': ram.percent,
            'neuro_os_ram_gb': neuro_ram
        }
    
    def benchmark_upscaling_performance(self) -> Dict:
        """
        Benchmark de upscaling
        Mide velocidad de upscaling con diferentes métodos
        """
        print("[Benchmark] Upscaling Performance Test...")
        
        import cv2
        
        # Crear imagen de prueba (1080p)
        test_image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        target_size = (3840, 2160)  # 4K
        iterations = 20
        
        results = {}
        
        # Test 1: CPU - INTER_LINEAR (FAST)
        start = time.time()
        for _ in range(iterations):
            _ = cv2.resize(test_image, target_size, interpolation=cv2.INTER_LINEAR)
        time_linear = (time.time() - start) / iterations
        results['cpu_linear_ms'] = time_linear * 1000
        results['cpu_linear_fps'] = 1.0 / time_linear if time_linear > 0 else 0
        
        # Test 2: CPU - INTER_CUBIC (BALANCED)
        start = time.time()
        for _ in range(iterations):
            _ = cv2.resize(test_image, target_size, interpolation=cv2.INTER_CUBIC)
        time_cubic = (time.time() - start) / iterations
        results['cpu_cubic_ms'] = time_cubic * 1000
        results['cpu_cubic_fps'] = 1.0 / time_cubic if time_cubic > 0 else 0
        
        # Test 3: CPU - INTER_LANCZOS4 (QUALITY)
        start = time.time()
        for _ in range(iterations):
            _ = cv2.resize(test_image, target_size, interpolation=cv2.INTER_LANCZOS4)
        time_lanczos = (time.time() - start) / iterations
        results['cpu_lanczos_ms'] = time_lanczos * 1000
        results['cpu_lanczos_fps'] = 1.0 / time_lanczos if time_lanczos > 0 else 0
        
        # Test 4: GPU (si está disponible)
        try:
            from gpu_accelerator import GPUAccelerator
            gpu = GPUAccelerator()
            
            if gpu.acceleration_available:
                start = time.time()
                for _ in range(iterations):
                    _ = gpu.upscale_with_gpu(test_image, target_size)
                time_gpu = (time.time() - start) / iterations
                results['gpu_ms'] = time_gpu * 1000
                results['gpu_fps'] = 1.0 / time_gpu if time_gpu > 0 else 0
                results['gpu_speedup'] = time_cubic / time_gpu if time_gpu > 0 else 1.0
        except:
            results['gpu_available'] = False
        
        return results
    
    def benchmark_startup_time(self) -> Dict:
        """
        Benchmark de tiempo de inicio
        Mide cuánto tarda en iniciar Neuro-OS
        """
        print("[Benchmark] Startup Time Test...")
        
        # Este benchmark debe ejecutarse al inicio de la app
        # Por ahora retornamos placeholder
        return {
            'startup_time_ms': 0,
            'note': 'Run at app startup to measure'
        }
    
    def benchmark_game_boost(self, game_name: str = "Test Game") -> Dict:
        """
        Benchmark de boost de juegos
        Mide mejora de FPS con optimizaciones
        
        NOTA: Requiere juego real para medición precisa
        """
        print(f"[Benchmark] Game Boost Test - {game_name}...")
        
        return {
            'game': game_name,
            'baseline_fps': 0,
            'optimized_fps': 0,
            'fps_improvement': 0,
            'note': 'Requires real game for accurate measurement'
        }
    
    def run_all_benchmarks(self) -> Dict:
        """Ejecutar todos los benchmarks"""
        print("=" * 60)
        print("NEURO-OS BENCHMARK SUITE")
        print("=" * 60)
        print()
        
        # CPU
        self.results['benchmarks']['cpu'] = self.benchmark_cpu_usage(duration_seconds=5)
        
        # RAM
        self.results['benchmarks']['ram'] = self.benchmark_ram_usage()
        
        # Upscaling
        self.results['benchmarks']['upscaling'] = self.benchmark_upscaling_performance()
        
        # Startup
        self.results['benchmarks']['startup'] = self.benchmark_startup_time()
        
        print()
        print("=" * 60)
        print("BENCHMARK COMPLETED")
        print("=" * 60)
        
        return self.results
    
    def save_results(self, filename: str = "benchmark_results.json"):
        """Guardar resultados en JSON"""
        output_path = Path(filename)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\nResults saved to: {output_path.absolute()}")
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        
        # System Info
        print("\nSystem Information:")
        sys_info = self.results['system_info']
        print(f"  CPU: {sys_info['cpu']}")
        print(f"  Cores: {sys_info['cpu_cores']} | Threads: {sys_info['cpu_threads']}")
        print(f"  RAM: {sys_info['ram_total_gb']:.1f} GB")
        
        # CPU Usage
        if 'cpu' in self.results['benchmarks']:
            cpu = self.results['benchmarks']['cpu']
            print("\nCPU Usage:")
            print(f"  Average: {cpu['avg_cpu_percent']:.1f}%")
            print(f"  Max: {cpu['max_cpu_percent']:.1f}%")
        
        # RAM Usage
        if 'ram' in self.results['benchmarks']:
            ram = self.results['benchmarks']['ram']
            print("\nRAM Usage:")
            print(f"  System: {ram['ram_percent']:.1f}% ({ram['used_ram_gb']:.1f} GB)")
            print(f"  Neuro-OS: {ram['neuro_os_ram_gb']:.2f} GB")
        
        # Upscaling
        if 'upscaling' in self.results['benchmarks']:
            up = self.results['benchmarks']['upscaling']
            print("\nUpscaling Performance (1080p → 4K):")
            print(f"  CPU Linear:  {up['cpu_linear_ms']:.1f} ms ({up['cpu_linear_fps']:.1f} FPS)")
            print(f"  CPU Cubic:   {up['cpu_cubic_ms']:.1f} ms ({up['cpu_cubic_fps']:.1f} FPS)")
            print(f"  CPU Lanczos: {up['cpu_lanczos_ms']:.1f} ms ({up['cpu_lanczos_fps']:.1f} FPS)")
            
            if 'gpu_ms' in up:
                print(f"  GPU:         {up['gpu_ms']:.1f} ms ({up['gpu_fps']:.1f} FPS)")
                print(f"  GPU Speedup: {up['gpu_speedup']:.2f}x faster")


if __name__ == "__main__":
    # Ejecutar benchmark
    benchmark = NeuroBenchmark()
    results = benchmark.run_all_benchmarks()
    
    # Mostrar resumen
    benchmark.print_summary()
    
    # Guardar resultados
    benchmark.save_results("neuro_os_benchmark_results.json")
    
    print("\n✅ Benchmark completed successfully!")
