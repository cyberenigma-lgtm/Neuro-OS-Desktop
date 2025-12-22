#!/bin/bash
# NEURO-OS GENESIS LAUNCHER (Linux)

echo ""
echo "  ======================================================="
echo "   NEURO-OS GENESIS: INICIANDO SISTEMA"
echo "  ======================================================="
echo ""
echo "   [+] Cargando entorno Python..."
echo "   [+] Verificando assets..."
echo "   [+] Lanzando Desktop Environment..."
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Ejecutar Neuro-OS
python3 src/NEURO_OS_MASTER.py

# Verificar si hubo error
if [ $? -ne 0 ]; then
    echo ""
    echo "   [!] ERROR CRITICO: El sistema se ha detenido."
    read -p "Presiona Enter para salir..."
fi
