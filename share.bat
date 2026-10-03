@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title ShopX - Public Sharing Launcher
echo ========================================================
echo   Starting ShopX with Public Worldwide URL
echo ========================================================
echo.

:: Start Flask server in background if not already running
netstat -ano | findstr :5000 >nul
if %errorlevel% neq 0 (
    echo Starting ShopX Flask server on port 5000...
    start /b python app.py
    timeout /t 3 /nobreak >nul
)

echo Starting Cloudflare Tunnel...
echo.
echo Look for your public URL below:
echo.
.\cloudflared.exe tunnel --url http://127.0.0.1:5000
pause
