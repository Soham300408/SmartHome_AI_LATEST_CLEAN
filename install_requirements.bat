@echo off
title SmartHome AI - Install Requirements
cd /d "%~dp0"
echo.
echo Installing SmartHome AI requirements...
echo.
python -m pip install -r requirements.txt
echo.
echo ==========================================
echo Installation finished.
echo You can now double-click run_app.bat
echo ==========================================
pause
