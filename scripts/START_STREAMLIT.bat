@echo off
echo ========================================
echo PulseCheck - Starting Frontend (Streamlit)
echo ========================================
echo.
echo Starting Streamlit frontend...
echo Browser will open automatically!
echo.
cd /d "%~dp0.."
streamlit run streamlit_app.py
pause
