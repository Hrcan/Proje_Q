"""
Arama Paneli - Arama ve filtreleme bileşeni
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QCheckBox, QPushButton)
from PyQt5.QtCore import Qt


class SearchPanel(QGroupBox):
    """Arama ve Filtreleme Paneli"""
    
    def __init__(self, parent):
        """
        Args:
            parent: Ana pencere (MainWindow) referansı
        """
        super().__init__("🔍 Arama ve Filtreleme")
        self.parent = parent
        
        # Widget'ları oluştur
        self.create_widgets()
        self.setup_layout()
        self.apply_styling()
    
    def create_widgets(self):
        """Widget'ları oluştur"""
        # JCL Arama
        self.jcl_label = QLabel("JCL Adı:")
        self.jcl_label.setFixedWidth(100)
        self.jcl_search = QLineEdit()
        self.jcl_search.setPlaceholderText("JCL adı girin (çoklu: virgül, wildcard: PONT*)")
        
        # Ekip ComboBox
        self.ekip_label = QLabel("Ekip:")
        self.ekip_label.setFixedWidth(100)
        self.ekip_combo = QComboBox()
        self.ekip_combo.addItem("Tümü")
        
        # Ay ComboBox
        self.ay_label = QLabel("Ay:")
        self.ay_label.setFixedWidth(100)
        self.ay_combo = QComboBox()
        self.ay_combo.addItem("Tümü")
        
        # Rapor Tipi CheckBox'ları
        self.cb_hatali = QCheckBox("✅ Hatalı İşler")
        self.cb_hatali.setChecked(True)
        
        self.cb_uzun = QCheckBox("⏱️ Uzun İşler")
        self.cb_uzun.setChecked(True)
        
        # Butonlar
        self.btn_bulk_search = QPushButton("📋 Toplu Arama")
        self.btn_bulk_search.setToolTip("Birden fazla JCL'yi aynı anda arayın")
        
        self.btn_advanced_filter = QPushButton("🔍 Gelişmiş Filtreler")
        
        self.btn_clear_filter = QPushButton("🧹 Filtreleri Temizle")
        
        # Gelişmiş filtre durumu label'ı
        self.advanced_filter_label = QLabel("")
        self.advanced_filter_label.setStyleSheet("color: #2196F3; font-weight: bold;")
    
    def setup_layout(self):
        """Layout'u düzenle"""
        layout = QVBoxLayout(self)
        
        # Satır 1: JCL Arama
        row1 = QHBoxLayout()
        row1.addWidget(self.jcl_label)
        row1.addWidget(self.jcl_search)
        
        # Satır 2: Ekip ve Ay
        row2 = QHBoxLayout()
        row2.addWidget(self.ekip_label)
        row2.addWidget(self.ekip_combo, 1)
        row2.addWidget(self.ay_label)
        row2.addWidget(self.ay_combo, 1)
        
        # Satır 3: Rapor Tipi
        row3 = QHBoxLayout()
        row3.addWidget(self.cb_hatali)
        row3.addWidget(self.cb_uzun)
        row3.addStretch()
        
        # Satır 4: Butonlar
        row4 = QHBoxLayout()
        row4.addWidget(self.btn_bulk_search)
        row4.addWidget(self.btn_advanced_filter)
        row4.addWidget(self.btn_clear_filter)
        row4.addWidget(self.advanced_filter_label)
        row4.addStretch()
        
        # Tüm satırları ekle
        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        layout.addLayout(row4)
    
    def apply_styling(self):
        """Stil uygula"""
        self.setStyleSheet("""
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
    
    def connect_signals(self):
        """Sinyalleri bağla (parent tarafından çağrılır)"""
        self.jcl_search.textChanged.connect(self.parent.on_search_changed)
        self.ekip_combo.currentTextChanged.connect(self.parent.on_filter_changed)
        self.ay_combo.currentTextChanged.connect(self.parent.on_filter_changed)
        self.cb_hatali.stateChanged.connect(self.parent.on_filter_changed)
        self.cb_uzun.stateChanged.connect(self.parent.on_filter_changed)
        self.btn_bulk_search.clicked.connect(self.parent.show_bulk_search)
        self.btn_advanced_filter.clicked.connect(self.parent.show_advanced_filters)
        self.btn_clear_filter.clicked.connect(self.parent.clear_filters)
    
    def get_filters(self):
        """Mevcut filtreleri al"""
        return {
            'jcl': self.jcl_search.text().strip(),
            'ekip': self.ekip_combo.currentText(),
            'ay': self.ay_combo.currentText(),
            'hatali': self.cb_hatali.isChecked(),
            'uzun': self.cb_uzun.isChecked()
        }
    
    def clear_filters(self):
        """Filtreleri temizle"""
        self.jcl_search.clear()
        self.ekip_combo.setCurrentIndex(0)
        self.ay_combo.setCurrentIndex(0)
        self.cb_hatali.setChecked(True)
        self.cb_uzun.setChecked(True)
        self.advanced_filter_label.setText("")
    
    def populate_combo_boxes(self, ekipler, aylar):
        """ComboBox'ları doldur"""
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
    
    def set_advanced_filter_active(self, active):
        """Gelişmiş filtre durumunu göster"""
        if active:
            self.advanced_filter_label.setText("🔍 Gelişmiş filtre aktif")
        else:
            self.advanced_filter_label.setText("")
    
    def restore_filters(self, filters):
        """Filtreleri geri yükle"""
        if 'last_jcl' in filters:
            self.jcl_search.setText(filters['last_jcl'])
        
        if 'last_ekip' in filters:
            index = self.ekip_combo.findText(filters['last_ekip'])
            if index >= 0:
                self.ekip_combo.setCurrentIndex(index)
        
        if 'last_ay' in filters:
            index = self.ay_combo.findText(filters['last_ay'])
            if index >= 0:
                self.ay_combo.setCurrentIndex(index)
        
        if 'cb_hatali' in filters:
            self.cb_hatali.setChecked(filters['cb_hatali'])
        
        if 'cb_uzun' in filters:
            self.cb_uzun.setChecked(filters['cb_uzun'])