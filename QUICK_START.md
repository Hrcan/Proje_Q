# ⚡ QUICK START - Token Tasarruflu Başlangıç

**Yeni sohbete başlarken bu dosyayı oku!**

## 📁 Kritik Dosyalar (Sadece bunları oku)

### Ana Dosyalar:
1. **src/main.py** - Entry point (50 satır)
2. **src/ui/main_window.py** - Ana pencere (600 satır)
3. **src/database/db_manager.py** - DB işlemleri (400 satır)

### Modüler Bileşenler (src/ui/components/):
- **dialog_manager.py** - Tüm dialogları yönetir
- **menu_builder.py** - Menü yapısı
- **search_panel.py** - Arama paneli
- **table_manager.py** - Tablo yönetimi
- **toolbar_builder.py** - Toolbar

## 🎯 Sık Kullanılan İşlemler

### Yeni Dialog Eklemek:
1. `src/ui/yeni_dialog.py` oluştur
2. `dialog_manager.py`'e ekle
3. `menu_builder.py` veya `toolbar_builder.py`'den çağır

### Yeni Menü Öğesi:
- `src/ui/components/menu_builder.py` → `build_menu_bar()`

### Yeni Tablo Kolonu:
- `src/ui/components/table_manager.py` → ilgili `create_*_table()`

## 📊 Veritabanı Şeması

```sql
hatali_isler: id, jcl_adi, ay, hatali_sayi_ay, sorumlu_ekip, ...
uzun_isler: id, jcl_adi, ay, sure_dk, sorumlu_ekip, ...
yukleme_gecmisi: id, dosya_adi, yuklenme_tarihi, kayit_sayisi, durum
```

## 🔧 Önemli Kod Lokasyonları

### Log Sistemi:
- **Başlatma:** `src/utils/logger.py` → `app_logger`
- **Kullanım:** `app_logger.info("mesaj")`

### Tema Değiştirme:
- **Dosya:** `src/ui/main_window.py` → `change_theme()`
- **Temalar:** light, dark, blue

### Excel Yükleme:
- **Dosya:** `src/ui/main_window.py` → `load_excel()`
- **Reader:** `src/utils/excel_reader.py`

## 🚀 Yeni Sohbete Başlarken

**Sadece şu dosyaları oku:**
1. ✅ Bu dosya (QUICK_START.md)
2. ✅ NEXT_SESSION_PLAN.md

**Diğer dosyaları sadece gerekirse oku!**

## 💡 Token Tasarrufu İpuçları

1. **Tam dosya okuma yerine:**
   - "src/ui/main_window.py dosyasındaki load_excel metodunu göster"
   - Sadece ilgili bölümü oku

2. **Yapı soruları için:**
   - "list_code_definition_names src/ui/components"
   - Tüm dosyayı okumadan yapıyı gör

3. **Değişiklikler için:**
   - Küçük değişiklikler → replace_in_file
   - Büyük değişiklikler → Önce plan, sonra uygula

## 📋 Son Durum (v0.5.0)

- ✅ Modüler yapı (components/)
- ✅ Canlı log paneli
- ✅ İstatistikler (Tüm İşler tab)
- ✅ Tema sistemi + logging
- ✅ Yedekleme sistemi
- ✅ Git aktif (commit: a05e6b9)

## 🎯 Sonraki Görevler

**Planlar:**
- 🔜 Yeni arama modülü
- 🔜 [Kullanıcıdan alınacak]

---
**Not:** Bu dosya ile başla, gerekirse diğer dosyalara bak!