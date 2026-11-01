@echo off
setlocal enabledelayedexpansion
title Thermal YOLO Vision Studio - Nhan dien Nguoi trong Anh Nhiet
chcp 65001 >nul

:: Chuyen thu muc lam viec ve chinh thu muc chua file run_app.bat
cd /d "%~dp0"

echo ==============================================================================
echo   THERMAL YOLO VISION STUDIO - PHAT HIEN NGUOI TRONG ANH NHIET (YOLOv8)
echo   De tai Mon hoc: Tri tue Nhan tao - Khoa CNTT - Truong Dai hoc HUTECH
echo   Sinh vien: Nguyen Duc Hieu (MSSV: 24800600314)
echo   GVHD: ThS./TS. Vu Thanh Hien
echo   Repository: https://github.com/11Hiu2k5/ThermalYoloPerson
echo ==============================================================================
echo.

:: -----------------------------------------------------------------------------
:: BUOC 1: KIEM TRA CAC FILE DU AN QUAN TRONG
:: -----------------------------------------------------------------------------
echo [*] Buoc 1/6: Kiem tra cac file nguon quan trong...

if not exist "app.py" goto :ERR_NO_APP
echo  [OK] Da tim thay file giao dien chinh: app.py

if not exist "requirements.txt" (
    echo  [CANH BAO] Khong tim thay requirements.txt trong thu muc du an.
) else (
    echo  [OK] Da tim thay danh sach thu vien: requirements.txt
)
echo.

:: -----------------------------------------------------------------------------
:: BUOC 2: XAC DINH MOI TRUONG PYTHON (UU TIEN TRUC TIEP .venv\Scripts\python.exe)
:: -----------------------------------------------------------------------------
echo [*] Buoc 2/6: Kiem tra va thiet lap moi truong Python...

set "PYTHON_EXE="
set "VENV_PY=.\.venv\Scripts\python.exe"

if exist "%VENV_PY%" goto :VENV_EXIST

:: Truong hop .venv chua ton tai
echo  [INFO] Moi truong ao cuc bo .venv chua ton tai.
echo  [*] Dang kiem tra Python tren he thong...

set "SYS_PY="
for /f "delims=" %%i in ('py -3 -c "import sys; print(sys.executable)" 2^>nul') do (
    if not defined SYS_PY set "SYS_PY=%%i"
)
if not defined SYS_PY (
    for /f "delims=" %%i in ('python -c "import sys; print(sys.executable)" 2^>nul') do (
        if not defined SYS_PY set "SYS_PY=%%i"
    )
)

if not defined SYS_PY goto :ERR_NO_PYTHON

echo  [OK] Tim thay Python he thong: "!SYS_PY!"
for /f "tokens=*" %%v in ('"!SYS_PY!" --version 2^>^&1') do echo      %%v
echo.
echo Ban co muon he thong tu dong tao moi truong ao .venv ngay bay gio khong?
set "AUTO_VENV="
set /p AUTO_VENV="[Y/N, Khuyen nghi Y, Mac dinh=Y]: "
if "!AUTO_VENV!"=="" set "AUTO_VENV=Y"
if /i not "!AUTO_VENV!"=="Y" goto :SKIP_AUTO_VENV

echo  [*] Dang khoi tao moi truong ao .venv tai "%cd%\.venv"...
"!SYS_PY!" -m venv .venv
if not exist "%VENV_PY%" goto :ERR_CREATE_VENV

set "PYTHON_EXE=%VENV_PY%"
echo  [OK] Tao moi truong ao .venv thanh cong!
echo  [*] Dang cap nhat pip va cai dat thu vien tu requirements.txt...
"%PYTHON_EXE%" -m pip install --upgrade pip
if exist "requirements.txt" (
    "%PYTHON_EXE%" -m pip install -r requirements.txt
)
goto :AFTER_PY_CHECK

:ERR_CREATE_VENV
echo  [CANH BAO] Tao .venv khong thanh cong. Chuyen sang dung Python he thong.
set "PYTHON_EXE=!SYS_PY!"
goto :AFTER_PY_CHECK

:SKIP_AUTO_VENV
echo  [INFO] Bo qua tao .venv. Chay truc tiep bang Python he thong: "!SYS_PY!"
set "PYTHON_EXE=!SYS_PY!"
goto :AFTER_PY_CHECK

