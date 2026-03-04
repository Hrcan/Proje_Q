# Veritabanı Şeması - Proje_Q

## 📊 Genel Bakış

Proje_Q, SQLite veritabanı kullanarak JCL verilerini saklar. Veritabanı, normalize edilmiş yapıda 2 ana tablo içerir.

## 🗄️ Tablolar

### 1. jcl_kayitlari (Ana Veri Tablosu)

**Amaç:** JCL kayıtlarını ve ilişkili verilerini saklar.

```sql
CREATE TABLE IF NOT EXISTS jcl_kayitlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jcl_adi TEXT NOT NULL,
    ekip_adi TEXT,
    kolon_c TEXT,
    kolon_d TEXT,
    kolon_e TEXT,
    rapor_tipi TEXT NOT NULL,
    yuklenme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    guncelleme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    kaynak_dosya TEXT,
    UNIQUE(jcl_adi, rapor_tipi)
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_jcl_adi ON jcl_kayitlari(jcl_adi);
CREATE INDEX IF NOT EXISTS idx_ekip_adi ON jcl_kayitlari(ekip_adi);
CREATE INDEX IF NOT EXISTS idx_rapor_tipi ON jcl_kayitlari(rapor_tipi);
CREATE INDEX IF NOT EXISTS idx_yuklenme_tarihi ON jcl_kayitlari(yuklenme_tarihi);
```

#### Kolon Açıklamaları

| Kolon | Tip | Null | Açıklama |
|-------|-----|------|----------|
| **id** | INTEGER | NO | Otomatik artan benzersiz kimlik (Primary Key) |
| **jcl_adi** | TEXT | NO | JCL adı (ör: "Hurcan123"). Rapor tipi ile birlikte UNIQUE |
| **ekip_adi** | TEXT | YES | Sorumlu ekip/ekip adı (ör: "Ekip1", "Ekip77") |
| **kolon_c** | TEXT | YES | Excel'deki C kolonundan okunan veri |
| **kolon_d** | TEXT | YES | Excel'deki D kolonundan okunan veri |
| **kolon_e** | TEXT | YES | Excel'deki E kolonundan okunan veri |
| **rapor_tipi** | TEXT | NO | Rapor tipi: "HATALI_ISLER" veya "UZUN_ISLER" |
| **yuklenme_tarihi** | DATETIME | NO | İlk kez veritabanına eklenme zamanı |
| **guncelleme_tarihi** | DATETIME | NO | Son güncelleme zamanı |
| **kaynak_dosya** | TEXT | YES | Verinin geldiği dosya adı |

#### İş Kuralları

1. **UNIQUE Constraint:** `(jcl_adi, rapor_tipi)` kombinasyonu benzersiz olmalı
   - Aynı JCL, farklı rapor tiplerinde olabilir
   - Örnek: "Hurcan123" hem HATALI_ISLER hem UZUN_ISLER'de olabilir

2. **Güncelleme Stratejisi:**
   - Aynı JCL_ADI + Rapor Tipi için yeni veri gelirse → UPDATE
   - `guncelleme_tarihi` otomatik güncellenir
   - Eski veri log'a kaydedilir

3. **NULL Değerler:**
   - `ekip_adi`, `kolon_c`, `kolon_d`, `kolon_e` NULL olabilir
   - Eksik veriler için boş string değil, NULL kullanılır

#### Örnek Kayıtlar

```sql
-- Örnek 1: Hatalı işler raporu
INSERT INTO jcl_kayitlari 
(jcl_adi, ekip_adi, kolon_c, kolon_d, kolon_e, rapor_tipi, kaynak_dosya)
VALUES 
('HURCAN123', 'EKIP1', 'HATA_KODU_001', 'SISTEM_HATASI', '2024-12-15', 
 'HATALI_ISLER', 'SAO_Ana_Sistemler_Hatalı_Biten_İsler_Raporu_(ARALIK_2024).xlsx');

-- Örnek 2: Uzun süren işler raporu (aynı JCL, farklı rapor tipi)
INSERT INTO jcl_kayitlari 
(jcl_adi, ekip_adi, kolon_c, kolon_d, kolon_e, rapor_tipi, kaynak_dosya)
VALUES 
('HURCAN123', 'EKIP99', '45 DAKİKA', 'YAVAŞ_İŞLEM', '2024-12-20', 
 'UZUN_ISLER', 'SAO_Sistem_Operasyon_Uzun_Süren_İşler(ARALIK_2024).xlsx');
```

