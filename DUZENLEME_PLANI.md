# Düzenleme Planı - 07.03.2026

## 🎯 Hedef
Projeyi optimize etmek ve iyileştirmek

## ✅ Tamamlanan Hazırlıklar
- ✅ Full backup alındı: `backup/backup_20260307_165810.zip`
- ✅ BACKUP_INFO.md oluşturuldu
- ✅ Git commit yapıldı (commit: 1b02f35)
- ⏳ Git push devam ediyor...

## 🔍 Analiz Sonuçları

### 📊 Kod Boyutları (Token Limiti Analizi):
1. **src/ui/main_window.py** - ~1000 satır ⚠️ **EN BÜYÜK**
   - Menü oluşturma: ~100 satır
   - Toolbar oluşturma: ~50 satır
   - Arama bölümü: ~100 satır
   - Tablo işlemleri: ~200 satır
   - Dialog çağrıları: ~100 satır
   - Event handler'lar: ~150 satır
   - Tema ve ayarlar: ~100 satır
   - Toplam: ~1000 satır

2. **src/database/db_manager.py** - ~400 satır
   - Tablo oluşturma: ~200 satır
   - CRUD işlemleri: ~150 satır
   - Optimizasyon: ~50 satır

3. **test_gui.py** - ~490 satır (artık kullanılmıyor)

4. **UI Dialogları** - Her biri ~200-300 satır
   - advanced_filters_dialog.py
   - bulk_search_dialog.py
   - bulk_search_results_dialog.py
   - export_dialog.py
   - log_viewer_dialog.py
   - settings_dialog.py
   - statistics_dialog.py

### ⚠️ Bilinen Sorunlar:
1. **Logger Sorunu** - Kullanıcı beklentisini karşılamıyor
2. **Token Limiti** - main_window.py çok büyük
3. **Kod Tekrarları** - 3 tablo için benzer kodlar

## 💡 ÖNERİLEN DÜZENLEMELERVE SEÇENEKLERİ:

### Seçenek 1: Logger Düzeltmesi (ÖNCELİKLİ)
**Yapılacaklar:**
- [ ] Logger'ın tam sorununu tespit et
- [ ] Format düzeltmesi (timestamp, mesaj yapısı)
- [ ] Türkçe karakter kodlaması kontrolü
- [ ] Log viewer görüntüleme iyileştirmesi
- [ ] Test ve doğrulama

**Süre:** ~30-45 dk
**Fayda:** Kullanıcı memnuniyeti

### Seçenek 2: Token Optimizasyonu
**Yapılacaklar:**
- [ ] main_window.py'ı modüler hale getir:
  - `src/ui/components/menu_builder.py` (menü oluşturma)
  - `src/ui/components/toolbar_builder.py` (toolbar)
  - `src/ui/components/table_manager.py` (tablo işlemleri)
- [ ] Kod tekrarlarını azalt
- [ ] Ortak fonksiyonlar oluştur

**Süre:** ~2-3 saat
**Fayda:** Token tasarrufu, sürdürülebilirlik

### Seçenek 3: Hızlı İyileştirmeler
**Yapılacaklar:**
- [ ] test_gui.py'yi sil/arşivle (artık gerekmiyor)
- [ ] README'yi kısalt (core bilgi + link)
- [ ] Gereksiz yorumları temizle
- [ ] Duplicate kodları birleştir

**Süre:** ~20-30 dk
**Fayda:** Hızlı token tasarrufu

### Seçenek 4: Kombine Yaklaşım (ÖNERİLEN)
**Sıralama:**
1. **Hızlı İyileştirmeler** (20 dk)
   - test_gui.py arşivle
   - Gereksiz kod temizliği
   
2. **Logger Düzeltmesi** (30 dk)
   - Kullanıcı isteklerine göre düzelt
   - Test ve doğrula
   
3. **Modüler Yapı** (isteğe bağlı, sonraki oturum)
   - main_window.py'ı böl
   - Daha sürdürülebilir kod

**Toplam Süre:** ~50 dk + isteğe bağlı
**Fayda:** Dengeli yaklaşım

## ❓ KULLANICIYA SORULAR:

1. **Hangi seçeneği tercih edersin?**
   - A) Sadece Logger düzeltmesi (hızlı)
   - B) Token optimizasyonu (kapsamlı)
   - C) Hızlı iyileştirmeler (temizlik)
   - D) Kombine (önerilen)

2. **Logger'da tam olarak ne sorun var?**
   - Format mu?
   - Türkçe karakterler mi?
   - Görüntüleme mi?
   - Eksik özellik mi?

3. **main_window.py modüler yapıya çevrilsin mi?**
   - Evet, şimdi yapalım
   - Hayır, sonraya bırakalım
   - Sadece en kritik kısmı bölelim

4. **test_gui.py silinsin mi?**
   - Evet, artık gerekmiyor
   - Hayır, arşivde tutalım

## 📋 EYLEM PLANI (Kullanıcı Seçimine Göre Güncellenecek)

**Bekleniyor:** Kullanıcının tercihi...

---

**Not:** Bu plan esnek bir plandır. Kullanıcı tercihi doğrultusunda şekillenecektir.