#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 GPU ACCELERATOR
Detecta y usa la GPU del PC anfitrión para acelerar Neuro-GFX
"""

import sys
from typing import Optional, Dict

class GPUAccelerator:
    """Gestor de aceleración por GPU"""
    
    def __init__(self):
        self.gpu_info = self.detect_gpu()
        self.acceleration_available = self.check_acceleration()
    
    def detect_gpu(self) -> Dict:
        """Detectar GPU disponible"""
        gpu_info = {
            'vendor': 'Unknown',
            'name': 'Unknown',
            'memory': 0,
            'cuda_available': False,
            'opencl_available': False,
            'vulkan_available': False
        }
        
        # Intentar detectar con diferentes métodos
        
        # 1. Intentar con PyTorch (CUDA)
        try:
            import torch
            if torch.cuda.is_available():
                gpu_info['cuda_available'] = True
                gpu_info['name'] = torch.cuda.get_device_name(0)
                gpu_info['memory'] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
                gpu_info['vendor'] = 'NVIDIA'
                print(f"[GPU] CUDA detected: {gpu_info['name']}")
        except ImportError:
            pass
        
        # 2. Intentar con OpenCL
        try:
            import pyopencl as cl
            platforms = cl.get_platforms()
            if platforms:
                gpu_info['opencl_available'] = True
                device = platforms[0].get_devices()[0]
                gpu_info['name'] = device.name
                gpu_info['vendor'] = device.vendor
                gpu_info['memory'] = device.global_mem_size / (1024**3)
                print(f"[GPU] OpenCL detected: {gpu_info['name']}")
        except:
            pass
        
        # 3. Intentar con wmi (Windows)
        if sys.platform == 'win32':
            try:
                import wmi
                c = wmi.WMI()
                for gpu in c.Win32_VideoController():
                    gpu_info['name'] = gpu.Name
                    gpu_info['vendor'] = gpu.AdapterCompatibility
                    if gpu.AdapterRAM:
                        gpu_info['memory'] = int(gpu.AdapterRAM) / (1024**3)
                    print(f"[GPU] WMI detected: {gpu_info['name']}")
                    break
            except:
                pass
        
        return gpu_info
    
    def check_acceleration(self) -> bool:
        """Verificar si hay aceleración disponible"""
        return (self.gpu_info['cuda_available'] or 
                self.gpu_info['opencl_available'] or 
                self.gpu_info['memory'] > 0)
    
    def get_best_backend(self) -> str:
        """Obtener el mejor backend de aceleración"""
        if self.gpu_info['cuda_available']:
            return 'CUDA'
        elif self.gpu_info['opencl_available']:
            return 'OpenCL'
        else:
            return 'CPU'
    
    def upscale_with_gpu(self, image, target_size):
        """
        Upscalear imagen usando GPU
        
        Args:
            image: Imagen en formato numpy array
            target_size: Tamaño objetivo (width, height)
        
        Returns:
            Imagen upscaleada
        """
        backend = self.get_best_backend()
        
        if backend == 'CUDA':
            return self._upscale_cuda(image, target_size)
        elif backend == 'OpenCL':
            return self._upscale_opencl(image, target_size)
        else:
            return self._upscale_cpu(image, target_size)
    
    def _upscale_cuda(self, image, target_size):
        """Upscaling con CUDA (NVIDIA)"""
        try:
            import torch
            import torch.nn.functional as F
            
            # Convertir a tensor
            img_tensor = torch.from_numpy(image).float()
            img_tensor = img_tensor.permute(2, 0, 1).unsqueeze(0)  # BHWC -> BCHW
            
            # Mover a GPU
            img_tensor = img_tensor.cuda()
            
            # Upscale con interpolación bicúbica
            upscaled = F.interpolate(
                img_tensor,
                size=target_size,
                mode='bicubic',
                align_corners=False
            )
            
            # Volver a CPU y numpy
            result = upscaled.squeeze(0).permute(1, 2, 0).cpu().numpy()
            
            print(f"[GPU] Upscaled with CUDA: {image.shape} -> {result.shape}")
            return result
        except Exception as e:
            print(f"[GPU] CUDA upscaling failed: {e}")
            return self._upscale_cpu(image, target_size)
    
    def _upscale_opencl(self, image, target_size):
        """Upscaling con OpenCL (AMD/Intel)"""
        # TODO: Implementar con OpenCL
        print("[GPU] OpenCL upscaling not implemented yet, using CPU")
        return self._upscale_cpu(image, target_size)
    
    def _upscale_cpu(self, image, target_size):
        """Upscaling con CPU (fallback)"""
        import cv2
        upscaled = cv2.resize(image, target_size, interpolation=cv2.INTER_CUBIC)
        print(f"[GPU] Upscaled with CPU: {image.shape} -> {upscaled.shape}")
        return upscaled
    
    def get_info(self) -> Dict:
        """Obtener información de la GPU"""
        return {
            'gpu_name': self.gpu_info['name'],
            'gpu_vendor': self.gpu_info['vendor'],
            'gpu_memory_gb': f"{self.gpu_info['memory']:.1f}",
            'cuda_available': self.gpu_info['cuda_available'],
            'opencl_available': self.gpu_info['opencl_available'],
            'acceleration_available': self.acceleration_available,
            'best_backend': self.get_best_backend()
        }


if __name__ == "__main__":
    print("=== GPU ACCELERATOR TEST ===\n")
    
    # Detectar GPU
    gpu = GPUAccelerator()
    
    # Mostrar info
    info = gpu.get_info()
    print("GPU Information:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test de upscaling
    if gpu.acceleration_available:
        import numpy as np
        
        # Crear imagen de prueba (720p)
        test_image = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
        
        # Upscalear a 4K
        upscaled = gpu.upscale_with_gpu(test_image, (2160, 3840))
        
        print(f"\nUpscaling test:")
        print(f"  Input: {test_image.shape}")
        print(f"  Output: {upscaled.shape}")
        print(f"  Backend: {gpu.get_best_backend()}")
    else:
        print("\nNo GPU acceleration available")