:VENV_EXIST
set "PYTHON_EXE=%VENV_PY%"
echo  [OK] Phat hien moi truong ao cuc bo: %VENV_PY%
for /f "tokens=*" %%v in ('"%PYTHON_EXE%" --version 2^>^&1') do echo      %%v

:AFTER_PY_CHECK
echo.

:: -----------------------------------------------------------------------------
:: BUOC 3: KIEM TRA THU VIEN BAT BUOC (STREAMLIT, ULTRALYTICS, TORCH, OPENCV, NUMPY, PANDAS, PILLOW)
:: -----------------------------------------------------------------------------
echo [*] Buoc 3/6: Kiem tra cac thu vien bat buoc...

"%PYTHON_EXE%" -c "import importlib.util as u, sys; mods=('streamlit','ultralytics','torch','cv2','numpy','pandas','PIL'); [sys.exit(1) for m in mods if not u.find_spec(m)]" >nul 2>&1
if errorlevel 1 goto :LIBS_MISSING

echo  [OK] Tat ca thu vien cot loi da san sang: streamlit, ultralytics, torch, opencv, numpy, pandas, pillow.
goto :AFTER_LIBS_CHECK

:LIBS_MISSING
echo.
echo ==============================================================================
echo [LOI THIEU THU VIEN] Phat hien thieu mot so thu vien can thiet:
"%PYTHON_EXE%" -c "import importlib.util as u; [print(f'   [-] Thieu module: {m}') for m in ('streamlit','ultralytics','torch','cv2','numpy','pandas','PIL') if not u.find_spec(m)]"
echo.
echo Huong dan khac phuc:
echo  Ban co the mo Terminal va chay lenh cai dat:
echo     "%PYTHON_EXE%" -m pip install -r requirements.txt
echo ==============================================================================
echo.
set "INSTALL_REQ="
set /p INSTALL_REQ="Ban co muon he thong tu dong chay pip install tu requirements.txt ngay bay gio? [Y/N, Mac dinh=N]: "
if /i "!INSTALL_REQ!"=="Y" goto :DO_PIP_INSTALL
goto :ABORT_MISSING_LIBS

:DO_PIP_INSTALL
echo  [*] Dang cai dat thu vien tu requirements.txt, vui long doi...
"%PYTHON_EXE%" -m pip install -r requirements.txt
if errorlevel 1 goto :ERR_PIP_INSTALL

echo  [OK] Cai dat thu vien hoan tat thanh cong!
goto :AFTER_LIBS_CHECK

:ERR_PIP_INSTALL
echo.
echo ==============================================================================
echo [LOI CAI DAT] Qua trinh cai dat thu vien gap su co.
echo Vui long kiem tra lai ket noi Internet hoac chay lenh thu cong:
echo    "%PYTHON_EXE%" -m pip install -r requirements.txt
echo ==============================================================================
echo.
pause
exit /b 3

:ABORT_MISSING_LIBS
echo [HUY] Khong the khoi chay ung dung khi thieu cac thu vien can thiet.
pause
exit /b 3

:AFTER_LIBS_CHECK
echo.

:: -----------------------------------------------------------------------------
:: BUOC 4: KIEM TRA TRONG SO MO HINH (FLIR / LLVIP)
:: -----------------------------------------------------------------------------
echo [*] Buoc 4/6: Kiem tra cac file trong so mo hinh YOLO...

set "MODEL_FOUND=0"
if exist "models\flir_best.pt" (
    echo  [OK] Da tim thay mo hinh FLIR ADAS v2: models\flir_best.pt
    set "MODEL_FOUND=1"
) else (
    echo  [INFO] Chua co file: models\flir_best.pt
)

if exist "models\llvip_best.pt" (
    echo  [OK] Da tim thay mo hinh LLVIP: models\llvip_best.pt
    set "MODEL_FOUND=1"
) else (
    echo  [INFO] Chua co file: models\llvip_best.pt
)

if "!MODEL_FOUND!"=="0" (
    echo.
    echo  [CANH BAO MO HINH] Chua tim thay flir_best.pt hoac llvip_best.pt trong thu muc models\.
    echo  Ung dung se van khoi chay nhung chuc nang nhan dien anh nhiet co the bi anh huong.
    echo.
)
echo.

:: -----------------------------------------------------------------------------
:: BUOC 5: KIEM TRA CONG MANG 8501
:: -----------------------------------------------------------------------------
echo [*] Buoc 5/6: Kiem tra tinh trang cong mang 8501...

