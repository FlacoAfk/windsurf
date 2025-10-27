@echo off
chcp 65001 >nul
title Windsurf Reset Tool - Simulación (Dry-Run)

echo.
echo ================================================
echo   SIMULACIÓN DE RESETEO (DRY-RUN)
echo ================================================
echo.
echo Este script muestra QUÉ HARÁ el reseteo
echo SIN hacer ningún cambio real.
echo.
echo Es 100%% SEGURO - No modifica nada.
echo.

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

:: Verificar dependencias
python -c "import rich" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    python -m pip install -r requirements.txt >nul 2>&1
)

:: Ejecutar simulación
python simulate_reset.py

echo.
pause
