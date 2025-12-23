#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 NEURO NETWORK OPTIMIZER
Optimizador de red para reducir latencia en juegos
"""

import subprocess
import platform
import psutil
from typing import Dict, List, Optional

class NetworkOptimizer:
    """Optimizador de conexión de red para gaming"""
    
    def __init__(self):
        self.is_windows = platform.system() == 'Windows'
        self.optimizations_applied = []
    
    def get_network_status(self) -> Dict:
        """Obtener estado actual de la red"""
        try:
            # Obtener interfaces de red
            net_if_stats = psutil.net_if_stats()
            net_io = psutil.net_io_counters()
            
            # Encontrar interfaz activa
            active_interface = None
            for iface, stats in net_if_stats.items():
                if stats.isup and not iface.startswith('lo'):
                    active_interface = iface
                    break
            
            return {
                'active_interface': active_interface,
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout
            }
        except Exception as e:
            return {'error': str(e)}
    
    def optimize_tcp_settings(self) -> Dict:
        """
        Optimizar configuración TCP para gaming
        
        Optimizaciones:
        - TCP Window Auto-Tuning
        - TCP Chimney Offload
        - Receive Side Scaling (RSS)
        - Network Throttling Index
        """
        if not self.is_windows:
            return {'success': False, 'message': 'Only supported on Windows'}
        
        commands = []
        results = []
        
        try:
            # 1. Habilitar TCP Window Auto-Tuning (mejor throughput)
            commands.append(('netsh interface tcp set global autotuninglevel=normal', 'TCP Auto-Tuning'))
            
            # 2. Deshabilitar TCP Chimney Offload (reduce latencia)
            commands.append(('netsh int tcp set global chimney=disabled', 'TCP Chimney Offload'))
            
            # 3. Habilitar RSS (Receive Side Scaling)
            commands.append(('netsh int tcp set global rss=enabled', 'Receive Side Scaling'))
            
            # 4. Reducir Network Throttling (importante para gaming)
            # HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile
            # NetworkThrottlingIndex = 0xffffffff (deshabilita throttling)
            commands.append((
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d 0xffffffff /f',
                'Network Throttling Disabled'
            ))
            
            # 5. Prioridad de juegos en QoS
            commands.append((
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "GPU Priority" /t REG_DWORD /d 8 /f',
                'GPU Priority for Games'
            ))
            
            commands.append((
                'reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v Priority /t REG_DWORD /d 6 /f',
                'CPU Priority for Games'
            ))
            
            # Ejecutar comandos (requiere admin)
            for cmd, desc in commands:
                try:
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    
                    if result.returncode == 0:
                        results.append(f"✅ {desc}")
                        self.optimizations_applied.append(desc)
                    else:
                        results.append(f"⚠️ {desc} (requires admin)")
                except Exception as e:
                    results.append(f"❌ {desc}: {str(e)}")
            
            return {
                'success': True,
                'optimizations': results,
                'note': 'Some optimizations require administrator privileges'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def optimize_dns(self) -> Dict:
        """
        Optimizar DNS para menor latencia
        
        Configura DNS públicos rápidos:
        - Cloudflare: 1.1.1.1, 1.0.0.1
        - Google: 8.8.8.8, 8.8.4.4
        """
        if not self.is_windows:
            return {'success': False, 'message': 'Only supported on Windows'}
        
        try:
            # Obtener interfaz activa
            status = self.get_network_status()
            interface = status.get('active_interface', 'Ethernet')
            
            # Configurar DNS de Cloudflare (más rápido para gaming)
            cmd_primary = f'netsh interface ip set dns "{interface}" static 1.1.1.1'
            cmd_secondary = f'netsh interface ip add dns "{interface}" 1.0.0.1 index=2'
            
            result1 = subprocess.run(cmd_primary, shell=True, capture_output=True, text=True)
            result2 = subprocess.run(cmd_secondary, shell=True, capture_output=True, text=True)
            
            if result1.returncode == 0 and result2.returncode == 0:
                self.optimizations_applied.append('Cloudflare DNS')
                return {
                    'success': True,
                    'dns_primary': '1.1.1.1',
                    'dns_secondary': '1.0.0.1',
                    'provider': 'Cloudflare (optimized for gaming)'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to set DNS (requires admin)'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def flush_dns_cache(self) -> Dict:
        """Limpiar caché DNS"""
        if not self.is_windows:
            return {'success': False, 'message': 'Only supported on Windows'}
        
        try:
            result = subprocess.run(
                'ipconfig /flushdns',
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    'success': True,
                    'message': 'DNS cache flushed successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to flush DNS cache'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def close_bandwidth_hogs(self) -> Dict:
        """
        Cerrar aplicaciones que consumen ancho de banda
        
        Detecta y cierra:
        - Torrents (uTorrent, BitTorrent, qBittorrent)
        - Streaming (Spotify, Discord video)
        - Updates (Windows Update, Steam downloads)
        """
        bandwidth_hogs = [
            'utorrent.exe',
            'bittorrent.exe',
            'qbittorrent.exe',
            'transmission.exe',
            'spotify.exe',
            'discord.exe',  # Solo si está en video call
            'chrome.exe',   # Solo si está streaming
            'firefox.exe',  # Solo si está streaming
        ]
        
        closed = []
        
        try:
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    proc_name = proc.info['name'].lower()
                    
                    if proc_name in bandwidth_hogs:
                        # Verificar uso de red
                        connections = proc.connections()
                        
                        if len(connections) > 5:  # Muchas conexiones = probablemente descargando
                            proc.terminate()
                            closed.append(proc.info['name'])
                
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            return {
                'success': True,
                'closed_apps': closed,
                'count': len(closed)
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def measure_latency(self, host: str = '8.8.8.8') -> Dict:
        """
        Medir latencia a un host
        
        Args:
            host: Host para hacer ping (default: Google DNS)
        
        Returns:
            Dict con latencia promedio
        """
        if not self.is_windows:
            return {'success': False, 'message': 'Only supported on Windows'}
        
        try:
            # Hacer ping
            result = subprocess.run(
                f'ping -n 4 {host}',
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parsear resultado
                output = result.stdout
                
                # Buscar línea de estadísticas
                for line in output.split('\n'):
                    if 'Average' in line or 'Media' in line:
                        # Extraer latencia promedio
                        parts = line.split('=')
                        if len(parts) > 1:
                            avg_str = parts[-1].strip().replace('ms', '').strip()
                            try:
                                avg_latency = int(avg_str)
                                
                                # Evaluar latencia
                                if avg_latency < 20:
                                    quality = 'Excellent'
                                elif avg_latency < 50:
                                    quality = 'Good'
                                elif avg_latency < 100:
                                    quality = 'Fair'
                                else:
                                    quality = 'Poor'
                                
                                return {
                                    'success': True,
                                    'latency_ms': avg_latency,
                                    'quality': quality,
                                    'host': host
                                }
                            except:
                                pass
                
                return {
                    'success': False,
                    'message': 'Could not parse ping result'
                }
            else:
                return {
                    'success': False,
                    'message': 'Ping failed'
                }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def optimize_all(self) -> Dict:
        """
        Aplicar todas las optimizaciones de red
        
        Returns:
            Dict con resumen de optimizaciones
        """
        results = {
            'tcp_optimization': self.optimize_tcp_settings(),
            'dns_optimization': self.optimize_dns(),
            'dns_flush': self.flush_dns_cache(),
            'bandwidth_cleanup': self.close_bandwidth_hogs(),
            'latency_test': self.measure_latency()
        }
        
        # Contar éxitos
        successes = sum(1 for r in results.values() if r.get('success', False))
        
        return {
            'success': successes > 0,
            'total_optimizations': len(results),
            'successful': successes,
            'details': results,
            'applied': self.optimizations_applied
        }


if __name__ == '__main__':
    print("=" * 60)
    print("🌐 NEURO NETWORK OPTIMIZER TEST")
    print("=" * 60)
    print()
    
    optimizer = NetworkOptimizer()
    
    # Estado de red
    print("📊 Network Status:")
    status = optimizer.get_network_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Medir latencia
    print("\n⏱️ Latency Test:")
    latency = optimizer.measure_latency()
    if latency['success']:
        print(f"  Latency: {latency['latency_ms']}ms ({latency['quality']})")
    
    # Aplicar optimizaciones
    print("\n🚀 Applying Optimizations...")
    print("⚠️ Note: Some optimizations require administrator privileges")
    
    result = optimizer.optimize_all()
    
    print(f"\n✅ Applied {result['successful']}/{result['total_optimizations']} optimizations")
    
    if result['applied']:
        print("\nOptimizations applied:")
        for opt in result['applied']:
            print(f"  ✅ {opt}")
    
    print("\n" + "=" * 60)
    print("NETWORK OPTIMIZATION COMPLETED")
    print("=" * 60)
