# 🚀 Proje_Q - Kurulum Kılavuzu

Bu kılavuz, Proje_Q'yu farklı bilgisayarlarda kurmanız için adım adım talimatlar içerir.

---

## 📋 İçindekiler

- [Sistem Gereksinimleri](#sistem-gereksinimleri)
- [Hızlı Kurulum](#hızlı-kurulum)
- [Detaylı Kurulum](#detaylı-kurulum)
- [Sorun Giderme](#sorun-giderme)
- [Sık Sorulan Sorular](#sık-sorulan-sorular)

---

## 💻 Sistem Gereksinimleri

### Zorunlu Programlar

| Program | Minimum Versiyon | Önerilen | İndirme Linki |
|---------|------------------|----------|---------------|
| **Python** | 3.8+ | 3.12+ | [python.org](https://www.python.org/downloads/) |
| **pip** | 20.0+ | En son | Python ile gelir |
| **Git** | 2.0+ | En son | [git-scm.com](https://git-scm.com/downloads) |

### Donanım Gereksinimleri

- **RAM:** Minimum 4GB (Önerilen: 8GB+)
- **Disk:** 500MB boş alan
- **İşletim Sistemi:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)

---

## ⚡ Hızlı Kurulum

### Otomatik Kurulum (Önerilen)

```bash
# 1. Repository'yi klonlayın
git clone https://github.com/Hrcan/proje_q.git
cd proje_q

# 2. Gereksinimleri kontrol edin
python check_requirements.py

# 3. Otomatik kurulum
python setup_environment.py

# 4. Virtual environment'ı aktive edin
# Windows:
activate_env.bat
# Linux/macOS:
./activate_env.sh
```

### Manuel Kurulum

```bash
# 1. Virtual environment oluştur
python -m venv venv

# 2. Aktive et
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 3. Paketleri kur
pip install -r requirements.txt
```

---

## 📚 Detaylı Kurulum

### 1. Python Kurulumu

#### Windows

1. [Python İndirme Sayfası](https://www.python.org/downloads/windows/) adresine gidin
2. En son Python 3.x sürümünü indirin (örn: Python 3.12.10)
3. İndirilen dosyayı çalıştırın
4. **ÖNEMLİ:** "Add Python to PATH" seçeneğini işaretleyin
5. "Install Now" tıklayın

**Kurulumu Doğrula:**
```bash
python --version
# Çıktı: Python 3.12.10
```

#### macOS

```bash
# Homebrew ile:
brew install python@3.12

# Veya resmi installer:
# https://www.python.org/downloads/macos/
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

---

### 2. Git Kurulumu

#### Windows

1. [Git for Windows](https://git-scm.com/download/win) indirin
2. Installer'ı çalıştırın
3. Varsayılan ayarlarla devam edin

#### macOS

```bash
# Xcode Command Line Tools ile:
xcode-select --install

# Veya Homebrew ile:
brew install git
```

#### Linux

```bash
sudo apt install git  # Ubuntu/Debian
sudo yum install git  # CentOS/RHEL
```

**Kurulumu Doğrula:**
```bash
git --version
# Çıktı: git version 2.53.0
```

---

### 3. Proje Kurulumu

#### Adım 1: Projeyi İndirin

**Git ile (Önerilen):**
```bash
git clone https://github.com/Hrcan/proje_q.git
cd proje_q
```

**Veya ZIP olarak:**
1. [GitHub Repository](https://github.com/Hrcan/proje_q) sayfasına gidin
2. "Code" → "Download ZIP" tıklayın
3. ZIP'i çıkarın ve klasöre girin

#### Adım 2: Sistem Kontrolü

```bash
python check_requirements.py
```

Bu script:
- ✅ Python versiyonunu kontrol eder
- ✅ pip kurulumunu doğrular
- ✅ Git'in varlığını kontrol eder
- ✅ Proje yapısını doğrular
- ✅ Kurulu paketleri listeler

#### Adım 3: Virtual Environment Oluşturma

**Neden Virtual Environment?**
- Projeyi izole eder
- Sistem Python'unu kirletmez
- Farklı projeler için farklı paket versiyonları kullanabilirsiniz

```bash
python -m venv venv
```

#### Adım 4: Virtual Environment Aktivasyonu

**Windows CMD:**
```bash
venv\Scripts\activate.bat
```

**Windows PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Aktif olduğunu nasıl anlarsınız?**
Komut satırında `(venv)` öneki görünür:
```bash
(venv) C:\Users\H\Desktop\proje_q>
```

#### Adım 5: Paket Kurulumu

```bash
pip install -r requirements.txt
```

Bu işlem şunları kurar:
- **PyQt5** (GUI framework)
- **pandas** (Excel/veri işleme)
- **openpyxl** (Excel okuma/yazma)
- **reportlab** (PDF oluşturma)
- **pyinstaller** (.exe oluşturma)
- **Geliştirme araçları** (pylint, black, pytest, mypy)

**İşlem süresi:** 2-5 dakika (internet hızınıza bağlı)

#### Adım 6: Kurulum Doğrulama

```bash
python -c "import PyQt5, pandas, openpyxl, reportlab; print('✅ Başarılı!')"
```

Çıktı:
```
✅ Başarılı!
```

---

### 4. Projeyi Çalıştırma

```bash
# Virtual environment aktif olduğundan emin olun
python src/main.py
```

**İlk çalıştırmada:**
- Veritabanı otomatik oluşturulur (`database/jcl_data.db`)
- Log klasörü oluşturulur
- Backup klasörü hazırlanır

---

## 🔧 Sorun Giderme

### Sık Karşılaşılan Hatalar

#### 1. "python is not recognized"

**Sebep:** Python PATH'e eklenmemiş

**Çözüm (Windows):**
```bash
# 1. Python kurulum yolunu bulun:
where python

# 2. Sistem değişkenlerine ekleyin:
# Kontrol Paneli → Sistem → Gelişmiş Sistem Ayarları
# → Ortam Değişkenleri → Path → Düzenle
# Python yolunu ekleyin (örn: C:\Python312)
```

#### 2. "pip install" çalışmıyor

**Sebep:** pip güncel değil veya kurulu değil

**Çözüm:**
```bash
# pip'i güncelle:
python -m pip install --upgrade pip

# pip yoksa:
python -m ensurepip --upgrade
```

#### 3. PyQt5 kurulum hatası

**Sebep:** C++ build tools eksik (Windows)

**Çözüm:**
1. [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/) indirin
2. "Desktop development with C++" seçeneğini işaretleyin
3. Kur ve bilgisayarı yeniden başlat

#### 4. "Permission denied" (Linux/macOS)

**Çözüm:**
```bash
# Script'lere çalıştırma izni verin:
chmod +x *.sh
chmod +x *.py

# Veya sudo ile çalıştırın:
sudo python setup_environment.py
```

#### 5. Virtual environment aktive edilemiyor

**Windows PowerShell için:**
```powershell
# Execution policy değiştirin:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 6. Import hataları

**Çözüm:**
```bash
# Virtual environment'ın aktif olduğundan emin olun
# Paketleri yeniden kurun:
pip install --force-reinstall -r requirements.txt
```

---

## ❓ Sık Sorulan Sorular

### Q1: Virtual environment her seferinde aktive etmem gerekiyor mu?

**Cevap:** Evet, her yeni terminal/komut satırı açtığınızda aktive etmelisiniz.

**İpucu:** `activate_env.bat` (Windows) veya `activate_env.sh` (Linux/macOS) scriptini kullanın.

---

### Q2: Başka bir PC'ye nasıl taşırım?

**Yöntem 1: Git ile**
```bash
# Yeni PC'de:
git clone https://github.com/Hrcan/proje_q.git
cd proje_q
python setup_environment.py
```

**Yöntem 2: Manuel**
1. Tüm proje klasörünü kopyalayın
2. Yeni PC'de:
```bash
cd proje_q
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### Q3: requirements.txt'i nasıl güncellerim?

```bash
# Mevcut paketleri listele:
pip freeze > requirements_new.txt

# Karşılaştır ve birleştir
```

---

### Q4: .exe dosyası nasıl oluştururum?

```bash
# Virtual environment aktif iken:
pyinstaller --onefile --windowed src/main.py

# .exe dosyası dist/ klasöründe olacak
```

---

### Q5: Hangi Python versiyonunu kullanmalıyım?

- **Minimum:** Python 3.8
- **Önerilen:** Python 3.12 (en yeni özellikler ve optimizasyonlar)
- **Test edildi:** Python 3.8, 3.9, 3.10, 3.11, 3.12

---

### Q6: Geliştirme araçları olmadan kurabilir miyim?

**Evet!** `requirements.txt` dosyasını düzenleyin:

```bash
# Sadece ana paketler (satır 1-18):
pip install PyQt5==5.15.10 PyQt5-Qt5==5.15.2 PyQt5-sip==12.13.0
pip install pandas==2.1.4 openpyxl==3.1.2 xlrd==2.0.1
pip install reportlab==4.0.9
pip install pyinstaller==6.3.0
```

---

### Q7: Disk alanı ne kadar?

- **Proje dosyaları:** ~50MB
- **Python paketleri:** ~300-400MB
- **Virtual environment:** ~500MB
- **Toplam:** ~850MB - 1GB

---

## 📞 Destek ve İletişim

### Sorun mu yaşıyorsunuz?

1. **check_requirements.py** çalıştırarak sisteminizi kontrol edin
2. **Hata mesajlarını** tam olarak kopyalayın
3. GitHub'da [Issue](https://github.com/Hrcan/proje_q/issues) açın

### Yararlı Kaynaklar

- 📖 [README.md](README.md) - Proje genel bakış
- 🔧 [TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md) - Teknik detaylar
- 🗄️ [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) - Veritabanı yapısı
- 📝 [CHANGELOG.md](CHANGELOG.md) - Versiyon geçmişi

---

## ✅ Kurulum Checklist

Kurulumunuzun tamamlandığından emin olmak için:

- [ ] Python 3.8+ kurulu ve PATH'te
- [ ] pip çalışıyor
- [ ] Git kurulu (opsiyonel)
- [ ] Proje indirildi
- [ ] Virtual environment oluşturuldu
- [ ] Virtual environment aktive edildi
- [ ] requirements.txt kuruldu
- [ ] Import testleri başarılı
- [ ] check_requirements.py ✅ veriyor
- [ ] src/main.py çalışıyor (gelecek versiyonda)

---

## 🎉 Tebrikler!

Kurulum tamamlandı! Artık Proje_Q üzerinde çalışmaya başlayabilirsiniz.

**Sonraki adımlar:**
1. [README.md](README.md) dosyasını okuyun
2. [TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md) ile projeyi anlayın
3. Geliştirmeye başlayın!

---

**Son Güncelleme:** 05.03.2026  
**Versiyon:** 1.0  
**Yazar:** Proje_Q Ekibi