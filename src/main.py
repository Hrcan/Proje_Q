"""
Ana Program - Proje_Q JCL Veri Yönetim Sistemi
"""
import sys
import os
import json
from PyQt5.QtWidgets import QApplication

# Main window'u import et
from ui.main_window import MainWindow
from ui.first_run_dialog import FirstRunDialog
from utils.logger import app_logger


def is_first_run():
    """İlk çalıştırma kontrolü"""
    config_file = os.path.join('config', 'user_prefs.json')
    
    if not os.path.exists(config_file):
        return True
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return not config.get('setup_completed', False)
    except:
        return True


def save_first_run_settings(settings):
    """İlk çalıştırma ayarlarını kaydet"""
    config_dir = 'config'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_file = os.path.join(config_dir, 'user_prefs.json')
    
    # Mevcut config'i oku
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except:
            pass
    
    # Setup ayarlarını ekle
    config['setup_completed'] = True
    config['excel_default_folder'] = settings.get('excel_folder', '')
    config['auto_load_last_db'] = settings.get('auto_load', True)
    config['auto_backup'] = settings.get('create_backup', True)
    
    # Kaydet
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
    
    app_logger.info(f"İlk çalıştırma ayarları kaydedildi: {config}")


def main():
    """Ana fonksiyon"""
    app_logger.info("=" * 60)
    app_logger.info("Proje_Q - JCL Veri Yönetim Sistemi v1.0.0")
    app_logger.info("=" * 60)
    
    app = QApplication(sys.argv)
    
    app_logger.info("PyQt5 uygulaması başlatıldı")
    
    # İlk çalıştırma kontrolü
    if is_first_run():
        app_logger.info("İlk çalıştırma tespit edildi - Setup dialog gösteriliyor")
        
        setup_dialog = FirstRunDialog()
        result = setup_dialog.exec_()
        
        if result == FirstRunDialog.Accepted:
            settings = setup_dialog.get_settings()
            save_first_run_settings(settings)
            app_logger.info("Setup tamamlandı - ayarlar kaydedildi")
        else:
            app_logger.info("Setup atlandı - varsayılan ayarlar kullanılacak")
            save_first_run_settings({})  # Sadece setup_completed flag'i kaydet
    
    window = MainWindow()
    window.show()
    
    app_logger.info("Ana pencere açıldı - Kullanıcı arayüzü hazır")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()