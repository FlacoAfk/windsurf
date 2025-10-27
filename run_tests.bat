@echo off
chcp 65001 >nul
title Windsurf Reset Tool - Pruebas Intensivas

echo.
echo ================================================
echo   Windsurf Reset Tool - PRUEBAS INTENSIVAS
echo ================================================
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

:: Verificar si las dependencias están instaladas
echo Verificando dependencias...
python -c "import rich" >nul 2>&1
if errorlevel 1 (
    echo [!] Instalando dependencias necesarias...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas correctamente
) else (
    echo [OK] Dependencias ya instaladas
)

echo.
echo ================================================
echo   Ejecutando suite de pruebas...
echo ================================================
echo.
echo Este script NO hace cambios destructivos.
echo Solo verifica que todo está listo para el reseteo.
echo.

:: Ejecutar el script de pruebas
python test_script.py

if errorlevel 1 (
    echo.
    echo ================================================
    echo   [ERROR] Algunas pruebas fallaron
    echo ================================================
    echo.
    echo Revisa los errores antes de ejecutar el reseteo.
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   [OK] Todas las pruebas pasaron
echo ================================================
echo.
echo El script está listo para ejecutarse.
echo.
echo Para ejecutar el reseteo real, ejecuta:
echo   run_reset.bat
echo.
pause
