@echo off
title Thermal YOLO Person Detection - Streamlit App
chcp 65001 >nul
cd /d "%~dp0"

echo =====================================================================
echo  THERMAL YOLO VISION - PHAT HIEN NGUOI TRONG ANH NHIET
echo  Khoa CNTT - Truong Dai hoc Cong nghe TP.HCM (HUTECH)
echo  Sinh vien: Nguyen Duc Hieu - MSSV: 24800600314
echo =====================================================================
echo.
echo Dang kiem tra moi truong Python va thu vien...

set PYTHON_EXE=.\.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo Khong tim thay Python trong .venv, thu tim trong he thong...
    set PYTHON_EXE=python
)

echo Dang khoi chay Streamlit Web Application...
"%PYTHON_EXE%" -m streamlit run app.py --server.headless=false

pause
