#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 NEURO-OS PERFORMANCE BENCHMARK SUITE
========================================
Mide y compara el rendimiento del sistema Neuro-OS Desktop
"""

import sys
import io
import time
import psutil
import json
from datetime import datetime
from pathlib import Path

# Fix UTF-8 encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class NeuroOSBenchmark:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'system_info': {},
            'benchmarks': {}
        }
        self.process = None
        
    def get_system_info(self):
        """Recopila información del sistema"""
        print("📊 Recopilando información del sistema...")
        
        cpu_freq = psutil.cpu_freq()
        mem = psutil.virtual_memory()
        
        self.results['system_info'] = {
            'cpu_count': psutil.cpu_count(logical=False),
            'cpu_threads': psutil.cpu_count(logical=True),
            'cpu_freq_max': f"{cpu_freq.max:.0f} MHz" if cpu_freq else "N/A",
            'cpu_freq_current': f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A",
            'ram_total_gb': f"{mem.total / (1024**3):.2f} GB",
            'ram_available_gb': f"{mem.available / (1024**3):.2f} GB",
            'platform': sys.platform,
            'python_version': sys.version.split()[0]
        }
        
        print("✅ Sistema detectado:")
        for key, value in self.results['system_info'].items():
            print(f"   • {key}: {value}")
    
    def benchmark_idle_resources(self, duration=10):
        """Mide consumo de recursos en estado idle"""
        print(f"\n🔍 Midiendo consumo en IDLE durante {duration}s...")
        
        cpu_samples = []
        ram_samples = []
        
        start_time = time.time()
        while time.time() - start_time < duration:
            cpu_samples.append(psutil.cpu_percent(interval=0.5))
            ram_samples.append(psutil.virtual_memory().percent)
        
        self.results['benchmarks']['idle_state'] = {
            'cpu_avg': f"{sum(cpu_samples) / len(cpu_samples):.2f}%",
            'cpu_min': f"{min(cpu_samples):.2f}%",
            'cpu_max': f"{max(cpu_samples):.2f}%",
            'ram_avg': f"{sum(ram_samples) / len(ram_samples):.2f}%",
            'ram_min': f"{min(ram_samples):.2f}%",
            'ram_max': f"{max(ram_samples):.2f}%",
            'duration_s': duration
        }
        
        print(f"   ✅ CPU promedio: {self.results['benchmarks']['idle_state']['cpu_avg']}")
        print(f"   ✅ RAM promedio: {self.results['benchmarks']['idle_state']['ram_avg']}")
    
    def benchmark_neuro_os_launch(self):
        """Mide tiempo de arranque y consumo de Neuro-OS"""
        print("\n🚀 Iniciando Neuro-OS Desktop para benchmark...")
        
        import subprocess
        
        # Medir recursos antes del lanzamiento
        mem_before = psutil.virtual_memory().used / (1024**2)  # MB
        
        start_time = time.time()
        
        # Lanzar Neuro-OS en modo headless (sin mostrar ventana)
        proc = subprocess.Popen(
            [sys.executable, 'src/NEURO_OS_MASTER.py'],
            cwd='C:/Users/cyber/Documents/NeuroOs/Neuro-OS-Genesis/Neuro-OS-Desktop-Release',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )
        
        # Esperar a que el proceso se estabilice
        time.sleep(3)
        
        launch_time = time.time() - start_time
        
        # Obtener el proceso de Python que ejecuta Neuro-OS
        try:
            neuro_proc = psutil.Process(proc.pid)
            
            # Esperar 5 segundos para medir consumo estable
            time.sleep(5)
            
            cpu_samples = []
            mem_samples = []
            
            for _ in range(10):
                cpu_samples.append(neuro_proc.cpu_percent(interval=0.5))
                mem_info = neuro_proc.memory_info()
                mem_samples.append(mem_info.rss / (1024**2))  # MB
            
            mem_after = psutil.virtual_memory().used / (1024**2)  # MB
            
            self.results['benchmarks']['neuro_os_launch'] = {
                'launch_time_s': f"{launch_time:.3f}",
                'cpu_avg': f"{sum(cpu_samples) / len(cpu_samples):.2f}%",
                'cpu_peak': f"{max(cpu_samples):.2f}%",
                'ram_process_avg_mb': f"{sum(mem_samples) / len(mem_samples):.2f}",
                'ram_process_peak_mb': f"{max(mem_samples):.2f}",
                'ram_system_delta_mb': f"{mem_after - mem_before:.2f}",
                'pid': proc.pid
            }
            
            print(f"   ✅ Tiempo de arranque: {self.results['benchmarks']['neuro_os_launch']['launch_time_s']}s")
            print(f"   ✅ CPU promedio: {self.results['benchmarks']['neuro_os_launch']['cpu_avg']}")
            print(f"   ✅ RAM del proceso: {self.results['benchmarks']['neuro_os_launch']['ram_process_avg_mb']} MB")
            
            # Terminar el proceso
            proc.terminate()
            proc.wait(timeout=5)
            
        except Exception as e:
            print(f"   ⚠️ Error midiendo proceso: {e}")
            proc.terminate()
    
    def benchmark_stress_test(self, duration=30):
        """Simula carga pesada y mide rendimiento"""
        print(f"\n⚡ Ejecutando stress test durante {duration}s...")
        
        cpu_samples = []
        ram_samples = []
        
        start_time = time.time()
        
        # Simular carga
        import threading
        
        def cpu_load():
            end = time.time() + duration
            while time.time() < end:
                _ = sum(i*i for i in range(10000))
        
        # Lanzar threads de carga
        threads = [threading.Thread(target=cpu_load) for _ in range(2)]
        for t in threads:
            t.start()
        
        # Medir mientras corre el stress
        while time.time() - start_time < duration:
            cpu_samples.append(psutil.cpu_percent(interval=0.5))
            ram_samples.append(psutil.virtual_memory().percent)
        
        for t in threads:
            t.join()
        
        self.results['benchmarks']['stress_test'] = {
            'duration_s': duration,
            'cpu_avg': f"{sum(cpu_samples) / len(cpu_samples):.2f}%",
            'cpu_peak': f"{max(cpu_samples):.2f}%",
            'ram_avg': f"{sum(ram_samples) / len(ram_samples):.2f}%",
            'ram_peak': f"{max(ram_samples):.2f}%"
        }
        
        print(f"   ✅ CPU promedio bajo carga: {self.results['benchmarks']['stress_test']['cpu_avg']}")
        print(f"   ✅ CPU pico: {self.results['benchmarks']['stress_test']['cpu_peak']}")
    
    def save_results(self):
        """Guarda resultados en JSON"""
        output_file = Path('benchmark_results.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultados guardados en: {output_file.absolute()}")
        
        # También crear un reporte legible
        self.create_report()
    
    def create_report(self):
        """Crea un reporte en markdown"""
        report_file = Path('benchmark_report.md')
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# 🧪 NEURO-OS PERFORMANCE BENCHMARK REPORT\n\n")
            f.write(f"**Fecha:** {self.results['timestamp']}\n\n")
            
            f.write("## 📊 Información del Sistema\n\n")
            f.write("| Métrica | Valor |\n")
            f.write("|---------|-------|\n")
            for key, value in self.results['system_info'].items():
                f.write(f"| {key} | {value} |\n")
            
            f.write("\n## 🔍 Resultados de Benchmarks\n\n")
            
            for bench_name, bench_data in self.results['benchmarks'].items():
                f.write(f"### {bench_name.replace('_', ' ').title()}\n\n")
                f.write("| Métrica | Valor |\n")
                f.write("|---------|-------|\n")
                for key, value in bench_data.items():
                    f.write(f"| {key} | {value} |\n")
                f.write("\n")
            
            f.write("\n---\n")
            f.write("*Generado por Neuro-OS Benchmark Suite*\n")
        
        print(f"📄 Reporte generado en: {report_file.absolute()}")
    
    def run_all(self):
        """Ejecuta todos los benchmarks"""
        print("=" * 60)
        print("🧠 NEURO-OS PERFORMANCE BENCHMARK SUITE")
        print("=" * 60)
        
        self.get_system_info()
        self.benchmark_idle_resources(duration=10)
        self.benchmark_neuro_os_launch()
        self.benchmark_stress_test(duration=20)
        
        self.save_results()
        
        print("\n" + "=" * 60)
        print("✅ BENCHMARK COMPLETADO")
        print("=" * 60)

if __name__ == '__main__':
    benchmark = NeuroOSBenchmark()
    benchmark.run_all()
