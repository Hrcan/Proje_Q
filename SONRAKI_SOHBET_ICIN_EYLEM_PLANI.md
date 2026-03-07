# Sonraki Sohbet İçin Eylem Planı - 08.03.2026

## 🎯 MODÜLER YAPIYA GEÇİŞ - Devam

## 📋 ÖNCEKİ SOHBET ÖZETİ (07.03.2026)

### ✅ Tamamlanan İşler:
1. **Hızlı Temizlik**
   - README: 581 → 150 satır
   - Git: 4432bef

2. **Logger İyileştirmesi**
   - Auto-refresh (2sn)
   - Real-time görüntüleme
   - Git: 76557a5

3. **Modüler Yapı Başlatıldı**
   - FULL BACKUP: `backup/full_backups/full_backup_before_modular_20260307_175415.zip`
   - **table_manager.py oluşturuldu** (291 satır) ✅
   - Git: a6d3bfe

---

## 🚀 BU SOHBETTE YAPILACAKLAR

### ÖNCELİK 1: menu_builder.py + toolbar_builder.py

#### 1. menu_builder.py Oluştur (~200 satır)

**Görevler:**
```python
class MenuBuilder:
    def __init__(self, parent)
    def build_menu_bar()           # Ana menü çubuğu
    def build_file_menu()           # Dosya menüsü
    def build_edit_menu()           # Düzenle menüsü
    def build_view_menu()           # Görünüm menüsü
    def build_tools_menu()          # Araçlar menüsü
    def build_help_menu()           # Yardım menüsü
```

**İçerik:**
- Dosya: Yükle, Export, Yedekle, Geri Yükle, Çıkış
- Düzenle: Yenile, Filtreleri Temizle, Veritabanı Temizle
- Görünüm: Tema seçenekleri, İstatistikler
- Araçlar: Ayarlar, Loglar, Optimize
- Yardım: Kılavuz, Hakkında

**Adımlar:**
- [ ] menu_builder.py dosyasını oluştur
- [ ] Sınıfı ve metotları yaz
- [ ] main_window.py'den menü kodlarını kopyala
- [ ] Git commit + push

#### 2. toolbar_builder.py Oluştur (~100 satır)

**Görevler:**
```python
class ToolbarBuilder:
    def __init__(self, parent)
    def build_toolbar()             # Ana toolbar
    def add_file_actions()          # Dosya işlemleri
    def add_view_actions()          # Görünüm işlemleri
```

**İçerik:**
- Yükle, Yenile, Aktar, Yedekle
- İstatistik, Ayarlar

**Adımlar:**
- [ ] toolbar_builder.py dosyasını oluştur
- [ ] Sınıfı ve metotları yaz
- [ ] main_window.py'den toolbar kodlarını kopyala
- [ ] Git commit + push

---

### ÖNCELİK 2: search_panel.py + dialog_manager.py

#### 3. search_panel.py Oluştur (~150 satır)

**Görevler:**
```python
class SearchPanel(QGroupBox):
    def __init__(self, parent)
    def create_search_widgets()     # Arama widget'ları
    def get_filters()               # Mevcut filtreleri al
    def clear_filters()             # Filtreleri temizle
    def on_search_changed()         # Arama değiştiğinde
```

**İçerik:**
- JCL arama kutusu
- Ekip ve Ay combo box'ları
- Checkbox'lar (Hatalı, Uzun)
- Butonlar (Toplu Arama, Gelişmiş Filtre, Temizle)

**Adımlar:**
- [ ] search_panel.py dosyasını oluştur
- [ ] QGroupBox inherit et
- [ ] main_window.py'den arama bölümünü taşı
- [ ] Git commit + push

#### 4. dialog_manager.py Oluştur (~100 satır)

**Görevler:**
```python
class DialogManager:
    def __init__(self, parent)
    def show_bulk_search()          # Toplu arama
    def show_advanced_filters()     # Gelişmiş filtreler
    def show_statistics()           # İstatistikler
    def show_settings()             # Ayarlar
    def show_logs()                 # Loglar
    def show_backup_dialogs()       # Yedekleme dialog'ları
```

**İçerik:**
- Dialog açma fonksiyonları
- İmport'lar merkezi yerden

**Adımlar:**
- [ ] dialog_manager.py dosyasını oluştur
- [ ] Tüm dialog açma fonksiyonlarını taşı
- [ ] Git commit + push

---

### ÖNCELİK 3: main_window.py Refactor

#### 5. main_window.py'yi Güncelle

**Değişiklikler:**
```python
from .components.table_manager import TableManager
from .components.menu_builder import MenuBuilder
from .components.toolbar_builder import ToolbarBuilder
from .components.search_panel import SearchPanel
from .components.dialog_manager import DialogManager

class MainWindow(QMainWindow):
    def __init__(self):
        # Modülleri başlat
        self.table_manager = TableManager(self)
        self.menu_builder = MenuBuilder(self)
        self.toolbar_builder = ToolbarBuilder(self)
        self.dialog_manager = DialogManager(self)
        
        # SearchPanel widget olarak kullan
        self.search_panel = SearchPanel(self)
```

