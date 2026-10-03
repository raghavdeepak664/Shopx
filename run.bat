@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title ShopX - Modern E-Commerce Server
echo ========================================================
echo   Starting ShopX E-Commerce Server (Amazon / Flipkart)
echo ========================================================
echo.
echo Server starting at http://127.0.0.1:5000 ...
echo Press Ctrl+C to stop.
echo.
python app.py
pause
