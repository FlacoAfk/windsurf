# 📋 Changelog - Windsurf Reset Tool

## 🎉 Versión 2.0 - Mejora Mayor (Actual)

### ✨ Nuevas Funcionalidades

1. **🔐 Reseteo Completo de Autenticación**
   - Ahora elimina cookies y sesiones almacenadas
   - Limpia tokens API antiguos
   - Remueve archivos de workspace storage
   - Elimina cache y datos temporales

2. **🔍 Detección Automática de Procesos**
   - Detecta si Windsurf está en ejecución
   - Ofrece cerrar automáticamente los procesos de Windsurf
   - Previene errores por archivos bloqueados

3. **🧹 Limpieza Profunda**
   - Elimina 15+ tipos de archivos diferentes
   - Limpia directorios de cache (Cache, GPUCache, Code Cache)
   - Remueve archivos de sesión (Session Storage, Local Storage)
   - Elimina IndexedDB y cookies
   - Limpia workspace storage específico de Windsurf

4. **📦 Instalación Simplificada**
   - Archivo `requirements.txt` para instalar dependencias fácilmente
   - Script batch `run_reset.bat` para Windows (inicio rápido)
   - Verifica automáticamente las dependencias

### 🔧 Mejoras Técnicas

1. **Limpieza de Claves en storage.json**
   - Ahora elimina TODAS las claves relacionadas con autenticación
   - Remueve claves que empiezan con: `telemetry`, `codeium`, `windsurf`, `auth`, `session`
   - Esto fuerza a Windsurf a generar nuevas API keys

2. **Mejor Manejo de Errores**
   - Mensajes de error más descriptivos
   - Continúa el proceso aunque algunos archivos no se puedan eliminar
   - Reporta cuántos archivos fueron eliminados

3. **Interfaz Mejorada**
   - Mensajes más claros sobre el proceso
   - Advertencias cuando Windsurf está en ejecución
   - Indicación clara de reiniciar Windsurf después del reseteo

### 📚 Documentación

1. **README_ES.md** - Documentación completa en español
2. **check_windsurf.py** - Script independiente para verificar procesos
3. **run_reset.bat** - Script de inicio rápido para Windows
4. **requirements.txt** - Lista de dependencias necesarias

---

## 📌 Versión 1.0 - Versión Original

### Funcionalidades Básicas

- Reseteo de IDs de dispositivo (machineId, macMachineId, devDeviceId)
- Creación de backups con timestamp
- Interfaz con Rich (colores y barras de progreso)
- Soporte multiplataforma (Windows, macOS, Linux)
- Visualización de IDs actuales y nuevos

### Problema Principal

❌ **No reseteaba la API key de Windsurf**
- Solo cambiaba los IDs de telemetría
- No eliminaba cookies ni sesiones
- La API key permanecía igual después del reseteo

---

## 🔄 ¿Por qué la Versión 2.0 Soluciona el Problema?

### El problema era:
La API key de Windsurf se almacena en **múltiples lugares**, no solo en `storage.json`:

1. **Cookies** - Tokens de sesión
2. **Local Storage** - Datos de autenticación persistentes
3. **Session Storage** - Tokens de sesión temporal
4. **IndexedDB** - Base de datos local con información de usuario
5. **Workspace Storage** - Configuraciones específicas de Windsurf/Codeium
6. **Cache** - Archivos temporales que pueden contener tokens

### La solución:
La versión 2.0 **elimina TODOS estos archivos**, forzando a Windsurf a:
- Generar nuevos identificadores de dispositivo
- Crear una nueva sesión desde cero
- Solicitar una nueva API key al servidor
- No reutilizar ningún token almacenado en cache

---

## 🚀 Mejoras Futuras Planificadas (v2.1+)

- [ ] Soporte para resetear múltiples instancias de VS Code
- [ ] Modo silencioso (sin confirmaciones)
- [ ] Exportar/importar configuraciones personalizadas
- [ ] Interfaz gráfica (GUI) opcional
- [ ] Auto-actualización del script

---

## 📞 Reporte de Problemas

Si después de usar la versión 2.0 sigues obteniendo la misma API key:

1. Asegúrate de que Windsurf esté **completamente cerrado**
2. Verifica que el script eliminó los archivos (debería mostrar "Removed X cache/session files")
3. **REINICIA** Windsurf después del reseteo (muy importante)
4. Si persiste, intenta ejecutar el script como administrador
5. Como última opción, desinstala Windsurf, ejecuta el script, y reinstala
