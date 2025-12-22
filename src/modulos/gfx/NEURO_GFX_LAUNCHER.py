#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 NEURO-GFX LAUNCHER (Simplified Version)
------------------------------------------
Launches games with optimized settings.
No DLL injection - Pure process optimization.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def launch_game(target, mode="PASSIVE", **kwargs):
    """
    Launch target executable with optimization
    
    Args:
        target: Path to executable or steam:// URL
        mode: PASSIVE (default), HOOK, STREAM
        **kwargs: Additional parameters (out_res, render_res, fps, upscaling)
    """
    print(f"[NEURO-GFX] Launching: {target}")
    print(f"[NEURO-GFX] Mode: {mode}")
    
    # For now, just launch the target directly
    # Advanced modes (HOOK, STREAM) would require additional DLL injection
    
    if target.startswith("steam://"):
        # Steam URL - let Windows handle it
        os.startfile(target)
        print("[NEURO-GFX] Steam launch command sent")
    else:
        # Regular executable
        target_path = Path(target)
        if not target_path.exists():
            print(f"[ERROR] Target not found: {target}")
            return 1
        
        # Launch with subprocess
        try:
            cwd = target_path.parent if target_path.parent.exists() else None
            proc = subprocess.Popen(
                [str(target_path)],
                cwd=cwd,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
            print(f"[NEURO-GFX] Process started (PID: {proc.pid})")
            
            # TODO: Apply priority optimization here if needed
            # import psutil
            # p = psutil.Process(proc.pid)
            # p.nice(psutil.HIGH_PRIORITY_CLASS)
            
        except Exception as e:
            print(f"[ERROR] Failed to launch: {e}")
            return 1
    
    print("[NEURO-GFX] Launch successful")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Neuro-GFX Game Launcher")
    parser.add_argument("--target", required=True, help="Path to game executable or steam:// URL")
    parser.add_argument("--mode", default="PASSIVE", choices=["PASSIVE", "HOOK", "STREAM"])
    parser.add_argument("--out-res", default="1920x1080")
    parser.add_argument("--render-res", default="100%")
    parser.add_argument("--fps", default="UNCAPPED")
    parser.add_argument("--upscaling", default="OFF")
    
    args = parser.parse_args()
    
    exit_code = launch_game(
        target=args.target,
        mode=args.mode,
        out_res=args.out_res,
        render_res=args.render_res,
        fps=args.fps,
        upscaling=args.upscaling
    )
    
    sys.exit(exit_code)
