@echo off
chcp 65001 >nul
title Verificación de API Key - Windsurf

echo.
echo ================================================
echo   Verificación de API Key - Windsurf
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

:: Verificar dependencias
echo Verificando dependencias...
python -c "import rich" >nul 2>&1
if errorlevel 1 (
    echo [!] Instalando dependencias...
    python -m pip install rich
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias
        pause
        exit /b 1
    )
)

echo [OK] Dependencias instaladas
echo.

:: Ejecutar verificación
python verify_api_key.py

if errorlevel 1 (
    echo.
    echo [ERROR] La verificación terminó con errores
    pause
    exit /b 1
)

echo.
pause
