"""
Veritabanı Yöneticisi
SQL işlemlerini yöneten ana modül
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os


class DatabaseManager:
    """Veritabanı işlemlerini yöneten sınıf"""
    
    def __init__(self, db_path: str = "database/jcl_data.db"):
        """
        Args:
            db_path: Veritabanı dosya yolu
        """
        self.db_path = db_path
        self.connection = None
        
        # Veritabanı dizinini oluştur
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
    
    def connect(self):
        """Veritabanına bağlan"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Dict-like rows
        
        # Foreign key desteğini aktif et
        self.connection.execute("PRAGMA foreign_keys = ON")
        
        # Write-Ahead Logging (WAL) modunu aktif et - daha iyi performans
        self.connection.execute("PRAGMA journal_mode = WAL")
        
        # Synchronous modu optimize et
        self.connection.execute("PRAGMA synchronous = NORMAL")
        
        # Cache boyutunu artır (daha hızlı sorgular)
        self.connection.execute("PRAGMA cache_size = -64000")  # 64MB
        
        return self.connection
    
    def disconnect(self):
        """Veritabanı bağlantısını kapat"""
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
        cursor = self.connection.cursor()
        
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
                CHECK(ay LIKE '____-__'),  -- YYYY-MM formatı
                CHECK(hatali_sayi_ay >= 0 OR hatali_sayi_ay IS NULL),
                CHECK(hatali_sayi_yil >= 0 OR hatali_sayi_yil IS NULL)
            )
        """)
        
        # Single column indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_jcl 
            ON hatali_isler(jcl_adi)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_ay 
            ON hatali_isler(ay DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_sheet 
            ON hatali_isler(sheet_adi)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_ekip 
            ON hatali_isler(sorumlu_ekip)
        """)
        
        # Composite indexes - Sık kullanılan sorgular için
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_jcl_ay 
            ON hatali_isler(jcl_adi, ay DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_ay_jcl 
            ON hatali_isler(ay DESC, jcl_adi)
        """)
        
        # Tarih bazlı sorgular için
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_hatali_guncelleme 
            ON hatali_isler(guncelleme_tarihi DESC)
        """)
        
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
                
                -- Composite UNIQUE: (JCL + Ay + Sheet) benzersiz olmalı
                UNIQUE(jcl_adi, ay, sheet_adi),
                
                -- CHECK constraints: Veri bütünlüğü
                CHECK(length(jcl_adi) > 0),
                CHECK(ay LIKE '____-__'),  -- YYYY-MM formatı
                CHECK(calisma_sayisi >= 0 OR calisma_sayisi IS NULL),
                CHECK(calisma_suresi >= 0 OR calisma_suresi IS NULL)
            )
        """)
        
        # Single column indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_jcl 
            ON uzun_isler(jcl_adi)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_ay 
            ON uzun_isler(ay DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_sheet 
            ON uzun_isler(sheet_adi)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_ekip 
            ON uzun_isler(sorumlu_ekip)
        """)
        
        # Composite indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_jcl_ay 
            ON uzun_isler(jcl_adi, ay DESC)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_ay_jcl 
            ON uzun_isler(ay DESC, jcl_adi)
        """)
        
        # Tarih bazlı sorgular için
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_uzun_guncelleme 
            ON uzun_isler(guncelleme_tarihi DESC)
        """)
        
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
                
                -- CHECK constraints
                CHECK(length(dosya_adi) > 0),
                CHECK(kayit_sayisi >= 0)
            )
        """)
        
        # Index
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_yukleme_tarih 
            ON yukleme_gecmisi(yuklenme_tarihi DESC)
        """)
        
        # ==========================================
        # View'ler - Performanslı sorgular için
        # ==========================================
        
        # View 1: JCL bazlı özet
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
        
        self.connection.commit()
        print("Tablolar ve indeksler basariyla olusturuldu")
        
        # İstatistikleri güncelle (performans için)
        cursor.execute("ANALYZE")
        self.connection.commit()
    
    # Hatalı İşler İşlemleri
    def insert_hatali_is(self, data: Dict) -> int:
        """Hatalı iş kaydı ekle veya güncelle"""
        cursor = self.connection.cursor()
        
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
        
        self.connection.commit()
        return cursor.lastrowid
    
    def get_all_hatali_isler(self) -> List[Dict]:
        """Tüm hatalı işleri getir"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM hatali_isler 
            ORDER BY ay DESC, jcl_adi
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    # Uzun Süren İşler İşlemleri
    def insert_uzun_is(self, data: Dict) -> int:
        """Uzun süren iş kaydı ekle veya güncelle"""
        cursor = self.connection.cursor()
        
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
        
        self.connection.commit()
        return cursor.lastrowid
    
    def get_all_uzun_isler(self) -> List[Dict]:
        """Tüm uzun süren işleri getir"""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM uzun_isler 
            ORDER BY ay DESC, jcl_adi
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    # Yükleme Geçmişi
    def insert_yukleme_gecmisi(self, data: Dict) -> int:
        """Yükleme geçmişi ekle"""
        cursor = self.connection.cursor()
        
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
        
        self.connection.commit()
        return cursor.lastrowid
    
    def get_tablo_istatistikleri(self) -> Dict:
        """Tablo istatistiklerini getir"""
        cursor = self.connection.cursor()
        
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
        """Veritabanını optimize et - Periyodik olarak çağrılmalı"""
        cursor = self.connection.cursor()
        
        # İstatistikleri güncelle
        cursor.execute("ANALYZE")
        
        # Boş alanları temizle
        cursor.execute("VACUUM")
        
        # WAL checkpoint
        cursor.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        
        self.connection.commit()
        print("Veritabani optimize edildi")
    
    def get_database_info(self) -> Dict:
        """Veritabanı bilgilerini getir"""
        cursor = self.connection.cursor()
        
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