---

### 2. yukleme_gecmisi (Log Tablosu)

**Amaç:** Dosya yükleme işlemlerinin geçmişini saklar.

```sql
CREATE TABLE IF NOT EXISTS yukleme_gecmisi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dosya_adi TEXT NOT NULL,
    yuklenme_tarihi DATETIME DEFAULT CURRENT_TIMESTAMP,
    kayit_sayisi INTEGER DEFAULT 0,
    durum TEXT NOT NULL CHECK(durum IN ('BASARILI', 'HATALI', 'UYARI')),
    hata_mesaji TEXT,
    islem_suresi REAL
);

-- İndeksler
CREATE INDEX IF NOT EXISTS idx_dosya_adi ON yukleme_gecmisi(dosya_adi);
CREATE INDEX IF NOT EXISTS idx_yukleme_tarihi ON yukleme_gecmisi(yuklenme_tarihi);
CREATE INDEX IF NOT EXISTS idx_durum ON yukleme_gecmisi(durum);
```

#### Kolon Açıklamaları

| Kolon | Tip | Null | Açıklama |
|-------|-----|------|----------|
| **id** | INTEGER | NO | Otomatik artan benzersiz kimlik |
| **dosya_adi** | TEXT | NO | Yüklenen dosyanın tam adı |
| **yuklenme_tarihi** | DATETIME | NO | Yükleme işleminin başlangıç zamanı |
| **kayit_sayisi** | INTEGER | NO | Başarıyla eklenen/güncellenen kayıt sayısı |
| **durum** | TEXT | NO | İşlem durumu: BASARILI, HATALI, UYARI |
| **hata_mesaji** | TEXT | YES | Hata veya uyarı detayları |
| **islem_suresi** | REAL | YES | İşlem süresi (saniye cinsinden) |

#### Durum Değerleri

- **BASARILI:** Tüm kayıtlar sorunsuz yüklendi
- **HATALI:** İşlem başarısız oldu
- **UYARI:** Bazı kayıtlar yüklendi ama uyarılar var

#### Örnek Kayıtlar

```sql
-- Başarılı yükleme
INSERT INTO yukleme_gecmisi 
(dosya_adi, kayit_sayisi, durum, islem_suresi)
VALUES 
('SAO_Ana_Sistemler_Hatalı_Biten_İsler_Raporu_(ARALIK_2024).xlsx', 
 45, 'BASARILI', 2.34);

-- Uyarılı yükleme
INSERT INTO yukleme_gecmisi 
(dosya_adi, kayit_sayisi, durum, hata_mesaji, islem_suresi)
VALUES 
('SAO_Sistem_Operasyon_Uzun_Süren_İşler(KASIM_2024).xlsx', 
 38, 'UYARI', '5 kayıtta eksik kolon bulundu', 1.89);

-- Hatalı yükleme
INSERT INTO yukleme_gecmisi 
(dosya_adi, kayit_sayisi, durum, hata_mesaji)
VALUES 
('bozuk_dosya.xlsx', 
 0, 'HATALI', 'Dosya formatı desteklenmiyor');
```

---

## 🔍 Önemli Sorgular

### Temel CRUD İşlemleri

#### INSERT (Yeni Kayıt)
```sql
INSERT INTO jcl_kayitlari 
(jcl_adi, ekip_adi, kolon_c, kolon_d, kolon_e, rapor_tipi, kaynak_dosya)
VALUES (?, ?, ?, ?, ?, ?, ?);
```

