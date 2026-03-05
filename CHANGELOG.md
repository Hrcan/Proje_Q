# Changelog

Tüm önemli değişiklikler bu dosyada belgelenecektir.

Bu proje [Semantic Versioning](https://semver.org/lang/tr/) standartlarını takip eder.

## Format

- **Added** - Yeni özellikler
- **Changed** - Mevcut özelliklerde değişiklikler
- **Deprecated** - Yakında kaldırılacak özellikler
- **Removed** - Kaldırılan özellikler
- **Fixed** - Bug düzeltmeleri
- **Security** - Güvenlik yamalarında

---

## [Unreleased]

### Planlanan
- Veritabanı katmanı implementasyonu (v0.3.0)
- Excel okuyucu modülü (v0.4.0)
- PyQt5 GUI geliştirme (v0.5.0)
- Raporlama sistemi (v0.6.0)

---

## [0.2.0] - 2026-03-05

### Added
- 🚀 **Otomatik Kurulum Sistemi**
  - `check_requirements.py` - Sistem gereksinimlerini kontrol eden script
  - `setup_environment.py` - Otomatik kurulum ve yapılandırma scripti
  - `INSTALLATION_GUIDE.md` - Kapsamlı kurulum kılavuzu
- 🔧 **Geliştirme Ortamı Hazırlığı**
  - Virtual environment (venv) oluşturma desteği
  - Platform bağımsız kurulum scriptleri (Windows/Linux/macOS)
  - Otomatik aktivasyon scriptleri (activate_env.bat/sh)
- 📦 **Paket Yönetimi**
  - Tüm Python paketleri başarıyla kuruldu ve doğrulandı
  - PyQt5 5.15.10, pandas 2.1.4, openpyxl 3.1.2, reportlab 4.0.9
  - Geliştirme araçları: pylint, black, mypy, pytest
- 📊 **Sistem Doğrulama**
  - Python 3.12.10 desteği
  - pip 25.0.1 güncelleme
  - Git 2.53.0 entegrasyonu
  - Renklendirme ve kullanıcı dostu çıktılar
- 📝 **Dokümantasyon Güncellemeleri**
  - Detaylı kurulum adımları
  - Sorun giderme rehberi
  - Sık sorulan sorular (FAQ)
  - Platform bazlı kurulum talimatları

### Changed
- 📄 README.md güncellendi (kurulum scriptleri eklendi)
- 🔧 Windows için UTF-8 karakter desteği eklendi
- 📦 requirements.txt doğrulandı (14 paket)

### Technical Details
- **Environment**: Virtual environment desteği
- **Automation**: Tam otomatik kurulum süreci
- **Cross-Platform**: Windows, Linux, macOS desteği
- **Validation**: Import testleri ve sistem kontrolleri

### Developer Experience
- ✅ Tek komutla kurulum: `python setup_environment.py`
- ✅ Hızlı kontrol: `python check_requirements.py`
- ✅ Farklı PC'lere kolay taşıma
- ✅ Renklendirme ile kullanıcı dostu arayüz

---

## [0.1.0] - 2026-03-05

### Added
- 🎉 İlk proje yapısı oluşturuldu
- 📝 Kapsamlı dokümantasyon:
  - README.md - Proje özeti ve genel bilgiler
  - docs/TECHNICAL_SPECS.md - Teknik spesifikasyonlar ve mimari
  - docs/DATABASE_SCHEMA.md - Veritabanı şeması ve SQL detayları
- 📁 Klasör yapısı:
  - src/ - Kaynak kodlar (ui, database, utils, config alt modülleri)
  - database/ - SQLite veritabanı dizini
  - logs/ - Log dosyaları dizini
  - backup/ - Yedek dosyaları dizini
  - tests/ - Test dosyaları dizini
  - docs/ - Dokümantasyon dizini
- 🔧 Konfigürasyon dosyaları:
  - .gitignore - Git ignore kuralları
  - requirements.txt - Python bağımlılıkları listesi
  - __init__.py - Python paket yapısı
- 🌐 Git repository kurulumu ve GitHub bağlantısı
- 📊 Excel ve TXT örnek dosyaları (Data/TXT-jpeg/)

### Technical Details
- **Python Version**: 3.8+
- **Database**: SQLite 3.x
- **GUI Framework**: PyQt5 5.15.10
- **Version Scheme**: Semantic Versioning 2.0.0

---

## Versiyon Notları

### 0.x.x - Development Stage
Proje henüz geliştirme aşamasındadır. 0.x.x versiyonlarında API ve yapı değişiklikleri beklenebilir.

**Mevcut Durum (v0.2.0):**
- ✅ Proje yapısı tamamlandı
- ✅ Dokümantasyon hazır
- ✅ Geliştirme ortamı kurulum sistemi hazır
- ⏳ Kod implementasyonu başlamadı (v0.3.0+)

**Sonraki Adımlar:**
- v0.3.0: Veritabanı katmanı
- v0.4.0: Veri okuma modülleri
- v0.5.0: GUI implementasyonu
- v0.6.0: Raporlama sistemi
- v1.0.0: İlk stabil versiyon

### 1.0.0 - İlk Stabil Versiyon (Planlanan)
- Tüm temel özellikler tamamlanmış
- Kapsamlı testler yazılmış
- .exe deployment hazır
- Kullanım kılavuzu tamamlanmış

---

## Semantic Versioning Kuralları

Versiyon formatı: `MAJOR.MINOR.PATCH[-PRERELEASE]`

1. **MAJOR** (0.x.x → 1.x.x): Geriye dönük uyumsuz API değişiklikleri
2. **MINOR** (x.0.x → x.1.x): Geriye dönük uyumlu yeni özellikler
3. **PATCH** (x.x.0 → x.x.1): Geriye dönük uyumlu bug düzeltmeleri
4. **PRERELEASE**: -alpha, -beta, -rc1 gibi ön sürüm işaretleri

**Örnekler:**
- `0.1.0` → İlk development sürümü
- `0.2.0` → Kurulum sistemi eklendi ✅
- `0.3.0` → Veritabanı katmanı (planlanan)
- `1.0.0-beta` → İlk beta sürümü
- `1.0.0` → İlk stabil sürüm

[Unreleased]: https://github.com/Hrcan/proje_q/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Hrcan/proje_q/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/Hrcan/proje_q/releases/tag/v0.1.0