#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 GAME PROFILE MANAGER
Gestor de perfiles de optimización por juego con IA
"""

import json
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass, asdict
from enum import Enum

class GameCategory(Enum):
    """Categorías de juegos para optimización"""
    COMPETITIVE_FPS = "competitive_fps"  # CS2, Valorant, Apex
    BATTLE_ROYALE = "battle_royale"      # Fortnite, Warzone, PUBG
    MOBA = "moba"                        # LoL, Dota 2
    RPG = "rpg"                          # Skyrim, Witcher 3
    SANDBOX = "sandbox"                  # Minecraft, Terraria
    RACING = "racing"                    # Forza, F1
    STRATEGY = "strategy"                # Civilization, Age of Empires
    CASUAL = "casual"                    # Fall Guys, Among Us

@dataclass
class GameProfile:
    """Perfil de optimización para un juego"""
    name: str
    category: GameCategory
    target_fps: int = 60
    
    # Optimizaciones de resolución
    render_scale: float = 1.0  # 0.5 = 720p, 0.75 = 1080p, 1.0 = native
    
    # Prioridades de sistema
    cpu_priority: str = "high"  # low, normal, high, realtime
    gpu_priority: int = 8  # 0-8, 8 = máxima
    
    # Optimizaciones de RAM
    ram_cleanup_before_launch: bool = True
    aggressive_ram_cleanup: bool = False
    
    # Optimizaciones de red
    network_optimization: bool = False
    close_bandwidth_hogs: bool = False
    
    # Configuraciones específicas
    disable_overlays: bool = False  # Discord, Steam overlay
    disable_recording: bool = False  # OBS, ShadowPlay
    
    # Benchmarks
    last_fps: Optional[float] = None
    avg_fps: Optional[float] = None
    min_fps: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convertir a diccionario"""
        data = asdict(self)
        data['category'] = self.category.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GameProfile':
        """Crear desde diccionario"""
        data['category'] = GameCategory(data['category'])
        return cls(**data)

