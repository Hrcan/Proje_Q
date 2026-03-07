"""
Ana Pencere - Profesyonel GUI (Refactored - Modular)
Proje_Q - JCL Veri Yönetim Sistemi
v0.5.0 - Modüler Yapı
"""
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, 
                             QProgressBar, QSplitter, QStatusBar, QApplication)
from PyQt5.QtCore import Qt, QTimer

# Relative imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from utils.excel_reader import ExcelReader
from utils.backup_manager import BackupManager
from config.user_preferences import UserPreferences
from utils.logger import app_logger

# Modüler bileşenler
from .components import (TableManager, MenuBuilder, ToolbarBuilder, 
                         SearchPanel, DialogManager)


class MainWindow(QMainWindow):
    """Ana Uygulama Penceresi - Modüler Yapı"""
    
    def __init__(self):
        super().__init__()
        
        # Veritabanı ve yöneticiler
        self.db_manager = DatabaseManager()
        self.backup_manager = BackupManager()
        self.preferences = UserPreferences('config/user_prefs.json')
        
        # Gelişmiş filtre değişkenleri
        self.advanced_filters = {
            'tarih_baslangic': None,
            'tarih_bitis': None,
            'hatali_min': None,
            'hatali_max': None,
            'uzun_min': None,
            'uzun_max': None
        }
        
        # UI'yi başlat
        self.init_ui()
        self.init_database()
        self.restore_preferences()
        
        # Otomatik yedekleme kontrolü
        if self.preferences.needs_backup():
            QTimer.singleShot(1000, self.auto_backup_check)
    
    def init_ui(self):
        """Arayüzü oluştur - Modüler"""
        # Pencere ayarları
        self.setWindowTitle("Proje_Q - JCL Veri Yönetim Sistemi v0.5.0")
        self.setGeometry(100, 50, 1800, 900)
        
        # Modüler bileşenleri başlat
        self.menu_builder = MenuBuilder(self)
        self.toolbar_builder = ToolbarBuilder(self)
        self.dialog_manager = DialogManager(self)
        
        # Menü ve toolbar oluştur
        self.menu_builder.build_menu_bar()
        self.toolbar_builder.build_toolbar()
        
        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Başlık
        self.create_header(main_layout)
        
        # Ana içerik için yatay splitter (Sol: Tablolar, Sağ: Log Paneli)
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Sol panel - Arama ve Tablolar
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Dikey splitter (Arama + Tablo)
        splitter = QSplitter(Qt.Vertical)
        
        # Arama paneli (modüler)
        self.search_panel = SearchPanel(self)
        self.search_panel.connect_signals()
        splitter.addWidget(self.search_panel)
        
        # Tablo manager (modüler)
        self.table_manager = TableManager(self, self.db_manager)
        splitter.addWidget(self.table_manager)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        
        left_layout.addWidget(splitter)
        
        # Sağ panel - Log Görüntüleyici
        self.log_panel = self.create_log_panel()
        
        # Ana splitter'a ekle
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(self.log_panel)
        
        # Sol panele %65, sağ panele %35 yer ver (daha geniş log paneli)
        main_splitter.setStretchFactor(0, 65)
        main_splitter.setStretchFactor(1, 35)
        main_splitter.setSizes([1170, 630])  # Başlangıç boyutları - daha geniş log
        
        main_layout.addWidget(main_splitter)
        
        # Alt bölüm
        self.create_footer(main_layout)
        
        # Status bar
        self.create_status_bar()
        
        # Tema uygula
        self.apply_theme(self.preferences.get('theme', 'light'))
    
    def create_header(self, layout):
        """Başlık oluştur - Kompakt"""
        header = QLabel("🎯 JCL VERİ YÖNETİM SİSTEMİ")
        header.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #4CAF50);
                color: white;
                border-radius: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        header.setMaximumHeight(35)  # Sabit yükseklik
        layout.addWidget(header)
    
    def create_status_bar(self):
        """Status bar oluştur"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Sol: Genel durum
        self.status_label = QLabel("Hazır")
        self.status_bar.addWidget(self.status_label)
        
        # Sağ: Saat
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)
        
        # Saat güncelle
        self.update_time()
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
    
    def update_time(self):
        """Saati güncelle"""
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        self.time_label.setText(f"🕐 {current_time}")
    
    def create_footer(self, layout):
        """Alt bölüm - Progress bar ve butonlar"""
        footer = QVBoxLayout()
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumHeight(25)
        self.progress.setTextVisible(True)
        footer.addWidget(self.progress)
        
        # İstatistikler ve Butonlar
        stats_buttons = QHBoxLayout()
        
        # İstatistikler
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            QLabel {
                padding: 10px;
                background-color: #f0f0f0;
                border-radius: 5px;
                font-size: 11px;
            }
        """)
        stats_buttons.addWidget(self.stats_label, 1)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_load = QPushButton("📁 Excel Yükle")
        self.btn_load.clicked.connect(self.load_excel)
        self.btn_load.setFixedHeight(40)
        
        self.btn_refresh = QPushButton("🔄 Yenile")
        self.btn_refresh.clicked.connect(self.refresh_all)
        self.btn_refresh.setFixedHeight(40)
        
        self.btn_export = QPushButton("📊 Excel'e Aktar")
        self.btn_export.clicked.connect(self.export_to_excel)
        self.btn_export.setFixedHeight(40)
        
        self.btn_clear = QPushButton("🗑️ Temizle")
        self.btn_clear.clicked.connect(self.clear_database)
        self.btn_clear.setFixedHeight(40)
        
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_clear)
        
        stats_buttons.addLayout(btn_layout)
        footer.addLayout(stats_buttons)
        
        layout.addLayout(footer)
    
    def init_database(self):
        """Veritabanını başlat"""
        try:
            app_logger.info("Veritabanı bağlantısı kuruluyor...")
            self.db_manager.connect()
            self.db_manager.create_tables()
            app_logger.info("Veriler yükleniyor...")
            self.load_all_data()
            self.populate_filters()
            self.status_label.setText("✅ Veritabanı hazır")
            app_logger.info("Veritabanı başarıyla hazırlandı")
        except Exception as e:
            app_logger.error(f"Veritabanı hatası: {e}")
            QMessageBox.critical(self, "Hata", f"Veritabanı hatası: {e}")
            self.status_label.setText("❌ Veritabanı hatası")
    
    def restore_preferences(self):
        """Tercihleri geri yükle"""
        # Pencere boyutu
        window = self.preferences.get('window', {})
        if window:
            self.setGeometry(
                window.get('x', 100),
                window.get('y', 50),
                window.get('width', 1800),
                window.get('height', 900)
            )
        
        # Filtreleri geri yükle
        filters = self.preferences.get('filters', {})
        if filters:
            self.search_panel.restore_filters(filters)
    
    def save_preferences(self):
        """Tercihleri kaydet"""
        # Pencere geometrisi
        self.preferences.update_window_geometry(
            self.x(), self.y(), self.width(), self.height()
        )
        
        # Filtreleri kaydet
        filters = self.search_panel.get_filters()
        self.preferences.update_filters(
            jcl=filters['jcl'],
            ekip=filters['ekip'],
            ay=filters['ay'],
            hatali=filters['hatali'],
            uzun=filters['uzun']
        )
    
    def populate_filters(self):
        """Filtreleri doldur"""
        ekipler = set()
        aylar = set()
        
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
        for record in hatali_data + uzun_data:
            if record.get('sorumlu_ekip'):
                ekipler.add(record['sorumlu_ekip'])
            if record.get('ay'):
                aylar.add(record['ay'])
        
        self.search_panel.populate_combo_boxes(ekipler, aylar)
    
    def load_all_data(self):
        """Tüm verileri yükle"""
        self.table_manager.load_all_tables(self.search_panel.get_filters())
        self.update_stats()
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        stats = self.db_manager.get_tablo_istatistikleri()
        visible_counts = self.table_manager.get_visible_counts()
        
        self.stats_label.setText(
            f"📊 İstatistikler: "
            f"Hatalı: {visible_counts['hatali']}/{stats['hatali_isler']} | "
            f"Uzun: {visible_counts['uzun']}/{stats['uzun_isler']} | "
            f"Birleşik: {visible_counts['birlesik']} | "
            f"Yükleme: {stats['yukleme_gecmisi']}"
        )
    
    def on_search_changed(self):
        """Arama değişti"""
        jcl_text = self.search_panel.jcl_search.text().strip()
        if jcl_text:
            app_logger.info(f"Arama yapildi: {jcl_text}")
        self.refresh_all()
    
    def on_filter_changed(self):
        """Filtre değişti"""
        self.refresh_all()
    
    def clear_filters(self):
        """Filtreleri temizle"""
        self.search_panel.clear_filters()
        self.advanced_filters = {
            'tarih_baslangic': None,
            'tarih_bitis': None,
            'hatali_min': None,
            'hatali_max': None,
            'uzun_min': None,
            'uzun_max': None
        }
        self.refresh_all()
        self.status_label.setText("✅ Filtreler temizlendi")
    
    def refresh_all(self):
        """Tüm tabloları yenile"""
        filters = self.search_panel.get_filters()
        self.table_manager.load_all_tables(filters)
        self.update_stats()
        self.status_label.setText("✅ Tablolar yenilendi")
    
    def load_excel(self):
        """Excel dosyası yükle - Senkron (Thread yok, SQLite uyumlu)"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Excel Dosyası Seç", "Data/Excel", 
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not files:
            return
        
        app_logger.info(f"Excel yükleme başlatıldı: {len(files)} dosya seçildi")
        
        # Progress bar göster
        self.progress.setVisible(True)
        self.progress.setMaximum(len(files))
        self.progress.setValue(0)
        self.status_label.setText("⏳ Excel dosyaları yükleniyor...")
        
        # Butonları devre dışı bırak
        self.btn_load.setEnabled(False)
        QApplication.processEvents()
        
        total_kayit = 0
        errors = []
        
        for idx, file_path in enumerate(files):
            try:
                file_name = os.path.basename(file_path)
                app_logger.info(f"Yükleniyor: {file_name}")
                
                self.progress.setValue(idx + 1)
                self.progress.setFormat(f"Yükleniyor: {file_name} ({idx + 1}/{len(files)})")
                QApplication.processEvents()  # UI'yı responsive tut
                
                reader = ExcelReader(file_path)
                kayitlar, hata = reader.read_all_sheets()
                
                if hata:
                    errors.append(f"{os.path.basename(file_path)}: {hata}")
                    continue
                
                for kayit in kayitlar:
                    if reader.rapor_tipi == 'HATALI':
                        self.db_manager.insert_hatali_is(kayit)
                    elif reader.rapor_tipi == 'UZUN':
                        self.db_manager.insert_uzun_is(kayit)
                
                total_kayit += len(kayitlar)
                
                self.db_manager.insert_yukleme_gecmisi({
                    'dosya_adi': reader.file_name,
                    'kayit_sayisi': len(kayitlar),
                    'durum': 'BASARILI'
                })
                
                app_logger.info(f"{file_name}: {len(kayitlar)} kayit eklendi")
                
            except Exception as e:
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        
        # Progress bar gizle
        self.progress.setVisible(False)
        self.btn_load.setEnabled(True)
        
        # Tabloları güncelle
        self.populate_filters()
        self.refresh_all()
        
        # Hata mesajları
        if errors:
            error_msg = "\n".join(errors[:5])
            if len(errors) > 5:
                error_msg += f"\n... ve {len(errors) - 5} hata daha"
            QMessageBox.warning(
                self, "Uyarılar",
                f"Bazı dosyalar yüklenemedi:\n\n{error_msg}"
            )
        
        # Başarı mesajı
        if total_kayit > 0:
            app_logger.info(f"Excel yukleme tamamlandi: {total_kayit} kayit eklendi")
            QMessageBox.information(
                self, "Başarılı", 
                f"✅ Toplam {total_kayit} kayıt eklendi/güncellendi!"
            )
            self.status_label.setText(f"✅ {total_kayit} kayıt yüklendi")
        else:
            app_logger.warning("Excel yukleme: Hic kayit eklenemedi")
            self.status_label.setText("⚠️ Hiç kayıt yüklenemedi")
    
    def export_to_excel(self):
        """Excel'e aktar"""
        current_tab = self.table_manager.tabs.currentIndex()
        
        if current_tab == 0:
            table = self.table_manager.hatali_table
            default_name = "hatali_isler"
        elif current_tab == 1:
            table = self.table_manager.uzun_table
            default_name = "uzun_isler"
        else:
            table = self.table_manager.birlesik_table
            default_name = "birlesik_gorunum"
        
        self.dialog_manager.show_export_dialog(table, default_name)
    
    def clear_database(self):
        """Veritabanını temizle"""
        reply = QMessageBox.question(
            self, "⚠️ Onay", 
            "Tüm veritabanını temizlemek istediğinize emin misiniz?\n\n"
            "Bu işlem geri alınamaz!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # İkinci onay
            reply2 = QMessageBox.warning(
                self, "⚠️ Son Onay",
                "SON UYARI: Tüm veriler silinecek!\n\nDevam edilsin mi?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply2 == QMessageBox.Yes:
                app_logger.warning("Veritabani temizleniyor...")
                cursor = self.db_manager.connection.cursor()
                cursor.execute("DELETE FROM hatali_isler")
                cursor.execute("DELETE FROM uzun_isler")
                cursor.execute("DELETE FROM yukleme_gecmisi")
                self.db_manager.connection.commit()
                
                app_logger.info("Veritabani basariyla temizlendi")
                self.populate_filters()
                self.refresh_all()
                QMessageBox.information(self, "✅ Başarılı", "Veritabanı temizlendi!")
                self.status_label.setText("✅ Veritabanı temizlendi")
    
    # Dialog metodları - DialogManager'a yönlendir
    def show_bulk_search(self):
        """Toplu arama dialogu"""
        self.dialog_manager.show_bulk_search()
    
    def show_advanced_filters(self):
        """Gelişmiş filtreler dialogu"""
        self.dialog_manager.show_advanced_filters()
    
    def show_statistics(self):
        """İstatistikler dialogu"""
        self.dialog_manager.show_statistics()
    
    def show_settings(self):
        """Ayarlar dialogu"""
        self.dialog_manager.show_settings()
    
    def show_logs(self):
        """Log görüntüleyici dialogu"""
        self.dialog_manager.show_logs()
    
    def create_backup_dialog(self):
        """Yedek oluştur dialogu"""
        self.dialog_manager.create_backup_dialog()
    
    def restore_backup_dialog(self):
        """Yedekten geri yükle dialogu"""
        self.dialog_manager.restore_backup_dialog()
    
    def show_user_guide(self):
        """Kullanım kılavuzu"""
        self.dialog_manager.show_user_guide()
    
    def show_about(self):
        """Hakkında dialogu"""
        self.dialog_manager.show_about()
    
    def change_theme(self, theme_name):
        """Tema değiştir"""
        app_logger.info(f"Tema değiştiriliyor: {theme_name}")
        self.apply_theme(theme_name)
        self.preferences.set('theme', theme_name)
        self.status_label.setText(f"✅ Tema değiştirildi: {theme_name}")
    
    def apply_theme(self, theme_name):
        """Tema uygula"""
        try:
            from .themes import get_theme_stylesheet
            
            stylesheet = get_theme_stylesheet(theme_name)
            self.setStyleSheet(stylesheet)
        except Exception as e:
            print(f"Tema uygulama hatası: {e}")
    
    def optimize_database(self):
        """Veritabanını optimize et"""
        reply = QMessageBox.question(
            self, "Optimizasyon",
            "Veritabanı optimize edilsin mi?\n\n"
            "Bu işlem birkaç saniye sürebilir.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.status_label.setText("⏳ Optimize ediliyor...")
            QApplication.processEvents()
            
            try:
                self.db_manager.optimize_database()
                QMessageBox.information(self, "Başarılı", "✅ Veritabanı optimize edildi!")
                self.status_label.setText("✅ Optimize tamamlandı")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Optimizasyon hatası: {e}")
                self.status_label.setText("❌ Optimizasyon hatası")
    
    def auto_backup_check(self):
        """Otomatik yedekleme kontrolü"""
        reply = QMessageBox.question(
            self, "Otomatik Yedekleme",
            "Düzenli yedekleme zamanı geldi.\n\n"
            "Şimdi yedek oluşturulsun mu?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, result = self.backup_manager.create_backup('Otomatik yedek')
            if success:
                self.preferences.update_backup_time()
                QMessageBox.information(self, "Başarılı", f"✅ Yedek oluşturuldu:\n{result}")
    
    def create_log_panel(self):
        """Log görüntüleyici paneli oluştur"""
        from PyQt5.QtWidgets import QTextEdit, QGroupBox
        
        log_group = QGroupBox("📋 Canlı Log Görüntüleyici")
        log_layout = QVBoxLayout(log_group)
        
        # Log text alanı
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: Consolas, monospace;
                font-size: 11px;
                border: 1px solid #3c3c3c;
                line-height: 1.4;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        # Log kontrol butonları
        btn_layout = QHBoxLayout()
        
        btn_clear_log = QPushButton("🗑️ Temizle")
        btn_clear_log.clicked.connect(lambda: self.log_text.clear())
        btn_clear_log.setMaximumWidth(100)
        
        btn_refresh_log = QPushButton("🔄 Yenile")
        btn_refresh_log.clicked.connect(self.update_log_panel)
        btn_refresh_log.setMaximumWidth(100)
        
        btn_layout.addWidget(btn_clear_log)
        btn_layout.addWidget(btn_refresh_log)
        btn_layout.addStretch()
        
        log_layout.addLayout(btn_layout)
        
        # Log otomatik güncelleme timer'ı (gerçek zamanlı için hızlı güncelleme)
        self.log_timer = QTimer(self)
        self.log_timer.timeout.connect(self.update_log_panel)
        self.log_timer.start(500)  # Her 0.5 saniyede bir güncelle (senkron akış)
        
        # İlk güncelleme
        self.update_log_panel()
        
        return log_group
    
    def update_log_panel(self):
        """Log panelini güncelle - Dialog ile aynı"""
        try:
            # Log dosyasını oku (dialog ile aynı yol)
            log_file = os.path.join("logs", "app.log")
            
            if not os.path.exists(log_file):
                # Log dosyası yoksa bilgi göster
                self.log_text.setHtml(
                    '<div style="font-family: Consolas, monospace; font-size: 12px; color: #FF9800;">'
                    '<p>⚠️ Log dosyası henüz oluşturulmamış</p>'
                    '<p>Uygulama işlemlerini yapmaya başladığınızda loglar burada görünecek</p>'
                    '</div>'
                )
                return
            
            # Log dosyasını oku (son 50 satır - en yeni en altta)
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_lines = lines[-50:] if len(lines) > 50 else lines
                # Ters çevirme - en eski üstte, en yeni altta (doğal sıra)
                # last_lines zaten kronolojik sırada gelir
                
                # Renklendirme için HTML (dialog ile aynı)
                html_content = '<div style="font-family: Consolas, monospace; font-size: 12px;">'
                for line in last_lines:  # Sıra değişmedi - en yeni en altta
                    line = line.strip()
                    if '[ERROR]' in line:
                        html_content += f'<p style="color: #ff6b6b; margin: 2px;">{line}</p>'
                    elif '[WARNING]' in line:
                        html_content += f'<p style="color: #ffa500; margin: 2px;">{line}</p>'
                    elif '[INFO]' in line:
                        html_content += f'<p style="color: #51cf66; margin: 2px;">{line}</p>'
                    else:
                        html_content += f'<p style="color: #d4d4d4; margin: 2px;">{line}</p>'
                html_content += '</div>'
                
                # Scroll pozisyonunu koru
                scrollbar = self.log_text.verticalScrollBar()
                was_at_bottom = scrollbar.value() >= scrollbar.maximum() - 10
                
                self.log_text.setHtml(html_content)
                
                # En alta scroll et (en yeni loglar en altta)
                if was_at_bottom:
                    scrollbar.setValue(scrollbar.maximum())
                    
        except Exception as e:
            # Hata durumunda bilgi göster
            self.log_text.setHtml(
                f'<div style="font-family: Consolas; font-size: 12px; color: #f44336;">'
                f'<p>❌ Log okuma hatası: {str(e)}</p>'
                '</div>'
            )
    
    def show_context_menu(self, pos, table):
        """Sağ tık menüsü"""
        from PyQt5.QtWidgets import QMenu, QAction
        
        # Tablo boşsa menü gösterme
        if table.rowCount() == 0:
            return
        
        menu = QMenu(self)
        
        refresh_action = QAction("🔄 Yenile", self)
        refresh_action.triggered.connect(self.refresh_all)
        menu.addAction(refresh_action)
        
        menu.exec_(table.viewport().mapToGlobal(pos))
    
    def closeEvent(self, event):
        """Pencere kapatılırken"""
        self.save_preferences()
        self.db_manager.disconnect()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())