@echo off
REM ========================================
REM   NEURO-OS GENESIS - GIT SETUP
REM ========================================

echo.
echo Preparando repositorio para GitHub...
echo.

REM Navegar al directorio del proyecto
cd /d "c:\Users\cyber\Documents\NeuroOs\Neuro-OS-Genesis\Neuro-OS-Desktop-Release"

REM Verificar si ya existe .git
if exist .git (
    echo [INFO] Repositorio Git ya inicializado
) else (
    echo [INIT] Inicializando repositorio Git...
    git init
)

REM Añadir todos los archivos
echo.
echo [ADD] Añadiendo archivos...
git add .

REM Commit inicial
echo.
echo [COMMIT] Creando commit...
git commit -m "feat: initial release of Neuro-OS Genesis v1.0.0"

echo.
echo ========================================
echo   REPOSITORIO PREPARADO!
echo ========================================
echo.
echo Proximos pasos:
echo.
echo 1. Crea un repositorio en GitHub:
echo    https://github.com/new
echo.
echo 2. Ejecuta estos comandos (reemplaza TU-USUARIO):
echo.
echo    git remote add origin https://github.com/TU-USUARIO/Neuro-OS-Genesis.git
echo    git branch -M main
echo    git push -u origin main
echo.
pause
