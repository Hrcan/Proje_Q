"""
Ana GUI - Proje_Q JCL Veri Yönetim Sistemi
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QFileDialog, QMessageBox, QProgressBar,
                             QLineEdit, QComboBox, QGroupBox, QCheckBox, QDateEdit,
                             QSplitter, QFrame)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont

from database.db_manager import DatabaseManager
from utils.excel_reader import ExcelReader


class MainWindow(QMainWindow):
    """Ana Uygulama Penceresi"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.init_database()
        
    def init_ui(self):
        """Arayüzü oluştur"""
        self.setWindowTitle("Proje_Q - JCL Veri Yönetim Sistemi")
        self.setGeometry(100, 50, 1800, 900)
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Başlık
        self.create_header(main_layout)
        
        # Splitter (Arama + Tablo)
        splitter = QSplitter(Qt.Vertical)
        
        # Arama ve Filtreleme Bölümü
        search_widget = self.create_search_section()
        splitter.addWidget(search_widget)
        
        # Tablo Bölümü
        table_widget = self.create_table_section()
        splitter.addWidget(table_widget)
        
        # Splitter oranları
        splitter.setStretchFactor(0, 1)  # Arama bölümü
        splitter.setStretchFactor(1, 4)  # Tablo bölümü
        
        main_layout.addWidget(splitter)
        
        # Alt Bölüm (İstatistikler + Butonlar)
        self.create_footer(main_layout)
        
    def create_header(self, layout):
        """Başlık oluştur"""
        header = QLabel("JCL VERİ YÖNETİM SİSTEMİ")
        header.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                padding: 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2196F3, stop:1 #4CAF50);
                color: white;
                border-radius: 5px;
            }
        """)
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
    
    def create_search_section(self):
        """Arama ve Filtreleme Bölümü"""
        search_group = QGroupBox("Arama ve Filtreleme")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2196F3;
                border-radius: 5px;
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
        self.jcl_search.setPlaceholderText("JCL adı girin (örn: PKRBI330) - çoklu için virgülle ayırın")
        self.jcl_search.textChanged.connect(self.on_search_changed)
        
        row1.addWidget(jcl_label)
        row1.addWidget(self.jcl_search)
        
        # Satır 2: Ekip ve Ay Filtreleme
        row2 = QHBoxLayout()
        
        # Ekip Filtreleme
        ekip_label = QLabel("Ekip:")
        ekip_label.setFixedWidth(100)
        self.ekip_combo = QComboBox()
        self.ekip_combo.addItem("Tümü")
        self.ekip_combo.currentTextChanged.connect(self.on_filter_changed)
        
        # Ay Filtreleme
        ay_label = QLabel("Ay:")
        ay_label.setFixedWidth(100)
        self.ay_combo = QComboBox()
        self.ay_combo.addItem("Tümü")
        self.ay_combo.currentTextChanged.connect(self.on_filter_changed)
        
        row2.addWidget(ekip_label)
        row2.addWidget(self.ekip_combo, 1)
        row2.addWidget(ay_label)
        row2.addWidget(self.ay_combo, 1)
        
        # Satır 3: Rapor Tipi ve Hızlı Butonlar
        row3 = QHBoxLayout()
        
        # Rapor Tipi Checkboxlar
        self.cb_hatali = QCheckBox("Hatalı İşler")
        self.cb_hatali.setChecked(True)
        self.cb_hatali.stateChanged.connect(self.on_filter_changed)
        
        self.cb_uzun = QCheckBox("Uzun İşler")
        self.cb_uzun.setChecked(True)
        self.cb_uzun.stateChanged.connect(self.on_filter_changed)
        
        # Hızlı Butonlar
        self.btn_clear_filter = QPushButton("Filtreleri Temizle")
        self.btn_clear_filter.clicked.connect(self.clear_filters)
        self.btn_clear_filter.setStyleSheet("""
            QPushButton {
                padding: 5px 15px;
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        row3.addWidget(self.cb_hatali)
        row3.addWidget(self.cb_uzun)
        row3.addStretch()
        row3.addWidget(self.btn_clear_filter)
        
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        
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
        self.hatali_table = QTableWidget()
        self.hatali_table.setAlternatingRowColors(True)
        self.hatali_table.setSortingEnabled(True)  # Sıralama aktif
        self.hatali_table.setSelectionBehavior(QTableWidget.SelectRows)  # Satır seçimi
        self.hatali_table.setContextMenuPolicy(Qt.CustomContextMenu)  # Sağ tık menü
        self.hatali_table.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.hatali_table, 'hatali'))
        self.hatali_table.setStyleSheet("""
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
                cursor: pointer;
            }
        """)
        self.tabs.addTab(self.hatali_table, "HATALI İŞLER")
        
        # Tab 2: Uzun İşler
        self.uzun_table = QTableWidget()
        self.uzun_table.setAlternatingRowColors(True)
        self.uzun_table.setSortingEnabled(True)  # Sıralama aktif
        self.uzun_table.setSelectionBehavior(QTableWidget.SelectRows)  # Satır seçimi
        self.uzun_table.setContextMenuPolicy(Qt.CustomContextMenu)  # Sağ tık menü
        self.uzun_table.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.uzun_table, 'uzun'))
        self.uzun_table.setStyleSheet(self.hatali_table.styleSheet())
        self.tabs.addTab(self.uzun_table, "UZUN SÜREN İŞLER")
        
        # Tab 3: Birleşik Görünüm
        self.birlesik_table = QTableWidget()
        self.birlesik_table.setAlternatingRowColors(True)
        self.birlesik_table.setSortingEnabled(True)  # Sıralama aktif
        self.birlesik_table.setSelectionBehavior(QTableWidget.SelectRows)  # Satır seçimi
        self.birlesik_table.setContextMenuPolicy(Qt.CustomContextMenu)  # Sağ tık menü
        self.birlesik_table.customContextMenuRequested.connect(lambda pos: self.show_context_menu(pos, self.birlesik_table, 'birlesik'))
        self.birlesik_table.setStyleSheet(self.hatali_table.styleSheet())
        self.tabs.addTab(self.birlesik_table, "BİRLEŞİK GÖRÜNÜM")
        
        layout.addWidget(self.tabs)
        return table_widget
    
    def create_footer(self, layout):
        """Alt bölüm (İstatistikler + Butonlar)"""
        footer = QHBoxLayout()
        
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
        footer.addWidget(self.stats_label, 1)
        
        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMaximumHeight(25)
        
        # Butonlar
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        self.btn_load = QPushButton("📁 Excel Yükle")
        self.btn_load.clicked.connect(self.load_excel)
        self.btn_load.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                font-size: 13px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.btn_refresh = QPushButton("🔄 Yenile")
        self.btn_refresh.clicked.connect(self.refresh_all)
        self.btn_refresh.setStyleSheet(self.btn_load.styleSheet().replace("#2196F3", "#4CAF50").replace("#1976D2", "#388E3C"))
        
        self.btn_export = QPushButton("📊 Excel'e Aktar")
        self.btn_export.clicked.connect(self.export_to_excel)
        self.btn_export.setStyleSheet(self.btn_load.styleSheet().replace("#2196F3", "#FF9800").replace("#1976D2", "#F57C00"))
        
        self.btn_clear = QPushButton("🗑️ Veritabanını Temizle")
        self.btn_clear.clicked.connect(self.clear_database)
        self.btn_clear.setStyleSheet(self.btn_load.styleSheet().replace("#2196F3", "#f44336").replace("#1976D2", "#d32f2f"))
        
        btn_layout.addWidget(self.btn_load)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_export)
        btn_layout.addWidget(self.btn_clear)
        
        footer.addLayout(btn_layout)
        
        # Alt layout
        bottom = QVBoxLayout()
        bottom.addWidget(self.progress)
        bottom.addLayout(footer)
        
        layout.addLayout(bottom)
    
    def init_database(self):
        """Veritabanını başlat"""
        try:
            self.db_manager.connect()
            self.db_manager.create_tables()
            self.load_all_data()
            self.populate_filters()
            print("Veritabani hazir")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabani hatasi: {e}")
    
    def populate_filters(self):
        """Filtreleme combobox'larını doldur"""
        # Ekip listesi
        ekipler = set()
        aylar = set()
        
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
        for record in hatali_data + uzun_data:
            if record.get('sorumlu_ekip'):
                ekipler.add(record['sorumlu_ekip'])
            if record.get('ay'):
                aylar.add(record['ay'])
        
        # Ekip combobox
        self.ekip_combo.clear()
        self.ekip_combo.addItem("Tümü")
        for ekip in sorted(ekipler):
            self.ekip_combo.addItem(ekip)
        
        # Ay combobox
        self.ay_combo.clear()
        self.ay_combo.addItem("Tümü")
        for ay in sorted(aylar, reverse=True):
            self.ay_combo.addItem(ay)
    
    def load_all_data(self):
        """Tüm verileri yükle"""
        self.load_hatali_table()
        self.load_uzun_table()
        self.load_birlesik_table()
        self.update_stats()
    
    def apply_filters(self, data):
        """Filtreleri uygula"""
        # JCL arama
        jcl_text = self.jcl_search.text().strip()
        if jcl_text:
            jcl_list = [j.strip().upper() for j in jcl_text.split(',')]
            data = [r for r in data if any(jcl in r['jcl_adi'].upper() for jcl in jcl_list)]
        
        # Ekip filtresi
        ekip = self.ekip_combo.currentText()
        if ekip != "Tümü":
            data = [r for r in data if r.get('sorumlu_ekip') == ekip]
        
        # Ay filtresi
        ay = self.ay_combo.currentText()
        if ay != "Tümü":
            data = [r for r in data if r.get('ay') == ay]
        
        return data
    
    def load_hatali_table(self):
        """Hatalı işler tablosunu yükle"""
        if not self.cb_hatali.isChecked():
            self.hatali_table.setRowCount(0)
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
        """Birleşik görünüm - JCL bazlı"""
        hatali_data = self.db_manager.get_all_hatali_isler() if self.cb_hatali.isChecked() else []
        uzun_data = self.db_manager.get_all_uzun_isler() if self.cb_uzun.isChecked() else []
        
        # Filtreleri uygula
        hatali_data = self.apply_filters(hatali_data)
        uzun_data = self.apply_filters(uzun_data)
        
        # JCL + Ay bazında grupla
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
            # JCL ve Ay
            self.birlesik_table.setItem(row_idx, 0, QTableWidgetItem(item['jcl_adi']))
            self.birlesik_table.setItem(row_idx, 1, QTableWidgetItem(item['ay']))
            
            # Hatalı
            if item['hatali_kayitlar']:
                sheets_h = ', '.join(set([r['sheet_adi'] for r in item['hatali_kayitlar']]))
                ekipler_h = ', '.join(set([r['sorumlu_ekip'] for r in item['hatali_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 2, QTableWidgetItem(sheets_h))
                self.birlesik_table.setItem(row_idx, 3, QTableWidgetItem(ekipler_h))
            
            # Uzun
            if item['uzun_kayitlar']:
                sheets_u = ', '.join(set([r['sheet_adi'] for r in item['uzun_kayitlar']]))
                ekipler_u = ', '.join(set([r['sorumlu_ekip'] for r in item['uzun_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 4, QTableWidgetItem(sheets_u))
                self.birlesik_table.setItem(row_idx, 5, QTableWidgetItem(ekipler_u))
            
            # Durum
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
        
        # Görünen kayıt sayıları
        hatali_visible = self.hatali_table.rowCount()
        uzun_visible = self.uzun_table.rowCount()
        birlesik_visible = self.birlesik_table.rowCount()
        
        self.stats_label.setText(
            f"📊 İstatistikler: "
            f"Hatalı İşler: {hatali_visible}/{stats['hatali_isler']} | "
            f"Uzun Süren İşler: {uzun_visible}/{stats['uzun_isler']} | "
            f"Birleşik: {birlesik_visible} | "
            f"Yükleme Sayısı: {stats['yukleme_gecmisi']}"
        )
    
    def on_search_changed(self):
        """Arama değiştiğinde"""
        self.refresh_all()
    
    def on_filter_changed(self):
        """Filtre değiştiğinde"""
        self.refresh_all()
    
    def clear_filters(self):
        """Filtreleri temizle"""
        self.jcl_search.clear()
        self.ekip_combo.setCurrentIndex(0)
        self.ay_combo.setCurrentIndex(0)
        self.cb_hatali.setChecked(True)
        self.cb_uzun.setChecked(True)
    
    def refresh_all(self):
        """Tüm tabloları yenile"""
        self.load_hatali_table()
        self.load_uzun_table()
        self.load_birlesik_table()
        self.update_stats()
    
    def load_excel(self):
        """Excel dosyası yükle"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Excel Dosyası Seç", "Data/Excel", 
            "Excel Files (*.xlsx *.xls)"
        )
        
        if not files:
            return
        
        self.progress.setVisible(True)
        self.progress.setMaximum(len(files))
        
        total_kayit = 0
        
        for idx, file_path in enumerate(files):
            try:
                reader = ExcelReader(file_path)
                kayitlar, hata = reader.read_all_sheets()
                
                if hata:
                    QMessageBox.warning(self, "Uyarı", f"Dosya okuma hatası: {hata}")
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
                
                self.progress.setValue(idx + 1)
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya yükleme hatası: {e}")
        
        self.progress.setVisible(False)
        self.populate_filters()
        self.refresh_all()
        
        QMessageBox.information(
            self, "Başarılı", 
            f"{len(files)} dosya başarıyla yüklendi!\n"
            f"Toplam {total_kayit} kayıt eklendi/güncellendi."
        )
    
    def export_to_excel(self):
        """Mevcut görünümü Excel'e aktar"""
        # Hangi tab aktif?
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
        
        # Tüm kolon başlıklarını al
        all_headers = []
        for col in range(table.columnCount()):
            all_headers.append(table.horizontalHeaderItem(col).text())
        
        # Kolon seçim dialogu göster
        selected_columns = self.show_column_selection_dialog(all_headers)
        
        if not selected_columns:
            return  # Kullanıcı iptal etti veya kolon seçmedi
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Excel Olarak Kaydet", 
            f"{default_name}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return
        
        try:
            import pandas as pd
            
            # Seçili kolonların index'lerini bul
            selected_indices = [all_headers.index(col) for col in selected_columns]
            
            # Tablo verilerini al (sadece seçili kolonlar)
            data = []
            for row in range(table.rowCount()):
                row_data = []
                for col_idx in selected_indices:
                    item = table.item(row, col_idx)
                    row_data.append(item.text() if item else '')
                data.append(row_data)
            
            # DataFrame oluştur ve kaydet
            df = pd.DataFrame(data, columns=selected_columns)
            df.to_excel(file_path, index=False, sheet_name='Veri')
            
            QMessageBox.information(
                self, "Başarılı", 
                f"✅ Veri başarıyla kaydedildi!\n\n"
                f"📁 Dosya: {file_path}\n"
                f"📊 Satır: {len(df)}\n"
                f"📋 Kolon: {len(selected_columns)}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Excel export hatası: {e}")
    
    def show_column_selection_dialog(self, all_columns):
        """Kolon seçim dialogu göster"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel, QScrollArea, QWidget
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Kolonları Seç")
        dialog.setModal(True)
        dialog.setMinimumWidth(500)
        dialog.setMinimumHeight(400)
        
        layout = QVBoxLayout(dialog)
        
        # Başlık
        title = QLabel("📋 Excel'e aktarılacak kolonları seçin:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Hızlı seçim butonları
        quick_select = QHBoxLayout()
        
        btn_all = QPushButton("✅ Tümünü Seç")
        btn_all.setStyleSheet("padding: 5px 10px;")
        
        btn_none = QPushButton("❌ Hiçbirini Seçme")
        btn_none.setStyleSheet("padding: 5px 10px;")
        
        btn_important = QPushButton("⭐ Önemli Kolonlar")
        btn_important.setStyleSheet("padding: 5px 10px;")
        
        quick_select.addWidget(btn_all)
        quick_select.addWidget(btn_none)
        quick_select.addWidget(btn_important)
        quick_select.addStretch()
        
        layout.addLayout(quick_select)
        
        # Scroll area için checkbox'lar
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        checkboxes = {}
        
        # Önemli kolonlar listesi (ID, tarihler hariç)
        important_cols = {'JCL Adı', 'Ay', 'Sheet', 'Sorumlu Ekip', 
                         'Hatalı Sayı (Ay)', 'Son Hatalı Tarih', 'Hatalı Sayı (Yıl)',
                         'Çalışma Sayısı', 'Çalışma Süresi',
                         'Hatalı Sheets', 'Hatalı Ekipler', 'Uzun Sheets', 'Uzun Ekipler', 'Durum'}
        
        for col in all_columns:
            cb = QCheckBox(col)
            cb.setStyleSheet("padding: 5px;")
            
            # Önemli kolonları başlangıçta seçili yap
            if col in important_cols:
                cb.setChecked(True)
            
            checkboxes[col] = cb
            scroll_layout.addWidget(cb)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Hızlı seçim buton fonksiyonları
        def select_all():
            for cb in checkboxes.values():
                cb.setChecked(True)
        
        def select_none():
            for cb in checkboxes.values():
                cb.setChecked(False)
        
        def select_important():
            for col, cb in checkboxes.items():
                cb.setChecked(col in important_cols)
        
        btn_all.clicked.connect(select_all)
        btn_none.clicked.connect(select_none)
        btn_important.clicked.connect(select_important)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        
        btn_ok = QPushButton("✅ Tamam")
        btn_ok.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        btn_cancel = QPushButton("❌ İptal")
        btn_cancel.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        btn_ok.clicked.connect(dialog.accept)
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_ok)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        
        # Dialog'u göster
        if dialog.exec_() == QDialog.Accepted:
            # Seçili kolonları döndür
            selected = [col for col, cb in checkboxes.items() if cb.isChecked()]
            if not selected:
                QMessageBox.warning(self, "Uyarı", "Hiç kolon seçmediniz!")
                return None
            return selected
        else:
            return None
    
    def clear_database(self):
        """Veritabanını temizle"""
        reply = QMessageBox.question(
            self, "Onay", 
            "Tüm veritabanını temizlemek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("DELETE FROM hatali_isler")
            cursor.execute("DELETE FROM uzun_isler")
            cursor.execute("DELETE FROM yukleme_gecmisi")
            self.db_manager.connection.commit()
            
            self.populate_filters()
            self.refresh_all()
            QMessageBox.information(self, "Başarılı", "Veritabanı temizlendi!")
    
    def show_context_menu(self, pos, table, table_type):
        """Sağ tık menüsü göster"""
        from PyQt5.QtWidgets import QMenu, QAction
        
        # Seçili satır var mı kontrol et
        if table.rowCount() == 0:
            return
        
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #ccc;
            }
            QMenu::item {
                padding: 8px 25px;
            }
            QMenu::item:selected {
                background-color: #2196F3;
                color: white;
            }
        """)
        
        # Düzenle
        if table_type != 'birlesik':
            edit_action = QAction("✏️ Düzenle", self)
            edit_action.triggered.connect(lambda: self.edit_record(table, table_type))
            menu.addAction(edit_action)
        
        # Sil
        delete_action = QAction("🗑️ Sil", self)
        delete_action.triggered.connect(lambda: self.delete_records(table, table_type))
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        # Kopyala (ID)
        copy_action = QAction("📋 ID'yi Kopyala", self)
        copy_action.triggered.connect(lambda: self.copy_id(table))
        menu.addAction(copy_action)
        
        # Yenile
        refresh_action = QAction("🔄 Yenile", self)
        refresh_action.triggered.connect(self.refresh_all)
        menu.addAction(refresh_action)
        
        # Menüyü göster
        menu.exec_(table.viewport().mapToGlobal(pos))
    
    def edit_record(self, table, table_type):
        """Kayıt düzenle"""
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen düzenlemek için bir satır seçin!")
            return
        
        if len(selected_rows) > 1:
            QMessageBox.warning(self, "Uyarı", "Aynı anda sadece bir kayıt düzenleyebilirsiniz!")
            return
        
        row = selected_rows[0].row()
        record_id = int(table.item(row, 0).text())
        
        # Düzenleme dialogunu aç
        self.show_edit_dialog(record_id, table_type)
    
    def show_edit_dialog(self, record_id, table_type):
        """Düzenleme dialogu göster"""
        from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox
        
        # Kayıt bilgilerini al
        if table_type == 'hatali':
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SELECT * FROM hatali_isler WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            if not record:
                return
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Kayıt Düzenle - ID: {record_id}")
            dialog.setMinimumWidth(500)
            
            layout = QFormLayout()
            
            # Düzenlenebilir alanlar
            jcl_edit = QLineEdit(record[1])  # jcl_adi
            ay_edit = QLineEdit(record[2])  # ay
            sheet_edit = QLineEdit(record[3])  # sheet_adi
            hatali_ay_edit = QLineEdit(str(record[4] or ''))  # hatali_sayi_ay
            tarih_edit = QLineEdit(str(record[5] or ''))  # son_hatali_tarih
            hatali_yil_edit = QLineEdit(str(record[6] or ''))  # hatali_sayi_yil
            ekip_edit = QLineEdit(record[7] or '')  # sorumlu_ekip
            
            layout.addRow("JCL Adı:", jcl_edit)
            layout.addRow("Ay:", ay_edit)
            layout.addRow("Sheet:", sheet_edit)
            layout.addRow("Hatalı Sayı (Ay):", hatali_ay_edit)
            layout.addRow("Son Hatalı Tarih:", tarih_edit)
            layout.addRow("Hatalı Sayı (Yıl):", hatali_yil_edit)
            layout.addRow("Sorumlu Ekip:", ekip_edit)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            dialog.setLayout(layout)
            
            if dialog.exec_() == QDialog.Accepted:
                # Güncelleme yap
                try:
                    cursor.execute("""
                        UPDATE hatali_isler 
                        SET jcl_adi=?, ay=?, sheet_adi=?, hatali_sayi_ay=?, 
                            son_hatali_tarih=?, hatali_sayi_yil=?, sorumlu_ekip=?,
                            guncelleme_tarihi=CURRENT_TIMESTAMP
                        WHERE id=?
                    """, (jcl_edit.text(), ay_edit.text(), sheet_edit.text(),
                          int(hatali_ay_edit.text()) if hatali_ay_edit.text() else None,
                          tarih_edit.text() if tarih_edit.text() else None,
                          int(hatali_yil_edit.text()) if hatali_yil_edit.text() else None,
                          ekip_edit.text(), record_id))
                    self.db_manager.connection.commit()
                    self.refresh_all()
                    QMessageBox.information(self, "Başarılı", "Kayıt güncellendi!")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {e}")
        
        elif table_type == 'uzun':
            cursor = self.db_manager.connection.cursor()
            cursor.execute("SELECT * FROM uzun_isler WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            if not record:
                return
            
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Kayıt Düzenle - ID: {record_id}")
            dialog.setMinimumWidth(500)
            
            layout = QFormLayout()
            
            # Düzenlenebilir alanlar
            jcl_edit = QLineEdit(record[1])  # jcl_adi
            ay_edit = QLineEdit(record[2])  # ay
            sheet_edit = QLineEdit(record[3])  # sheet_adi
            sayi_edit = QLineEdit(str(record[4] or ''))  # calisma_sayisi
            sure_edit = QLineEdit(str(record[5] or ''))  # calisma_suresi
            ekip_edit = QLineEdit(record[6] or '')  # sorumlu_ekip
            
            layout.addRow("JCL Adı:", jcl_edit)
            layout.addRow("Ay:", ay_edit)
            layout.addRow("Sheet:", sheet_edit)
            layout.addRow("Çalışma Sayısı:", sayi_edit)
            layout.addRow("Çalışma Süresi:", sure_edit)
            layout.addRow("Sorumlu Ekip:", ekip_edit)
            
            buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addRow(buttons)
            
            dialog.setLayout(layout)
            
            if dialog.exec_() == QDialog.Accepted:
                # Güncelleme yap
                try:
                    cursor.execute("""
                        UPDATE uzun_isler 
                        SET jcl_adi=?, ay=?, sheet_adi=?, calisma_sayisi=?, 
                            calisma_suresi=?, sorumlu_ekip=?,
                            guncelleme_tarihi=CURRENT_TIMESTAMP
                        WHERE id=?
                    """, (jcl_edit.text(), ay_edit.text(), sheet_edit.text(),
                          int(sayi_edit.text()) if sayi_edit.text() else None,
                          sure_edit.text() if sure_edit.text() else None,
                          ekip_edit.text(), record_id))
                    self.db_manager.connection.commit()
                    self.refresh_all()
                    QMessageBox.information(self, "Başarılı", "Kayıt güncellendi!")
                except Exception as e:
                    QMessageBox.critical(self, "Hata", f"Güncelleme hatası: {e}")
    
    def delete_records(self, table, table_type):
        """Seçili kayıtları sil"""
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Uyarı", "Lütfen silmek için en az bir satır seçin!")
            return
        
        # Onay al
        count = len(selected_rows)
        reply = QMessageBox.question(
            self, "Onay", 
            f"{count} kayıt silinecek. Emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Silme işlemi
        try:
            cursor = self.db_manager.connection.cursor()
            deleted_count = 0
            
            for row in selected_rows:
                record_id = int(table.item(row.row(), 0).text())
                
                if table_type == 'hatali':
                    cursor.execute("DELETE FROM hatali_isler WHERE id = ?", (record_id,))
                elif table_type == 'uzun':
                    cursor.execute("DELETE FROM uzun_isler WHERE id = ?", (record_id,))
                
                deleted_count += 1
            
            self.db_manager.connection.commit()
            self.refresh_all()
            self.populate_filters()
            
            QMessageBox.information(
                self, "Başarılı", 
                f"✅ {deleted_count} kayıt başarıyla silindi!"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Silme hatası: {e}")
    
    def copy_id(self, table):
        """Seçili satırın ID'sini kopyala"""
        selected_rows = table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        ids = []
        for row in selected_rows:
            record_id = table.item(row.row(), 0).text()
            ids.append(record_id)
        
        # Clipboard'a kopyala
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(', '.join(ids))
        
        QMessageBox.information(
            self, "Bilgi", 
            f"✅ {len(ids)} ID kopyalandı!\n{', '.join(ids)}"
        )
    
    def closeEvent(self, event):
        """Pencere kapatılırken"""
        self.db_manager.disconnect()
        event.accept()


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()