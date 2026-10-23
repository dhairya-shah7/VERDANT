@echo off
title Packaging VERDANT Standalone Windows Executable (.EXE)
echo ========================================================
echo   Building Standalone VERDANT (.EXE) for Windows x64
echo ========================================================
cd /d "%~dp0"
call npm run build:exe
echo ========================================================
echo   BUILD COMPLETE!
echo   Executable created at: dist\VERDANT-win32-x64\VERDANT.exe
echo ========================================================
pause