**Silinecek Kodlar:**
- ~200 satır menü kodu → menu_builder'a
- ~100 satır toolbar kodu → toolbar_builder'a
- ~150 satır arama paneli → search_panel'a
- ~100 satır dialog kodları → dialog_manager'a
- ~350 satır tablo kodları → ZATEN table_manager'da

**Kalan:** ~300 satır (koordinasyon kodu)

**Adımlar:**
- [ ] İmport'ları ekle
- [ ] Modülleri başlat
- [ ] Eski kodları sil
- [ ] Yeni modül metodlarını çağır
- [ ] Test et
- [ ] Git commit + push

---

### ÖNCELİK 4: Test ve Doğrulama

**Test Senaryoları:**
- [ ] Uygulama açılıyor mu?
- [ ] Menüler çalışıyor mu?
- [ ] Toolbar butonları çalışıyor mu?
- [ ] Arama ve filtreleme çalışıyor mu?
- [ ] Tablolar yükleniyor mu?
- [ ] Dialog'lar açılıyor mu?
- [ ] Excel yükleme çalışıyor mu?
- [ ] Export çalışıyor mu?

**Hata Varsa:**
- [ ] Hata mesajını kaydet
- [ ] main_window.py'de eksik fonksiyon var mı kontrol et
- [ ] İmport'lar doğru mu kontrol et
- [ ] Düzelt ve tekrar test et

---

## 📊 BAŞARI KRİTERLERİ

### Kod Metrikleri:
- ✅ main_window.py: 1028 → ~300 satır (**-700 satır!**)
- ✅ 5 yeni modül oluşturuldu
- ✅ Kod tekrarı yok
- ✅ Her modül tek bir sorumluluğa sahip

### Kalite Metrikleri:
- ✅ Tüm özellikler çalışıyor
- ✅ Hata yok
- ✅ Git commit'ler yapıldı
- ✅ Backup'lar alındı

---

## 🔄 ADIM ADIM PLAN

### Adım 1: menu_builder.py (45 dk)
1. Dosya oluştur
2. MenuBuilder sınıfı yaz
3. main_window'dan kodları kopyala
4. Git commit

### Adım 2: toolbar_builder.py (20 dk)
1. Dosya oluştur
2. ToolbarBuilder sınıfı yaz
3. main_window'dan kodları kopyala
4. Git commit

### Adım 3: search_panel.py (30 dk)
1. Dosya oluştur
2. SearchPanel sınıfı yaz (QGroupBox)
3. main_window'dan kodları kopyala
4. Git commit

### Adım 4: dialog_manager.py (20 dk)
1. Dosya oluştur
2. DialogManager sınıfı yaz
3. main_window'dan kodları kopyala
4. Git commit

### Adım 5: main_window.py Refactor (45 dk)
1. Modülleri import et
2. __init__'de modülleri başlat
3. Eski kodları sil
4. Yeni metodları çağır
5. Git commit

### Adım 6: Test (30 dk)
1. Uygulamayı çalıştır
2. Tüm özellikleri test et
3. Hataları düzelt
4. Final test

### Adım 7: Dokümantasyon (15 dk)
1. README'yi güncelle
2. CHANGELOG'u güncelle
3. SONRAKI_SOHBET_NOTLARI'nı güncelle
4. Final git commit + push

**TOPLAM SÜRE:** ~3-3.5 saat

---

## ⚠️ DİKKAT EDİLECEKLER

1. **Her Modül Sonrası:**
   - Git commit yap
   - Kısa test et (import çalışıyor mu?)

2. **main_window Refactor:**
   - Eski kodları silmeden önce yedek al
   - Adım adım ilerle
   - Her değişiklikten sonra test et

3. **Test Aşaması:**
   - Tüm özellikleri test et
   - Hataları belge
   - Düzelt ve tekrar test et

4. **Backup:**
   - Refactor öncesi full backup al
   - Her major değişiklikten sonra git commit

---

## 📝 BAŞLANGIÇ KOD ŞABLONU

### menu_builder.py Template:
```python
"""
Menü Oluşturucu - Ana menü çubuğu yönetimi
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import QAction, QMenu

class MenuBuilder:
    def __init__(self, parent):
        self.parent = parent
    
    def build_menu_bar(self):
        """Tüm menüleri oluştur"""
        menubar = self.parent.menuBar()
        self.build_file_menu(menubar)
        self.build_edit_menu(menubar)
        # ...
```

---

## 🎯 BEKLENTİ

**Sohbet Sonunda:**
- ✅ 5 modül oluşturulmuş
- ✅ main_window.py refactor edilmiş (300 satır)
- ✅ Tüm özellikler çalışıyor
- ✅ Git'e gönderilmiş
- ✅ Versiyon: 0.5.0

**Sonuç:**
- 🎉 Modüler, sürdürülebilir, temiz kod
- 🎉 Token kullanımı optimize
- 🎉 Kod tekrarı yok
- 🎉 Test edilebilir yapı

---

**Hazırlayan:** Claude (Cline) - 07.03.2026
**Onaylayan:** Kullanıcı
**Başlangıç:** Sonraki sohbet
**Tahmini Süre:** 3-3.5 saat