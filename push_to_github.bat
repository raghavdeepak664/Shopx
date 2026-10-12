@echo off
title Push ShopX to GitHub
echo ========================================================
echo   Pushing ShopX Repository to GitHub
echo ========================================================
echo.
cd /d "%~dp0"
echo Running: git push -u origin main
echo (If a browser popup appears, click 'Sign in with your browser' to authorize)
echo.
git push -u origin main
echo.
echo ========================================================
if %errorlevel% equ 0 (
    echo SUCCESS! Project successfully uploaded to:
    echo https://github.com/raghavdeepak664/shopx
) else (
    echo Push failed. Please check the error above.
)
echo ========================================================
pause
