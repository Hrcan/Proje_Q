# Teknik Spesifikasyonlar - Proje_Q

## 📐 Mimari Tasarım

### Genel Mimari
```
┌─────────────────────────────────────────────────────┐
│                   GUI Katmanı (PyQt5)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Ana     │  │  Veri    │  │  Rapor   │         │
│  │  Pencere │  │  Yükleme │  │  Ekranı  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│              İş Mantığı Katmanı                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  Excel   │  │  TXT     │  │  Rapor   │         │
│  │  Reader  │  │  Reader  │  │  Gen.    │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────┐
│            Veritabanı Katmanı (SQLite)              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │  CRUD    │  │  Backup  │  │  Search  │         │
│  │  Ops     │  │  Manager │  │  Engine  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

## 🗂️ Modül Detayları

### 1. Ana Uygulama Modülü (src/main.py)
**Sorumluluk:** Uygulamanın başlangıç noktası

```python
class Application:
    - initialize_app()
    - setup_logging()
    - load_configuration()
    - start_gui()
    - handle_exceptions()
```

### 2. GUI Modülleri (src/ui/)

#### 2.1 Ana Pencere (main_window.py)
```python
class MainWindow(QMainWindow):
    - setup_ui()
    - create_menu_bar()
    - create_toolbar()
    - create_status_bar()
    - apply_theme(theme_name)
    - show_about_dialog()
```

**Menü Yapısı:**
- Dosya
  - Excel/TXT Yükle (Ctrl+O)
  - Veritabanı Yedeği Al (Ctrl+B)
  - Veritabanı Geri Yükle (Ctrl+R)
  - Çıkış (Ctrl+Q)
- Veritabanı
  - Kayıt Görüntüle (Ctrl+V)
  - Yeni Kayıt Ekle (Ctrl+N)
  - Kayıt Düzenle (Ctrl+E)
  - Kayıt Sil (Delete)
  - Toplu Temizlik (Ctrl+Shift+D)
- Raporlar
  - JCL Bazlı Rapor
  - Ekip Bazlı Rapor
  - Rapor Tipi Raporu
  - Tarih Aralığı Raporu
  - Excel'e Aktar (Ctrl+Shift+E)
  - PDF'e Aktar (Ctrl+Shift+P)
- Görünüm
  - Light Theme
  - Dark Theme
  - Blue Theme
  - Log Penceresi (Ctrl+L)
- Yardım
  - Kullanım Kılavuzu (F1)
  - Hakkında

#### 2.2 Veri Yükleme Ekranı (data_loader.py)
```python
class DataLoaderWidget(QWidget):
    - select_files()
    - validate_files()
    - start_loading()
    - update_progress(current, total)
    - show_results()
    - handle_errors()
```

**Özellikler:**
- Çoklu dosya seçimi
- Dosya önizleme
- İlerleme çubuğu
- Hata gösterimi
- Yükleme istatistikleri

#### 2.3 Veritabanı Yöneticisi Ekranı (database_manager.py)
```python
class DatabaseManagerWidget(QWidget):
    - load_data(filters)
    - search_records(query)
    - edit_record(record_id)
    - delete_record(record_id)
    - bulk_delete(record_ids)
    - refresh_table()
    - export_to_excel()
```

**Tablo Kolonları:**
- ID
- JCL Adı
- Ekip Adı
- Kolon C
- Kolon D
- Kolon E
- Rapor Tipi
- Yüklenme Tarihi
- Güncelleme Tarihi
- Kaynak Dosya

#### 2.4 Rapor Görüntüleyici (report_viewer.py)
```python
class ReportViewerWidget(QWidget):
    - set_filter_criteria()
    - generate_report()
    - display_chart()
    - export_report(format)
```

#### 2.5 Tema Yöneticisi (themes.py)
```python
class ThemeManager:
    - load_theme(theme_name)
    - get_stylesheet()
    - register_theme(name, stylesheet)
    
class LightTheme:
    - get_colors()
    - get_stylesheet()

