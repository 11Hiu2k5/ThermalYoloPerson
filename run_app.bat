@echo off
setlocal enabledelayedexpansion
title Thermal YOLO Vision Studio - Nhan dien Nguoi trong Anh Nhiet
chcp 65001 >nul

:: Chuyen thu muc lam viec ve thu muc chua file bat nay
cd /d "%~dp0"

echo ==============================================================================
echo   THERMAL YOLO VISION STUDIO - PHAT HIEN NGUOI TRONG ANH NHIET (YOLOv8)
echo   De tai Mon hoc: Tri tue Nhan tao - Khoa CNTT - Truong Dai hoc HUTECH
echo   Sinh vien: Nguyen Duc Hieu (MSSV: 24800600314)
echo   GVHD: ThS./TS. Vu Thanh Hien
echo ==============================================================================
echo.

:: 1. Kiem tra va kich hoat moi truong ao .venv neu ton tai
set VENV_ACTIVATE=.\.venv\Scripts\activate.bat
if exist "%VENV_ACTIVATE%" (
    echo [OK] Phat hien moi truong ao cuc bo .venv
    echo [*] Dang kich hoat moi truong ao...
    call "%VENV_ACTIVATE%"
    if errorlevel 1 (
        echo [CANH BAO] Khong the kich hoat .venv, se thu dung Python he thong.
    )
) else (
    echo [THONG TIN] Khong thay thu muc .venv cuc bo, kiem tra Python tren he thong...
)

:: 2. Kiem tra lenh python co kha dung hay khong
where python >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==============================================================================
    echo [LOI NGHIEP TRONG] Khong tim thay Python tren may tinh cua ban!
    echo.
    echo Huong dan khac phuc:
    echo  1. Vui long cai dat Python 3.10, 3.11 hoac 3.12 tu trang chu https://www.python.org/
    echo  2. Khi cai dat, bat buoc tich vao o: "Add Python to PATH"
    echo  3. Sau do khoi dong lai may tinh hoac mo lai file nay.
    echo ==============================================================================
    echo.
    pause
    exit /b 1
)

:: 3. Kiem tra thu vien Streamlit
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==============================================================================
    echo [LOI] Tim thay Python nhung thieu thu vien "streamlit"!
    echo.
    echo Huong dan khac phuc:
    echo  Vui long mo terminal tai thu muc du an va chay lenh cai dat cac thu vien:
    echo     pip install -r requirements.txt
    echo ==============================================================================
    echo.
    pause
    exit /b 1
)

:: 4. Kiem tra thu vien Ultralytics & PyTorch
python -c "import ultralytics, torch, cv2" >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==============================================================================
    echo [CANH BAO] Mot so thu vien cot loi (ultralytics, torch hoac opencv) chua day du.
    echo Neu gap loi khi chay, vui long cai dat lai bang lenh:
    echo     pip install -r requirements.txt
    echo ==============================================================================
    echo.
)

:: 5. Khoi chay Streamlit Web Application
echo [*] Dang khoi chay ung dung Streamlit Web Studio...
echo [*] Trinh duyet se tu dong mo tai dia chi: http://localhost:8501
echo.
python -m streamlit run app.py --server.headless=false

:: 6. Xu ly sau khi ung dung dung
if errorlevel 1 (
    echo.
    echo ==============================================================================
    echo [THONG BAO] Ung dung da dung hoac gap su co khoi chay (Ma loi: %errorlevel%).
    echo Vui long kiem tra lai thong bao loi o tren de xu ly.
    echo ==============================================================================
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo [OK] Ung dung da dong an toan.
pause
exit /b 0