#### UPDATE (Mevcut Kayıt Güncelle)
```sql
UPDATE jcl_kayitlari 
SET ekip_adi = ?,
    kolon_c = ?,
    kolon_d = ?,
    kolon_e = ?,
    guncelleme_tarihi = CURRENT_TIMESTAMP,
    kaynak_dosya = ?
WHERE jcl_adi = ? AND rapor_tipi = ?;
```

#### SELECT (Tüm Kayıtlar)
```sql
SELECT * FROM jcl_kayitlari 
ORDER BY guncelleme_tarihi DESC;
```

#### DELETE (Kayıt Sil)
```sql
DELETE FROM jcl_kayitlari 
WHERE id = ?;
```

---

### Gelişmiş Sorgular

#### 1. JCL Adına Göre Arama
```sql
SELECT * FROM jcl_kayitlari 
WHERE jcl_adi LIKE '%' || ? || '%'
ORDER BY jcl_adi;
```

#### 2. Ekip Bazlı Rapor
```sql
SELECT 
    ekip_adi,
    COUNT(*) as toplam_kayit,
    COUNT(CASE WHEN rapor_tipi = 'HATALI_ISLER' THEN 1 END) as hatali_isler,
    COUNT(CASE WHEN rapor_tipi = 'UZUN_ISLER' THEN 1 END) as uzun_isler
FROM jcl_kayitlari
WHERE ekip_adi IS NOT NULL
GROUP BY ekip_adi
ORDER BY toplam_kayit DESC;
```

#### 3. Tarih Aralığı Sorgusu
```sql
SELECT * FROM jcl_kayitlari
WHERE guncelleme_tarihi BETWEEN ? AND ?
ORDER BY guncelleme_tarihi DESC;
```

#### 4. Rapor Tipi Bazlı İstatistik
```sql
SELECT 
    rapor_tipi,
    COUNT(*) as toplam,
    COUNT(DISTINCT ekip_adi) as farkli_ekip_sayisi,
    MIN(yuklenme_tarihi) as ilk_kayit,
    MAX(guncelleme_tarihi) as son_guncelleme
FROM jcl_kayitlari
GROUP BY rapor_tipi;
```

#### 5. Son Yüklenen Dosyalar
```sql
SELECT 
    y.dosya_adi,
    y.yuklenme_tarihi,
    y.kayit_sayisi,
    y.durum,
    y.islem_suresi
FROM yukleme_gecmisi y
ORDER BY y.yuklenme_tarihi DESC
LIMIT 10;
```

#### 6. Duplicate Kontrolü (Yükleme Öncesi)
```sql
SELECT * FROM jcl_kayitlari
WHERE jcl_adi = ? AND rapor_tipi = ?;
```

#### 7. Bulk Insert Kontrolü
```sql
INSERT OR REPLACE INTO jcl_kayitlari 
(jcl_adi, ekip_adi, kolon_c, kolon_d, kolon_e, 
 rapor_tipi, yuklenme_tarihi, guncelleme_tarihi, kaynak_dosya)
VALUES (?, ?, ?, ?, ?, ?, 
        COALESCE((SELECT yuklenme_tarihi FROM jcl_kayitlari 
                  WHERE jcl_adi = ? AND rapor_tipi = ?), 
                 CURRENT_TIMESTAMP),
        CURRENT_TIMESTAMP, 
        ?);
```

---

## 🔐 Veritabanı Güvenliği

### SQL Injection Koruması
```python
# ✅ DOĞRU - Parametreli sorgu
cursor.execute(
    "SELECT * FROM jcl_kayitlari WHERE jcl_adi = ?", 
    (jcl_name,)
)

# ❌ YANLIŞ - String concatenation
cursor.execute(
    f"SELECT * FROM jcl_kayitlari WHERE jcl_adi = '{jcl_name}'"
)
```

### Transaction Yönetimi
```python
try:
    conn = sqlite3.connect('database/jcl_data.db')
    cursor = conn.cursor()
    
    # Birden fazla işlem
    cursor.execute("INSERT INTO jcl_kayitlari ...")
    cursor.execute("INSERT INTO yukleme_gecmisi ...")
    
    conn.commit()  # Tümü başarılıysa kaydet
except Exception as e:
    conn.rollback()  # Hata varsa geri al
    raise e
finally:
    conn.close()
```

