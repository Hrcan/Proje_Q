"""
Dialog Yöneticisi - Merkezi dialog yönetimi
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import QDialog, QMessageBox


class DialogManager:
    """Dialog açma ve yönetme sınıfı"""
    
    def __init__(self, parent):
        """
        Args:
            parent: Ana pencere (MainWindow) referansı
        """
        self.parent = parent
    
    def show_bulk_search(self):
        """Toplu arama dialogu göster"""
        try:
            from ..bulk_search_dialog import BulkSearchDialog
            from ..bulk_search_results_dialog import BulkSearchResultsDialog
            
            dialog = BulkSearchDialog(self.parent)
            if dialog.exec_() == QDialog.Accepted:
                jcl_list = dialog.get_jcl_list()
                unique_jcls = list(set(jcl_list))
                
                # Tüm verilerde ara
                all_hatali = self.parent.db_manager.get_all_hatali_isler()
                all_uzun = self.parent.db_manager.get_all_uzun_isler()
                
                # Eşleşen kayıtları bul (wildcard desteği ile)
                hatali_results = self._search_records(all_hatali, unique_jcls)
                uzun_results = self._search_records(all_uzun, unique_jcls)
                
                # Sonuçları ayrı bir dialogda göster
                results_dialog = BulkSearchResultsDialog(
                    self.parent, unique_jcls, hatali_results, uzun_results
                )
                results_dialog.exec_()
                
                # Dialog kapandıktan sonra ana arama kutusuna da yazdır
                jcl_text = ', '.join(unique_jcls)
                self.parent.search_panel.jcl_search.setText(jcl_text)
                
                # Tabloları güncelle
                self.parent.table_manager.refresh_all_tables()
                
                # Durum güncellemesi
                total_results = len(hatali_results) + len(uzun_results)
                self.parent.status_label.setText(
                    f"🔍 Toplu arama: {len(jcl_list)} JCL → {total_results} sonuç bulundu"
                )
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Toplu arama hatası:\n{str(e)}\n\n{error_detail}"
            )
    
    def _search_records(self, records, jcl_patterns):
        """Kayıtlarda wildcard destekli arama yap"""
        results = []
        
        for record in records:
            jcl_adi_upper = record['jcl_adi'].upper()
            for jcl_pattern in jcl_patterns:
                jcl_pattern_upper = jcl_pattern.upper()
                matched = False
                
                if '*' in jcl_pattern_upper:
                    # Wildcard pattern
                    pattern_parts = jcl_pattern_upper.split('*')
                    if len(pattern_parts) == 2:
                        prefix, suffix = pattern_parts
                        if prefix and suffix:
                            # PONT*ABC gibi
                            if jcl_adi_upper.startswith(prefix) and jcl_adi_upper.endswith(suffix):
                                matched = True
                        elif prefix:
                            # PONT* gibi
                            if jcl_adi_upper.startswith(prefix):
                                matched = True
                        elif suffix:
                            # *ABC gibi
                            if jcl_adi_upper.endswith(suffix):
                                matched = True
                    elif len(pattern_parts) == 1 and jcl_pattern_upper == '*':
                        # Sadece * - tümü
                        matched = True
                else:
                    # Normal arama (içinde geçmeli)
                    if jcl_pattern_upper in jcl_adi_upper:
                        matched = True
                
                if matched:
                    results.append(record)
                    break
        
        return results
    
    def show_advanced_filters(self):
        """Gelişmiş filtreler dialogu göster"""
        try:
            from ..advanced_filters_dialog import AdvancedFiltersDialog
            
            dialog = AdvancedFiltersDialog(self.parent, self.parent.advanced_filters)
            if dialog.exec_() == QDialog.Accepted:
                self.parent.advanced_filters = dialog.get_filters()
                self.parent.search_panel.set_advanced_filter_active(True)
                self.parent.table_manager.refresh_all_tables()
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Gelişmiş filtre dialog hatası: {e}"
            )
    
    def show_statistics(self):
        """İstatistikler dialogu göster"""
        try:
            from ..statistics_dialog import StatisticsDialog
            
            dialog = StatisticsDialog(self.parent, self.parent.db_manager)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"İstatistik dialog hatası: {e}"
            )
    
    def show_settings(self):
        """Ayarlar dialogu göster"""
        try:
            from ..settings_dialog import SettingsDialog
            
            dialog = SettingsDialog(self.parent, self.parent.preferences)
            if dialog.exec_() == QDialog.Accepted:
                self.parent.status_label.setText("✅ Ayarlar kaydedildi")
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Ayarlar dialog hatası: {e}"
            )
    
    def show_logs(self):
        """Log görüntüleyici dialogu göster"""
        try:
            from ..log_viewer_dialog import LogViewerDialog
            
            dialog = LogViewerDialog(self.parent)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Log viewer hatası: {e}"
            )
    
    def show_export_dialog(self, table, default_name):
        """Excel export dialogu göster"""
        try:
            from ..export_dialog import ExportDialog
            
            dialog = ExportDialog(self.parent, table, default_name)
            if dialog.exec_() == QDialog.Accepted:
                self.parent.status_label.setText("✅ Excel export başarılı")
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Export dialog hatası: {e}"
            )
    
    def create_backup_dialog(self):
        """Yedek oluşturma dialogu göster"""
        try:
            success, result = self.parent.backup_manager.create_backup('Manuel yedek')
            if success:
                self.parent.preferences.update_backup_time()
                QMessageBox.information(
                    self.parent, "Başarılı", 
                    f"✅ Yedek oluşturuldu:\n{result}"
                )
                self.parent.status_label.setText("✅ Yedek oluşturuldu")
            else:
                QMessageBox.critical(
                    self.parent, "Hata", 
                    f"Yedekleme hatası:\n{result}"
                )
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Yedekleme hatası: {e}"
            )
    
    def restore_backup_dialog(self):
        """Yedekten geri yükleme dialogu göster"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            backups = self.parent.backup_manager.list_backups()
            if not backups:
                QMessageBox.information(
                    self.parent, "Bilgi", 
                    "Yedek dosyası bulunamadı."
                )
                return
            
            # En son yedeği seç
            file_path, _ = QFileDialog.getOpenFileName(
                self.parent, "Yedek Dosyası Seç", "backup",
                "Backup Files (*.zip)"
            )
            
            if file_path:
                success, message = self.parent.backup_manager.restore_backup(file_path)
                if success:
                    self.parent.table_manager.refresh_all_tables()
                    QMessageBox.information(
                        self.parent, "Başarılı", 
                        "✅ Yedek geri yüklendi!"
                    )
                    self.parent.status_label.setText("✅ Yedek geri yüklendi")
                else:
                    QMessageBox.critical(
                        self.parent, "Hata", 
                        f"Geri yükleme hatası:\n{message}"
                    )
        except Exception as e:
            QMessageBox.critical(
                self.parent, "Hata", 
                f"Geri yükleme hatası: {e}"
            )
    
    def show_user_guide(self):
        """Kullanım kılavuzu göster"""
        QMessageBox.information(
            self.parent, "Kullanım Kılavuzu",
            "🎯 Proje_Q - JCL Veri Yönetim Sistemi\n\n"
            "📂 Excel Yükle: Data/Excel klasöründen dosya seçin\n"
            "🔍 Arama: JCL adı, ekip veya ay ile filtreleyin\n"
            "📊 Excel Export: Mevcut görünümü Excel'e aktarın\n"
            "💾 Yedekleme: Düzenli veritabanı yedekleri alın\n\n"
            "Detaylı bilgi için README.md dosyasına bakın."
        )
    
    def show_about(self):
        """Hakkında dialogu göster"""
        QMessageBox.about(
            self.parent, "Hakkında",
            "🎯 <b>Proje_Q - JCL Veri Yönetim Sistemi</b><br><br>"
            "📌 Versiyon: 0.5.0<br>"
            "📅 Tarih: Mart 2026<br>"
            "👨‍💻 Geliştirici: Proje Ekibi<br><br>"
            "📝 Excel ve TXT dosyalarından JCL verilerini<br>"
            "okuyup SQLite veritabanına kaydeden,<br>"
            "yöneten ve raporlayan masaüstü uygulaması.<br><br>"
            "🔧 Teknolojiler: Python, PyQt5, SQLite, pandas"
        )