class DarkTheme:
    - get_colors()
    - get_stylesheet()

class BlueTheme:
    - get_colors()
    - get_stylesheet()
```

### 3. Veritabanı Modülleri (src/database/)

#### 3.1 Veritabanı Yöneticisi (db_manager.py)
```python
class DatabaseManager:
    - __init__(db_path)
    - connect()
    - disconnect()
    - create_tables()
    - execute_query(query, params)
    - commit()
    - rollback()
    - backup_database(backup_path)
    - restore_database(backup_path)
    
    # CRUD Operations
    - insert_record(data)
    - update_record(record_id, data)
    - delete_record(record_id)
    - get_record(record_id)
    - get_all_records(filters)
    - search_records(criteria)
    
    # Bulk Operations
    - bulk_insert(data_list)
    - bulk_update(data_list)
    - bulk_delete(record_ids)
```

#### 3.2 Veri Modelleri (models.py)
```python
class JCLRecord:
    - id: int
    - jcl_adi: str
    - ekip_adi: str
    - kolon_c: str
    - kolon_d: str
    - kolon_e: str
    - rapor_tipi: str
    - yuklenme_tarihi: datetime
    - guncelleme_tarihi: datetime
    - kaynak_dosya: str
    
    - to_dict()
    - from_dict(data)
    - validate()

class YuklemeGecmisi:
    - id: int
    - dosya_adi: str
    - yuklenme_tarihi: datetime
    - kayit_sayisi: int
    - durum: str
    - hata_mesaji: str
    
    - to_dict()
    - from_dict(data)
```

### 4. Yardımcı Modüller (src/utils/)

#### 4.1 Excel Okuyucu (excel_reader.py)
```python
class ExcelReader:
    - __init__(file_path)
    - get_sheet_names()
    - read_sheet(sheet_name)
    - find_column_by_header(header_name)
    - find_jcl_data(sheet)
    - extract_data(sheet)
    - detect_report_type(filename)
    
    # Algoritma
    def extract_data(sheet):
        1. Tüm hücreleri tara
        2. "JCL" veya benzer başlık ara
        3. JCL satırını bul
        4. Aynı satırdaki diğer değerleri al
        5. A-E kolonları içindeki verileri topla
        6. Veri nesnesine dönüştür
```

#### 4.2 TXT Okuyucu (txt_reader.py)
```python
class TXTReader:
    - __init__(file_path)
    - detect_format()
    - read_data()
    - parse_line(line)
    - validate_data(data)
```

#### 4.3 Logger (logger.py)
```python
class AppLogger:
    - __init__(log_file)
    - setup_logger()
    - log_info(message)
    - log_warning(message)
    - log_error(message, exception)
    - get_recent_logs(count)
    - clear_old_logs(days)
```

#### 4.4 Veri Doğrulayıcı (validators.py)
```python
class DataValidator:
    - validate_jcl_name(jcl_name)
    - validate_file_format(file_path)
    - validate_excel_structure(workbook)
    - validate_txt_format(content)
    - check_required_columns(data)
```

### 5. Konfigürasyon Modülü (src/config/)

#### 5.1 Ayarlar (settings.py)
```python
class Settings:
    # Veritabanı
    DATABASE_PATH = "database/jcl_data.db"
    BACKUP_PATH = "backup/"
    
    # Log
    LOG_FILE = "logs/app.log"
    LOG_LEVEL = "INFO"
    LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Excel
    EXCEL_MAX_ROWS = 10000
    EXCEL_COLUMNS = ['A', 'B', 'C', 'D', 'E']
    
    # Kolon Başlıkları
    JCL_HEADERS = ['JCL', 'JCL ADI', 'JCL_ADI', 'JOB NAME']
    EKIP_HEADERS = ['EKIP', 'EKIP ADI', 'EKIP_ADI', 'SORUMLU EKIP']
    
    # Rapor Tipleri
    REPORT_TYPES = {
        'HATALI': 'HATALI_ISLER',
        'UZUN': 'UZUN_ISLER'
    }
    
    # UI
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    DEFAULT_THEME = 'Light'
```

## 🔄 Veri Akış Diyagramı

### Excel Yükleme Akışı
```
Kullanıcı Excel Seçer
        ↓
