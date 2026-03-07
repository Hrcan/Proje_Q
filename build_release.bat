@echo off
REM Proje_Q - Production Build Script
REM Version: 1.0.0
REM Windows Build Automation

echo ========================================
echo Proje_Q v1.0.0 - Production Build
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python bulunamadi! Lutfen Python yukleyin.
    pause
    exit /b 1
)

echo [1/7] Python kurulumu dogrulandi...

REM Clean previous builds
echo [2/7] Onceki build dosyalari temizleniyor...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
mkdir "dist"

REM Install/Update dependencies
echo [3/7] Gerekli kutuphaneler kontrol ediliyor...
pip install -r requirements.txt --quiet

REM Run PyInstaller
echo [4/7] Uygulama derleniyor (PyInstaller)...
pyinstaller Proje_Q.spec --clean --noconfirm

if not exist "dist\Proje_Q\Proje_Q.exe" (
    echo [ERROR] Build basarisiz! EXE olusturulamadi.
    pause
    exit /b 1
)

echo [5/7] EXE basariyla olusturuldu!

REM Copy additional files
echo [6/7] Ek dosyalar kopyalaniyor...
if not exist "dist\Proje_Q\config" mkdir "dist\Proje_Q\config"
if not exist "dist\Proje_Q\database" mkdir "dist\Proje_Q\database"
if not exist "dist\Proje_Q\logs" mkdir "dist\Proje_Q\logs"
if not exist "dist\Proje_Q\backup" mkdir "dist\Proje_Q\backup"

copy "README.md" "dist\Proje_Q\" >nul
copy "VERSION" "dist\Proje_Q\" >nul

REM Create .gitkeep files
type nul > "dist\Proje_Q\database\.gitkeep"
type nul > "dist\Proje_Q\logs\.gitkeep"
type nul > "dist\Proje_Q\backup\.gitkeep"

echo [7/7] Build tamamlandi!
echo.
echo ========================================
echo BUILD BASARILI!
echo ========================================
echo.
echo Dosya konumu: dist\Proje_Q\
echo Calistirmak icin: dist\Proje_Q\Proje_Q.exe
echo.
echo Installer olusturmak icin:
echo 1. Inno Setup yukleyin
echo 2. installer.iss dosyasini acin
echo 3. Compile butonuna basin
echo.

pause