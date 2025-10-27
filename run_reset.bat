@echo off
chcp 65001 >nul
title Windsurf Reset Tool - Inicio Rápido

echo.
echo ================================================
echo   Windsurf Reset Tool - Inicio Rápido
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
echo   Iniciando Windsurf Reset Tool...
echo ================================================
echo.

:: Ejecutar el script principal
python windsurf_reset.py

if errorlevel 1 (
    echo.
    echo [ERROR] El script terminó con errores
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Proceso completado
echo ================================================
echo.
pause
