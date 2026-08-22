@echo off
title SmartHome AI
cd /d "%~dp0"
echo Starting SmartHome AI...
echo.
python -m streamlit run app.py
pause
