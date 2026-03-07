# Proje_Q Dizin Haritası
*Son güncelleme: 2026-03-07 20:42*

Bu dosya, token tasarrufu için tüm proje dosya ve klasör yapısını içerir.
Yeni dosya/klasör eklendiğinde bu dosya güncellenmelidir.

## 📁 Kök Dizin (d:/Proje_Q)

### 📄 Yapılandırma Dosyaları
- `.coverage` - Test coverage raporu
- `.gitignore` - Git ignore kuralları
- `requirements.txt` - Python bağımlılıkları
- `VERSION` - Versiyon bilgisi

### 📄 Dokümantasyon Dosyaları
- `README.md` - Proje ana dokümantasyonu
- `QUICK_START.md` - Hızlı başlangıç kılavuzu (Token tasarrufu için kritik!)
- `DIRECTORY_MAP.md` - **[YENİ]** Bu dosya - Dizin haritası (Token tasarrufu için)
- `INSTALLATION_GUIDE.md` - Kurulum kılavuzu
- `PROGRESS_SUMMARY.md` - İlerleme özeti
- `CHANGELOG.md` - Değişiklik geçmişi
- `BACKUP_INFO.md` - Yedekleme bilgileri
- `NEXT_SESSION_PLAN.md` - Sonraki oturum planı
- `SONRAKI_SOHBET_ICIN_EYLEM_PLANI.md` - Türkçe eylem planı
- `SONRAKI_SOHBET_NOTLARI.md` - Türkçe notlar
- `DUZENLEME_PLANI.md` - Düzenleme planı
- `EXCEL_KOLON_LISTESI.md` - Excel kolon listesi

### 📄 Çalıştırılabilir Script'ler
- `analyze_excel.py` - Excel analiz scripti
- `check_requirements.py` - Gereksinim kontrol scripti
- `run_tests.py` - Test çalıştırıcı
- `setup_environment.py` - Ortam kurulum scripti

### 📄 Log ve Geçici Dosyalar
- `logs_20260306_190912.txt` - Eski log dosyası
- `birlesik_gorunum.xlsx` - Birleşik görünüm Excel dosyası
- `hatali_isler.xlsx` - Hatalı işler Excel dosyası

## 📁 src/ (Kaynak Kod Dizini)
**Amaç:** Ana uygulama kaynak kodları

### 📄 Ana Dosyalar
- `src/__init__.py` - Package init dosyası
- `src/main.py` - Ana uygulama giriş noktası

### 📁 src/config/
**Amaç:** Yapılandırma modülü
- `src/config/__init__.py` - Package init
- `src/config/constants.py` - Sabitler ve yapılandırma
- `src/config/user_preferences.py` - Kullanıcı tercihleri

### 📁 src/database/
**Amaç:** Veritabanı yönetimi
- `src/database/__init__.py` - Package init
- `src/database/db_manager.py` - SQLite veritabanı yöneticisi

### 📁 src/ui/
**Amaç:** Kullanıcı arayüzü bileşenleri (PyQt6)
- `src/ui/__init__.py` - Package init
- `src/ui/main_window.py` - Ana pencere (refactor edilmiş)
- `src/ui/advanced_filters_dialog.py` - Gelişmiş filtre diyalogu
- `src/ui/bulk_search_dialog.py` - Toplu arama diyalogu
- `src/ui/bulk_search_results_dialog.py` - Toplu arama sonuçları
- `src/ui/export_dialog.py` - Dışa aktarma diyalogu
- `src/ui/log_viewer_dialog.py` - Log görüntüleyici
- `src/ui/settings_dialog.py` - Ayarlar diyalogu
- `src/ui/statistics_dialog.py` - İstatistik diyalogu
- `src/ui/themes.py` - Tema yönetimi

### 📁 src/ui/components/
**Amaç:** UI bileşen modülleri (MVC pattern)
- `src/ui/components/__init__.py` - Package init
- `src/ui/components/dialog_manager.py` - Diyalog yöneticisi
- `src/ui/components/menu_builder.py` - Menü oluşturucu
- `src/ui/components/search_panel.py` - Arama paneli
- `src/ui/components/table_manager.py` - Tablo yöneticisi
- `src/ui/components/toolbar_builder.py` - Araç çubuğu oluşturucu

### 📁 src/utils/
**Amaç:** Yardımcı araçlar
- `src/utils/__init__.py` - Package init
- `src/utils/backup_manager.py` - Yedekleme yöneticisi
- `src/utils/excel_reader.py` - Excel okuyucu (openpyxl)
- `src/utils/logger.py` - Logging yöneticisi

## 📁 tests/ (Test Dizini)
**Amaç:** Unit testler
- `tests/__init__.py` - Package init
- `tests/test_db_manager.py` - Veritabanı testleri
- `tests/test_excel_reader.py` - Excel okuyucu testleri

## 📁 docs/ (Dokümantasyon)
**Amaç:** Teknik dokümantasyon
- `docs/DATABASE_SCHEMA.md` - Veritabanı şeması
- `docs/TECHNICAL_SPECS.md` - Teknik özellikler

