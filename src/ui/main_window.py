"""
Ana Pencere - Profesyonel GUI
Proje_Q - JCL Veri Yönetim Sistemi
"""
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QLabel, 
                             QTabWidget, QFileDialog, QMessageBox, QProgressBar,
                             QLineEdit, QComboBox, QGroupBox, QCheckBox, QSplitter,
                             QAction, QMenu, QToolBar, QStatusBar, QDialog,
                             QFormLayout, QSpinBox, QDialogButtonBox, QTextEdit,
                             QScrollArea, QDateEdit, QFrame, QApplication)
from PyQt5.QtCore import Qt, QTimer, QDate
from PyQt5.QtGui import QIcon, QColor, QFont, QPalette

# Relative imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from utils.excel_reader import ExcelReader
from utils.backup_manager import BackupManager
from config.user_preferences import UserPreferences
from utils.logger import app_logger


class MainWindow(QMainWindow):
    """Ana Uygulama Penceresi - Profesyonel GUI"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.backup_manager = BackupManager()
        self.preferences = UserPreferences('config/user_prefs.json')
        
        self.init_ui()
        self.init_database()
        self.restore_preferences()
        
        # Otomatik yedekleme kontrolü
        if self.preferences.needs_backup():
            QTimer.singleShot(1000, self.auto_backup_check)
    
    def init_ui(self):
        """Arayüzü oluştur"""
        # Pencere ayarları
        self.setWindowTitle("Proje_Q - JCL Veri Yönetim Sistemi v0.4.0")
        self.setGeometry(100, 50, 1800, 900)
        
        # Merkezi widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Menü çubuğu
        self.create_menu_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Başlık
        self.create_header(main_layout)
        
        # Splitter (Arama + Tablo)
        splitter = QSplitter(Qt.Vertical)
        
        # Arama ve Filtreleme
        search_widget = self.create_search_section()
        splitter.addWidget(search_widget)
        
        # Tablo
        table_widget = self.create_table_section()
        splitter.addWidget(table_widget)
        
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 4)
        
        main_layout.addWidget(splitter)
        
        # Alt bölüm
        self.create_footer(main_layout)
        
        # Status bar
        self.create_status_bar()
        
        # Tema uygula
        self.apply_theme(self.preferences.get('theme', 'light'))
        
        # Gelişmiş filtre değişkenleri
        self.advanced_filters = {
            'tarih_baslangic': None,
            'tarih_bitis': None,
            'hatali_min': None,
            'hatali_max': None,
            'uzun_min': None,
            'uzun_max': None
        }
    
    def create_menu_bar(self):
        """Menü çubuğu oluştur"""
        menubar = self.menuBar()
        
        # Dosya Menüsü
        file_menu = menubar.addMenu('📁 Dosya')
        
        load_action = QAction('📂 Excel Yükle...', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_excel)
        file_menu.addAction(load_action)
        
        export_action = QAction('📊 Excel\'e Aktar...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_to_excel)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        backup_action = QAction('💾 Yedek Oluştur...', self)
        backup_action.triggered.connect(self.create_backup_dialog)
        file_menu.addAction(backup_action)
        
        restore_action = QAction('📥 Yedekten Geri Yükle...', self)
        restore_action.triggered.connect(self.restore_backup_dialog)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('❌ Çıkış', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Düzenle Menüsü
        edit_menu = menubar.addMenu('✏️ Düzenle')
        
        refresh_action = QAction('🔄 Yenile', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_all)
        edit_menu.addAction(refresh_action)
        
        clear_filters_action = QAction('🧹 Filtreleri Temizle', self)
        clear_filters_action.setShortcut('Ctrl+R')
        clear_filters_action.triggered.connect(self.clear_filters)
        edit_menu.addAction(clear_filters_action)
        
        edit_menu.addSeparator()
        
        clear_db_action = QAction('🗑️ Veritabanını Temizle...', self)
        clear_db_action.triggered.connect(self.clear_database)
        edit_menu.addAction(clear_db_action)
        
        # Görünüm Menüsü
        view_menu = menubar.addMenu('👁️ Görünüm')
        
        theme_menu = view_menu.addMenu('🎨 Tema')
        
        light_theme = QAction('☀️ Açık Tema', self)
        light_theme.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_theme)
        
        dark_theme = QAction('🌙 Koyu Tema', self)
        dark_theme.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_theme)
        
        blue_theme = QAction('🔵 Mavi Tema', self)
        blue_theme.triggered.connect(lambda: self.change_theme('blue'))
        theme_menu.addAction(blue_theme)
        
        view_menu.addSeparator()
        
        stats_action = QAction('📈 İstatistikler', self)
        stats_action.triggered.connect(self.show_statistics)
        view_menu.addAction(stats_action)
        
        # Araçlar Menüsü
        tools_menu = menubar.addMenu('🔧 Araçlar')
        
        settings_action = QAction('⚙️ Ayarlar...', self)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)
        
        tools_menu.addSeparator()
        
        logs_action = QAction('📋 Logları Görüntüle...', self)
        logs_action.triggered.connect(self.show_logs)
        tools_menu.addAction(logs_action)
        
        tools_menu.addSeparator()
        
        optimize_action = QAction('⚡ Veritabanını Optimize Et', self)
        optimize_action.triggered.connect(self.optimize_database)
        tools_menu.addAction(optimize_action)
        
        # Yardım Menüsü
        help_menu = menubar.addMenu('❓ Yardım')
        
        guide_action = QAction('📖 Kullanım Kılavuzu', self)
        guide_action.setShortcut('F1')
        guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(guide_action)
        
        help_menu.addSeparator()
        
        about_action = QAction('ℹ️ Hakkında', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_toolbar(self):
        """Toolbar oluştur"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 1.5)
        self.addToolBar(toolbar)
        
        # Excel Yükle
        load_btn = QAction('📂 Yükle', self)
        load_btn.setToolTip('Excel dosyası yükle (Ctrl+O)')
        load_btn.triggered.connect(self.load_excel)
        toolbar.addAction(load_btn)
        
        # Yenile
        refresh_btn = QAction('🔄 Yenile', self)
        refresh_btn.setToolTip('Tabloları yenile (F5)')
        refresh_btn.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_btn)
        
        toolbar.addSeparator()
        
        # Excel'e Aktar
        export_btn = QAction('📊 Aktar', self)
        export_btn.setToolTip('Excel\'e aktar (Ctrl+E)')
        export_btn.triggered.connect(self.export_to_excel)
        toolbar.addAction(export_btn)
        
        # Yedek Oluştur
        backup_btn = QAction('💾 Yedekle', self)
        backup_btn.setToolTip('Veritabanı yedeği oluştur')
        backup_btn.triggered.connect(self.create_backup_dialog)
        toolbar.addAction(backup_btn)
        
        toolbar.addSeparator()
        
        # İstatistikler
        stats_btn = QAction('📈 İstatistik', self)
        stats_btn.setToolTip('İstatistikleri görüntüle')
        stats_btn.triggered.connect(self.show_statistics)
        toolbar.addAction(stats_btn)
        
        # Ayarlar
        settings_btn = QAction('⚙️ Ayarlar', self)
        settings_btn.setToolTip('Ayarları aç (Ctrl+,)')
        settings_btn.triggered.connect(self.show_settings)
        toolbar.addAction(settings_btn)
    
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
    
    def create_header(self, layout):
        """Başlık oluştur"""
        header = QLabel("🎯 JCL VERİ YÖNETİM SİSTEMİ")
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #4CAF50);
                color: white;
                border-radius: 8px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
    
    def create_search_section(self):
        """Arama ve Filtreleme Bölümü"""
        search_group = QGroupBox("🔍 Arama ve Filtreleme")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2196F3;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #2196F3;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout(search_group)
        
        # Satır 1: JCL Arama
        row1 = QHBoxLayout()
        
        jcl_label = QLabel("JCL Adı:")
        jcl_label.setFixedWidth(100)
        self.jcl_search = QLineEdit()
        self.jcl_search.setPlaceholderText("JCL adı girin (çoklu: virgül, wildcard: PONT*)")
        self.jcl_search.textChanged.connect(self.on_search_changed)
        
        row1.addWidget(jcl_label)
        row1.addWidget(self.jcl_search)
        
        # Satır 2: Ekip ve Ay
        row2 = QHBoxLayout()
        
        ekip_label = QLabel("Ekip:")
        ekip_label.setFixedWidth(100)
        self.ekip_combo = QComboBox()
        self.ekip_combo.addItem("Tümü")
        self.ekip_combo.currentTextChanged.connect(self.on_filter_changed)
        
        ay_label = QLabel("Ay:")
        ay_label.setFixedWidth(100)
        self.ay_combo = QComboBox()
        self.ay_combo.addItem("Tümü")
        self.ay_combo.currentTextChanged.connect(self.on_filter_changed)
        
        row2.addWidget(ekip_label)
        row2.addWidget(self.ekip_combo, 1)
        row2.addWidget(ay_label)
        row2.addWidget(self.ay_combo, 1)
        
        # Satır 3: Rapor Tipi
        row3 = QHBoxLayout()
        
        self.cb_hatali = QCheckBox("✅ Hatalı İşler")
        self.cb_hatali.setChecked(True)
        self.cb_hatali.stateChanged.connect(self.on_filter_changed)
        
        self.cb_uzun = QCheckBox("⏱️ Uzun İşler")
        self.cb_uzun.setChecked(True)
        self.cb_uzun.stateChanged.connect(self.on_filter_changed)
        
        row3.addWidget(self.cb_hatali)
        row3.addWidget(self.cb_uzun)
        row3.addStretch()
        
        # Satır 4: Butonlar
        row4 = QHBoxLayout()
        
        self.btn_bulk_search = QPushButton("📋 Toplu Arama")
        self.btn_bulk_search.clicked.connect(self.show_bulk_search)
        self.btn_bulk_search.setToolTip("Birden fazla JCL'yi aynı anda arayın")
        
        self.btn_advanced_filter = QPushButton("🔍 Gelişmiş Filtreler")
        self.btn_advanced_filter.clicked.connect(self.show_advanced_filters)
        
        self.btn_clear_filter = QPushButton("🧹 Filtreleri Temizle")
        self.btn_clear_filter.clicked.connect(self.clear_filters)
        
        self.advanced_filter_label = QLabel("")
        self.advanced_filter_label.setStyleSheet("color: #2196F3; font-weight: bold;")
        
        row4.addWidget(self.btn_bulk_search)
        row4.addWidget(self.btn_advanced_filter)
        row4.addWidget(self.btn_clear_filter)
        row4.addWidget(self.advanced_filter_label)
        row4.addStretch()
        
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
        
        return search_group
    
    def create_table_section(self):
        """Tablo Bölümü"""
        table_widget = QWidget()
        layout = QVBoxLayout(table_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                padding: 10px 20px;
                font-size: 12px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
            }
        """)
        
        # Tab 1: Hatalı İşler
        self.hatali_table = self.create_table()
        self.tabs.addTab(self.hatali_table, "❌ HATALI İŞLER")
        
        # Tab 2: Uzun İşler
        self.uzun_table = self.create_table()
        self.tabs.addTab(self.uzun_table, "⏱️ UZUN SÜREN İŞLER")
        
        # Tab 3: Birleşik Görünüm
        self.birlesik_table = self.create_table()
        self.tabs.addTab(self.birlesik_table, "📊 BİRLEŞİK GÖRÜNÜM")
        
        layout.addWidget(self.tabs)
        return table_widget
    
    def create_table(self):
        """Tablo oluştur"""
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(
            lambda pos, t=table: self.show_context_menu(pos, t)
        )
        table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f5f5f5;
                gridline-color: #ddd;
            }
            QHeaderView::section {
                background-color: #2196F3;
                color: white;
                padding: 5px;
                border: 1px solid #1976D2;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #1976D2;
            }
        """)
        return table
    
    def create_footer(self, layout):
        """Alt bölüm"""
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
            self.jcl_search.setText(filters.get('last_jcl', ''))
            
            ekip = filters.get('last_ekip', 'Tümü')
            index = self.ekip_combo.findText(ekip)
            if index >= 0:
                self.ekip_combo.setCurrentIndex(index)
            
            ay = filters.get('last_ay', 'Tümü')
            index = self.ay_combo.findText(ay)
            if index >= 0:
                self.ay_combo.setCurrentIndex(index)
            
            self.cb_hatali.setChecked(filters.get('cb_hatali', True))
            self.cb_uzun.setChecked(filters.get('cb_uzun', True))
    
    def save_preferences(self):
        """Tercihleri kaydet"""
        # Pencere geometrisi
        self.preferences.update_window_geometry(
            self.x(), self.y(), self.width(), self.height()
        )
        
        # Filtreleri kaydet
        self.preferences.update_filters(
            jcl=self.jcl_search.text(),
            ekip=self.ekip_combo.currentText(),
            ay=self.ay_combo.currentText(),
            hatali=self.cb_hatali.isChecked(),
            uzun=self.cb_uzun.isChecked()
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
        
        # Ekip
        current_ekip = self.ekip_combo.currentText()
        self.ekip_combo.clear()
        self.ekip_combo.addItem("Tümü")
        for ekip in sorted(ekipler):
            self.ekip_combo.addItem(ekip)
        
        index = self.ekip_combo.findText(current_ekip)
        if index >= 0:
            self.ekip_combo.setCurrentIndex(index)
        
        # Ay
        current_ay = self.ay_combo.currentText()
        self.ay_combo.clear()
        self.ay_combo.addItem("Tümü")
        for ay in sorted(aylar, reverse=True):
            self.ay_combo.addItem(ay)
        
        index = self.ay_combo.findText(current_ay)
        if index >= 0:
            self.ay_combo.setCurrentIndex(index)
    
    def load_all_data(self):
        """Tüm verileri yükle"""
        self.load_hatali_table()
        self.load_uzun_table()
        self.load_birlesik_table()
        self.update_stats()
    
    def apply_filters(self, data):
        """Filtreleri uygula"""
        # JCL arama (virgül, boşluk, satır ve wildcard (*) desteklenir)
        jcl_text = self.jcl_search.text().strip()
        if jcl_text:
            # Virgül, boşluk ve satır ile ayır
            jcl_list = []
            for line in jcl_text.split('\n'):
                parts = line.replace(',', ' ').split()
                for part in parts:
                    part = part.strip().upper()
                    if part:
                        jcl_list.append(part)
            
            if jcl_list:
                # Wildcard desteği
                filtered_data = []
                for record in data:
                    jcl_adi_upper = record['jcl_adi'].upper()
                    for jcl_pattern in jcl_list:
                        if '*' in jcl_pattern:
                            # Wildcard pattern
                            pattern_parts = jcl_pattern.split('*')
                            if len(pattern_parts) == 2:
                                prefix, suffix = pattern_parts
                                if prefix and suffix:
                                    # PONT*ABC gibi
                                    if jcl_adi_upper.startswith(prefix) and jcl_adi_upper.endswith(suffix):
                                        filtered_data.append(record)
                                        break
                                elif prefix:
                                    # PONT* gibi
                                    if jcl_adi_upper.startswith(prefix):
                                        filtered_data.append(record)
                                        break
                                elif suffix:
                                    # *ABC gibi
                                    if jcl_adi_upper.endswith(suffix):
                                        filtered_data.append(record)
                                        break
                            elif len(pattern_parts) == 1 and jcl_pattern == '*':
                                # Sadece * - tümü
                                filtered_data.append(record)
                                break
                        else:
                            # Normal arama (içinde geçmeli)
                            if jcl_pattern in jcl_adi_upper:
                                filtered_data.append(record)
                                break
                data = filtered_data
        
        # Ekip
        ekip = self.ekip_combo.currentText()
        if ekip != "Tümü":
            data = [r for r in data if r.get('sorumlu_ekip') == ekip]
        
        # Ay
        ay = self.ay_combo.currentText()
        if ay != "Tümü":
            data = [r for r in data if r.get('ay') == ay]
        
        return data
    
    def load_hatali_table(self):
        """Hatalı işler tablosunu yükle"""
        if not self.cb_hatali.isChecked():
            self.hatali_table.setRowCount(0)
            self.hatali_table.setColumnCount(0)
            return
        
        data = self.db_manager.get_all_hatali_isler()
        data = self.apply_filters(data)
        
        self.hatali_table.clear()
        self.hatali_table.setRowCount(len(data))
        self.hatali_table.setColumnCount(11)
        
        headers = ['ID', 'JCL Adı', 'Ay', 'Sheet', 'Hatalı Sayı (Ay)', 
                   'Son Hatalı Tarih', 'Hatalı Sayı (Yıl)', 'Sorumlu Ekip',
                   'Yüklenme Tarihi', 'Güncelleme Tarihi', 'Kaynak Dosya']
        self.hatali_table.setHorizontalHeaderLabels(headers)
        
        for row_idx, record in enumerate(data):
            self.hatali_table.setItem(row_idx, 0, QTableWidgetItem(str(record['id'])))
            self.hatali_table.setItem(row_idx, 1, QTableWidgetItem(record['jcl_adi']))
            self.hatali_table.setItem(row_idx, 2, QTableWidgetItem(record['ay']))
            self.hatali_table.setItem(row_idx, 3, QTableWidgetItem(record['sheet_adi']))
            self.hatali_table.setItem(row_idx, 4, QTableWidgetItem(str(record['hatali_sayi_ay'] or '')))
            self.hatali_table.setItem(row_idx, 5, QTableWidgetItem(str(record['son_hatali_tarih'] or '')))
            self.hatali_table.setItem(row_idx, 6, QTableWidgetItem(str(record['hatali_sayi_yil'] or '')))
            self.hatali_table.setItem(row_idx, 7, QTableWidgetItem(record['sorumlu_ekip'] or ''))
            self.hatali_table.setItem(row_idx, 8, QTableWidgetItem(str(record['yuklenme_tarihi'])[:19]))
            self.hatali_table.setItem(row_idx, 9, QTableWidgetItem(str(record['guncelleme_tarihi'])[:19]))
            self.hatali_table.setItem(row_idx, 10, QTableWidgetItem(record['kaynak_dosya'] or ''))
        
        self.hatali_table.resizeColumnsToContents()
    
    def load_uzun_table(self):
        """Uzun süren işler tablosunu yükle"""
        if not self.cb_uzun.isChecked():
            self.uzun_table.setRowCount(0)
            self.uzun_table.setColumnCount(0)
            return
        
        data = self.db_manager.get_all_uzun_isler()
        data = self.apply_filters(data)
        
        self.uzun_table.clear()
        self.uzun_table.setRowCount(len(data))
        self.uzun_table.setColumnCount(10)
        
        headers = ['ID', 'JCL Adı', 'Ay', 'Sheet', 'Çalışma Sayısı', 
                   'Çalışma Süresi', 'Sorumlu Ekip', 'Yüklenme Tarihi', 
                   'Güncelleme Tarihi', 'Kaynak Dosya']
        self.uzun_table.setHorizontalHeaderLabels(headers)
        
        for row_idx, record in enumerate(data):
            self.uzun_table.setItem(row_idx, 0, QTableWidgetItem(str(record['id'])))
            self.uzun_table.setItem(row_idx, 1, QTableWidgetItem(record['jcl_adi']))
            self.uzun_table.setItem(row_idx, 2, QTableWidgetItem(record['ay']))
            self.uzun_table.setItem(row_idx, 3, QTableWidgetItem(record['sheet_adi']))
            self.uzun_table.setItem(row_idx, 4, QTableWidgetItem(str(record['calisma_sayisi'] or '')))
            self.uzun_table.setItem(row_idx, 5, QTableWidgetItem(str(record['calisma_suresi'] or '')))
            self.uzun_table.setItem(row_idx, 6, QTableWidgetItem(record['sorumlu_ekip'] or ''))
            self.uzun_table.setItem(row_idx, 7, QTableWidgetItem(str(record['yuklenme_tarihi'])[:19]))
            self.uzun_table.setItem(row_idx, 8, QTableWidgetItem(str(record['guncelleme_tarihi'])[:19]))
            self.uzun_table.setItem(row_idx, 9, QTableWidgetItem(record['kaynak_dosya'] or ''))
        
        self.uzun_table.resizeColumnsToContents()
    
    def load_birlesik_table(self):
        """Birleşik görünüm"""
        hatali_data = self.db_manager.get_all_hatali_isler() if self.cb_hatali.isChecked() else []
        uzun_data = self.db_manager.get_all_uzun_isler() if self.cb_uzun.isChecked() else []
        
        hatali_data = self.apply_filters(hatali_data)
        uzun_data = self.apply_filters(uzun_data)
        
        combined = {}
        
        for record in hatali_data:
            key = (record['jcl_adi'], record['ay'])
            if key not in combined:
                combined[key] = {
                    'jcl_adi': record['jcl_adi'],
                    'ay': record['ay'],
                    'hatali_kayitlar': [],
                    'uzun_kayitlar': []
                }
            combined[key]['hatali_kayitlar'].append(record)
        
        for record in uzun_data:
            key = (record['jcl_adi'], record['ay'])
            if key not in combined:
                combined[key] = {
                    'jcl_adi': record['jcl_adi'],
                    'ay': record['ay'],
                    'hatali_kayitlar': [],
                    'uzun_kayitlar': []
                }
            combined[key]['uzun_kayitlar'].append(record)
        
        data_list = sorted(combined.values(), key=lambda x: (x['ay'], x['jcl_adi']), reverse=True)
        
        self.birlesik_table.clear()
        self.birlesik_table.setRowCount(len(data_list))
        self.birlesik_table.setColumnCount(7)
        
        headers = ['JCL Adı', 'Ay', 'Hatalı Sheets', 'Hatalı Ekipler', 
                   'Uzun Sheets', 'Uzun Ekipler', 'Durum']
        self.birlesik_table.setHorizontalHeaderLabels(headers)
        
        for row_idx, item in enumerate(data_list):
            self.birlesik_table.setItem(row_idx, 0, QTableWidgetItem(item['jcl_adi']))
            self.birlesik_table.setItem(row_idx, 1, QTableWidgetItem(item['ay']))
            
            if item['hatali_kayitlar']:
                sheets_h = ', '.join(set([r['sheet_adi'] for r in item['hatali_kayitlar']]))
                ekipler_h = ', '.join(set([r['sorumlu_ekip'] for r in item['hatali_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 2, QTableWidgetItem(sheets_h))
                self.birlesik_table.setItem(row_idx, 3, QTableWidgetItem(ekipler_h))
            
            if item['uzun_kayitlar']:
                sheets_u = ', '.join(set([r['sheet_adi'] for r in item['uzun_kayitlar']]))
                ekipler_u = ', '.join(set([r['sorumlu_ekip'] for r in item['uzun_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 4, QTableWidgetItem(sheets_u))
                self.birlesik_table.setItem(row_idx, 5, QTableWidgetItem(ekipler_u))
            
            if item['hatali_kayitlar'] and item['uzun_kayitlar']:
                durum = f"Her İkisi ({len(item['hatali_kayitlar'])}H + {len(item['uzun_kayitlar'])}U)"
                color = QColor(144, 238, 144)
            elif item['hatali_kayitlar']:
                durum = f"Sadece Hatalı ({len(item['hatali_kayitlar'])})"
                color = QColor(255, 200, 200)
            else:
                durum = f"Sadece Uzun ({len(item['uzun_kayitlar'])})"
                color = QColor(200, 220, 255)
            
            durum_item = QTableWidgetItem(durum)
            durum_item.setBackground(color)
            self.birlesik_table.setItem(row_idx, 6, durum_item)
        
        self.birlesik_table.resizeColumnsToContents()
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        stats = self.db_manager.get_tablo_istatistikleri()
        
        hatali_visible = self.hatali_table.rowCount()
        uzun_visible = self.uzun_table.rowCount()
        birlesik_visible = self.birlesik_table.rowCount()
        
        self.stats_label.setText(
            f"📊 İstatistikler: "
            f"Hatalı: {hatali_visible}/{stats['hatali_isler']} | "
            f"Uzun: {uzun_visible}/{stats['uzun_isler']} | "
            f"Birleşik: {birlesik_visible} | "
            f"Yükleme: {stats['yukleme_gecmisi']}"
        )
    
    def on_search_changed(self):
        """Arama değişti"""
        jcl_text = self.jcl_search.text().strip()
        if jcl_text:
            app_logger.info(f"Arama yapildi: {jcl_text}")
        self.refresh_all()
    
    def on_filter_changed(self):
        """Filtre değişti"""
        self.refresh_all()
    
    def clear_filters(self):
        """Filtreleri temizle"""
        self.jcl_search.clear()
        self.ekip_combo.setCurrentIndex(0)
        self.ay_combo.setCurrentIndex(0)
        self.cb_hatali.setChecked(True)
        self.cb_uzun.setChecked(True)
        self.advanced_filters = {
            'tarih_baslangic': None,
            'tarih_bitis': None,
            'hatali_min': None,
            'hatali_max': None,
            'uzun_min': None,
            'uzun_max': None
        }
        self.advanced_filter_label.setText("")
        self.status_label.setText("✅ Filtreler temizlendi")
    
    def refresh_all(self):
        """Tüm tabloları yenile"""
        self.load_hatali_table()
        self.load_uzun_table()
        self.load_birlesik_table()
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
        try:
            from .export_dialog import ExportDialog
            
            current_tab = self.tabs.currentIndex()
            
            if current_tab == 0:
                table = self.hatali_table
                default_name = "hatali_isler"
            elif current_tab == 1:
                table = self.uzun_table
                default_name = "uzun_isler"
            else:
                table = self.birlesik_table
                default_name = "birlesik_gorunum"
            
            dialog = ExportDialog(self, table, default_name)
            if dialog.exec_() == QDialog.Accepted:
                self.status_label.setText("✅ Excel export başarılı")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Export dialog hatası: {e}")
    
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
    
    def show_context_menu(self, pos, table):
        """Sağ tık menüsü"""
        # Basit sağ tık menüsü
        if table.rowCount() == 0:
            return
        
        menu = QMenu(self)
        
        refresh_action = QAction("🔄 Yenile", self)
        refresh_action.triggered.connect(self.refresh_all)
        menu.addAction(refresh_action)
        
        menu.exec_(table.viewport().mapToGlobal(pos))
    
    def show_bulk_search(self):
        """Toplu arama dialogu"""
        try:
            from .bulk_search_dialog import BulkSearchDialog
            from .bulk_search_results_dialog import BulkSearchResultsDialog
            
            dialog = BulkSearchDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                jcl_list = dialog.get_jcl_list()
                unique_jcls = list(set(jcl_list))
                
                # Tüm verilerde ara
                all_hatali = self.db_manager.get_all_hatali_isler()
                all_uzun = self.db_manager.get_all_uzun_isler()
                
                # Eşleşen kayıtları bul (wildcard desteği ile)
                hatali_results = []
                uzun_results = []
                
                for record in all_hatali:
                    jcl_adi_upper = record['jcl_adi'].upper()
                    for jcl_pattern in unique_jcls:
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
                            hatali_results.append(record)
                            break
                
                for record in all_uzun:
                    jcl_adi_upper = record['jcl_adi'].upper()
                    for jcl_pattern in unique_jcls:
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
                            uzun_results.append(record)
                            break
                
                # Sonuçları ayrı bir dialogda göster
                results_dialog = BulkSearchResultsDialog(
                    self, unique_jcls, hatali_results, uzun_results
                )
                results_dialog.exec_()
                
                # Dialog kapandıktan sonra ana arama kutusuna da yazdır
                jcl_text = ', '.join(unique_jcls)
                self.jcl_search.setText(jcl_text)
                
                # Tabloları güncelle
                self.refresh_all()
                
                # Durum güncellemesi
                total_results = len(hatali_results) + len(uzun_results)
                self.status_label.setText(
                    f"🔍 Toplu arama: {len(jcl_list)} JCL → {total_results} sonuç bulundu"
                )
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            QMessageBox.critical(self, "Hata", f"Toplu arama hatası:\n{str(e)}\n\n{error_detail}")
    
    def show_advanced_filters(self):
        """Gelişmiş filtreler dialogu"""
        try:
            from .advanced_filters_dialog import AdvancedFiltersDialog
            
            dialog = AdvancedFiltersDialog(self, self.advanced_filters)
            if dialog.exec_() == QDialog.Accepted:
                self.advanced_filters = dialog.get_filters()
                self.advanced_filter_label.setText("🔍 Gelişmiş filtre aktif")
                self.refresh_all()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Gelişmiş filtre dialog hatası: {e}")
    
    def change_theme(self, theme_name):
        """Tema değiştir"""
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
    
    def show_settings(self):
        """Ayarlar penceresi"""
        try:
            from .settings_dialog import SettingsDialog
            
            dialog = SettingsDialog(self, self.preferences)
            if dialog.exec_() == QDialog.Accepted:
                self.status_label.setText("✅ Ayarlar kaydedildi")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Ayarlar dialog hatası: {e}")
    
    def show_statistics(self):
        """İstatistikler penceresi"""
        try:
            from .statistics_dialog import StatisticsDialog
            
            dialog = StatisticsDialog(self, self.db_manager)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İstatistik dialog hatası: {e}")
    
    def show_logs(self):
        """Log görüntüleyici penceresi"""
        try:
            from .log_viewer_dialog import LogViewerDialog
            
            dialog = LogViewerDialog(self)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Log viewer hatası: {e}")
    
    def create_backup_dialog(self):
        """Yedek oluştur"""
        try:
            success, result = self.backup_manager.create_backup('Manuel yedek')
            if success:
                self.preferences.update_backup_time()
                QMessageBox.information(self, "Başarılı", f"✅ Yedek oluşturuldu:\n{result}")
                self.status_label.setText("✅ Yedek oluşturuldu")
            else:
                QMessageBox.critical(self, "Hata", f"Yedekleme hatası:\n{result}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Yedekleme hatası: {e}")
    
    def restore_backup_dialog(self):
        """Yedekten geri yükle"""
        try:
            backups = self.backup_manager.list_backups()
            if not backups:
                QMessageBox.information(self, "Bilgi", "Yedek dosyası bulunamadı.")
                return
            
            # En son yedeği seç
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Yedek Dosyası Seç", "backup",
                "Backup Files (*.zip)"
            )
            
            if file_path:
                success, message = self.backup_manager.restore_backup(file_path)
                if success:
                    self.refresh_all()
                    QMessageBox.information(self, "Başarılı", "✅ Yedek geri yüklendi!")
                    self.status_label.setText("✅ Yedek geri yüklendi")
                else:
                    QMessageBox.critical(self, "Hata", f"Geri yükleme hatası:\n{message}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Geri yükleme hatası: {e}")
    
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
    
    def show_user_guide(self):
        """Kullanım kılavuzu"""
        QMessageBox.information(
            self, "Kullanım Kılavuzu",
            "🎯 Proje_Q - JCL Veri Yönetim Sistemi\n\n"
            "📂 Excel Yükle: Data/Excel klasöründen dosya seçin\n"
            "🔍 Arama: JCL adı, ekip veya ay ile filtreleyin\n"
            "📊 Excel Export: Mevcut görünümü Excel'e aktarın\n"
            "💾 Yedekleme: Düzenli veritabanı yedekleri alın\n\n"
            "Detaylı bilgi için README.md dosyasına bakın."
        )
    
    def show_about(self):
        """Hakkında dialogu"""
        QMessageBox.about(
            self, "Hakkında",
            "🎯 <b>Proje_Q - JCL Veri Yönetim Sistemi</b><br><br>"
            "📌 Versiyon: 0.4.0<br>"
            "📅 Tarih: Mart 2026<br>"
            "👨‍💻 Geliştirici: Proje Ekibi<br><br>"
            "📝 Excel ve TXT dosyalarından JCL verilerini<br>"
            "okuyup SQLite veritabanına kaydeden,<br>"
            "yöneten ve raporlayan masaüstü uygulaması.<br><br>"
            "🔧 Teknolojiler: Python, PyQt5, SQLite, pandas"
        )
    
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