set "PORT_IN_USE=0"
set "OCCUPIED_PID="
for /f "tokens=5" %%p in ('netstat -ano ^| findstr /i ":8501 " ^| findstr /i "LISTENING"') do (
    set "PORT_IN_USE=1"
    set "OCCUPIED_PID=%%p"
)

if "!PORT_IN_USE!"=="1" goto :PORT_CONFLICT
echo  [OK] Cong mang 8501 dang trong va san sang ket noi.
goto :AFTER_PORT_CHECK

:PORT_CONFLICT
echo.
echo ==============================================================================
echo [CANH BAO CONG MANG] Cong 8501 dang bi su dung boi tien trinh co PID: !OCCUPIED_PID!
echo Nguyen nhan: Ung dung Streamlit truoc do hoac mot chuong trinh khac dang chay tren cong nay.
echo.
echo Huong dan xu ly:
echo  - Cach 1: Dong ung dung Streamlit dang chay o tab trinh duyet / CMD khac.
echo  - Cach 2: Mo Task Manager hoac chay CMD voi quyen Admin de giai phong cong:
echo             taskkill /F /PID !OCCUPIED_PID!
echo  - Cach 3: Neu tiep tuc chay, Streamlit se tu dong dung cong tiep theo (vi du 8502).
echo ==============================================================================
echo.
set "PROCEED_PORT="
set /p PROCEED_PORT="Ban co muon tiep tuc khoi chay ung dung khong? [Y/N, Mac dinh=Y]: "
if "!PROCEED_PORT!"=="" set "PROCEED_PORT=Y"
if /i "!PROCEED_PORT!"=="N" goto :CANCEL_PORT
goto :AFTER_PORT_CHECK

:CANCEL_PORT
echo [THONG TIN] Da huy khoi chay theo yeu cau.
pause
exit /b 0

:AFTER_PORT_CHECK
echo.

:: -----------------------------------------------------------------------------
:: BUOC 6: KHOI CHAY STREAMLIT WEB APPLICATION
:: -----------------------------------------------------------------------------
echo ==============================================================================
echo [*] Buoc 6/6: KHOI CHAY UNG DUNG THERMAL VISION STUDIO...
echo [*] Dia chi truy cap: http://localhost:8501
echo [*] Trinh duyet mac dinh se tu dong mo ngay khi Streamlit khoi dong thanh cong.
echo [*] Nhan Ctrl+C tai cua so nay neu ban muon dung ung dung.
echo ==============================================================================
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --server.address localhost --server.headless false
set "STREAMLIT_EXIT_CODE=%ERRORLEVEL%"

echo.
if !STREAMLIT_EXIT_CODE! neq 0 goto :ERR_STREAMLIT

echo ==============================================================================
echo [THONG BAO] Ung dung Streamlit da ket thuc thanh cong (Ma thoat: 0).
echo ==============================================================================
echo.
pause
exit /b 0

:ERR_STREAMLIT
echo ==============================================================================
echo [LOI STREAMLIT] Ung dung dung hoac gap su co (Ma loi thoat: !STREAMLIT_EXIT_CODE!).
echo Vui long doc ky cac thong bao loi chi tiet cua Python / Streamlit o tren.
echo ==============================================================================
echo.
pause
exit /b !STREAMLIT_EXIT_CODE!

:ERR_NO_PYTHON
echo.
echo ==============================================================================
echo [LOI HE THONG] Khong tim thay Python tren he thong Windows!
echo.
echo Huong dan cai dat Python:
echo  1. Truy cap trang chu: https://www.python.org/downloads/
echo  2. Tai ban cai dat Python 3.10, 3.11 hoac 3.12 [khuyen nghi ban 64-bit].
echo  3. Chay file cai dat, BAT BUOC TICH CHON: "Add python.exe to PATH".
echo  4. Sau khi cai dat xong, dong cua so nay va khoi chay lai run_app.bat.
echo ==============================================================================
echo.
pause
exit /b 1

:ERR_NO_APP
echo.
echo ==============================================================================
echo [LOI FILE NGUON] Khong tim thay file "app.py" tai: "%cd%"!
echo Nguyen nhan: File giao dien Streamlit bi xoa, doi ten hoac file .bat dat sai thu muc.
echo Huong dan: Vui long kiem tra lai thu muc du an ThermalYoloPerson.
echo ==============================================================================
echo.
pause
exit /b 2