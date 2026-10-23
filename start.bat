@echo off
title VERDANT — Alexa+ Smart Companion Display
echo ========================================================
echo   Launching VERDANT Alexa+ Autonomous Companion System
echo   Powered by VERDE Consequence Runtime ^& Graph Salience
echo ========================================================

echo [1/2] Verifying Backend status on 127.0.0.1:8000...
netstat -ano | findstr /R /C:":8000 .*LISTENING" >nul
if %errorlevel% equ 0 (
    echo [INFO] Backend is already active on port 8000. Reusing live instance.
) else (
    echo [INFO] Starting VERDANT Backend on port 8000...
    cd /d "%~dp0backend"
    start /b python -m uvicorn server:app --host 127.0.0.1 --port 8000
    timeout /t 2 /nobreak >nul
)

echo [2/2] Launching Native Companion Display...
cd /d "%~dp0"
if exist "node_modules\electron" (
    start "" npx electron .
) else if exist "dist\VERDANT-win32-x64\VERDANT.exe" (
    start "" "dist\VERDANT-win32-x64\VERDANT.exe"
) else (
    start "" "%~dp0frontend\index.html"
)

echo ========================================================
echo   SYSTEM READY. Tap the microphone or click a prompt!
echo ========================================================
