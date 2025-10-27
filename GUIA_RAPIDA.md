# ⚡ GUÍA RÁPIDA - Windsurf Reset Tool

## 🎯 Objetivo
Obtener una **NUEVA API KEY** de Windsurf eliminando TODOS los datos de sesión anteriores.

---

## 📋 PASOS RÁPIDOS (3 minutos)

### 1️⃣ INSTALAR DEPENDENCIAS (solo la primera vez)

#### Opción A - Automática (Recomendado):
```bash
# Doble click en:
run_reset.bat
```

#### Opción B - Manual:
```bash
pip install -r requirements.txt
```

---

### 2️⃣ CERRAR WINDSURF

**IMPORTANTE:** Windsurf debe estar completamente cerrado.

Si no lo cierras, el script te lo recordará y lo cerrará automáticamente.

---

### 3️⃣ EJECUTAR RESETEO

#### Opción A - Automática:
```bash
# Doble click en:
run_reset.bat
```

#### Opción B - Manual:
```bash
python windsurf_reset.py
```

---

### 4️⃣ EN EL MENÚ

```
Main Menu
━━━━━━━━━━━━━━━━━━━━━━━━
[1]  Reset device identifiers  ← SELECCIONA ESTA
[2]  View current configuration
[3]  Exit

Press a key to choose an option
```

Presiona `1` y luego `Enter`

---

### 5️⃣ CONFIRMAR

```
Would you like to create a backup before continuing? (y/n)
```

Recomendado: Presiona `y` para crear backup

```
Are you sure you want to reset the device identifiers? (y/n)
```

Presiona `y` para confirmar

---

### 6️⃣ ESPERA

El script mostrará:

```
🔍 Locating configuration files...
🧹 Cleaning authentication and session files...
Removed 12 cache/session files              ← Debe ser > 0
📁 Creating directories if missing...
📖 Loading configuration...
🔄 Generating new identifiers...
💾 Saving updated configuration...
✅ Finalizing reset...
```

---

### 7️⃣ REINICIAR WINDSURF

**MUY IMPORTANTE:**

```
⚠️  You must RESTART Windsurf completely for changes to take effect.
```

1. Cierra esta ventana
2. Abre Windsurf
3. Crea una cuenta nueva o inicia sesión

---

## ✅ VERIFICAR QUE FUNCIONÓ

### Método 1 - Ver configuración:
1. Ejecuta el script nuevamente
2. Presiona `2` (View current configuration)
3. Los IDs deberían ser diferentes

### Método 2 - Revisar API key:
1. Después de reiniciar Windsurf
2. Verifica tu API key en la configuración
3. Debería ser diferente a: `sk-ws-01-MbT-y1ibft2FFGhFLYzLkQMBhsM4fk6sUrsuRzuWM2hQBepmc0nbdAf2NeJd4tpyomfcC8_R8_60khHVamrO0n1t7fpYHQ`

---

## 🚨 SOLUCIÓN DE PROBLEMAS RÁPIDA

### Problema: "Mismo API key después del reseteo"

✅ **Solución:**
```bash
1. Cerrar Windsurf COMPLETAMENTE (verificar Task Manager)
2. Ejecutar el script COMO ADMINISTRADOR
3. Verificar que dice "Removed X files" (X > 0)
4. REINICIAR la computadora
5. Abrir Windsurf
```

---

### Problema: "Windsurf está en ejecución"

✅ **Solución:**
El script preguntará:
```
Would you like to automatically close Windsurf processes? (y/n)
```
Presiona `y` para cerrar automáticamente

---

### Problema: "No se instalaron las dependencias"

✅ **Solución:**
```bash
pip install rich psutil
```

O usa el script batch:
```bash
run_reset.bat
```

---

### Problema: "Permission denied" o "Acceso denegado"

✅ **Solución:**
```bash
# Windows: Click derecho en run_reset.bat
# → "Ejecutar como administrador"
```

---

## 📁 ARCHIVOS INCLUIDOS

| Archivo | Descripción |
|---------|-------------|
| `windsurf_reset.py` | Script principal mejorado |
| `run_reset.bat` | Inicio rápido (Windows) |
| `requirements.txt` | Dependencias necesarias |
| `README_ES.md` | Documentación completa |
| `RESUMEN_MEJORAS.md` | Cambios implementados |
| `GUIA_RAPIDA.md` | Esta guía |
| `check_windsurf.py` | Verificador independiente |
| `CHANGELOG.md` | Historial de versiones |

---

## 🎯 LO MÁS IMPORTANTE

### ✅ ANTES del reseteo:
- [ ] Instalar dependencias (`pip install -r requirements.txt`)
- [ ] Cerrar Windsurf completamente

### ✅ DURANTE el reseteo:
- [ ] Presionar `1` en el menú
- [ ] Crear backup (recomendado)
- [ ] Confirmar el reseteo
- [ ] Verificar que dice "Removed X files" (X > 0)

### ✅ DESPUÉS del reseteo:
- [ ] **REINICIAR WINDSURF** ← ¡MUY IMPORTANTE!
- [ ] Crear cuenta nueva / Iniciar sesión
- [ ] Verificar que la API key sea diferente

---

## 💡 TIPS ADICIONALES

1. **Ejecuta como administrador** si tienes problemas de permisos
2. **Reinicia la PC** si persisten problemas
3. **Crea backup** siempre antes del reseteo
4. **Espera 10-15 segundos** antes de abrir Windsurf después del reseteo
5. **No uses la opción 3 (Exit)** hasta completar el proceso

---

## 📞 FLUJO COMPLETO EN 1 IMAGEN

```
┌─────────────────────────────────────────┐
│  1. Instalar dependencias               │
│     run_reset.bat                       │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  2. Cerrar Windsurf                     │
│     (o dejar que el script lo cierre)   │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  3. Ejecutar script                     │
│     python windsurf_reset.py            │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  4. Presionar 1 (Reset)                 │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  5. Crear backup (y)                    │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  6. Confirmar reseteo (y)               │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  7. Esperar (automático)                │
│     - Limpia archivos                   │
│     - Genera nuevos IDs                 │
│     - Guarda configuración              │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  8. REINICIAR WINDSURF                  │
│     ⚠️  PASO CRÍTICO                    │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  9. Crear cuenta / Iniciar sesión       │
└─────────────┬───────────────────────────┘
              ▼
┌─────────────────────────────────────────┐
│  10. ✅ NUEVA API KEY GENERADA          │
└─────────────────────────────────────────┘
```

---

## 🎉 ¡LISTO!

Si seguiste estos pasos, deberías tener una **NUEVA API KEY**.

Si aún tienes problemas, revisa:
- `README_ES.md` - Documentación completa
- `RESUMEN_MEJORAS.md` - Detalles técnicos
- `CHANGELOG.md` - Historial de cambios

---

*¡Mucha suerte con tu nueva API key de Windsurf! 🚀*
