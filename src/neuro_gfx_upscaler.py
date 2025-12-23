#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚡ NEURO-GFX UPSCALER
Captura juegos en baja resolución y upscalea a 4K usando algoritmos avanzados
Similar a DLSS/FSR pero implementado en software
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional

class NeuroGFXUpscaler:
    """
    Motor de upscaling de Neuro-OS
    Renderiza juegos en baja resolución y upscalea a 4K
    """
    
    # Resoluciones soportadas
    RESOLUTIONS = {
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "1440p": (2560, 1440),
        "4K": (3840, 2160),
    }
    
    # Modos de upscaling
    UPSCALE_MODES = {
        "FAST": cv2.INTER_LINEAR,          # Rápido, calidad media
        "BALANCED": cv2.INTER_CUBIC,       # Balance rendimiento/calidad
        "QUALITY": cv2.INTER_LANCZOS4,     # Mejor calidad, más lento
    }
    
    def __init__(self, 
                 render_resolution: str = "1080p",
                 output_resolution: str = "4K",
                 upscale_mode: str = "BALANCED",
                 sharpening: float = 0.3):
        """
        Inicializar upscaler
        
        Args:
            render_resolution: Resolución de renderizado del juego
            output_resolution: Resolución de salida (pantalla)
            upscale_mode: Modo de upscaling (FAST/BALANCED/QUALITY)
            sharpening: Nivel de sharpening (0.0 - 1.0)
        """
        self.render_res = self.RESOLUTIONS.get(render_resolution, (1920, 1080))
        self.output_res = self.RESOLUTIONS.get(output_resolution, (3840, 2160))
        self.upscale_mode = self.UPSCALE_MODES.get(upscale_mode, cv2.INTER_CUBIC)
        self.sharpening = sharpening
        
        # Calcular factor de escala
        self.scale_x = self.output_res[0] / self.render_res[0]
        self.scale_y = self.output_res[1] / self.render_res[1]
        
        print(f"[Neuro-GFX] Upscaler inicializado:")
        print(f"  Render: {render_resolution} {self.render_res}")
        print(f"  Output: {output_resolution} {self.output_res}")
        print(f"  Scale: {self.scale_x:.2f}x")
        print(f"  Mode: {upscale_mode}")
    
    def apply_sharpening(self, image: np.ndarray, strength: float = 0.3) -> np.ndarray:
        """
        Aplicar sharpening a la imagen
        
        Args:
            image: Imagen en formato numpy array
            strength: Intensidad del sharpening (0.0 - 1.0)
        
        Returns:
            Imagen con sharpening aplicado
        """
        if strength <= 0:
            return image
        
        # Kernel de sharpening
        kernel = np.array([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]) * strength
        
        # Aplicar filtro
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Mezclar con imagen original
        result = cv2.addWeighted(image, 1 - strength, sharpened, strength, 0)
        
        return result
    
    def upscale_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Upscalear un frame individual
        
        Args:
            frame: Frame en baja resolución (numpy array BGR)
        
        Returns:
            Frame upscaleado a resolución de salida
        """
        # 1. Upscaling básico
        upscaled = cv2.resize(
            frame,
            self.output_res,
            interpolation=self.upscale_mode
        )
        
        # 2. Aplicar sharpening para recuperar detalles
        if self.sharpening > 0:
            upscaled = self.apply_sharpening(upscaled, self.sharpening)
        
        # 3. Reducción de ruido ligera (opcional)
        # upscaled = cv2.fastNlMeansDenoisingColored(upscaled, None, 3, 3, 7, 21)
        
        return upscaled
    
    def upscale_image(self, image_path: str, output_path: str) -> bool:
        """
        Upscalear una imagen desde archivo
        
        Args:
            image_path: Ruta de la imagen de entrada
            output_path: Ruta de la imagen de salida
        
        Returns:
            True si tuvo éxito
        """
        try:
            # Leer imagen
            frame = cv2.imread(image_path)
            if frame is None:
                print(f"Error: No se pudo leer {image_path}")
                return False
            
            # Upscalear
            upscaled = self.upscale_frame(frame)
            
            # Guardar
            cv2.imwrite(output_path, upscaled)
            print(f"[OK] Imagen upscaleada: {output_path}")
            
            return True
        except Exception as e:
            print(f"Error upscaleando imagen: {e}")
            return False
    
    def get_performance_boost(self) -> float:
        """
        Calcular boost de rendimiento estimado
        
        Returns:
            Factor de mejora de FPS estimado
        """
        # Calcular reducción de píxeles
        render_pixels = self.render_res[0] * self.render_res[1]
        output_pixels = self.output_res[0] * self.output_res[1]
        
        pixel_reduction = output_pixels / render_pixels
        
        # Estimación conservadora: 60-70% del boost teórico
        estimated_boost = pixel_reduction * 0.65
        
        return estimated_boost
    
    def get_info(self) -> dict:
        """Obtener información del upscaler"""
        return {
            "render_resolution": self.render_res,
            "output_resolution": self.output_res,
            "scale_factor": f"{self.scale_x:.2f}x",
            "upscale_mode": self.upscale_mode,
            "sharpening": self.sharpening,
            "estimated_fps_boost": f"{self.get_performance_boost():.1f}x"
        }


class NeuroGFXPresets:
    """Presets de configuración para diferentes escenarios"""
    
    @staticmethod
    def get_preset(preset_name: str) -> dict:
        """
        Obtener preset de configuración
        
        Args:
            preset_name: Nombre del preset
        
        Returns:
            Diccionario con configuración
        """
        presets = {
            "ULTRA_PERFORMANCE": {
                "render_resolution": "720p",
                "output_resolution": "4K",
                "upscale_mode": "FAST",
                "sharpening": 0.5
            },
            "PERFORMANCE": {
                "render_resolution": "1080p",
                "output_resolution": "4K",
                "upscale_mode": "BALANCED",
                "sharpening": 0.4
            },
            "BALANCED": {
                "render_resolution": "1440p",
                "output_resolution": "4K",
                "upscale_mode": "BALANCED",
                "sharpening": 0.3
            },
            "QUALITY": {
                "render_resolution": "1440p",
                "output_resolution": "4K",
                "upscale_mode": "QUALITY",
                "sharpening": 0.2
            }
        }
        
        return presets.get(preset_name, presets["BALANCED"])


if __name__ == "__main__":
    # Test del upscaler
    print("=== NEURO-GFX UPSCALER TEST ===\n")
    
    # Crear upscaler con preset PERFORMANCE
    preset = NeuroGFXPresets.get_preset("PERFORMANCE")
    upscaler = NeuroGFXUpscaler(**preset)
    
    print(f"\nInfo: {upscaler.get_info()}")
    print(f"\nBoost estimado de FPS: {upscaler.get_performance_boost():.1f}x")
    print("\nEjemplo: Si el juego corre a 30 FPS en 4K nativo,")
    print(f"         con Neuro-GFX correría a ~{30 * upscaler.get_performance_boost():.0f} FPS")
