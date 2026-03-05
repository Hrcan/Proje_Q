# Proje_Q - JCL Veri Yönetim Sistemi

![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)
![Status](https://img.shields.io/badge/status-functional_test-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-private-red.svg)

## 📋 Proje Özeti
Excel ve TXT dosyalarından JCL verilerini okuyup SQLite veritabanına kaydeden, yöneten ve raporlayan masaüstü uygulaması.

## 🎯 Proje Amacı
SAO Ana Sistemler ve Sistem Operasyon raporlarındaki JCL (Job Control Language) verilerini merkezi bir veritabanında toplama, düzenleme ve raporlama.

## 🚀 Özellikler

### Veri Yönetimi
- ✅ Excel dosyalarından çoklu sheet okuma (tüm sheet'ler otomatik)
- ✅ TXT dosyalarından veri okuma
- ✅ Çoklu dosya yükleme (aynı anda birden fazla Excel)
- ✅ A-E kolonlarını otomatik algılama ve okuma
- ✅ JCL_ADI bazlı unique kayıt yönetimi
- ✅ İlerleme çubuğu ile yükleme takibi

### Veritabanı İşlemleri
- 📊 SQLite veritabanı
- 🔍 Gelişmiş arama ve filtreleme
- ✏️ Kayıt düzenleme
- 🗑️ Kayıt silme
- 💾 Veritabanı yedekleme/geri yükleme

### Raporlama
- 📈 Ekran üzerinde tablo görünümü
- 📄 Excel'e aktarma
- 📑 PDF rapor oluşturma
- 🔎 JCL, Ekip, Tarih bazlı filtreleme

### Kullanıcı Arayüzü
- 🎨 Modern PyQt5 arayüzü
- 🌓 3 tema seçeneği (Light, Dark, Blue)
- 📝 Log görüntüleme arayüzü
- ⚙️ Ayarlar menüsü

## 🛠️ Teknoloji Stack

### Ana Teknolojiler
- **Python 3.x**: Ana programlama dili
- **PyQt5**: Modern GUI framework
- **SQLite3**: Veritabanı
- **pandas**: Excel/veri işleme
- **openpyxl**: Excel okuma/yazma
- **reportlab**: PDF oluşturma

### Destekleyici Kütüphaneler
- **PyInstaller**: .exe oluşturma
- **logging**: Log yönetimi
- **datetime**: Tarih/zaman işlemleri

## 📁 Klasör Yapısı

```
Proje_Q/
├── Data/                          # Veri dosyaları
│   ├── Excel/                     # Excel kaynak dosyaları
│   │   ├── SAO_Ana_Sistemler_*.xlsx
│   │   └── SAO_Sistem_Operasyon_*.xlsx
│   └── txt-jpeg/                  # TXT örnek ve görseller
│       ├── 1.jpeg
│       ├── 2.jpeg
│       └── 3.jpeg
│
├── backup/                        # Yerel veritabanı yedekleri
│
├── src/                           # Kaynak kodlar
│   ├── main.py                    # Ana uygulama
│   ├── ui/                        # UI bileşenleri
│   │   ├── main_window.py
│   │   ├── data_loader.py
│   │   ├── database_manager.py
│   │   ├── report_viewer.py
│   │   └── themes.py
│   ├── database/                  # Veritabanı işlemleri
│   │   ├── db_manager.py
│   │   └── models.py
│   ├── utils/                     # Yardımcı fonksiyonlar
│   │   ├── excel_reader.py
│   │   ├── txt_reader.py
│   │   ├── logger.py
│   │   └── validators.py
│   └── config/                    # Konfigürasyon
│       └── settings.py
│
├── database/                      # SQLite veritabanı dizini
│   └── jcl_data.db
│
├── logs/                          # Log dosyaları
│   └── app.log
│
├── docs/                          # Dokümantasyon
│   ├── TECHNICAL_SPECS.md
│   ├── DATABASE_SCHEMA.md
│   ├── USER_GUIDE.md
│   └── DEVELOPMENT_ROADMAP.md
│
├── build/                         # Build çıktıları
│   └── dist/                      # .exe dosyası
│
├── tests/                         # Test dosyaları
│
├── requirements.txt               # Python bağımlılıkları
├── .gitignore                     # Git ignore dosyası
├── CHANGELOG.md                   # Versiyon değişiklikleri
├── VERSION                        # Mevcut versiyon
└── README.md                      # Bu dosya
```

## 📊 Veritabanı Yapısı

### Tablo 1: hatali_isler (11 Kolon)

| Kolon Adı | Tip | Açıklama |
|-----------|-----|----------|
| id | INTEGER PRIMARY KEY | Otomatik artan ID |
| jcl_adi | TEXT NOT NULL | JCL adı (örn: PKRBI330) |
| ay | TEXT NOT NULL | Rapor ayı (YYYY-MM formatı) |
| sheet_adi | TEXT NOT NULL | Excel sheet adı |
| hatali_sayi_ay | INTEGER | Aylık hatalı çalışma sayısı |
| son_hatali_tarih | DATE | Son hatalı çalışma tarihi |
| hatali_sayi_yil | INTEGER | Yıllık toplam hatalı sayı |
| sorumlu_ekip | TEXT | Sorumlu ekip adı |
| yuklenme_tarihi | DATETIME | İlk yüklenme zamanı |
| guncelleme_tarihi | DATETIME | Son güncelleme zamanı |
| kaynak_dosya | TEXT | Kaynak Excel dosya adı |

**Unique Constraint:** (jcl_adi, ay, sheet_adi) - Aynı JCL aynı ayda aynı sheet'te tek kayıt

### Tablo 2: uzun_isler (10 Kolon)

| Kolon Adı | Tip | Açıklama |
|-----------|-----|----------|
| id | INTEGER PRIMARY KEY | Otomatik artan ID |
| jcl_adi | TEXT NOT NULL | JCL adı |
| ay | TEXT NOT NULL | Rapor ayı (YYYY-MM formatı) |
| sheet_adi | TEXT NOT NULL | Excel sheet adı |
| calisma_sayisi | INTEGER | Toplam çalışma sayısı |
| calisma_suresi | INTEGER | Toplam çalışma süresi (dakika) |
| sorumlu_ekip | TEXT | Sorumlu ekip adı |
| yuklenme_tarihi | DATETIME | İlk yüklenme zamanı |
| guncelleme_tarihi | DATETIME | Son güncelleme zamanı |
| kaynak_dosya | TEXT | Kaynak Excel dosya adı |

**Unique Constraint:** (jcl_adi, ay, sheet_adi)

### Tablo 3: yukleme_gecmisi

| Kolon Adı | Tip | Açıklama |
|-----------|-----|----------|
| id | INTEGER PRIMARY KEY | Otomatik artan ID |
| dosya_adi | TEXT | Yüklenen dosya adı |
| yuklenme_tarihi | DATETIME | Yüklenme zamanı |
| kayit_sayisi | INTEGER | Eklenen kayıt sayısı |
| durum | TEXT | BASARILI / HATALI / UYARI |
| hata_mesaji | TEXT | Varsa hata detayı |

### Performans Optimizasyonları
- ✅ 14 Index (single + composite)
- ✅ WAL Mode (Write-Ahead Logging)
- ✅ 64MB Cache
- ✅ CHECK Constraints (veri doğrulama)

## 🔄 Veri İşleme Kuralları

### JCL Adı (Primary Key)
- Her JCL_ADI benzersizdir (UNIQUE)
- Örnek: "Hurcan123"
- Aynı JCL farklı raporlarda (Hatalı/Uzun İşler) olabilir
- Rapor tipi ile birlikte kayıt tutulur

### Ekip Adı
- Değişken olabilir (Ekip1, Ekip77, Ekip99 gibi)
- Aynı ekip adı birden fazla JCL'de olabilir
- NULL olabilir (bazı kaynaklarda eksik olabilir)

### Kolon Okuma Stratejisi
- Excel'in her yerinde JCL_ADI ve EKIP_ADI aranır
- Kolon başlıklarına göre veri eşleştirilir
- Başlık yoksa kolon pozisyonuna göre (A, B, C, D, E)
- Örnek: A5→JCL_ADI, D5→EKIP_ADI veya B4→JCL_ADI, C4→EKIP_ADI

### Duplicate Handling
- Aynı JCL_ADI + Rapor Tipi için: SON VERİ GEÇERLİ (üzerine yaz)
- Güncelleme zamanı kaydedilir
- Eski kayıt log'a yazılır

## 🎨 Tema Sistemi

### 1. Light Theme (Açık)
- Beyaz arka plan
- Siyah/koyu gri yazılar
- Mavi vurgular

### 2. Dark Theme (Koyu)
- Koyu gri/siyah arka plan
- Beyaz/açık gri yazılar
- Turuncu vurgular

### 3. Blue Theme
- Mavi tonları arka plan
- Beyaz yazılar
- Sarı vurgular

## ⚠️ Hata Yönetimi

### Format Kontrolü
- Desteklenmeyen dosya formatı → Hata mesajı + devam et
- Eksik kolon → Kullanıcıdan düzeltme iste
- Boş sheet → Atla ve devam et

### Loglama
- Tüm işlemler log'lanır
- Log seviyeleri: INFO, WARNING, ERROR
- Arayüzden log görüntüleme
- Log dosyası: `logs/app.log`

### İlerleme Gösterimi
- Excel yükleme: Dosya bazında
- TXT yükleme: Satır bazında (100+ satır için)
- Veritabanı işlemleri: Kayıt bazında

## 🎯 Geliştirme Yol Haritası

### Faz 1: Temel Altyapı ✅ (Tamamlandı - v0.1.0)
- [x] Git repository kurulumu
- [x] Klasör yapısı oluşturma
- [x] Dokümantasyon yazma
- [x] Semantic Versioning sistemi

### Faz 2: Kurulum Sistemi ✅ (Tamamlandı - v0.2.0)
- [x] Otomatik kurulum scripti
- [x] Sistem gereksinim kontrolü
- [x] Virtual environment kurulumu
- [x] Detaylı kurulum kılavuzu

### Faz 3: Veritabanı ve Excel Okuyucu ✅ (Tamamlandı - v0.3.0)
- [x] SQLite veritabanı şeması (2 ana tablo)
- [x] CRUD operasyonları
- [x] 14 Index ile performans optimizasyonu
- [x] Excel okuma modülü (openpyxl)
- [x] Otomatik rapor tipi algılama
- [x] Çoklu sheet okuma
- [x] Test GUI (3 tab, 2 görünüm modu)

### Faz 4: GUI Geliştirme (v0.4.0)
- [ ] Ana pencere (PyQt5)
- [ ] Dosya yükleme arayüzü
- [ ] Veritabanı yönetim ekranı
- [ ] Rapor görüntüleme ekranı
- [ ] Tema sistemi implementasyonu
- [ ] Log görüntüleme ekranı

### Faz 5: Raporlama (v0.5.0)
- [ ] Tablo görünümü
- [ ] Excel export
- [ ] PDF oluşturma
- [ ] Filtreleme/arama

### Faz 6: Test ve Optimizasyon (v0.6.0)
- [ ] Unit testler
- [ ] Integration testler
- [ ] Performans optimizasyonu
- [ ] Kullanıcı testleri

### Faz 7: Deployment (v1.0.0)
- [ ] PyInstaller konfigürasyonu
- [ ] .exe oluşturma
- [ ] Kurulum paketi
- [ ] Kullanım kılavuzu

## 📝 Kaldığımız Yer (Progress Tracking)

### ✅ Tamamlanan (v0.3.0)
- ✅ Git repository ve GitHub entegrasyonu
- ✅ Proje yapısı ve dokümantasyon
- ✅ Otomatik kurulum sistemi
- ✅ **Veritabanı sistemi (src/database/db_manager.py - 418 satır)**
  - 2 ana tablo (hatali_isler, uzun_isler)
  - 14 performans index'i
  - CRUD operasyonları
  - Optimizasyon fonksiyonları
- ✅ **Excel okuyucu (src/utils/excel_reader.py - 130 satır)**
  - Otomatik rapor tipi algılama
  - Çoklu sheet okuma
  - Ay bilgisi çıkarma
- ✅ **Test GUI (test_gui.py - 490 satır)**
  - 3 tab arayüz
  - 2 görünüm modu (Sheet/JCL bazlı)
  - Excel yükleme
  - İstatistikler ve ilerleme çubuğu

### 🎯 Mevcut Durum
- **Test Edilen Veri:** 381 kayıt (90 hatalı + 291 uzun iş)
- **Toplam Kod:** ~1000 satır Python
- **Durum:** Fonksiyonel test GUI çalışıyor

### 🚀 Sonraki Adımlar (v0.4.0)
1. Filtreleme ve arama sistemi
2. Excel export (rapor çıktısı)
3. Kayıt düzenleme formu
4. Kayıt silme özellikleri
5. Grafik ve dashboard

## 📚 Dokümantasyon

- **[CHANGELOG.md](CHANGELOG.md)** - Versiyon geçmişi ve değişiklikler
- **[PROGRESS_SUMMARY.md](PROGRESS_SUMMARY.md)** - 🆕 İlerleme özeti ve tamamlananlar
- **[INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)** - Detaylı kurulum kılavuzu
- **[EXCEL_KOLON_LISTESI.md](EXCEL_KOLON_LISTESI.md)** - 🆕 Excel kolon detayları
- **[docs/TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md)** - Teknik spesifikasyonlar
- **[docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)** - Veritabanı detayları
- **[VERSION](VERSION)** - Mevcut versiyon numarası

## 🚀 Kurulum

### Hızlı Başlangıç

```bash
# 1. Repository'yi klonlayın
git clone https://github.com/Hrcan/proje_q.git
cd proje_q

# 2. Sistem kontrolü
python check_requirements.py

# 3. Otomatik kurulum
python setup_environment.py

# 4. Virtual environment'ı aktive edin
# Windows:
activate_env.bat
# Linux/macOS:
./activate_env.sh
```

Detaylı kurulum için: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

## 🔄 Versiyonlama

Bu proje [Semantic Versioning 2.0.0](https://semver.org/lang/tr/) standartlarını takip eder.

**Versiyon Formatı:** `MAJOR.MINOR.PATCH`

- **MAJOR**: Geriye dönük uyumsuz API değişiklikleri
- **MINOR**: Geriye dönük uyumlu yeni özellikler  
- **PATCH**: Geriye dönük uyumlu bug düzeltmeleri

**Mevcut Versiyon:** 0.3.0 (Functional Test)

Tüm değişiklikler için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.

## 📞 İletişim ve Destek

### Sorun Bildirme
- GitHub Issues kullanın
- Hata detaylarını ekleyin
- Log dosyasını paylaşın

### Özellik İsteği
- GitHub Issues'da "enhancement" etiketi ile
- Detaylı açıklama yapın
- Kullanım senaryosu belirtin

## 📄 Lisans

Bu proje özel kullanım içindir.

---

**Son Güncelleme:** 05.03.2026  
**Versiyon:** 0.3.0  
**Durum:** Test GUI Çalışıyor - 381 Kayıt Yüklendi  
**Sonraki Hedef:** Filtreleme, Arama ve Excel Export (v0.4.0)

## 🎉 Çalıştırma

```bash
# Test GUI'yi başlat
python test_gui.py

# Excel dosyalarını yükle
# "Excel Yukle" → Data/Excel/ klasöründen dosya seç
```
