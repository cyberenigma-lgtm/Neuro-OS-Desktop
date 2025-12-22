# 🧠 NEURO-OS GENESIS

<div align="center">

![Neuro-OS Banner](https://img.shields.io/badge/Neuro--OS-Genesis-00d4ff?style=for-the-badge&logo=windows&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)

**Un sistema operativo de escritorio revolucionario construido con Python y Qt**

[Características](#-características) • [Instalación](#-instalación) • [Uso](#-uso) • [Contribuir](#-contribuir)

</div>

---

## 📖 Descripción

**Neuro-OS Genesis** es un entorno de escritorio completo y moderno construido desde cero con Python y PySide6. Diseñado para ofrecer una experiencia única que combina la estética futurista con funcionalidad práctica.

### 🎯 ¿Qué hace único a Neuro-OS?

- **🎨 Interfaz Futurista**: Diseño inspirado en sistemas de ciencia ficción con animaciones fluidas
- **⚡ GFX Optimizer**: Sistema inteligente de optimización de juegos y aplicaciones
- **🛡️ Radar Automático**: Detección y optimización automática de procesos pesados
- **🌐 Navegador Integrado**: Navegador web completo dentro del sistema
- **📁 Explorador de Archivos**: Navegación de archivos con tema personalizado
- **🎮 Custom Apps**: Añade tus aplicaciones favoritas al escritorio
- **⚙️ Altamente Configurable**: Panel de configuración completo con persistencia

---

## ✨ Características

### 🖥️ Sistema Completo
- ✅ Pantalla de boot animada
- ✅ Sistema de login (usuario: `admin`, contraseña: `admin`)
- ✅ Escritorio con dock interactivo
- ✅ Barra de estado con monitoreo en tiempo real (CPU, RAM, batería, red)
- ✅ Múltiples aplicaciones integradas

### 🚀 Aplicaciones Incluidas

| Aplicación | Descripción |
|-----------|-------------|
| 📁 **Files** | Explorador de archivos con navegación completa |
| 🌐 **Net** | Navegador web integrado (Chromium) |
| 💻 **Terminal** | Terminal PowerShell funcional |
| 🎵 **Media Hub** | Reproductor multimedia con enlaces a servicios |
| ⚙️ **Settings** | Panel de configuración del sistema |
| 🎨 **GFX Optimizer** | Optimizador de rendimiento para juegos |

### 🎮 GFX Optimizer

El módulo estrella de Neuro-OS:

- **3 Modos de Operación**:
  - 🛡️ **STABILITY**: Modo pasivo (recomendado)
  - ⚡ **NEURO HOOK**: Inyección directa (avanzado)
  - 📡 **STREAM**: Contenedor virtual (experimental)

- **🪟 Captura de Ventanas**: Las aplicaciones se capturan y muestran **DENTRO** de Neuro-OS con estilo cyberpunk
- **Radar Automático**: Detecta juegos lanzados y los optimiza automáticamente
- **Configuración Avanzada**: Resolución, FPS, upscaling, etc.
- **Monitoreo en Tiempo Real**: CPU, RAM, procesos activos
- **Interfaz Personalizada**: Barra de título cyan, bordes neón, tema oscuro

### ⚙️ Sistema de Configuración

- 📁 Ruta por defecto del explorador
- 🌐 Navegador preferido (Auto/Opera/Chrome/Edge/Firefox/Custom)
- ⚡ Activar/Desactivar radar automático
- 🎮 Añadir aplicaciones personalizadas al desktop
- 💾 Guardado persistente en `config.json`

---

## 🛠️ Instalación

### Requisitos Previos

#### Windows
- **Windows 10/11** (64-bit)
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

#### Linux
- **Ubuntu 20.04+** / **Debian 11+** / **Fedora 35+** (o distribuciones similares)
- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Dependencias del sistema**:
  ```bash
  # Ubuntu/Debian
  sudo apt update
  sudo apt install python3-pip xdotool imagemagick
  
  # Fedora
  sudo dnf install python3-pip xdotool ImageMagick
  ```

---

### Instalación Rápida

#### 1. **Clonar el repositorio**:
```bash
git clone https://github.com/cyberenigma-lgtm/Neuro-OS-Desktop.git
cd Neuro-OS-Desktop
```

#### 2. **Instalar dependencias de Python**:
```bash
pip install -r requirements.txt
```

#### 3. **Lanzar Neuro-OS**:

**En Windows:**
```bash
# Opción 1: Usando el launcher
.\LAUNCH_NEURO_OS.bat

# Opción 2: Directamente con Python
cd src
python NEURO_OS_MASTER.py
```

**En Linux:**
```bash
# Opción 1: Dar permisos y ejecutar
chmod +x LAUNCH_NEURO_OS.sh
./LAUNCH_NEURO_OS.sh

# Opción 2: Directamente con Python
cd src
python3 NEURO_OS_MASTER.py
```

---

### Instalación del Navegador Web (Opcional pero Recomendado)

Para habilitar el navegador web integrado:
```bash
pip install PySide6-WebEngine
```

---

## 🎮 Uso

### Primer Inicio

1. **Boot Screen**: Espera a que el sistema termine de cargar
2. **Login**: 
   - Usuario: `admin`
   - Contraseña: `admin`
3. **Desktop**: ¡Explora las aplicaciones desde el dock!

### Atajos de Teclado

- `Esc`: Cerrar ventanas/aplicaciones
- `Enter`: Confirmar en campos de texto

### Configuración

1. Click en **⚙️ Settings** del dock
2. Navega por las pestañas:
   - **🧠 Neuro-OS**: Configuración del sistema
   - **🎮 Custom Apps**: Añade tus aplicaciones
   - **🪟 Windows**: Accesos rápidos a configuración de Windows

3. Haz cambios y click en **💾 SAVE & APPLY CHANGES**

### Añadir Aplicaciones Personalizadas

1. Abre **Settings** → **Custom Apps**
2. Rellena:
   - **App Name**: Nombre de la aplicación
   - **Executable Path**: Usa 📂 para buscar el .exe
   - **Icon**: Un emoji (🎨, 💬, 🎮, etc.)
3. Click **➕ Add Application**
4. Click **💾 SAVE & APPLY CHANGES**
5. Reinicia Neuro-OS para ver los iconos en el desktop

---

## 📁 Estructura del Proyecto

```
Neuro-OS-Desktop-Release/
├── src/
│   ├── NEURO_OS_MASTER.py      # Archivo principal
│   ├── config_manager.py        # Gestión de configuración
│   ├── web_browser.py           # Navegador integrado
│   └── window_capture.py        # Sistema de captura (experimental)
├── activos_generados/           # Assets visuales
├── config.json                  # Configuración del usuario
├── LAUNCH_NEURO_OS.bat         # Launcher de Windows
├── requirements.txt             # Dependencias Python
├── README.md                    # Este archivo
└── LICENSE                      # Licencia MIT
```

---

## 🔧 Configuración Avanzada

### Archivo `config.json`

El sistema guarda la configuración en `config.json`:

```json
{
    "file_explorer": {
        "default_path": "~/Desktop",
        "show_hidden": false
    },
    "browser": {
        "preferred": "auto",
        "custom_path": ""
    },
    "performance": {
        "enable_radar": true,
        "radar_interval_ms": 10000,
        "memory_threshold_mb": 250
    },
    "custom_apps": [
        {
            "name": "Discord",
            "path": "C:/Users/.../Discord.exe",
            "icon": "💬"
        }
    ]
}
```

### Optimización de Rendimiento

Para reducir el consumo de recursos:

1. Abre **Settings** → **Neuro-OS**
2. Desmarca **"Enable Background Game Radar"**
3. Guarda cambios

---

## 🐛 Solución de Problemas

### El navegador no funciona

**Problema**: Aparece mensaje "QtWebEngine no instalado"

**Solución**:
```bash
pip install PySide6-WebEngine
```

### Alto consumo de CPU/RAM

**Solución**:
1. Deshabilita el radar automático en Settings
2. Cierra aplicaciones que no uses
3. Reduce el número de custom apps

### Error al lanzar

**Problema**: `ModuleNotFoundError`

**Solución**:
```bash
pip install -r requirements.txt --upgrade
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres mejorar Neuro-OS:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Áreas de Mejora

- [ ] Soporte para Linux/macOS
- [ ] Más aplicaciones integradas
- [ ] Temas personalizables
- [ ] Sistema de plugins
- [ ] Captura de ventanas nativas mejorada
- [ ] Detección de cuellos de botella (CPU/GPU/RAM)

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **PySide6/Qt**: Framework UI increíble
- **psutil**: Monitoreo de sistema
- **Comunidad Python**: Por las herramientas y soporte

---

## 📞 Contacto

**Proyecto**: [Neuro-OS Genesis](https://github.com/tu-usuario/Neuro-OS-Genesis)

**Desarrollado con** ❤️ **y mucho** ☕

---

<div align="center">

### ⭐ Si te gusta el proyecto, dale una estrella en GitHub!

![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)
![Powered by Qt](https://img.shields.io/badge/Powered%20by-Qt-green?style=for-the-badge&logo=qt)

</div>
