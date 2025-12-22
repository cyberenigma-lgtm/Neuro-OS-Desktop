@echo off
title NEURO-OS GENESIS LAUNCHER
color 0b
cls
echo.
echo  =======================================================
echo   NEURO-OS GENESIS: INICIANDO SISTEMA
echo  =======================================================
echo.
echo   [+] Cargando entorno Python...
echo   [+] Verificando assets...
echo   [+] Lanzando Desktop Environment...
echo.

cd /d "%~dp0"
python src\NEURO_OS_MASTER.py

if %errorlevel% neq 0 (
    echo.
    echo   [!] ERROR CRITICO: El sistema se ha detenido.
    pause
)
