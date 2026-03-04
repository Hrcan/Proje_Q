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
- Veritabanı katmanı implementasyonu
- Excel okuyucu modülü
- PyQt5 GUI geliştirme
- Raporlama sistemi

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
- 📊 Excel ve TXT örnek dosyaları (Data/txt-jpeg/)

### Technical Details
- **Python Version**: 3.8+
- **Database**: SQLite 3.x
- **GUI Framework**: PyQt5 5.15.10
- **Version Scheme**: Semantic Versioning 2.0.0

---

## Versiyon Notları

### 0.x.x - Development Stage
Proje henüz geliştirme aşamasındadır. 0.x.x versiyonlarında API ve yapı değişiklikleri beklenebilir.

### 1.0.0 - İlk Stabil Versiyon (Planlanan)
- Tüm temel özellikler tamamlanmış
- Kapsamlı testler yazılmış
- .exe deployment hazır
- Kullanım kılavuzu tamamlanmış

---

**Semantic Versioning Kuralları:**

Versiyon formatı: `MAJOR.MINOR.PATCH[-PRERELEASE]`

1. **MAJOR** (0.x.x → 1.x.x): Geriye dönük uyumsuz API değişiklikleri
2. **MINOR** (x.0.x → x.1.x): Geriye dönük uyumlu yeni özellikler
3. **PATCH** (x.x.0 → x.x.1): Geriye dönük uyumlu bug düzeltmeleri
4. **PRERELEASE**: -alpha, -beta, -rc1 gibi ön sürüm işaretleri

**Örnekler:**
- `0.1.0` → İlk development sürümü
- `0.2.0` → Yeni modül eklendi (veritabanı katmanı)
- `0.2.1` → Bug düzeltmesi
- `1.0.0-beta` → İlk beta sürümü
- `1.0.0` → İlk stabil sürüm

[Unreleased]: https://github.com/Hrcan/Proje_Q/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Hrcan/Proje_Q/releases/tag/v0.1.0