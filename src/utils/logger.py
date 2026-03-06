"""
Logging Sistemi - Tüm işlemleri logla
"""
import logging
import os
from datetime import datetime


class AppLogger:
    """Uygulama logger'ı"""
    
    def __init__(self, log_file='logs/app.log'):
        """Logger'ı başlat"""
        # logs klasörünü oluştur
        os.makedirs('logs', exist_ok=True)
        
        self.log_file = log_file
        self.logger = logging.getLogger('Proje_Q')
        self.logger.setLevel(logging.DEBUG)
        
        # Formatter - Türkçe tarih formatı
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # File handler - Dosyaya yaz
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler - Konsola yaz
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Bilgi logu"""
        self.logger.info(message)
    
    def warning(self, message):
        """Uyarı logu"""
        self.logger.warning(message)
    
    def error(self, message):
        """Hata logu"""
        self.logger.error(message)
    
    def debug(self, message):
        """Debug logu"""
        self.logger.debug(message)


# Global logger instance
app_logger = AppLogger()