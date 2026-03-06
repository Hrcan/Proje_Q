"""
Gelişmiş Filtreler Dialogu
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QDateEdit, QSpinBox, QGroupBox,
                             QFormLayout)
from PyQt5.QtCore import Qt, QDate


class AdvancedFiltersDialog(QDialog):
    """Gelişmiş filtreleme seçenekleri"""
    
    def __init__(self, parent, current_filters):
        super().__init__(parent)
        self.current_filters = current_filters.copy()
        
        self.setWindowTitle("🔍 Gelişmiş Filtreler")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("🔍 Gelişmiş Filtreleme Seçenekleri")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 10px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        layout.addWidget(title)
        
        # Tarih Filtresi
        date_group = QGroupBox("📅 Tarih Aralığı")
        date_layout = QFormLayout()
        
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDate(QDate.currentDate().addMonths(-6))
        
        self.date_end = QDateEdit()
        self.date_end.setCalendarPopup(True)
        self.date_end.setDate(QDate.currentDate())
        
        date_layout.addRow("Başlangıç:", self.date_start)
        date_layout.addRow("Bitiş:", self.date_end)
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # Hatalı Sayı Filtresi
        hatali_group = QGroupBox("❌ Hatalı İş Sayısı")
        hatali_layout = QFormLayout()
        
        self.hatali_min = QSpinBox()
        self.hatali_min.setRange(0, 999999)
        self.hatali_min.setValue(0)
        
        self.hatali_max = QSpinBox()
        self.hatali_max.setRange(0, 999999)
        self.hatali_max.setValue(999999)
        
        hatali_layout.addRow("Minimum:", self.hatali_min)
        hatali_layout.addRow("Maksimum:", self.hatali_max)
        
        hatali_group.setLayout(hatali_layout)
        layout.addWidget(hatali_group)
        
        # Çalışma Süresi Filtresi
        uzun_group = QGroupBox("⏱️ Çalışma Süresi (dakika)")
        uzun_layout = QFormLayout()
        
        self.uzun_min = QSpinBox()
        self.uzun_min.setRange(0, 999999)
        self.uzun_min.setValue(0)
        
        self.uzun_max = QSpinBox()
        self.uzun_max.setRange(0, 999999)
        self.uzun_max.setValue(999999)
        
        uzun_layout.addRow("Minimum:", self.uzun_min)
        uzun_layout.addRow("Maksimum:", self.uzun_max)
        
        uzun_group.setLayout(uzun_layout)
        layout.addWidget(uzun_group)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        btn_reset = QPushButton("🔄 Sıfırla")
        btn_reset.clicked.connect(self.reset_filters)
        
        btn_apply = QPushButton("✅ Uygula")
        btn_apply.clicked.connect(self.accept)
        btn_apply.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        
        btn_cancel = QPushButton("❌ İptal")
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addWidget(btn_reset)
        button_layout.addStretch()
        button_layout.addWidget(btn_apply)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
        
        # Mevcut filtreleri yükle
        self.load_current_filters()
    
    def load_current_filters(self):
        """Mevcut filtreleri yükle"""
        if self.current_filters.get('tarih_baslangic'):
            self.date_start.setDate(QDate.fromString(
                self.current_filters['tarih_baslangic'], 'yyyy-MM-dd'
            ))
        
        if self.current_filters.get('tarih_bitis'):
            self.date_end.setDate(QDate.fromString(
                self.current_filters['tarih_bitis'], 'yyyy-MM-dd'
            ))
        
        if self.current_filters.get('hatali_min') is not None:
            self.hatali_min.setValue(self.current_filters['hatali_min'])
        
        if self.current_filters.get('hatali_max') is not None:
            self.hatali_max.setValue(self.current_filters['hatali_max'])
        
        if self.current_filters.get('uzun_min') is not None:
            self.uzun_min.setValue(self.current_filters['uzun_min'])
        
        if self.current_filters.get('uzun_max') is not None:
            self.uzun_max.setValue(self.current_filters['uzun_max'])
    
    def reset_filters(self):
        """Filtreleri sıfırla"""
        self.date_start.setDate(QDate.currentDate().addMonths(-6))
        self.date_end.setDate(QDate.currentDate())
        self.hatali_min.setValue(0)
        self.hatali_max.setValue(999999)
        self.uzun_min.setValue(0)
        self.uzun_max.setValue(999999)
    
    def get_filters(self):
        """Filtre değerlerini döndür"""
        return {
            'tarih_baslangic': self.date_start.date().toString('yyyy-MM-dd'),
            'tarih_bitis': self.date_end.date().toString('yyyy-MM-dd'),
            'hatali_min': self.hatali_min.value() if self.hatali_min.value() > 0 else None,
            'hatali_max': self.hatali_max.value() if self.hatali_max.value() < 999999 else None,
            'uzun_min': self.uzun_min.value() if self.uzun_min.value() > 0 else None,
            'uzun_max': self.uzun_max.value() if self.uzun_max.value() < 999999 else None
        }