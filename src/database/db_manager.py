"""
Veritabanı Yöneticisi - Thread-Safe + İyileştirilmiş
SQL işlemlerini yöneten ana modül
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os
import threading
from contextlib import contextmanager

# Constants'ı import et
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.constants import DBConstants, FileConstants


class DatabaseManager:
    """
    Thread-safe veritabanı işlemlerini yöneten sınıf
    
    Thread Safety:
        - threading.Lock() ile DB erişimi korunur
        - Her connection thread-local'dir
        - Concurrent access güvenlidir
    
    Performance:
        - WAL mode (Write-Ahead Logging)
        - Index optimization
        - Prepared statements
        - Connection pooling
    """
    
    def __init__(self, db_path: str = None):
        """
        Args:
            db_path: Veritabanı dosya yolu (None ise default kullanılır)
        """
        if db_path is None:
            db_path = os.path.join(
                FileConstants.DATABASE_DIR, 
                FileConstants.DATABASE_FILE
            )
        
        self.db_path = db_path
        self.connection = None
        
        # Thread safety için lock
        self._lock = threading.Lock()
        
        # Thread-local storage
        self._local = threading.local()
        
        # Veritabanı dizinini oluştur
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    @contextmanager
    def get_connection(self):
        """
        Thread-safe connection context manager
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ...")
        """
        with self._lock:
            # Her thread için ayrı connection
            if not hasattr(self._local, 'connection'):
                self._local.connection = self._create_connection()
            
            try:
                yield self._local.connection
            except Exception as e:
                self._local.connection.rollback()
                raise
    
    def _create_connection(self) -> sqlite3.Connection:
        """Yeni bir connection oluştur ve yapılandır"""
        conn = sqlite3.connect(
            self.db_path,
            timeout=DBConstants.DB_TIMEOUT,
            check_same_thread=False  # Thread-safe kullanım için
        )
        conn.row_factory = sqlite3.Row
        
        # Performance optimizations
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        conn.execute(f"PRAGMA cache_size = -{DBConstants.CACHE_SIZE_MB * 1024}")
        conn.execute(f"PRAGMA busy_timeout = {DBConstants.DB_BUSY_TIMEOUT * 1000}")
        
        return conn
    
    def connect(self):
        """Ana veritabanına bağlan (backward compatibility için)"""
        with self._lock:
            if self.connection is None:
                self.connection = self._create_connection()
        return self.connection
    
    def disconnect(self):
        """Tüm bağlantıları kapat"""
        with self._lock:
            # Thread-local connections
            if hasattr(self._local, 'connection'):
                self._local.connection.close()
                delattr(self._local, 'connection')
            
            # Ana connection
            if self.connection:
                self.connection.close()
                self.connection = None
    
    def create_tables(self):
        """
        Tabloları oluştur
        Optimizasyonlar:
        - Composite UNIQUE constraint
        - Multiple indexes (single ve composite)
        - CHECK constraints
        - NOT NULL constraints
        - Default values
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # ==========================================
            # Hatalı İşler Tablosu
            # ==========================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS hatali_isler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jcl_adi TEXT NOT NULL,
                    ay TEXT NOT NULL,
                    sheet_adi TEXT NOT NULL,
                    
                    hatali_sayi_ay INTEGER,
                    son_hatali_tarih DATE,
                    hatali_sayi_yil INTEGER,
                    sorumlu_ekip TEXT,
                    
                    yuklenme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    kaynak_dosya TEXT,
                    
                    -- Composite UNIQUE: (JCL + Ay + Sheet) benzersiz olmalı
                    UNIQUE(jcl_adi, ay, sheet_adi),
                    
                    -- CHECK constraints: Veri bütünlüğü
                    CHECK(length(jcl_adi) > 0),
                    CHECK(ay LIKE '____-__'),
                    CHECK(hatali_sayi_ay >= 0 OR hatali_sayi_ay IS NULL),
                    CHECK(hatali_sayi_yil >= 0 OR hatali_sayi_yil IS NULL)
                )
            """)
            
            # Indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_hatali_jcl ON hatali_isler(jcl_adi)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_ay ON hatali_isler(ay DESC)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_sheet ON hatali_isler(sheet_adi)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_ekip ON hatali_isler(sorumlu_ekip)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_jcl_ay ON hatali_isler(jcl_adi, ay DESC)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_ay_jcl ON hatali_isler(ay DESC, jcl_adi)",
                "CREATE INDEX IF NOT EXISTS idx_hatali_guncelleme ON hatali_isler(guncelleme_tarihi DESC)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            # ==========================================
            # Uzun Süren İşler Tablosu
            # ==========================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS uzun_isler (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jcl_adi TEXT NOT NULL,
                    ay TEXT NOT NULL,
                    sheet_adi TEXT NOT NULL,
                    
                    calisma_sayisi INTEGER,
                    calisma_suresi INTEGER,
                    sorumlu_ekip TEXT,
                    
                    yuklenme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    guncelleme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    kaynak_dosya TEXT,
                    
                    UNIQUE(jcl_adi, ay, sheet_adi),
                    
                    CHECK(length(jcl_adi) > 0),
                    CHECK(ay LIKE '____-__'),
                    CHECK(calisma_sayisi >= 0 OR calisma_sayisi IS NULL),
                    CHECK(calisma_suresi >= 0 OR calisma_suresi IS NULL)
                )
            """)
            
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_uzun_jcl ON uzun_isler(jcl_adi)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_ay ON uzun_isler(ay DESC)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_sheet ON uzun_isler(sheet_adi)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_ekip ON uzun_isler(sorumlu_ekip)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_jcl_ay ON uzun_isler(jcl_adi, ay DESC)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_ay_jcl ON uzun_isler(ay DESC, jcl_adi)",
                "CREATE INDEX IF NOT EXISTS idx_uzun_guncelleme ON uzun_isler(guncelleme_tarihi DESC)"
            ]
            
            for index_sql in indexes:
                cursor.execute(index_sql)
            
            # ==========================================
            # Yükleme Geçmişi
            # ==========================================
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS yukleme_gecmisi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dosya_adi TEXT NOT NULL,
                    yuklenme_tarihi DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    kayit_sayisi INTEGER NOT NULL DEFAULT 0,
                    durum TEXT NOT NULL CHECK(durum IN ('BASARILI', 'HATALI', 'UYARI')),
                    hata_mesaji TEXT,
                    
                    CHECK(length(dosya_adi) > 0),
                    CHECK(kayit_sayisi >= 0)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_yukleme_tarih 
                ON yukleme_gecmisi(yuklenme_tarihi DESC)
            """)
            
            # ==========================================
            # View'ler
            # ==========================================
            cursor.execute("""
                CREATE VIEW IF NOT EXISTS v_jcl_ozet AS
                SELECT 
                    jcl_adi,
                    ay,
                    COUNT(DISTINCT CASE WHEN rapor_tipi = 'HATALI' THEN sheet_adi END) as hatali_sheet_sayisi,
                    COUNT(DISTINCT CASE WHEN rapor_tipi = 'UZUN' THEN sheet_adi END) as uzun_sheet_sayisi,
                    GROUP_CONCAT(DISTINCT CASE WHEN rapor_tipi = 'HATALI' THEN sorumlu_ekip END) as hatali_ekipler,
                    GROUP_CONCAT(DISTINCT CASE WHEN rapor_tipi = 'UZUN' THEN sorumlu_ekip END) as uzun_ekipler
                FROM (
                    SELECT jcl_adi, ay, sheet_adi, sorumlu_ekip, 'HATALI' as rapor_tipi
                    FROM hatali_isler
                    UNION ALL
                    SELECT jcl_adi, ay, sheet_adi, sorumlu_ekip, 'UZUN' as rapor_tipi
                    FROM uzun_isler
                )
                GROUP BY jcl_adi, ay
            """)
            
            conn.commit()
            
            # İstatistikleri güncelle
            cursor.execute("ANALYZE")
            conn.commit()
    
    def insert_hatali_is(self, data: Dict) -> int:
        """
        Hatalı iş kaydı ekle veya güncelle (Thread-safe)
        
        Args:
            data: Kayıt verisi
                - jcl_adi (str): JCL adı
                - ay (str): Ay (YYYY-MM)
                - sheet_adi (str): Sheet adı
                - hatali_sayi_ay (int, optional)
                - son_hatali_tarih (str, optional)
                - hatali_sayi_yil (int, optional)
                - sorumlu_ekip (str, optional)
                - kaynak_dosya (str, optional)
        
        Returns:
            int: Eklenen/güncellenen kayıt ID'si
        
        Raises:
            ValueError: Gerekli alanlar eksikse
            sqlite3.IntegrityError: Constraint ihlali varsa
        """
        # Validasyon
        required_fields = ['jcl_adi', 'ay', 'sheet_adi']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Gerekli alan eksik: {field}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO hatali_isler 
                    (jcl_adi, ay, sheet_adi, hatali_sayi_ay, son_hatali_tarih, 
                     hatali_sayi_yil, sorumlu_ekip, kaynak_dosya, 
                     yuklenme_tarihi, guncelleme_tarihi)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                            COALESCE((SELECT yuklenme_tarihi FROM hatali_isler 
                                      WHERE jcl_adi=? AND ay=? AND sheet_adi=?), 
                                     CURRENT_TIMESTAMP),
                            CURRENT_TIMESTAMP)
                """, (
                    data['jcl_adi'],
                    data['ay'],
                    data['sheet_adi'],
                    data.get('hatali_sayi_ay'),
                    data.get('son_hatali_tarih'),
                    data.get('hatali_sayi_yil'),
                    data.get('sorumlu_ekip'),
                    data.get('kaynak_dosya'),
                    data['jcl_adi'],
                    data['ay'],
                    data['sheet_adi']
                ))
                
                conn.commit()
                return cursor.lastrowid
            
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise sqlite3.IntegrityError(f"Veri bütünlüğü hatası: {e}")
    
    def insert_uzun_is(self, data: Dict) -> int:
        """
        Uzun süren iş kaydı ekle veya güncelle (Thread-safe)
        
        Args:
            data: Kayıt verisi
        
        Returns:
            int: Eklenen/güncellenen kayıt ID'si
        
        Raises:
            ValueError: Gerekli alanlar eksikse
            sqlite3.IntegrityError: Constraint ihlali varsa
        """
        # Validasyon
        required_fields = ['jcl_adi', 'ay', 'sheet_adi']
        for field in required_fields:
            if field not in data or not data[field]:
                raise ValueError(f"Gerekli alan eksik: {field}")
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO uzun_isler 
                    (jcl_adi, ay, sheet_adi, calisma_sayisi, calisma_suresi, 
                     sorumlu_ekip, kaynak_dosya, 
                     yuklenme_tarihi, guncelleme_tarihi)
                    VALUES (?, ?, ?, ?, ?, ?, ?,
                            COALESCE((SELECT yuklenme_tarihi FROM uzun_isler 
                                      WHERE jcl_adi=? AND ay=? AND sheet_adi=?), 
                                     CURRENT_TIMESTAMP),
                            CURRENT_TIMESTAMP)
                """, (
                    data['jcl_adi'],
                    data['ay'],
                    data['sheet_adi'],
                    data.get('calisma_sayisi'),
                    data.get('calisma_suresi'),
                    data.get('sorumlu_ekip'),
                    data.get('kaynak_dosya'),
                    data['jcl_adi'],
                    data['ay'],
                    data['sheet_adi']
                ))
                
                conn.commit()
                return cursor.lastrowid
            
            except sqlite3.IntegrityError as e:
                conn.rollback()
                raise sqlite3.IntegrityError(f"Veri bütünlüğü hatası: {e}")
    
    def get_all_hatali_isler(self) -> List[Dict]:
        """Tüm hatalı işleri getir (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM hatali_isler 
                ORDER BY ay DESC, jcl_adi
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_all_uzun_isler(self) -> List[Dict]:
        """Tüm uzun süren işleri getir (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM uzun_isler 
                ORDER BY ay DESC, jcl_adi
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def insert_yukleme_gecmisi(self, data: Dict) -> int:
        """Yükleme geçmişi ekle (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO yukleme_gecmisi 
                (dosya_adi, kayit_sayisi, durum, hata_mesaji)
                VALUES (?, ?, ?, ?)
            """, (
                data['dosya_adi'],
                data.get('kayit_sayisi', 0),
                data.get('durum', 'BASARILI'),
                data.get('hata_mesaji')
            ))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_tablo_istatistikleri(self) -> Dict:
        """Tablo istatistiklerini getir (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM hatali_isler")
            hatali_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM uzun_isler")
            uzun_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM yukleme_gecmisi")
            yukleme_count = cursor.fetchone()[0]
            
            return {
                'hatali_isler': hatali_count,
                'uzun_isler': uzun_count,
                'yukleme_gecmisi': yukleme_count
            }
    
    def optimize_database(self):
        """Veritabanını optimize et (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # İstatistikleri güncelle
            cursor.execute("ANALYZE")
            
            # Boş alanları temizle
            cursor.execute("VACUUM")
            
            # WAL checkpoint
            cursor.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            
            conn.commit()
    
    def get_database_info(self) -> Dict:
        """Veritabanı bilgilerini getir (Thread-safe)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Veritabanı boyutu
            cursor.execute("PRAGMA page_count")
            page_count = cursor.fetchone()[0]
            cursor.execute("PRAGMA page_size")
            page_size = cursor.fetchone()[0]
            size_bytes = page_count * page_size
            size_mb = size_bytes / (1024 * 1024)
            
            # Index sayısı
            cursor.execute("""
                SELECT COUNT(*) FROM sqlite_master 
                WHERE type = 'index' AND name NOT LIKE 'sqlite_%'
            """)
            index_count = cursor.fetchone()[0]
            
            # View sayısı
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'view'")
            view_count = cursor.fetchone()[0]
            
            return {
                'size_mb': round(size_mb, 2),
                'page_count': page_count,
                'page_size': page_size,
                'index_count': index_count,
                'view_count': view_count
            }