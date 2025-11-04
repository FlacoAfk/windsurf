@echo off
REM Script completo de verificación y reset para Windsurf
REM Este script ejecuta todas las verificaciones necesarias
setlocal EnableDelayedExpansion

title Windsurf Complete Check Tool

REM Colores ANSI
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

echo.
echo %BLUE%================================================%RESET%
echo %BLUE%   Windsurf Complete Check Tool v1.0%RESET%
echo %BLUE%================================================%RESET%
echo.

REM Verificar que Python esté instalado
echo %YELLOW%[1/6] Verificando Python...%RESET%
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Error: Python no está instalado%RESET%
    echo Por favor instala Python desde https://www.python.org/
    pause
    exit /b 1
)
echo %GREEN%   ✓ Python instalado correctamente%RESET%
echo.

REM Verificar dependencias
echo %YELLOW%[2/6] Verificando dependencias...%RESET%
pip show rich >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%   Instalando dependencias...%RESET%
    pip install -r requirements.txt
)
echo %GREEN%   ✓ Dependencias instaladas%RESET%
echo.

REM Ejecutar pruebas intensivas
echo %YELLOW%[3/6] Ejecutando pruebas del sistema...%RESET%
python test_script.py
if errorlevel 1 (
    echo %RED%   × Algunas pruebas fallaron%RESET%
    echo %YELLOW%   Revisa los errores antes de continuar%RESET%
    pause
    exit /b 1
)
echo %GREEN%   ✓ Pruebas completadas%RESET%
echo.

REM Verificar API keys (sin exponerlas)
echo %YELLOW%[4/6] Verificando API keys (seguro)...%RESET%
python api_key_extractor.py
echo.

REM Guardar snapshot ANTES
echo %YELLOW%[5/6] Guardando snapshot del estado actual...%RESET%
python post_reset_verify.py --snapshot before
echo %GREEN%   ✓ Snapshot guardado%RESET%
echo.

REM Menú de opciones
echo %BLUE%================================================%RESET%
echo %BLUE%   MENÚ DE OPCIONES%RESET%
echo %BLUE%================================================%RESET%
echo.
echo   [1] Ejecutar SIMULACIÓN (seguro, no hace cambios)
echo   [2] Ejecutar RESET REAL
echo   [3] Solo VERIFICAR estado actual
echo   [4] Salir
echo.
set /p choice="Selecciona una opción (1-4): "

if "%choice%"=="1" (
    echo.
    echo %YELLOW%Ejecutando simulación...%RESET%
    python simulate_reset.py
    echo.
    echo %GREEN%Simulación completada. No se hicieron cambios reales.%RESET%
    pause
) else if "%choice%"=="2" (
    echo.
    echo %RED%================================================%RESET%
    echo %RED%   ADVERTENCIA: RESET REAL%RESET%
    echo %RED%================================================%RESET%
    echo.
    echo Este proceso hará cambios REALES en tu sistema:
    echo   - Cerrará Windsurf si está abierto
    echo   - Eliminará cookies y cache
    echo   - Reseteará Device IDs
    echo.
    set /p confirm="¿Estás seguro? (SI/no): "
    
    if /i "!confirm!"=="SI" (
        echo.
        echo %YELLOW%Ejecutando reset...%RESET%
        python windsurf_reset.py
        
        echo.
        echo %YELLOW%[6/6] Verificando cambios post-reset...%RESET%
        python post_reset_verify.py
        
        echo.
        echo %GREEN%================================================%RESET%
        echo %GREEN%   RESET COMPLETADO%RESET%
        echo %GREEN%================================================%RESET%
        echo.
        echo %YELLOW%IMPORTANTE:%RESET%
        echo   1. REINICIA Windsurf completamente
        echo   2. Inicia sesión con tu cuenta
        echo   3. Verifica que la API key sea DIFERENTE
        echo.
        pause
    ) else (
        echo.
        echo %YELLOW%Reset cancelado.%RESET%
        pause
    )
) else if "%choice%"=="3" (
    echo.
    echo %YELLOW%Verificando estado actual...%RESET%
    python post_reset_verify.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo %BLUE%Saliendo...%RESET%
    exit /b 0
) else (
    echo.
    echo %RED%Opción inválida%RESET%
    pause
)

endlocal
