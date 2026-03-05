#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proje_Q - Otomatik Ortam Kurulum Scripti
Bu script, projenin çalışması için gerekli tüm Python paketlerini otomatik kurar.
"""

import sys
import subprocess
import os
from pathlib import Path
import io

# Windows için UTF-8 desteği
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Renk kodları
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Başlık yazdır"""
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}{text:^60}{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")

def print_success(text):
    """Başarı mesajı"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_warning(text):
    """Uyarı mesajı"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_error(text):
    """Hata mesajı"""
    print(f"{RED}❌ {text}{RESET}")

def print_info(text):
    """Bilgi mesajı"""
    print(f"{BLUE}ℹ️  {text}{RESET}")

def print_step(step_num, total_steps, text):
    """Adım mesajı"""
    print(f"\n{BOLD}[{step_num}/{total_steps}] {text}{RESET}")

def check_python_version():
    """Python versiyonunu kontrol et"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} uygun")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor}.{version.micro} çok eski!")
        print_error("Python 3.8 veya üzeri gerekli")
        return False

def create_virtual_environment():
    """Virtual environment oluştur"""
    print_header("VIRTUAL ENVIRONMENT OLUŞTURMA")
    
    venv_path = Path('venv')
    
    if venv_path.exists():
        print_warning("Virtual environment zaten mevcut")
        response = input("Yeniden oluşturmak ister misiniz? (e/h): ")
        if response.lower() != 'e':
            print_info("Mevcut venv kullanılacak")
            return True
        else:
            print_info("Mevcut venv siliniyor...")
            import shutil
            shutil.rmtree(venv_path)
    
    print_info("Virtual environment oluşturuluyor...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], 
                      check=True)
        print_success("Virtual environment başarıyla oluşturuldu!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Virtual environment oluşturulamadı: {e}")
        return False

def get_pip_command():
    """Platform'a göre pip komutunu al"""
    if sys.platform == 'win32':
        return str(Path('venv') / 'Scripts' / 'pip.exe')
    else:
        return str(Path('venv') / 'bin' / 'pip')

def upgrade_pip():
    """pip'i güncelle"""
    print_header("PIP GÜNCELLEME")
    
    pip_cmd = get_pip_command()
    
    print_info("pip güncelleniyor...")
    try:
        subprocess.run([pip_cmd, 'install', '--upgrade', 'pip'], 
                      check=True)
        print_success("pip başarıyla güncellendi!")
        return True
    except subprocess.CalledProcessError as e:
        print_warning(f"pip güncellenemedi: {e}")
        return False

def install_requirements():
    """requirements.txt'ten paketleri kur"""
    print_header("PYTHON PAKETLERİNİ KURMA")
    
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print_error("requirements.txt dosyası bulunamadı!")
        return False
    
    pip_cmd = get_pip_command()
    
    print_info("Paketler kuruluyor... (Bu işlem birkaç dakika sürebilir)")
    print_info("Lütfen bekleyin...")
    
    try:
        subprocess.run([pip_cmd, 'install', '-r', 'requirements.txt'], 
                      check=True)
        print_success("Tüm paketler başarıyla kuruldu!")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Paket kurulumunda hata: {e}")
        return False

def verify_installation():
    """Kurulumu doğrula"""
    print_header("KURULUM DOĞRULAMA")
    
    if sys.platform == 'win32':
        python_cmd = str(Path('venv') / 'Scripts' / 'python.exe')
    else:
        python_cmd = str(Path('venv') / 'bin' / 'python')
    
    test_script = """
import sys
try:
    import PyQt5
    import pandas
    import openpyxl
    import reportlab
    print("✅ Tüm ana paketler başarıyla import edildi!")
    sys.exit(0)
except ImportError as e:
    print(f"❌ Import hatası: {e}")
    sys.exit(1)
"""
    
    try:
        result = subprocess.run([python_cmd, '-c', test_script], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print(result.stdout)
            return True
        else:
            print_error("Bazı paketler import edilemiyor!")
            print(result.stderr)
            return False
    except Exception as e:
        print_error(f"Doğrulama hatası: {e}")
        return False

def create_activation_script():
    """Aktivasyon scripti oluştur"""
    print_header("AKTİVASYON SCRİPTİ")
    
    if sys.platform == 'win32':
        script_name = 'activate_env.bat'
        content = """@echo off
echo Aktivating virtual environment...
call venv\\Scripts\\activate.bat
echo.
echo ✅ Virtual environment aktif!
echo.
echo Projeyi çalıştırmak için:
echo   python src/main.py
echo.
"""
    else:
        script_name = 'activate_env.sh'
        content = """#!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo ""
echo "✅ Virtual environment aktif!"
echo ""
echo "Projeyi çalıştırmak için:"
echo "  python src/main.py"
echo ""
"""
    
    with open(script_name, 'w') as f:
        f.write(content)
    
    # Unix sistemlerde executable yap
    if sys.platform != 'win32':
        os.chmod(script_name, 0o755)
    
    print_success(f"{script_name} oluşturuldu")
    print_info(f"Virtual environment'ı aktive etmek için: {script_name}")

def print_next_steps():
    """Sonraki adımları göster"""
    print_header("SONRAKİ ADIMLAR")
    
    print(f"{BOLD}Kurulum tamamlandı! 🎉{RESET}\n")
    
    if sys.platform == 'win32':
        print_info("1. Virtual environment'ı aktive edin:")
        print(f"   {BLUE}activate_env.bat{RESET}")
        print()
        print_info("2. Veya manuel olarak:")
        print(f"   {BLUE}venv\\Scripts\\activate{RESET}")
    else:
        print_info("1. Virtual environment'ı aktive edin:")
        print(f"   {BLUE}./activate_env.sh{RESET}")
        print()
        print_info("2. Veya manuel olarak:")
        print(f"   {BLUE}source venv/bin/activate{RESET}")
    
    print()
    print_info("3. Projeyi çalıştırın:")
    print(f"   {BLUE}python src/main.py{RESET}")
    print()
    print_info("4. Test etmek için:")
    print(f"   {BLUE}pytest tests/{RESET}")

def main():
    """Ana fonksiyon"""
    print(f"\n{BLUE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║          PROJE_Q - OTOMATIK ORTAM KURULUMU                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(RESET)
    
    total_steps = 6
    
    # Adım 1: Python versiyonu kontrolü
    print_step(1, total_steps, "Python versiyonu kontrolü")
    if not check_python_version():
        print_error("\nKurulum iptal edildi. Python 3.8+ kurun ve tekrar deneyin.")
        return False
    
    # Adım 2: Virtual environment oluştur
    print_step(2, total_steps, "Virtual environment oluşturma")
    if not create_virtual_environment():
        print_error("\nKurulum başarısız!")
        return False
    
    # Adım 3: pip'i güncelle
    print_step(3, total_steps, "pip güncelleme")
    upgrade_pip()  # Başarısız olsa da devam et
    
    # Adım 4: Paketleri kur
    print_step(4, total_steps, "Python paketlerini kurma")
    if not install_requirements():
        print_error("\nKurulum başarısız!")
        return False
    
    # Adım 5: Doğrula
    print_step(5, total_steps, "Kurulum doğrulama")
    if not verify_installation():
        print_warning("\nKurulum tamamlandı ama bazı sorunlar var!")
        return False
    
    # Adım 6: Aktivasyon scripti
    print_step(6, total_steps, "Aktivasyon scripti oluşturma")
    create_activation_script()
    
    # Sonraki adımlar
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Kurulum iptal edildi.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Beklenmeyen hata: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)