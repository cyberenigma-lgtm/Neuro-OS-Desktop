#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 NEURO-OS GAME SCANNER
Detecta juegos instalados de Steam, Epic Games, GOG, y otros launchers
"""

import os
import json
import winreg
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Game:
    """Representa un juego detectado"""
    name: str
    path: str
    launcher: str  # "Steam", "Epic", "GOG", "Standalone"
    app_id: Optional[str] = None
    icon: str = "🎮"

class GameScanner:
    """Escanea y detecta juegos instalados en el sistema"""
    
    def __init__(self):
        self.games: List[Game] = []
    
    def get_steam_path(self) -> Optional[str]:
        """Obtener ruta de instalación de Steam desde el registro"""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
            winreg.CloseKey(key)
            return steam_path
        except:
            # Intentar en 32-bit
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                    r"SOFTWARE\Valve\Steam")
                steam_path, _ = winreg.QueryValueEx(key, "InstallPath")
                winreg.CloseKey(key)
                return steam_path
            except:
                return None
    
    def scan_steam_library(self) -> List[Game]:
        """Escanear biblioteca de Steam"""
        games = []
        steam_path = self.get_steam_path()
        
        if not steam_path:
            print("⚠️ Steam no encontrado")
            return games
        
        # Buscar libraryfolders.vdf
        library_file = Path(steam_path) / "steamapps" / "libraryfolders.vdf"
        
        if not library_file.exists():
            return games
        
        # Leer carpetas de biblioteca
        library_paths = [Path(steam_path) / "steamapps"]
        
        try:
            with open(library_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Buscar rutas adicionales (formato simple)
                for line in content.split('\n'):
                    if '"path"' in line:
                        path = line.split('"')[3]
                        library_paths.append(Path(path) / "steamapps")
        except:
            pass
        
        # Escanear cada carpeta de biblioteca
        for lib_path in library_paths:
            if not lib_path.exists():
                continue
            
            # Buscar archivos .acf (manifiestos de juegos)
            for acf_file in lib_path.glob("appmanifest_*.acf"):
                try:
                    with open(acf_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Extraer nombre y appid
                        name = None
                        appid = None
                        install_dir = None
                        
                        for line in content.split('\n'):
                            if '"name"' in line:
                                name = line.split('"')[3]
                            elif '"appid"' in line:
                                appid = line.split('"')[3]
                            elif '"installdir"' in line:
                                install_dir = line.split('"')[3]
                        
                        if name and appid and install_dir:
                            game_path = lib_path / "common" / install_dir
                            
                            # Buscar .exe principal
                            exe_files = list(game_path.glob("*.exe"))
                            if exe_files:
                                games.append(Game(
                                    name=name,
                                    path=f"steam://rungameid/{appid}",
                                    launcher="Steam",
                                    app_id=appid,
                                    icon="🎮"
                                ))
                except Exception as e:
                    print(f"Error leyendo {acf_file}: {e}")
        
        print(f"✅ Steam: {len(games)} juegos encontrados")
        return games
    
    def get_epic_path(self) -> Optional[str]:
        """Obtener ruta de Epic Games"""
        epic_manifests = Path.home() / "AppData" / "Local" / "EpicGamesLauncher" / "Saved" / "Config" / "Windows"
        if epic_manifests.exists():
            return str(epic_manifests)
        return None
    
    def scan_epic_library(self) -> List[Game]:
        """Escanear biblioteca de Epic Games"""
        games = []
        
        # Epic guarda manifiestos en ProgramData
        manifests_path = Path("C:/ProgramData/Epic/EpicGamesLauncher/Data/Manifests")
        
        if not manifests_path.exists():
            print("⚠️ Epic Games no encontrado")
            return games
        
        for manifest_file in manifests_path.glob("*.item"):
            try:
                with open(manifest_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    name = data.get("DisplayName", "Unknown")
                    install_location = data.get("InstallLocation", "")
                    app_name = data.get("AppName", "")
                    
                    if name and install_location:
                        games.append(Game(
                            name=name,
                            path=install_location,
                            launcher="Epic",
                            app_id=app_name,
                            icon="🎮"
                        ))
            except Exception as e:
                print(f"Error leyendo Epic manifest: {e}")
        
        print(f"✅ Epic Games: {len(games)} juegos encontrados")
        return games
    
    def scan_gog_library(self) -> List[Game]:
        """Escanear biblioteca de GOG"""
        games = []
        
        try:
            # GOG guarda juegos en el registro
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                r"SOFTWARE\WOW6432Node\GOG.com\Games")
            
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        name, _ = winreg.QueryValueEx(subkey, "gameName")
                        path, _ = winreg.QueryValueEx(subkey, "path")
                        
                        games.append(Game(
                            name=name,
                            path=path,
                            launcher="GOG",
                            icon="🎮"
                        ))
                    except:
                        pass
                    
                    winreg.CloseKey(subkey)
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(key)
        except:
            print("⚠️ GOG no encontrado")
        
        print(f"✅ GOG: {len(games)} juegos encontrados")
        return games
    
    def scan_standalone_games(self, directories: List[str] = None) -> List[Game]:
        """Escanear juegos standalone en carpetas comunes"""
        games = []
        
        if directories is None:
            directories = [
                "C:/Program Files",
                "C:/Program Files (x86)",
                str(Path.home() / "Games")
            ]
        
        # Lista de ejecutables conocidos de juegos
        known_games = [
            "Warzone.exe", "ModernWarfare.exe",
            "Smite.exe", "SmiteLauncher.exe",
            "Warhammer.exe", "TotalWar.exe"
        ]
        
        for directory in directories:
            dir_path = Path(directory)
            if not dir_path.exists():
                continue
            
            # Buscar solo en primer nivel para no tardar mucho
            for exe in known_games:
                for exe_file in dir_path.rglob(exe):
                    if exe_file.is_file():
                        name = exe_file.stem
                        games.append(Game(
                            name=name,
                            path=str(exe_file),
                            launcher="Standalone",
                            icon="🎮"
                        ))
        
        print(f"✅ Standalone: {len(games)} juegos encontrados")
        return games
    
    def get_all_games(self) -> List[Game]:
        """Obtener todos los juegos detectados"""
        all_games = []
        
        print("🔍 Escaneando bibliotecas de juegos...")
        
        # Escanear cada launcher
        all_games.extend(self.scan_steam_library())
        all_games.extend(self.scan_epic_library())
        all_games.extend(self.scan_gog_library())
        # all_games.extend(self.scan_standalone_games())  # Comentado por ahora (puede tardar)
        
        self.games = all_games
        print(f"\n✅ Total: {len(all_games)} juegos detectados")
        
        return all_games

if __name__ == "__main__":
    # Test del scanner
    scanner = GameScanner()
    games = scanner.get_all_games()
    
    print("\n📋 Juegos detectados:")
    for game in games[:10]:  # Mostrar solo los primeros 10
        print(f"  {game.icon} {game.name} ({game.launcher})")
