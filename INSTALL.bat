@echo off
echo ========================================
echo   NEURO-OS GENESIS - INSTALADOR
echo ========================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no encontrado!
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Fallo al instalar dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA!
echo ========================================
echo.
echo Para lanzar Neuro-OS, ejecuta:
echo   LAUNCH_NEURO_OS.bat
echo.
pause
