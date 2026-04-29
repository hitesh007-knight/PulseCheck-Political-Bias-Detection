@echo off
echo ========================================
echo PulseCheck - Starting Backend Server
echo ========================================
echo.
echo Starting Flask backend...
echo Do NOT close this window while the app is running!
echo.
cd /d "%~dp0.."
python app.py
pause
