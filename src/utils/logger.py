"""
Logging Sistemi - Log Rotation ile İyileştirilmiş
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Constants'ı import et
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.constants import LogConstants, FileConstants


class AppLogger:
    """
    Uygulama logger'ı - Memory-safe log rotation ile
    
    Features:
        - Automatic log rotation (10MB max per file)
        - Keeps last 5 log files
        - UTF-8 encoding
        - Thread-safe
        - Both file and console output
    """
    
    def __init__(self, log_file: str = None):
        """
        Logger'ı başlat
        
        Args:
            log_file: Log dosya yolu (None ise default kullanılır)
        """
        # logs klasörünü oluştur
        os.makedirs(FileConstants.LOGS_DIR, exist_ok=True)
        
        if log_file is None:
            log_file = os.path.join(
                FileConstants.LOGS_DIR,
                FileConstants.LOG_FILE
            )
        
        self.log_file = log_file
        self.logger = logging.getLogger('Proje_Q')
        self.logger.setLevel(logging.DEBUG)
        
        # Formatter - Türkçe tarih formatı
        formatter = logging.Formatter(
            LogConstants.LOG_FORMAT,
            datefmt=LogConstants.DATE_FORMAT
        )
        
        # Rotating File Handler - Memory-safe log rotation
        # Max 10MB per file, keep last 5 files
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LogConstants.LOG_ROTATION_SIZE_MB * 1024 * 1024,
            backupCount=LogConstants.MAX_LOG_FILES,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Console handler - Konsola yaz
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Handler'ları ekle (duplicate check)
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """
        Bilgi logu
        
        Args:
            message: Log mesajı
        """
        self.logger.info(message)
    
    def warning(self, message: str):
        """
        Uyarı logu
        
        Args:
            message: Log mesajı
        """
        self.logger.warning(message)
    
    def error(self, message: str):
        """
        Hata logu
        
        Args:
            message: Log mesajı
        """
        self.logger.error(message)
    
    def debug(self, message: str):
        """
        Debug logu
        
        Args:
            message: Log mesajı
        """
        self.logger.debug(message)
    
    def critical(self, message: str):
        """
        Kritik hata logu
        
        Args:
            message: Log mesajı
        """
        self.logger.critical(message)
    
    def get_recent_logs(self, max_lines: int = 100) -> list:
        """
        Son N satırı al - Memory-efficient
        
        Args:
            max_lines: Maksimum satır sayısı
        
        Returns:
            list: Log satırları listesi
        """
        try:
            if not os.path.exists(self.log_file):
                return []
            
            # Dosya sonundan oku (daha efficient)
            with open(self.log_file, 'r', encoding='utf-8') as f:
                # Son N satırı al - deque kullanımı memory-efficient
                from collections import deque
                return list(deque(f, maxlen=max_lines))
        
        except Exception as e:
            self.logger.error(f"Log okuma hatası: {e}")
            return []


# Global logger instance
app_logger = AppLogger()