Dosya Validasyonu
        ↓
    ┌───┴───┐
    │ Geçerli? │
    └───┬───┘
        ↓ Evet
Tüm Sheet'leri Oku
        ↓
Her Sheet İçin:
    ↓
JCL Verilerini Bul
    ↓
Kolon Eşleştir
    ↓
Veri Çıkar
    ↓
Validasyon
    ↓
┌───────────────┐
│ JCL Mevcut? │
└───┬───────┬───┘
    ↓ Evet  ↓ Hayır
UPDATE      INSERT
    ↓         ↓
    └────┬────┘
         ↓
    Log Kaydet
         ↓
İlerleme Güncelle
         ↓
Sonraki Sheet
```

### Arama ve Filtreleme Akışı
```
Kullanıcı Arama Kriteri Girer
        ↓
SQL Query Oluştur
        ↓
Veritabanı Sorgula
        ↓
Sonuçları Getir
        ↓
Tabloda Göster
        ↓
Kullanıcı İşlem Seçer
        ↓
    ┌───┴───┐
    │ İşlem? │
    └───┬───┘
        ├── Düzenle → Düzenleme Formu → Güncelle → Tabloyu Yenile
        ├── Sil → Onay İste → Sil → Tabloyu Yenile
        └── Rapor → Rapor Formatı Seç → Oluştur → Kaydet/Göster
```

## 📊 Performans Optimizasyonları

### 1. Veritabanı
- Index kullanımı (jcl_adi, rapor_tipi)
- Batch insert işlemleri
- Transaction yönetimi
- Connection pooling

### 2. Excel Okuma
- Lazy loading (sheet by sheet)
- Bellek yönetimi
- Paralel işleme (çoklu dosya için)
- Cache mekanizması

### 3. GUI
- Virtual scrolling (büyük tablolar için)
- Lazy rendering
- Thread kullanımı (IO işlemleri için)
- Progress feedback

## 🔒 Güvenlik

### Veri Güvenliği
- SQL injection koruması (parametreli sorgular)
- Dosya yolu validasyonu
- Yetkilendirme (gelecek versiyon)

### Hata Yönetimi
- Try-catch blokları
- Graceful degradation
- Kullanıcı dostu hata mesajları
- Detaylı log kayıtları

## 🧪 Test Stratejisi

### Unit Tests
- Database operations
- Data validation
- Excel/TXT parsing
- Business logic

### Integration Tests
- GUI → Database flow
- File loading → Database save
- Report generation
- Backup/restore

### UI Tests
- Button clicks
- Form validation
- Theme switching
- Window operations

## 📦 Deployment

### PyInstaller Konfigürasyonu
```python
# build.spec
a = Analysis(
    ['src/main.py'],
    pathex=['d:/Proje_Q'],
    binaries=[],
    datas=[
        ('src/ui/themes/*.qss', 'themes'),
        ('docs/*.md', 'docs')
    ],
    hiddenimports=[
        'PyQt5',
        'pandas',
        'openpyxl',
        'reportlab'
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Proje_Q',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='assets/icon.ico'
)
```

### Build Komutu
```bash
pyinstaller --clean --onefile --windowed build.spec
```

## 🔧 Geliştirme Ortamı Kurulumu

### Gereksinimler
```bash
# Python 3.8 veya üzeri
python --version

# Virtual environment oluştur
python -m venv venv

# Aktive et (Windows)
venv\Scripts\activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### Geliştirme Araçları
- IDE: Visual Studio Code / PyCharm
- Linter: pylint
- Formatter: black
- Type Checker: mypy

---

**Son Güncelleme:** 05.03.2026
**Versiyon:** 1.0