---

## 🔄 Veritabanı Bakım İşlemleri

### 1. Veritabanı Optimizasyonu
```sql
-- Boş alanları temizle
VACUUM;

-- İstatistikleri güncelle
ANALYZE;
```

### 2. Eski Logları Temizle
```sql
-- 30 günden eski logları sil
DELETE FROM yukleme_gecmisi
WHERE yuklenme_tarihi < datetime('now', '-30 days');
```

### 3. Veritabanı Boyutu
```sql
SELECT 
    page_count * page_size as size_bytes,
    page_count * page_size / 1024 / 1024 as size_mb
FROM pragma_page_count(), pragma_page_size();
```

### 4. Tablo İstatistikleri
```sql
SELECT 
    'jcl_kayitlari' as tablo,
    COUNT(*) as kayit_sayisi,
    COUNT(DISTINCT jcl_adi) as benzersiz_jcl,
    COUNT(DISTINCT ekip_adi) as benzersiz_ekip
FROM jcl_kayitlari

UNION ALL

SELECT 
    'yukleme_gecmisi' as tablo,
    COUNT(*) as kayit_sayisi,
    SUM(CASE WHEN durum='BASARILI' THEN 1 ELSE 0 END) as basarili,
    SUM(CASE WHEN durum='HATALI' THEN 1 ELSE 0 END) as hatali
FROM yukleme_gecmisi;
```

---

## 📦 Backup ve Restore

### Backup Stratejisi
```python
import shutil
import sqlite3
from datetime import datetime

def backup_database(db_path, backup_dir):
    """
    Veritabanını yedekler
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/jcl_data_backup_{timestamp}.db"
    
    # SQLite backup API kullan (daha güvenli)
    source = sqlite3.connect(db_path)
    dest = sqlite3.connect(backup_file)
    source.backup(dest)
    dest.close()
    source.close()
    
    return backup_file
```

### Restore İşlemi
```python
def restore_database(backup_file, db_path):
    """
    Veritabanını geri yükler
    """
    # Mevcut veritabanını yedekle
    safety_backup = f"{db_path}.before_restore"
    shutil.copy2(db_path, safety_backup)
    
    try:
        # Backup'tan geri yükle
        shutil.copy2(backup_file, db_path)
        return True
    except Exception as e:
        # Hata olursa eski haline döndür
        shutil.copy2(safety_backup, db_path)
        raise e
```

---

## 📈 Performans İyileştirmeleri

### 1. İndeks Kullanımı
```sql
-- Sık kullanılan sorgular için indeksler
CREATE INDEX IF NOT EXISTS idx_jcl_rapor 
ON jcl_kayitlari(jcl_adi, rapor_tipi);

CREATE INDEX IF NOT EXISTS idx_guncelleme 
ON jcl_kayitlari(guncelleme_tarihi DESC);
```

### 2. Batch Insert
```python
# Tek tek insert yerine (YAVAŞ)
for record in records:
    cursor.execute("INSERT INTO ...", record)

# Batch insert (HIZLI)
cursor.executemany("INSERT INTO ...", records)
conn.commit()
```

### 3. Connection Pool
```python
import sqlite3
from threading import Lock

class ConnectionPool:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.connections = []
        self.lock = Lock()
        
    def get_connection(self):
        with self.lock:
            if self.connections:
                return self.connections.pop()
            return sqlite3.connect(self.db_path)
    
    def return_connection(self, conn):
        with self.lock:
            self.connections.append(conn)
```

---

## 🎯 Migration Stratejisi

### Versiyon 1.0 → 1.1 (Örnek)
```sql
-- Yeni kolon ekle
ALTER TABLE jcl_kayitlari 
ADD COLUMN kolon_f TEXT;

-- Versiyon tablosu oluştur
CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_version (version) VALUES ('1.1.0');
```

---

**Son Güncelleme:** 05.03.2026
**Schema Versiyonu:** 1.0
**SQLite Versiyonu:** 3.x