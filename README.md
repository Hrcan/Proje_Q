# Proje_Q - Excel Veri Yönetim ve Analiz Sistemi

![Version](https://img.shields.io/badge/version-0.4.0-blue.svg)
![Status](https://img.shields.io/badge/status-active_development-green.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![License](https://img.shields.io/badge/license-private-red.svg)

## 📋 Proje Özeti

Excel raporlarından iş verilerini okuyup SQLite veritabanına kaydeden, yöneten ve raporlayan **modern masaüstü uygulaması**.

**Ana Özellikler:**
- 📊 Excel dosyalarından otomatik veri yükleme
- 🗄️ SQLite veritabanı yönetimi
- 🔍 Gelişmiş filtreleme ve arama
- 📈 İstatistikler ve raporlama
- 🎨 3 tema seçeneği (Light/Dark/Blue)
- 💾 Yedekleme/geri yükleme sistemi

---

## 🚀 Hızlı Başlangıç

### Kurulum

```bash
# 1. Projeyi klonlayın
git clone https://github.com/Hrcan/Proje_Q.git
cd Proje_Q

# 2. Sistem kontrolü
python check_requirements.py

# 3. Otomatik kurulum
python setup_environment.py

# 4. Virtual environment aktive edin (Windows)
activate_env.bat
```

### Çalıştırma

```bash
python -m src.main
```

**Detaylı kurulum:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 📁 Proje Yapısı

```
Proje_Q/
├── src/                    # Ana kaynak kodlar
│   ├── main.py            # Uygulama başlangıcı
│   ├── ui/                # Kullanıcı arayüzü
│   ├── database/          # Veritabanı yönetimi
│   └── utils/             # Yardımcı araçlar
├── Data/                  # Veri dosyaları
│   └── Excel/            # Excel raporları
├── database/             # SQLite veritabanı
├── backup/               # Veritabanı yedekleri
├── logs/                 # Log dosyaları
└── docs/                 # Dokümantasyon
```

---

## 🛠️ Teknoloji Stack

- **Python 3.8+** - Ana dil
- **PyQt5** - Modern GUI framework
- **SQLite** - Veritabanı
- **pandas** - Veri işleme
- **openpyxl** - Excel okuma/yazma

---

## 📊 Veritabanı

Proje 2 ana tablo kullanır:
- **hatali_isler** - Hatalı çalışan işler (11 kolon)
- **uzun_isler** - Uzun süren işler (10 kolon)

**Detaylı şema:** [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md)

---

## 🎨 Özellikler

### ✅ Tamamlanan
- Excel dosyalarından çoklu sheet okuma
- Otomatik rapor tipi algılama (HATALI/UZUN)
- 3 tab görünüm (Hatalı İşler, Uzun İşler, Birleşik)
- Gelişmiş filtreleme ve arama
- Toplu arama (wildcard * desteği)
- Excel export
- İstatistikler ve dashboard
- Logger sistemi
- Tema sistemi (Light/Dark/Blue)
- Yedekleme/geri yükleme

### 🔄 Devam Eden
- Log viewer iyileştirmeleri
- Performans optimizasyonları
- Modüler kod yapısı

---

## 📚 Dokümantasyon

| Dosya | Açıklama |
|-------|----------|
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | Detaylı kurulum kılavuzu |
| [CHANGELOG.md](CHANGELOG.md) | Versiyon geçmişi |
| [docs/TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md) | Teknik detaylar |
| [docs/DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) | Veritabanı şeması |
| [PROGRESS_SUMMARY.md](PROGRESS_SUMMARY.md) | Proje ilerlemesi |
| [EXCEL_KOLON_LISTESI.md](EXCEL_KOLON_LISTESI.md) | Excel kolon detayları |

---

## 🔄 Versiyonlama

**Mevcut Versiyon:** 1.0.0

Bu proje [Semantic Versioning](https://semver.org/lang/tr/) kullanır: `MAJOR.MINOR.PATCH`

**Değişiklikler:** [CHANGELOG.md](CHANGELOG.md)

---

## 📞 Destek

### Sorun Bildirme
- GitHub Issues kullanın
- Log dosyasını ekleyin (`logs/app.log`)
- Hata detaylarını belirtin

### Özellik İsteği
- GitHub Issues → "enhancement" etiketi
- Detaylı açıklama + kullanım senaryosu

---

## 📄 Lisans

Bu proje özel kullanım içindir.

---

**Son Güncelleme:** 07.03.2026  
**Versiyon:** 1.0.0  
**Durum:** Aktif Geliştirme  
**Git:** [github.com/Hrcan/Proje_Q](https://github.com/Hrcan/Proje_Q)
