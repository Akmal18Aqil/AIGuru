@echo off
title SiGURU AI Assistant Launcher
cls

echo ======================================================
echo           SIGURU AI ASSISTANT - LAUNCHER
echo ======================================================
echo.
echo Sedang menyiapkan aplikasi... mohon tunggu sebentar.
echo.

:: 1. Cek apakah Python terinstall
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan!
    echo Silakan install Python 10 ke atas dari python.org pertama kali.
    echo.
    pause
    exit /b
)

:: 2. Instalasi otomatis jika diperlukan
echo [1/2] Memeriksa kelengkapan sistem...
pip install -r requirements.txt --quiet

:: 3. Jalankan aplikasi
echo [2/2] Membuka antarmuka SiGURU...
echo.
echo JANGAN TUTUP JENDELA INI SELAMA MENGGUNAKAN APLIKASI.
echo.
streamlit run ui/app.py

pause
