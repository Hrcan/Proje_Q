"""
Uygulama Sabitleri - Magic Numbers Yerine
Proje_Q - JCL Veri Yönetim Sistemi
"""

# ==========================================
# UI CONSTANTS
# ==========================================
class UIConstants:
    """UI ile ilgili sabitler"""
    
    # Pencere Boyutları
    WINDOW_DEFAULT_WIDTH = 1800
    WINDOW_DEFAULT_HEIGHT = 900
    WINDOW_DEFAULT_X = 100
    WINDOW_DEFAULT_Y = 50
    
    # Splitter Boyutları
    MAIN_SPLITTER_LEFT_WIDTH = 1170
    MAIN_SPLITTER_RIGHT_WIDTH = 630
    
    # Güncellenme Süreleri (milisaniye)
    LOG_UPDATE_INTERVAL_MS = 500
    TIME_UPDATE_INTERVAL_MS = 1000
    
    # Log Panel
    LOG_PANEL_MAX_LINES = 100  # Artırıldı: 50 -> 100
    LOG_PANEL_WIDTH_PERCENT = 35
    
    # Tablo
    TABLE_SELECTION_MODE = "SelectRows"
    TABLE_ALTERNATING_ROWS = True
    
    # Başlık Yüksekliği
    HEADER_HEIGHT = 35


# ==========================================
# DATABASE CONSTANTS
# ==========================================
class DBConstants:
    """Veritabanı ile ilgili sabitler"""
    
    # Cache ve Performans
    CACHE_SIZE_MB = 64
    WAL_CHECKPOINT_INTERVAL = 1000
    
    # Timeouts (saniye)
    DB_TIMEOUT = 30
    DB_BUSY_TIMEOUT = 10
    
    # Yedekleme
    BACKUP_KEEP_COUNT = 10  # En son X yedek tutulur
    
    # Batch İşlemler
    BATCH_SIZE = 1000  # Batch insert için
    
    # Connection Pool
    MAX_CONNECTIONS = 5


# ==========================================
# FILE CONSTANTS
# ==========================================
class FileConstants:
    """Dosya işlemleri ile ilgili sabitler"""
    
    # Dizinler
    DATABASE_DIR = "database"
    BACKUP_DIR = "backup"
    LOGS_DIR = "logs"
    CONFIG_DIR = "config"
    DATA_DIR = "Data"
    
    # Dosya Adları
    DATABASE_FILE = "jcl_data.db"
    LOG_FILE = "app.log"
    PREFERENCES_FILE = "user_prefs.json"
    
    # Dosya Boyutları
    MAX_LOG_FILE_SIZE_MB = 10
    MAX_BACKUP_FILE_SIZE_MB = 100
    
    # Excel
    EXCEL_MAX_ROWS = 1000000  # Excel satır limiti


# ==========================================
# LOGGING CONSTANTS
# ==========================================
class LogConstants:
    """Logging ile ilgili sabitler"""
    
    # Log Levels
    LEVEL_DEBUG = "DEBUG"
    LEVEL_INFO = "INFO"
    LEVEL_WARNING = "WARNING"
    LEVEL_ERROR = "ERROR"
    LEVEL_CRITICAL = "CRITICAL"
    
    # Log Format
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
    
    # Log Rotation
    MAX_LOG_FILES = 5
    LOG_ROTATION_SIZE_MB = 10


# ==========================================
# VALIDATION CONSTANTS
# ==========================================
class ValidationConstants:
    """Veri doğrulama sabitleri"""
    
    # JCL Adı
    JCL_MIN_LENGTH = 1
    JCL_MAX_LENGTH = 255
    
    # Ay Formatı
    AY_REGEX = r"^\d{4}-\d{2}$"  # YYYY-MM
    
    # Sayısal Değerler
    MIN_HATALI_SAYI = 0
    MAX_HATALI_SAYI = 999999
    MIN_SURE = 0
    MAX_SURE = 999999999


# ==========================================
# SEARCH CONSTANTS
# ==========================================
class SearchConstants:
    """Arama ile ilgili sabitler"""
    
    # Wildcard
    WILDCARD_CHAR = "*"
    
    # Ayraçlar
    JCL_SEPARATORS = [",", " ", "\n", "\t"]
    
    # Sonuç Limitleri
    MAX_SEARCH_RESULTS = 10000
    DEFAULT_PAGE_SIZE = 100


# ==========================================
# THEME CONSTANTS
# ==========================================
class ThemeConstants:
    """Tema ile ilgili sabitler"""
    
    AVAILABLE_THEMES = ["light", "dark", "blue"]
    DEFAULT_THEME = "light"
    
    # Renkler
    PRIMARY_COLOR = "#2196F3"
    SECONDARY_COLOR = "#4CAF50"
    ERROR_COLOR = "#f44336"
    WARNING_COLOR = "#FF9800"
    SUCCESS_COLOR = "#4CAF50"


# ==========================================
# PERFORMANCE CONSTANTS
# ==========================================
class PerformanceConstants:
    """Performans ile ilgili sabitler"""
    
    # Thread Pool
    MAX_WORKER_THREADS = 4
    
    # Timeout'lar
    EXCEL_LOAD_TIMEOUT_SEC = 300  # 5 dakika
    DB_QUERY_TIMEOUT_SEC = 30
    
    # Memory
    MAX_MEMORY_USAGE_MB = 512


# ==========================================
# VERSION INFO
# ==========================================
VERSION = "1.0.0"
VERSION_DATE = "2026-03-08"
APP_NAME = "Proje_Q - JCL Veri Yönetim Sistemi"