class GameProfileManager:
    """Gestor de perfiles de juego con IA"""
    
    def __init__(self, profiles_file: str = "game_profiles.json"):
        self.profiles_file = Path(profiles_file)
        self.profiles: Dict[str, GameProfile] = {}
        self.load_profiles()
        self._init_default_profiles()
    
    def _init_default_profiles(self):
        """Inicializar perfiles por defecto para juegos populares"""
        defaults = {
            # Competitive FPS - Máximo rendimiento
            "Counter-Strike 2": GameProfile(
                name="Counter-Strike 2",
                category=GameCategory.COMPETITIVE_FPS,
                target_fps=144,
                render_scale=0.75,  # 1080p para más FPS
                cpu_priority="realtime",
                gpu_priority=8,
                ram_cleanup_before_launch=True,
                aggressive_ram_cleanup=True,
                network_optimization=True,
                close_bandwidth_hogs=True,
                disable_overlays=True
            ),
            
            "Valorant": GameProfile(
                name="Valorant",
                category=GameCategory.COMPETITIVE_FPS,
                target_fps=144,
                render_scale=0.75,
                cpu_priority="realtime",
                network_optimization=True,
                close_bandwidth_hogs=True
            ),
            
            # Battle Royale - Balance rendimiento/calidad
            "Call of Duty Warzone": GameProfile(
                name="Call of Duty Warzone",
                category=GameCategory.BATTLE_ROYALE,
                target_fps=60,
                render_scale=0.5,  # 720p para PCs bajos
                cpu_priority="high",
                gpu_priority=8,
                ram_cleanup_before_launch=True,
                aggressive_ram_cleanup=True,
                network_optimization=True
            ),
            
            "Fortnite": GameProfile(
                name="Fortnite",
                category=GameCategory.BATTLE_ROYALE,
                target_fps=60,
                render_scale=0.75,
                cpu_priority="high",
                network_optimization=True
            ),
            
            # MOBA - Estabilidad de FPS
            "League of Legends": GameProfile(
                name="League of Legends",
                category=GameCategory.MOBA,
                target_fps=60,
                render_scale=1.0,  # Puede correr nativo
                cpu_priority="high",
                network_optimization=True,
                close_bandwidth_hogs=True
            ),
            
            # Sandbox - CPU intensivo
            "Minecraft": GameProfile(
                name="Minecraft",
                category=GameCategory.SANDBOX,
                target_fps=60,
                render_scale=1.0,
                cpu_priority="high",
                ram_cleanup_before_launch=True,
                aggressive_ram_cleanup=False  # Minecraft usa mucha RAM
            ),
            
            # RPG - Calidad visual
            "The Witcher 3": GameProfile(
                name="The Witcher 3",
                category=GameCategory.RPG,
                target_fps=30,  # 30 FPS aceptable para RPG
                render_scale=0.75,
                cpu_priority="high",
                ram_cleanup_before_launch=True
            ),
        }
        
        # Añadir solo si no existen
        for name, profile in defaults.items():
            if name not in self.profiles:
                self.profiles[name] = profile
        
        self.save_profiles()
    
    def load_profiles(self):
        """Cargar perfiles desde archivo"""
        if self.profiles_file.exists():
            try:
                with open(self.profiles_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for name, profile_data in data.items():
                    self.profiles[name] = GameProfile.from_dict(profile_data)
            except Exception as e:
                print(f"Error loading profiles: {e}")
    
    def save_profiles(self):
        """Guardar perfiles a archivo"""
        try:
            data = {name: profile.to_dict() for name, profile in self.profiles.items()}
            
            with open(self.profiles_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving profiles: {e}")
    
    def get_profile(self, game_name: str) -> Optional[GameProfile]:
        """Obtener perfil de un juego"""
        return self.profiles.get(game_name)
    
    def create_profile(self, game_name: str, category: GameCategory) -> GameProfile:
        """Crear nuevo perfil para un juego"""
        profile = GameProfile(name=game_name, category=category)
        self.profiles[game_name] = profile
        self.save_profiles()
        return profile
    
    def update_profile(self, game_name: str, **kwargs):
        """Actualizar perfil existente"""
        if game_name in self.profiles:
            profile = self.profiles[game_name]
            
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            self.save_profiles()
    
    def optimize_for_game(self, game_name: str) -> Dict:
        """
        Aplicar optimizaciones para un juego específico
        
        Returns:
            Dict con acciones tomadas
        """
        profile = self.get_profile(game_name)
        
        if not profile:
            return {
                'success': False,
                'message': f'No profile found for {game_name}'
            }
        
        actions = []
        
        # 1. Optimización de RAM
        if profile.ram_cleanup_before_launch:
            try:
                from ram_manager import RAMManager
                ram_mgr = RAMManager()
                result = ram_mgr.free_ram(aggressive=profile.aggressive_ram_cleanup)
                actions.append(f"RAM freed: {result['ram_freed_gb']:.2f} GB")
            except Exception as e:
                actions.append(f"RAM cleanup failed: {e}")
        
        # 2. Optimización de red
        if profile.network_optimization:
            try:
                from network_optimizer import NetworkOptimizer
                net_opt = NetworkOptimizer()
                
                if profile.close_bandwidth_hogs:
                    result = net_opt.close_bandwidth_hogs()
                    if result['success'] and result['count'] > 0:
                        actions.append(f"Closed {result['count']} bandwidth hogs")
                
                # Flush DNS
                net_opt.flush_dns_cache()
                actions.append("DNS cache flushed")
            except Exception as e:
                actions.append(f"Network optimization failed: {e}")
        
        # 3. Configurar prioridades (esto se haría al lanzar el juego)
        actions.append(f"CPU Priority: {profile.cpu_priority}")
        actions.append(f"GPU Priority: {profile.gpu_priority}")
        actions.append(f"Target FPS: {profile.target_fps}")
        actions.append(f"Render Scale: {profile.render_scale * 100:.0f}%")
        
        return {
            'success': True,
            'game': game_name,
            'category': profile.category.value,
            'actions': actions,
            'profile': profile
        }
    
    def ai_auto_optimize(self, game_name: str, current_fps: float) -> Dict:
        """
        IA ajusta automáticamente el perfil basándose en FPS actual
        
        Args:
            game_name: Nombre del juego
            current_fps: FPS actual medido
        
        Returns:
            Dict con ajustes realizados
        """
        profile = self.get_profile(game_name)
        
        if not profile:
            return {'success': False, 'message': 'No profile found'}
        
        adjustments = []
        
        # Actualizar estadísticas
        if profile.last_fps is None:
            profile.avg_fps = current_fps
        else:
            # Promedio móvil
            profile.avg_fps = (profile.avg_fps * 0.9 + current_fps * 0.1) if profile.avg_fps else current_fps
        
        profile.last_fps = current_fps
        
        if profile.min_fps is None or current_fps < profile.min_fps:
            profile.min_fps = current_fps
        
        # IA: Ajustar render scale si FPS < target
        if current_fps < profile.target_fps * 0.8:  # 80% del target
            # Reducir render scale
            old_scale = profile.render_scale
            profile.render_scale = max(0.5, profile.render_scale - 0.1)
            
            if profile.render_scale != old_scale:
                adjustments.append(f"Render scale: {old_scale:.2f} → {profile.render_scale:.2f}")
                adjustments.append(f"Expected FPS boost: ~{((old_scale / profile.render_scale) ** 2 - 1) * 100:.0f}%")
        
        # IA: Aumentar render scale si FPS > target con margen
        elif current_fps > profile.target_fps * 1.3:  # 130% del target
            # Aumentar render scale para mejor calidad
            old_scale = profile.render_scale
            profile.render_scale = min(1.0, profile.render_scale + 0.1)
            
            if profile.render_scale != old_scale:
                adjustments.append(f"Render scale: {old_scale:.2f} → {profile.render_scale:.2f} (better quality)")
        
        # IA: Activar RAM agresivo si FPS muy bajo
        if current_fps < profile.target_fps * 0.5:  # 50% del target
            if not profile.aggressive_ram_cleanup:
                profile.aggressive_ram_cleanup = True
                adjustments.append("Enabled aggressive RAM cleanup")
        
        # Guardar cambios
        self.save_profiles()
        
        return {
            'success': True,
            'game': game_name,
            'current_fps': current_fps,
            'target_fps': profile.target_fps,
            'avg_fps': profile.avg_fps,
            'adjustments': adjustments,
            'profile': profile
        }
    
    def get_all_profiles(self) -> List[GameProfile]:
        """Obtener todos los perfiles"""
        return list(self.profiles.values())
    
    def delete_profile(self, game_name: str) -> bool:
        """Eliminar perfil"""
        if game_name in self.profiles:
            del self.profiles[game_name]
            self.save_profiles()
            return True
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("🎮 GAME PROFILE MANAGER TEST")
    print("=" * 60)
    print()
    
    manager = GameProfileManager()
    
    # Listar perfiles
    print("📋 Available Profiles:")
    for profile in manager.get_all_profiles():
        print(f"  • {profile.name} ({profile.category.value})")
        print(f"    Target: {profile.target_fps} FPS | Scale: {profile.render_scale * 100:.0f}%")
    
    # Optimizar para Warzone
    print("\n🚀 Optimizing for Warzone...")
    result = manager.optimize_for_game("Call of Duty Warzone")
    
    if result['success']:
        print(f"✅ Optimizations applied for {result['game']}:")
        for action in result['actions']:
            print(f"  • {action}")
    
    # Simular IA auto-ajuste
    print("\n🤖 AI Auto-Optimization (simulating 25 FPS)...")
    ai_result = manager.ai_auto_optimize("Call of Duty Warzone", 25.0)
    
    if ai_result['success']:
        print(f"Current FPS: {ai_result['current_fps']:.1f}")
        print(f"Target FPS: {ai_result['target_fps']}")
        
        if ai_result['adjustments']:
            print("Adjustments made:")
            for adj in ai_result['adjustments']:
                print(f"  • {adj}")
        else:
            print("No adjustments needed")
    
    print("\n" + "=" * 60)
    print("GAME PROFILE MANAGER TEST COMPLETED")
    print("=" * 60)
