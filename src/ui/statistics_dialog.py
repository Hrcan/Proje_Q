"""
İstatistikler Dialogu
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QTabWidget, QWidget, QGroupBox)
from PyQt5.QtCore import Qt


class StatisticsDialog(QDialog):
    """Detaylı istatistikler penceresi"""
    
    def __init__(self, parent, db_manager):
        super().__init__(parent)
        self.db_manager = db_manager
        
        self.setWindowTitle("📈 Detaylı İstatistikler")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("📈 Veritabanı İstatistikleri")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 15px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Genel İstatistikler
        stats = self.db_manager.get_tablo_istatistikleri()
        
        stats_layout = QHBoxLayout()
        
        # Hatalı İşler
        hatali_group = self.create_stat_card(
            "❌ Hatalı İşler",
            str(stats['hatali_isler']),
            "#f44336"
        )
        stats_layout.addWidget(hatali_group)
        
        # Uzun İşler
        uzun_group = self.create_stat_card(
            "⏱️ Uzun İşler",
            str(stats['uzun_isler']),
            "#FF9800"
        )
        stats_layout.addWidget(uzun_group)
        
        # Yükleme Sayısı
        yukleme_group = self.create_stat_card(
            "📥 Yükleme",
            str(stats['yukleme_gecmisi']),
            "#4CAF50"
        )
        stats_layout.addWidget(yukleme_group)
        
        layout.addLayout(stats_layout)
        
        # Detaylı İstatistikler Tablosu
        tabs = QTabWidget()
        
        # Ekip bazında
        ekip_table = self.create_ekip_stats_table()
        tabs.addTab(ekip_table, "👥 Ekip Bazında")
        
        # Ay bazında
        ay_table = self.create_ay_stats_table()
        tabs.addTab(ay_table, "📅 Ay Bazında")
        
        # En çok hatalı
        top_hatali = self.create_top_hatali_table()
        tabs.addTab(top_hatali, "🔴 En Çok Hatalı")
        
        layout.addWidget(tabs)
        
        # Kapat butonu
        btn_close = QPushButton("✅ Kapat")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                padding: 10px 20px;
                background-color: #2196F3;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(btn_close, alignment=Qt.AlignCenter)
    
    def create_stat_card(self, title, value, color):
        """İstatistik kartı oluştur"""
        group = QGroupBox()
        group.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid {color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        group.setLayout(layout)
        return group
    
    def create_ekip_stats_table(self):
        """Ekip bazında istatistikler"""
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Ekip', 'Hatalı İş', 'Uzun İş'])
        
        # Ekip bazında say
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
        ekip_stats = {}
        
        for record in hatali_data:
            ekip = record.get('sorumlu_ekip', 'Bilinmiyor')
            if ekip not in ekip_stats:
                ekip_stats[ekip] = {'hatali': 0, 'uzun': 0}
            ekip_stats[ekip]['hatali'] += 1
        
        for record in uzun_data:
            ekip = record.get('sorumlu_ekip', 'Bilinmiyor')
            if ekip not in ekip_stats:
                ekip_stats[ekip] = {'hatali': 0, 'uzun': 0}
            ekip_stats[ekip]['uzun'] += 1
        
        # Tabloya ekle
        table.setRowCount(len(ekip_stats))
        for idx, (ekip, stats) in enumerate(sorted(ekip_stats.items())):
            table.setItem(idx, 0, QTableWidgetItem(ekip))
            table.setItem(idx, 1, QTableWidgetItem(str(stats['hatali'])))
            table.setItem(idx, 2, QTableWidgetItem(str(stats['uzun'])))
        
        table.resizeColumnsToContents()
        return table
    
    def create_ay_stats_table(self):
        """Ay bazında istatistikler"""
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Ay', 'Hatalı İş', 'Uzun İş'])
        
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
        ay_stats = {}
        
        for record in hatali_data:
            ay = record.get('ay', 'Bilinmiyor')
            if ay not in ay_stats:
                ay_stats[ay] = {'hatali': 0, 'uzun': 0}
            ay_stats[ay]['hatali'] += 1
        
        for record in uzun_data:
            ay = record.get('ay', 'Bilinmiyor')
            if ay not in ay_stats:
                ay_stats[ay] = {'hatali': 0, 'uzun': 0}
            ay_stats[ay]['uzun'] += 1
        
        # Tabloya ekle (en yeni önce)
        table.setRowCount(len(ay_stats))
        for idx, (ay, stats) in enumerate(sorted(ay_stats.items(), reverse=True)):
            table.setItem(idx, 0, QTableWidgetItem(ay))
            table.setItem(idx, 1, QTableWidgetItem(str(stats['hatali'])))
            table.setItem(idx, 2, QTableWidgetItem(str(stats['uzun'])))
        
        table.resizeColumnsToContents()
        return table
    
    def create_top_hatali_table(self):
        """En çok hatalı JCL'ler"""
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['JCL Adı', 'Toplam Hata', 'Sorumlu Ekip', 'Son Ay'])
        
        hatali_data = self.db_manager.get_all_hatali_isler()
        
        # JCL bazında topla
        jcl_stats = {}
        for record in hatali_data:
            jcl = record['jcl_adi']
            if jcl not in jcl_stats:
                jcl_stats[jcl] = {
                    'total': 0,
                    'ekip': record.get('sorumlu_ekip', ''),
                    'son_ay': record.get('ay', '')
                }
            jcl_stats[jcl]['total'] += record.get('hatali_sayi_ay', 0) or 0
        
        # En çok hatalı 20'yi al
        top_jcls = sorted(jcl_stats.items(), key=lambda x: x[1]['total'], reverse=True)[:20]
        
        table.setRowCount(len(top_jcls))
        for idx, (jcl, stats) in enumerate(top_jcls):
            table.setItem(idx, 0, QTableWidgetItem(jcl))
            table.setItem(idx, 1, QTableWidgetItem(str(stats['total'])))
            table.setItem(idx, 2, QTableWidgetItem(stats['ekip']))
            table.setItem(idx, 3, QTableWidgetItem(stats['son_ay']))
        
        table.resizeColumnsToContents()
        return table