"""
Ana Program - Proje_Q JCL Veri Yönetim Sistemi
"""
import sys
from PyQt5.QtWidgets import QApplication

# Main window'u import et
from src.ui.main_window import MainWindow
from src.utils.logger import app_logger


def main():
    """Ana fonksiyon"""
    app_logger.info("=" * 60)
    app_logger.info("Proje_Q - JCL Veri Yönetim Sistemi v0.4.0")
    app_logger.info("=" * 60)
    
    app = QApplication(sys.argv)
    
    app_logger.info("PyQt5 uygulaması başlatıldı")
    
    window = MainWindow()
    window.show()
    
    app_logger.info("Ana pencere açıldı - Kullanıcı arayüzü hazır")
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()