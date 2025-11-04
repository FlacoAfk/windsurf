@echo off
echo.
echo ===============================================
echo    EJECUTANDO TODAS LAS PRUEBAS DE SEGURIDAD
echo ===============================================
echo.

echo [1/2] Ejecutando Test Basico...
echo.
python test_api_key_cleanup.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Test basico fallo
    exit /b 1
)

echo.
echo.
echo [2/2] Ejecutando Test Exhaustivo...
echo.
python test_comprehensive_security.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Test exhaustivo fallo
    exit /b 1
)

echo.
echo.
echo ===============================================
echo    TODAS LAS PRUEBAS COMPLETADAS CON EXITO
echo ===============================================
echo.
echo Estado: PROYECTO SEGURO
echo Archivo de reporte: REPORTE_LIMPIEZA.md
echo.
