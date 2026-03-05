#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Proje_Q - Sistem Gereksinimleri Kontrol Scripti
Bu script, projenin çalışması için gerekli tüm programları ve Python paketlerini kontrol eder.
"""

import sys
import subprocess
import importlib.util
from pathlib import Path
import io

# Windows için UTF-8 desteği
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Renk kodları (Windows için basit versiyon)
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

def check_python_version():
    """Python versiyonunu kontrol et"""
    print_header("PYTHON VERSİYONU KONTROLÜ")
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version_str} kurulu (Minimum: 3.8)")
        return True
    else:
        print_error(f"Python {version_str} çok eski! (Minimum: 3.8 gerekli)")
        print_info("https://www.python.org/downloads/ adresinden Python 3.8+ indirin")
        return False

def check_pip():
    """pip versiyonunu kontrol et"""
    print_header("PIP KONTROLÜ")
    try:
        result = subprocess.run(['pip', '--version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version = result.stdout.strip()
        print_success(f"{version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_error("pip bulunamadı!")
        print_info("pip kurulumu için: python -m ensurepip --upgrade")
        return False

def check_git():
    """Git versiyonunu kontrol et"""
    print_header("GIT KONTROLÜ")
    try:
        result = subprocess.run(['git', '--version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version = result.stdout.strip()
        print_success(f"{version}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print_warning("Git bulunamadı (Opsiyonel)")
        print_info("https://git-scm.com/download/win adresinden Git indirebilirsiniz")
        return False

def check_package(package_name, import_name=None):
    """Bir Python paketinin kurulu olup olmadığını kontrol et"""
    if import_name is None:
        import_name = package_name
    
    spec = importlib.util.find_spec(import_name)
    if spec is not None:
        try:
            # Versiyonu almayı dene
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'Unknown')
            print_success(f"{package_name:20} v{version}")
            return True
        except Exception as e:
            print_warning(f"{package_name:20} kurulu ama import edilemiyor: {e}")
            return False
    else:
        print_error(f"{package_name:20} KURULU DEĞİL!")
        return False

def check_python_packages():
    """Tüm Python paketlerini kontrol et"""
    print_header("PYTHON PAKETLERİ KONTROLÜ")
    
    # Ana paketler
    packages = {
        'PyQt5': 'PyQt5',
        'pandas': 'pandas',
        'openpyxl': 'openpyxl',
        'xlrd': 'xlrd',
        'reportlab': 'reportlab',
        'pyinstaller': 'PyInstaller',
    }
    
    # Geliştirme paketleri (opsiyonel)
    dev_packages = {
        'pylint': 'pylint',
        'black': 'black',
        'mypy': 'mypy',
        'pytest': 'pytest',
    }
    
    print(f"\n{BOLD}Ana Paketler:{RESET}")
    results = []
    for display_name, import_name in packages.items():
        results.append(check_package(display_name, import_name))
    
    print(f"\n{BOLD}Geliştirme Paketleri (Opsiyonel):{RESET}")
    for display_name, import_name in dev_packages.items():
        check_package(display_name, import_name)
    
    return all(results)

def check_requirements_file():
    """requirements.txt dosyasını kontrol et"""
    print_header("REQUIREMENTS.TXT KONTROLÜ")
    
    req_file = Path('requirements.txt')
    if req_file.exists():
        print_success("requirements.txt dosyası mevcut")
        
        # Dosyayı oku ve paket sayısını göster
        with open(req_file, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() 
                    if l.strip() and not l.strip().startswith('#')]
        
        print_info(f"Toplam {len(lines)} paket tanımlı")
        return True
    else:
        print_error("requirements.txt dosyası bulunamadı!")
        return False

def check_project_structure():
    """Proje klasör yapısını kontrol et"""
    print_header("PROJE YAPISI KONTROLÜ")
    
    required_dirs = ['src', 'Data', 'database', 'logs', 'docs', 'tests']
    required_files = ['README.md', 'requirements.txt', 'VERSION', 'CHANGELOG.md']
    
    all_ok = True
    
    print(f"\n{BOLD}Klasörler:{RESET}")
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print_success(f"{dir_name}/")
        else:
            print_warning(f"{dir_name}/ bulunamadı")
            all_ok = False
    
    print(f"\n{BOLD}Dosyalar:{RESET}")
    for file_name in required_files:
        if Path(file_name).exists():
            print_success(f"{file_name}")
        else:
            print_warning(f"{file_name} bulunamadı")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """Özet raporu yazdır"""
    print_header("ÖZET RAPOR")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"\n{BOLD}Toplam Kontrol:{RESET} {total}")
    print_success(f"Başarılı: {passed}")
    if failed > 0:
        print_error(f"Başarısız: {failed}")
    
    print("\n" + "="*60)
    
    if all(results.values()):
        print_success(f"\n{BOLD}🎉 TÜM KONTROLLER BAŞARILI!{RESET}")
        print_info("Proje geliştirmeye hazır.")
    else:
        print_warning(f"\n{BOLD}⚠️  BAZI SORUNLAR VAR{RESET}")
        print_info("Eksik paketleri kurmak için: python setup_environment.py")
        print_info("Manuel kurulum için: pip install -r requirements.txt")

def main():
    """Ana fonksiyon"""
    print(f"\n{BLUE}{BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       PROJE_Q - SİSTEM GEREKSİNİMLERİ KONTROLÜ           ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(RESET)
    
    results = {
        'Python Versiyon': check_python_version(),
        'pip': check_pip(),
        'Git': check_git(),
        'requirements.txt': check_requirements_file(),
        'Python Paketleri': check_python_packages(),
        'Proje Yapısı': check_project_structure(),
    }
    
    print_summary(results)
    
    # Exit code: 0 = success, 1 = failure
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Kontrol iptal edildi.{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Beklenmeyen hata: {e}{RESET}")
        sys.exit(1)