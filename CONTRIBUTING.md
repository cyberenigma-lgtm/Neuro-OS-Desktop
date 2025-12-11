# Contribuir a Neuro-OS Desktop

Gracias por tu interés en contribuir a Neuro-OS Desktop. Este proyecto busca crear una experiencia de escritorio modular en Python, abierta a mejoras de la comunidad.

Este documento explica cómo proponer cambios, cómo trabajar con el código y qué se espera en una contribución.

## 1. Cómo empezar

1. Haz un fork del repositorio.
2. Crea una rama para tu mejora o corrección:
```bash
git checkout -b feature/nombre-de-tu-feature
```
3. Realiza tus cambios y pruébalos localmente.
4. Abre un Pull Request siguiendo la plantilla incluida.

## 2. Requisitos técnicos básicos

Para ejecutar el proyecto necesitas:
- **Python 3.11+**
- **PySide6 (Qt for Python)**
- Dependencias listadas en el README

Para instalar dependencias:
```bash
pip install -r requirements.txt
```

Ejecutar el proyecto:
```bash
python src/neuro_os_v3_complete.py
```

## 3. Reglas de estilo y calidad

- Intenta que tu código sea claro, comentado y modularizado.
- No realices cambios en varias áreas no relacionadas en un mismo PR.
- Evita introducir dependencias nuevas sin discutirlo antes.
- Si tu cambio afecta la interfaz, incluye capturas de pantalla.

## 4. Issues

Antes de abrir un Issue:
- Revisa que no exista uno similar.
- Describe claramente el problema o propuesta.
- Incluye pasos para reproducir errores si corresponde.

Para tareas pequeñas aptas para principiantes, búscalas bajo la etiqueta: `good first issue`

## 5. Pull Requests

Tu PR debe incluir:
- Descripción clara del cambio.
- Justificación o motivación.
- Capturas si afecta la UI.
- Referencia al Issue asociado (si aplica).
- Confirmación de que lo has probado.

El equipo revisará y dará feedback si es necesario.

## 6. Conducta

Toda interacción debe seguir las reglas del CODE OF CONDUCT.
Este proyecto busca mantener un ambiente respetuoso, profesional y constructivo.

## 7. Preguntas

Si quieres discutir una idea antes de implementarla, utiliza **GitHub Discussions** (cuando esté activado).
