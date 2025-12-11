# 🧠 Neuro-OS Desktop Environment
> **Entorno de escritorio multiplataforma – Motor gráfico + gestor de ventanas + ecosistema de aplicaciones**

<div align="center">
  <img src="screenshots/readme_final/neuro_logo_header.png" alt="Neuro-OS Official Logo" width="600">
</div>

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Qt](https://img.shields.io/badge/PySide6-Qt%20for%20Python-green?style=for-the-badge&logo=qt)](https://doc.qt.io/qtforpython/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey?style=for-the-badge)](https://www.microsoft.com/windows)

---

| **Versión** | **Estado** | **Autor** |
|:---:|:---:|:---:|
| v3.0 | Release Candidate | José Manuel Moreno Cano |

![Neuro-Desktop Main](screenshots/readme_final/desktop_main_energy.png)

## 📌 ¿Qué es Neuro-OS Desktop?

**Neuro-OS Desktop** es un entorno de escritorio completo escrito en Python (PySide6/Qt), diseñado para ejecutarse sobre Windows o Linux.

No es un sistema operativo independiente, sino una capa gráfica avanzada que simula la experiencia de un SO moderno con:

*   ✅ Interfaz estilo sistema operativo futurista
*   ✅ Dock, multitarea, ventanas MDI
*   ✅ Gestor de aplicaciones & Temas visuales
*   ✅ Motor de IA autónoma
*   ✅ Suite multimedia y gráfica
*   ✅ Sistema de seguridad multicapa

> *Este repositorio contiene solo el Desktop Environment completo, no el kernel ni la ISO experimental.*

---

## ⚠️ Importante: Qué NO es este proyecto

Para evitar confusiones:

### ❌ Neuro-OS NO es (todavía):
*   Un sistema operativo autónomo o independiente.
*   Un reemplazo de Windows, Linux o macOS.
*   Un kernel propio customizado a bajo nivel.
*   Un entorno con drivers, hardware o kernel personalizados.

### ✔️ Neuro-OS SÍ es:
*   **Un entorno de escritorio** que funciona sobre un sistema operativo existente.
*   **Un ecosistema modular** de aplicaciones.
*   **Una simulación de SO multiplataforma**.
*   **Un proyecto educativo y experimental** para expandir funcionalidades con IA.

---

## 🚀 Características principales

### 🖥️ Entorno de escritorio completo
*   **Pantalla de arranque:** Secuencia de boot simulada.
*   **Login seguro:** Autenticación real (PBKDF2 + Salt) con visuales biométricos.
*   **Escritorio:** Wallpaper dinámico (StarField Engine) y Dock personalizable.
*   **Ventanas MDI:** Controles completos (min/max/close) y tiling.

![Secure Login](screenshots/readme_final/login_screen.png)

### 🧱 Seguridad integrada
*   **Neuro-ID v2:** Hashing avanzado con salt.
*   **Firewall activo & Anti-tamper:** Protección en tiempo real.
*   **TrustChain:** Firma digital de aplicaciones.
*   **EvoBridge:** Sistema de auto-reparación.

### 📦 Compatibilidad multiplataforma simulada
Neuro-OS Desktop incluye interfaces que permiten instalar software desde distintos ecosistemas.
*(IMPORTANTE: No redistribuye software propietario, actúa como launcher hacia tiendas oficiales).*

![Neuro-Store](screenshots/readme_final/neuro_store_android.png)

| Ecosistema | Gestor | Estado |
|:---|:---|:---:|
| **Windows** | Windows Store Launcher | ✅ Implementado |
| **Linux** | APT (WSL bridge) | ✅ Implementado |
| **Android** | ADB APK Installer | ✅ Implementado |
| **macOS** | App Store + Homebrew | ✅ Implementado |

### 🛠️ Herramientas del Sistema
*   **Update Manager & Drivers Installer**.
*   **Desfragmentador lógico & Gestor de caché**.
*   **Editor de registro & Texto**.

![System Manager](screenshots/readme_final/system_manager.png)

### 🎨 Suite gráfica & 🎧 Multimedia
*   **Gráficos:** Editor Paint 2D, CAD 2D, Visualizador 3D.
*   **Audio:** Reproductor musical, Grabadora, Panel de sonido.
*   **Apps:** Chat integrado, widgets flotantes.

![Apps Media](screenshots/readme_final/apps_media.png)

### ⚡ Optimización por IA
*   **Game Booster:** Optimizador de recursos para juegos.
*   **Modos de Energía:** Performance, Balanced, Power Saver.
*   **Smart Suspend:** Suspensión automática de ventanas inactivas.

---

## 📁 Estructura del repositorio

```text
/Neuro-OS-Desktop
│
├── neuro_os_v3_complete.py         # Entorno de escritorio principal
├── neuro_resource_manager.py       # Optimización y gestión de memoria
├── neuro_package_managers.py       # 4 gestores de paquetes
├── neuro_app_installer.py          # Instalador/desinstalador universal
├── neuro_essential_apps.py         # Apps esenciales
├── neuro_system_tools.py           # Herramientas del sistema
├── neuro_display_misc_control.py   # Configuración de pantalla y miscelánea
├── neuro_graphics_suite.py         # Paint + CAD + 3D Viewer
├── neuro_game_booster.py           # Optimizador de juegos con IA
├── about_neuro_os.py               # Panel About
│
└── SYSTEM_DATA/                    # Configuración, usuarios, iconos, cache
```

---

## ▶️ Ejecución

### Requisitos
*   **Python 3.11** o superior.
*   **PySide6** (Qt) + `pip` + `venv` recomendados.
*   Funciona en **Windows** o **Linux**.

### Instalación
```bash
pip install -r requirements.txt
```

### Ejecución
```bash
python neuro_os_v3_complete.py
```

---

## 🤖 Sobre el desarrollo

Este proyecto fue construido:
1.  En **2 días intensivos**.
2.  Con módulos previos del autor.
3.  Con **apoyo de IA** para acelerar arquitectura y código.
4.  Como **demostración técnica** y plataforma experimental.

> *No pretende competir con sistemas operativos reales, sino explorar conceptos de UX, IA, modularidad y ecosistemas cruzados.*

---

## ⭐ Estado del proyecto

### Actual
*   ✅ **100% funcional** como Desktop Environment.
*   ✅ Estable para pruebas, demos y entusiastas.
*   ✅ Compatible con Windows y Linux.

### Futuro
*   🚀 Kernel propio (**Neuro-Kernel v1.0**).
*   🚀 ISO completa booteable.
*   🚀 Versión Mobile & Integración VR/AR.
*   🚀 Marketplace oficial de apps.

---

## 🤝 Contribuciones & Contacto

**Pull requests bienvenidos.** Se aceptan módulos nuevos, apps, mejoras de seguridad y traducciones.

*   **Autor:** José Manuel Moreno Cano
*   **Email:** neuro.so.ia.sim@gmail.com

---

<div align="center">
  <h3>🧠 Neuro-OS Desktop</h3>
  <p><em>“Compatibilidad sin límites. Seguridad sin compromisos.”</em></p>
</div>
