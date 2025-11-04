# 🔧 Windsurf Reset Tool

[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/FlacoAfk/windsurf-reset-tool)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security](https://img.shields.io/badge/security-verified-brightgreen.svg)](docs/GUIA_SEGURIDAD.md)

> 🎓 **Proyecto Educativo**: Herramienta para estudiar el manejo de estado y persistencia de datos en aplicaciones de escritorio.

Herramienta completa en Python para resetear identificadores de dispositivo y datos de sesión de Windsurf, diseñada con fines educativos para comprender cómo las aplicaciones manejan la autenticación y el estado del usuario.

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar e instalar
git clone https://github.com/FlacoAfk/windsurf-reset-tool.git
cd windsurf-reset-tool
pip install -r requirements.txt

# 2. Ejecutar (Windows)
run_reset.bat

# 3. Reiniciar Windsurf
```

Para más opciones, consulta la sección [Uso](#-uso).

---

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Seguridad](#-seguridad)
- [Tests](#-tests)
- [Documentación](#-documentación)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## ⚠️ Propósito Educativo

Este proyecto fue creado con **fines educativos** para:

- 📚 Aprender sobre manejo de estado en aplicaciones desktop
- 🔍 Estudiar sistemas de persistencia de datos
- 💻 Practicar Python y administración de sistemas
- 🛠️ Comprender arquitectura de aplicaciones
- 🧪 Implementar suites de pruebas

**No está destinado a eludir términos de servicio.** Los usuarios son responsables de usar esta herramienta de acuerdo con las políticas de Windsurf.

---

## 🌟 Características

### ✨ Funcionalidades Principales

- 🗑️ **Limpieza completa** de 15+ tipos de archivos (cookies, cache, sesiones)
- 🆔 **Reseteo de identificadores** de dispositivo
- 🔐 **Eliminación de datos de autenticación**
- 💾 **Backups automáticos** con timestamp
- 🔍 **Detección automática** de procesos Windsurf
- ⚡ **Cierre automático** de la aplicación

### 🔒 Herramientas de Seguridad

- 🔑 **API Key Extractor** - Verifica claves de forma segura (enmascaradas)
- 📊 **Post-Reset Verify** - Confirmación de cambios con snapshots
- 🛡️ **Guía de Seguridad** - Aprende a proteger información sensible
- ✅ **Security Scanner** - Detecta API keys expuestas

### 🧪 Suite de Tests

- ✅ **Simulación dry-run** - Ver qué hará sin hacer cambios
- ✅ **Tests de seguridad** - Verificar limpieza de API keys
- ✅ **Verificación post-reset** - Confirmar cambios aplicados
- ✅ **Tests intensivos** - Validar configuración del sistema

---

## 🔧 Instalación

### Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes)

### Pasos

```bash
# Clonar repositorio
git clone https://github.com/FlacoAfk/windsurf-reset-tool.git
cd windsurf-reset-tool

# Instalar dependencias
pip install -r requirements.txt
```

---

## 📖 Uso

### Método 1: Launcher (Recomendado - Windows)

```bash
run_reset.bat
```

### Método 2: Python Directo

```bash
python windsurf_reset.py
```

### Método 3: Scripts Auxiliares

```bash
# Ver simulación (seguro, no hace cambios)
python scripts/simulate_reset.py

# Verificar procesos de Windsurf
python scripts/check_windsurf.py

# Verificar API keys de forma segura
python scripts/verify_api_key.py

# Verificar cambios después del reset
python scripts/post_reset_verify.py
```

### Método 4: Suite de Tests

```bash
# Ejecutar todos los tests
tests/run_all_tests.bat

# O individualmente
python tests/test_api_key_cleanup.py
python tests/test_comprehensive_security.py
python tests/test_script.py
```

---

## 📁 Estructura del Proyecto

```
windsurf-reset-tool/
│
├── 📄 README.md              # Este archivo
├── 📄 LICENSE                # Licencia MIT
├── 📄 requirements.txt       # Dependencias Python
├── 📄 .gitignore            # Archivos ignorados
│
├── 🔧 Scripts Principales
│   ├── windsurf_reset.py    # Script principal v2.1
│   ├── version.py           # Sistema de versionamiento
│   └── run_reset.bat        # Launcher Windows
│
├── 📁 docs/                  # Documentación
│   ├── README_ES.md         # Documentación en español
│   ├── GUIA_RAPIDA.md       # Guía de inicio rápido
│   ├── GUIA_SEGURIDAD.md    # Guía de seguridad
│   ├── GUIA_PRUEBAS.md      # Guía de tests
│   ├── CHANGELOG.md         # Historial de versiones
│   ├── CONTRIBUTING.md      # Guía de contribución
│   └── REPORTE_LIMPIEZA.md  # Reporte de seguridad
│
├── 📁 scripts/               # Scripts auxiliares
│   ├── api_key_extractor.py    # Extractor seguro de API keys
│   ├── check_windsurf.py       # Verificador de procesos
│   ├── post_reset_verify.py    # Verificación post-reset
│   ├── simulate_reset.py       # Simulación dry-run
│   ├── verify_api_key.py       # Verificador de API keys
│   ├── verify_changes.py       # Verificador de cambios
│   ├── run_simulation.bat      # Launcher simulación
│   ├── run_tests.bat           # Launcher tests
│   ├── run_complete_check.bat  # Check completo
│   └── verify_key.bat          # Launcher verificador
│
├── 📁 tests/                 # Suite de tests
│   ├── test_script.py              # Tests principales
│   ├── test_api_key_cleanup.py     # Tests de seguridad
│   ├── test_comprehensive_security.py  # Tests exhaustivos
│   └── run_all_tests.bat           # Ejecutar todos los tests
│
└── 📁 backups/               # Snapshots y backups
    └── snapshot_*.json       # Snapshots de estado
```

---

## 🔍 ¿Qué Hace Exactamente?

### Archivos que Elimina

```
%APPDATA%\Windsurf\
├── 🗑️ Cookies                 # Tokens de sesión
├── 🗑️ Local Storage           # Datos persistentes + API keys
├── 🗑️ Session Storage         # Sesiones temporales
├── 🗑️ Cache/                  # Cache general
├── 🗑️ IndexedDB/              # Base de datos local
├── 🗑️ User/globalStorage/codeium.windsurf/
├── 🗑️ User/workspaceStorage/
└── 🗑️ logs/                   # Logs
```

### Modificaciones en storage.json

- ✅ Elimina claves de telemetría antiguas
- ✅ Elimina claves de autenticación
- ✅ Genera 3 nuevos identificadores únicos:
  - `telemetry.machineId` (64 caracteres hex)
  - `telemetry.macMachineId` (64 caracteres hex)
  - `telemetry.devDeviceId` (UUID v4)

---

## 🛡️ Seguridad

### Características de Seguridad

- ✅ **Backups automáticos** antes de cualquier cambio
- ✅ **Enmascaramiento de API keys** en logs y output
- ✅ **Tests de seguridad** integrados
- ✅ **Scanner de API keys** para detectar exposiciones
- ✅ **Guía de seguridad** completa

### Verificar Seguridad del Proyecto

```bash
# Ejecutar scanner de seguridad
python tests/test_api_key_cleanup.py

# Ejecutar tests exhaustivos
python tests/test_comprehensive_security.py

# Ver reporte de seguridad
cat docs/REPORTE_LIMPIEZA.md
```

### Restaurar desde Backup

Los backups se guardan automáticamente como:
```
storage.json.backup_YYYYMMDD_HHMMSS
```

Para restaurar:
1. Ve a: `%APPDATA%\Windsurf\User\globalStorage\`
2. Renombra el backup a: `storage.json`
3. Reinicia Windsurf

---

## 🧪 Tests

### Ejecutar Tests

```bash
# Todos los tests
tests/run_all_tests.bat

# Tests individuales
python tests/test_script.py                      # Tests principales
python tests/test_api_key_cleanup.py             # Tests de seguridad
python tests/test_comprehensive_security.py       # Tests exhaustivos

# Simulación (seguro)
python scripts/simulate_reset.py
```

### Resultados Esperados

```
✅ Todas las pruebas pasadas
📊 45 archivos escaneados
🔒 0 vulnerabilidades encontradas
```

---

## 📚 Documentación

### Guías Principales

- 📖 [Guía Rápida](docs/GUIA_RAPIDA.md) - Inicio rápido en 5 minutos
- 🔒 [Guía de Seguridad](docs/GUIA_SEGURIDAD.md) - Protege tus API keys
- 🧪 [Guía de Pruebas](docs/GUIA_PRUEBAS.md) - Cómo usar los tests
- 📝 [Documentación ES](docs/README_ES.md) - Documentación completa

### Recursos Adicionales

- 📋 [Changelog](docs/CHANGELOG.md) - Historial de versiones
- 🤝 [Contributing](docs/CONTRIBUTING.md) - Guía de contribución
- 📊 [Reporte de Limpieza](docs/REPORTE_LIMPIEZA.md) - Reporte de seguridad

---

## 🎯 Flujo de Trabajo Recomendado

1. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar simulación** (seguro, no hace cambios)
   ```bash
   python scripts/simulate_reset.py
   ```

3. **Ejecutar tests** (verificar sistema)
   ```bash
   python tests/test_script.py
   ```

4. **Ejecutar reseteo** (hace cambios reales)
   ```bash
   python windsurf_reset.py
   ```

5. **Reiniciar Windsurf** (IMPORTANTE)

6. **Verificar cambios**
   ```bash
   python scripts/post_reset_verify.py
   ```

---

## 📊 Compatibilidad

### Sistemas Operativos

- ✅ Windows 10/11
- ✅ macOS (Monterey+)
- ✅ Linux (Ubuntu, Debian, Fedora)

### Python

- Versión mínima: **3.7**
- Recomendada: **3.9+**

### Dependencias

```txt
rich >= 13.0.0
psutil >= 5.9.0
```

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Este es un proyecto educativo.

### Proceso

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

Ver [CONTRIBUTING.md](docs/CONTRIBUTING.md) para más detalles.

---

## 📜 Licencia

Este proyecto está bajo la **Licencia MIT** - ver [LICENSE](LICENSE) para más detalles.

### ⚠️ Disclaimer Educativo

Este software se proporciona con **fines educativos**. Los autores no fomentan ni apoyan la elusión de términos de servicio. Los usuarios son responsables de asegurar que su uso cumple con todas las leyes aplicables y los términos de servicio de Windsurf.

---

## 🙏 Agradecimientos

- [Rich](https://github.com/Textualize/rich) - Interfaz de terminal hermosa
- [psutil](https://github.com/giampaolo/psutil) - Detección de procesos
- Comunidad de Python - Herramientas y bibliotecas

---

## 📞 Soporte

- 📖 **Documentación**: [docs/](docs/)
- 🐛 **Reportar Bugs**: [Issues](https://github.com/FlacoAfk/windsurf-reset-tool/issues)
- 💬 **Discusiones**: [Discussions](https://github.com/FlacoAfk/windsurf-reset-tool/discussions)

---

## 📈 Versionamiento

Versión actual: **2.1.0**

Este proyecto usa [Semantic Versioning](https://semver.org/):
- **MAJOR**: Cambios incompatibles
- **MINOR**: Nueva funcionalidad compatible
- **PATCH**: Corrección de bugs

Ver [CHANGELOG.md](docs/CHANGELOG.md) para el historial completo.

---

<div align="center">

### 🌟 Si este proyecto te fue útil, considera darle una estrella

**Hecho con ❤️ para la comunidad de aprendizaje de Python**

[⭐ Star](https://github.com/FlacoAfk/windsurf-reset-tool) • [🐛 Report Bug](https://github.com/FlacoAfk/windsurf-reset-tool/issues) • [✨ Request Feature](https://github.com/FlacoAfk/windsurf-reset-tool/issues)

</div>
