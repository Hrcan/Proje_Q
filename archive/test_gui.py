"""
Test GUI - Veritabanı Test Arayüzü
"""
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QTabWidget, QFileDialog, QMessageBox, QProgressBar,
                             QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from src.database.db_manager import DatabaseManager
from src.utils.excel_reader import ExcelReader


class TestGUI(QMainWindow):
    """Test GUI Ana Penceresi"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.birlesik_mod = "SHEET"  # "SHEET" veya "BIRLESIK"
        self.init_ui()
        self.init_database()
        
    def init_ui(self):
        """Arayüzü oluştur"""
        self.setWindowTitle("JCL Veri Yonetim Sistemi - Test")
        self.setGeometry(100, 100, 1600, 800)
        
        # Ana widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Başlık (emoji olmadan)
        title = QLabel("JCL VERITABANI TEST ARAYUZU")
        title.setStyleSheet("font-size: 20px; font-weight: bold; padding: 10px; background-color: #4CAF50; color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # İstatistikler
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; font-size: 12px;")
        layout.addWidget(self.stats_label)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        self.load_excel_btn = QPushButton("Excel Yukle")
        self.load_excel_btn.clicked.connect(self.load_excel)
        self.load_excel_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #2196F3; color: white;")
        button_layout.addWidget(self.load_excel_btn)
        
        self.refresh_btn = QPushButton("Yenile")
        self.refresh_btn.clicked.connect(self.refresh_tables)
        self.refresh_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #4CAF50; color: white;")
        button_layout.addWidget(self.refresh_btn)
        
        self.clear_btn = QPushButton("Veritabanini Temizle")
        self.clear_btn.clicked.connect(self.clear_database)
        self.clear_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #f44336; color: white;")
        button_layout.addWidget(self.clear_btn)
        
        # Birleşik görünüm modu seçimi (YENİ)
        button_layout.addStretch()
        mod_label = QLabel("Birlesik Gorunum:")
        mod_label.setStyleSheet("font-size: 12px; padding: 5px;")
        button_layout.addWidget(mod_label)
        
        self.mod_combo = QComboBox()
        self.mod_combo.addItems(["Sheet Bazinda (Ayri Satirlar)", "JCL Bazinda (Birlesik)"])
        self.mod_combo.currentIndexChanged.connect(self.on_mod_changed)
        self.mod_combo.setStyleSheet("padding: 5px; font-size: 12px;")
        button_layout.addWidget(self.mod_combo)
        
        layout.addLayout(button_layout)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 10px; font-size: 12px; }")
        
        # Tab 1: Hatalı İşler
        self.hatali_table = QTableWidget()
        self.tabs.addTab(self.hatali_table, "HATALI ISLER")
        
        # Tab 2: Uzun İşler
        self.uzun_table = QTableWidget()
        self.tabs.addTab(self.uzun_table, "UZUN SUREN ISLER")
        
        # Tab 3: Birleşik Görünüm
        self.birlesik_table = QTableWidget()
        self.tabs.addTab(self.birlesik_table, "BIRLESIK GORUNUM (TUM JCL)")
        
        layout.addWidget(self.tabs)
    
    def on_mod_changed(self, index):
        """Birleşik görünüm modu değiştirildiğinde"""
        self.birlesik_mod = "SHEET" if index == 0 else "BIRLESIK"
        self.load_birlesik_table()
        
    def init_database(self):
        """Veritabanını başlat"""
        try:
            self.db_manager.connect()
            self.db_manager.create_tables()
            self.refresh_tables()
            print("Veritabani hazir")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veritabani hatasi: {e}")
    
    def refresh_tables(self):
        """Tabloları yenile"""
        self.load_hatali_table()
        self.load_uzun_table()
        self.load_birlesik_table()
        self.update_stats()
    
    def update_stats(self):
        """İstatistikleri güncelle"""
        stats = self.db_manager.get_tablo_istatistikleri()
        self.stats_label.setText(
            f"Istatistikler: "
            f"Hatali Isler: {stats['hatali_isler']} | "
            f"Uzun Suren Isler: {stats['uzun_isler']} | "
            f"Yukleme Sayisi: {stats['yukleme_gecmisi']}"
        )
    
    def load_hatali_table(self):
        """Hatalı işler tablosunu yükle"""
        data = self.db_manager.get_all_hatali_isler()
        
        self.hatali_table.clear()
        self.hatali_table.setRowCount(len(data))
        self.hatali_table.setColumnCount(11)
        
        headers = ['ID', 'JCL Adi', 'Ay', 'Sheet', 'Hatali Sayi (Ay)', 
                   'Son Hatali Tarih', 'Hatali Sayi (Yil)', 'Sorumlu Ekip',
                   'Yuklenme Tarihi', 'Guncelleme Tarihi', 'Kaynak Dosya']
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
        data = self.db_manager.get_all_uzun_isler()
        
        self.uzun_table.clear()
        self.uzun_table.setRowCount(len(data))
        self.uzun_table.setColumnCount(10)
        
        headers = ['ID', 'JCL Adi', 'Ay', 'Sheet', 'Calisma Sayisi', 
                   'Calisma Suresi', 'Sorumlu Ekip', 'Yuklenme Tarihi', 
                   'Guncelleme Tarihi', 'Kaynak Dosya']
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
        """Birleşik görünüm tablosu - Mod'a göre"""
        if self.birlesik_mod == "SHEET":
            self.load_birlesik_sheet_bazli()
        else:
            self.load_birlesik_jcl_bazli()
    
    def load_birlesik_sheet_bazli(self):
        """Sheet bazında - Her sheet ayrı satır"""
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
        # JCL + Ay + Sheet kombinasyonları (YENİ: Sheet de dahil)
        combined = {}
        
        for record in hatali_data:
            key = (record['jcl_adi'], record['ay'], record['sheet_adi'])
            if key not in combined:
                combined[key] = {
                    'jcl_adi': record['jcl_adi'],
                    'ay': record['ay'],
                    'sheet': record['sheet_adi'],
                    'hatali': record,
                    'uzun': None
                }
        
        for record in uzun_data:
            key = (record['jcl_adi'], record['ay'], record['sheet_adi'])
            if key not in combined:
                combined[key] = {
                    'jcl_adi': record['jcl_adi'],
                    'ay': record['ay'],
                    'sheet': record['sheet_adi'],
                    'hatali': None,
                    'uzun': record
                }
            else:
                combined[key]['uzun'] = record
        
        data_list = sorted(combined.values(), key=lambda x: (x['ay'], x['jcl_adi'], x['sheet']), reverse=True)
        
        self.birlesik_table.clear()
        self.birlesik_table.setRowCount(len(data_list))
        self.birlesik_table.setColumnCount(13)
        
        headers = [
            'JCL Adi', 'Ay', 'Sheet',
            '--- HATALI ---', 'Hatali Sayi', 'Son Tarih', 'Sorumlu Ekip (H)',
            '--- UZUN ---', 'Calisma Sayisi', 'Calisma Suresi', 'Sorumlu Ekip (U)',
            'Durum', 'Guncelleme'
        ]
        self.birlesik_table.setHorizontalHeaderLabels(headers)
        
        for row_idx, item in enumerate(data_list):
            # JCL, Ay, Sheet
            self.birlesik_table.setItem(row_idx, 0, QTableWidgetItem(item['jcl_adi']))
            self.birlesik_table.setItem(row_idx, 1, QTableWidgetItem(item['ay']))
            self.birlesik_table.setItem(row_idx, 2, QTableWidgetItem(item['sheet']))
            
            # Hatalı
            sep1 = QTableWidgetItem('')
            sep1.setBackground(QColor(200, 200, 200))
            self.birlesik_table.setItem(row_idx, 3, sep1)
            
            if item['hatali']:
                h = item['hatali']
                self.birlesik_table.setItem(row_idx, 4, QTableWidgetItem(str(h['hatali_sayi_ay'] or '')))
                self.birlesik_table.setItem(row_idx, 5, QTableWidgetItem(str(h['son_hatali_tarih'] or '')))
                self.birlesik_table.setItem(row_idx, 6, QTableWidgetItem(h['sorumlu_ekip'] or ''))
            else:
                for col in range(4, 7):
                    item_widget = QTableWidgetItem('Veri Yok')
                    item_widget.setForeground(QColor(150, 150, 150))
                    self.birlesik_table.setItem(row_idx, col, item_widget)
            
            # Uzun
            sep2 = QTableWidgetItem('')
            sep2.setBackground(QColor(200, 200, 200))
            self.birlesik_table.setItem(row_idx, 7, sep2)
            
            if item['uzun']:
                u = item['uzun']
                self.birlesik_table.setItem(row_idx, 8, QTableWidgetItem(str(u['calisma_sayisi'] or '')))
                self.birlesik_table.setItem(row_idx, 9, QTableWidgetItem(str(u['calisma_suresi'] or '')))
                self.birlesik_table.setItem(row_idx, 10, QTableWidgetItem(u['sorumlu_ekip'] or ''))
            else:
                for col in range(8, 11):
                    item_widget = QTableWidgetItem('Veri Yok')
                    item_widget.setForeground(QColor(150, 150, 150))
                    self.birlesik_table.setItem(row_idx, col, item_widget)
            
            # Durum
            if item['hatali'] and item['uzun']:
                durum = 'Her Ikisinde'
                color = QColor(144, 238, 144)
            elif item['hatali']:
                durum = 'Sadece Hatalida'
                color = QColor(255, 200, 200)
            else:
                durum = 'Sadece Uzunda'
                color = QColor(200, 220, 255)
            
            durum_item = QTableWidgetItem(durum)
            durum_item.setBackground(color)
            self.birlesik_table.setItem(row_idx, 11, durum_item)
            
            # Güncelleme
            if item['hatali'] and item['uzun']:
                gun_tarih = max(item['hatali']['guncelleme_tarihi'], item['uzun']['guncelleme_tarihi'])
            elif item['hatali']:
                gun_tarih = item['hatali']['guncelleme_tarihi']
            else:
                gun_tarih = item['uzun']['guncelleme_tarihi']
            
            self.birlesik_table.setItem(row_idx, 12, QTableWidgetItem(str(gun_tarih)[:19]))
        
        self.birlesik_table.resizeColumnsToContents()
    
    def load_birlesik_jcl_bazli(self):
        """JCL bazında - Aynı JCL için tek satır, sheet'ler birleşik"""
        hatali_data = self.db_manager.get_all_hatali_isler()
        uzun_data = self.db_manager.get_all_uzun_isler()
        
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
        self.birlesik_table.setColumnCount(9)
        
        headers = [
            'JCL Adi', 'Ay',
            '--- HATALI ---', 'Sheets (H)', 'Sorumlu Ekipler (H)',
            '--- UZUN ---', 'Sheets (U)', 'Sorumlu Ekipler (U)',
            'Durum'
        ]
        self.birlesik_table.setHorizontalHeaderLabels(headers)
        
        for row_idx, item in enumerate(data_list):
            # JCL ve Ay
            self.birlesik_table.setItem(row_idx, 0, QTableWidgetItem(item['jcl_adi']))
            self.birlesik_table.setItem(row_idx, 1, QTableWidgetItem(item['ay']))
            
            # Hatalı
            sep1 = QTableWidgetItem('')
            sep1.setBackground(QColor(200, 200, 200))
            self.birlesik_table.setItem(row_idx, 2, sep1)
            
            if item['hatali_kayitlar']:
                sheets_h = ', '.join(set([r['sheet_adi'] for r in item['hatali_kayitlar']]))
                ekipler_h = ', '.join(set([r['sorumlu_ekip'] for r in item['hatali_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 3, QTableWidgetItem(sheets_h))
                self.birlesik_table.setItem(row_idx, 4, QTableWidgetItem(ekipler_h))
            else:
                for col in range(3, 5):
                    item_widget = QTableWidgetItem('Veri Yok')
                    item_widget.setForeground(QColor(150, 150, 150))
                    self.birlesik_table.setItem(row_idx, col, item_widget)
            
            # Uzun
            sep2 = QTableWidgetItem('')
            sep2.setBackground(QColor(200, 200, 200))
            self.birlesik_table.setItem(row_idx, 5, sep2)
            
            if item['uzun_kayitlar']:
                sheets_u = ', '.join(set([r['sheet_adi'] for r in item['uzun_kayitlar']]))
                ekipler_u = ', '.join(set([r['sorumlu_ekip'] for r in item['uzun_kayitlar'] if r['sorumlu_ekip']]))
                self.birlesik_table.setItem(row_idx, 6, QTableWidgetItem(sheets_u))
                self.birlesik_table.setItem(row_idx, 7, QTableWidgetItem(ekipler_u))
            else:
                for col in range(6, 8):
                    item_widget = QTableWidgetItem('Veri Yok')
                    item_widget.setForeground(QColor(150, 150, 150))
                    self.birlesik_table.setItem(row_idx, col, item_widget)
            
            # Durum
            if item['hatali_kayitlar'] and item['uzun_kayitlar']:
                durum = f"Her Ikisi ({len(item['hatali_kayitlar'])}H + {len(item['uzun_kayitlar'])}U)"
                color = QColor(144, 238, 144)
            elif item['hatali_kayitlar']:
                durum = f"Sadece Hatalida ({len(item['hatali_kayitlar'])} sheet)"
                color = QColor(255, 200, 200)
            else:
                durum = f"Sadece Uzunda ({len(item['uzun_kayitlar'])} sheet)"
                color = QColor(200, 220, 255)
            
            durum_item = QTableWidgetItem(durum)
            durum_item.setBackground(color)
            self.birlesik_table.setItem(row_idx, 8, durum_item)
        
        self.birlesik_table.resizeColumnsToContents()
    
    def load_excel(self):
        """Excel dosyası yükle"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Excel Dosyasi Sec", "Data/Excel", 
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
                    QMessageBox.warning(self, "Uyari", f"Dosya okuma hatasi: {hata}")
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
                QMessageBox.critical(self, "Hata", f"Dosya yukleme hatasi: {e}")
        
        self.progress.setVisible(False)
        self.refresh_tables()
        
        QMessageBox.information(
            self, "Basarili", 
            f"{len(files)} dosya basariyla yuklendi!\n"
            f"Toplam {total_kayit} kayit eklendi/guncellendi."
        )
    
    def clear_database(self):
        """Veritabanını temizle"""
        reply = QMessageBox.question(
            self, "Onay", 
            "Tum veritabanini temizlemek istediginize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            cursor = self.db_manager.connection.cursor()
            cursor.execute("DELETE FROM hatali_isler")
            cursor.execute("DELETE FROM uzun_isler")
            cursor.execute("DELETE FROM yukleme_gecmisi")
            self.db_manager.connection.commit()
            
            self.refresh_tables()
            QMessageBox.information(self, "Basarili", "Veritabani temizlendi!")
    
    def closeEvent(self, event):
        """Pencere kapatılırken"""
        self.db_manager.disconnect()
        event.accept()


def main():
    """Ana fonksiyon"""
    app = QApplication(sys.argv)
    window = TestGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()