## 📁 Data/ (Veri Dizini)
**Amaç:** Uygulama verileri

### 📁 Data/Excel/
**Amaç:** Excel veri dosyaları
- `Data/Excel/SAO_Ana_Sistemler_Hatalı_Biten_İsler_Raporu_(ARALIK_2024).xlsx`
- `Data/Excel/SAO_Ana_Sistemler_Hatalı_Biten_İsler_Raporu_(KASIM_2024).xlsx`
- `Data/Excel/SAO_Sistem_Operasyon_Uzun_Süren_İşler(ARALIK_2024).xlsx`
- `Data/Excel/SAO_Sistem_Operasyon_Uzun_Süren_İşler(EKİM_2024)_.xlsx`
- `Data/Excel/SAO_Sistem_Operasyon_Uzun_Süren_İşler(KASIM_2024).xlsx`

### 📁 Data/TXT-jpeg/
**Amaç:** Metin ve görsel veriler
- `Data/TXT-jpeg/1.jpeg`
- `Data/TXT-jpeg/2.jpeg`
- `Data/TXT-jpeg/3.jpeg`

## 📁 database/ (Veritabanı Dizini)
**Amaç:** SQLite veritabanı dosyaları
- `database/.gitkeep` - Git için placeholder

## 📁 logs/ (Log Dizini)
**Amaç:** Uygulama log dosyaları
- (Dinamik log dosyaları burada oluşturulur)

## 📁 backup/ (Yedekleme Dizini)
**Amaç:** Otomatik yedeklemeler
- `backup/.gitkeep` - Git için placeholder
- `backup/backup_20260306_132631.zip`
- `backup/backup_20260306_180138.zip`
- `backup/backup_20260307_165810.zip`
- `backup/backup_20260307_173241.zip`
- `backup/backup_20260307_173459.zip`
- `backup/full_backup_20260307_171311.zip`
- `backup/full_backup_20260307_171322.zip`
- `backup/main_window_before_refactor_20260307_181741.py` - Refactor öncesi yedek

### 📁 backup/full_backups/
**Amaç:** Tam yedeklemeler
- (Tam yedek dosyaları burada)

## 📁 archive/ (Arşiv Dizini)
**Amaç:** Eski/kullanılmayan dosyalar
- `archive/test_gui.py` - Eski GUI test dosyası

## 📁 config/ (Yapılandırma Dizini)
**Amaç:** Kullanıcı yapılandırma dosyaları
- (Kullanıcı ayarları burada saklanır)

## 📁 htmlcov/ (Coverage Raporu)
**Amaç:** HTML test coverage raporları
- (pytest-cov tarafından oluşturulan HTML raporları)

---

## 🔄 Güncelleme Notları

### Yeni Dosya/Klasör Eklendiğinde:
1. Bu dosyayı aç: `DIRECTORY_MAP.md`
2. İlgili bölüme yeni girişi ekle
3. Son güncelleme tarihini değiştir
4. Dosyanın amacını kısaca açıkla

### Token Tasarrufu İçin Kullanım:
- Bir dosya hakkında bilgi gerektiğinde önce bu haritaya bak
- Dosya yolunu buradan al
- Sadece o dosyayı oku
- Tüm klasörü taramaktan kaçın

### Proje Yapısı Özeti:
```
Proje_Q/
├── DIRECTORY_MAP.md        # [YENİ] Token tasarrufu için dizin haritası
├── QUICK_START.md          # Hızlı başlangıç kılavuzu
├── src/                    # Ana kaynak kod
│   ├── config/            # Yapılandırma
│   ├── database/          # Veritabanı
│   ├── ui/                # Kullanıcı arayüzü
│   │   └── components/    # UI bileşenleri
│   └── utils/             # Yardımcı araçlar
├── tests/                 # Test dosyaları
├── docs/                  # Dokümantasyon
├── Data/                  # Veri dosyaları
│   ├── Excel/            # Excel dosyaları
│   └── TXT-jpeg/         # Metin/görsel
├── database/             # SQLite veritabanı
├── logs/                 # Log dosyaları
├── backup/               # Yedeklemeler
├── archive/              # Arşiv
├── config/               # Kullanıcı ayarları
└── htmlcov/              # Coverage raporları
```

## 🎯 Ana Proje Bilgileri

**Proje Adı:** Proje_Q  
**Teknoloji:** Python 3.12, PyQt6, SQLite  
**Amaç:** Excel iş raporlarını yönetme ve analiz uygulaması  
**Mimari:** MVC pattern ile refactor edilmiş modüler yapı  
**Test Framework:** pytest  
**Versiyon Kontrol:** Git (GitHub)

## 📌 Önemli Dosyalar (Token Tasarrufu İçin)

Bu dosyalar yeni sohbete başlarken okunmalı:
1. ✅ **QUICK_START.md** - Hızlı başlangıç ve kritik bilgiler
2. ✅ **DIRECTORY_MAP.md** - Bu dosya (dizin haritası)
3. ✅ **NEXT_SESSION_PLAN.md** - Sonraki oturum planı

Diğer dosyalar sadece ihtiyaç duyulduğunda okunmalıdır.