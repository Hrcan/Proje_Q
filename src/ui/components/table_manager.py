"""
Tablo Yöneticisi - Tablo işlemleri için merkezi modül
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt


class TableManager:
    """Tablo oluşturma, yükleme ve filtreleme işlemlerini yöneten sınıf"""
    
    def __init__(self, parent):
        """
        Args:
            parent: Ana pencere referansı (MainWindow)
        """
        self.parent = parent
    
    def create_table(self):
        """Yeni bir tablo widget'ı oluştur ve yapılandır"""
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setContextMenuPolicy(Qt.CustomContextMenu)
        table.customContextMenuRequested.connect(
            lambda pos, t=table: self.parent.show_context_menu(pos, t)
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
    
    def apply_wildcard_search(self, jcl_list, data):
        """
        Wildcard desteğiyle JCL arama (PONT*, *ABC, PONT*ABC)
        
        Args:
            jcl_list: Aranacak JCL pattern listesi
            data: Aranacak veri listesi
            
        Returns:
            Eşleşen kayıtlar listesi
        """
        if not jcl_list:
            return data
        
        filtered_data = []
        for record in data:
            jcl_adi_upper = record['jcl_adi'].upper()
            for jcl_pattern in jcl_list:
                matched = False
                
                if '*' in jcl_pattern:
                    # Wildcard pattern
                    pattern_parts = jcl_pattern.split('*')
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
                    elif len(pattern_parts) == 1 and jcl_pattern == '*':
                        # Sadece * - tümü
                        matched = True
                else:
                    # Normal arama (içinde geçmeli)
                    if jcl_pattern in jcl_adi_upper:
                        matched = True
                
                if matched:
                    filtered_data.append(record)
                    break
        
        return filtered_data
    
    def apply_filters(self, data, jcl_text, ekip, ay):
        """
        Verilere filtreleri uygula
        
        Args:
            data: Filtrelenecek veri listesi
            jcl_text: JCL arama metni (virgül, boşluk, satır ve wildcard destekli)
            ekip: Seçilen ekip
            ay: Seçilen ay
            
        Returns:
            Filtrelenmiş veri listesi
        """
        # JCL arama (virgül, boşluk, satır ve wildcard (*) desteklenir)
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
                data = self.apply_wildcard_search(jcl_list, data)
        
        # Ekip
        if ekip != "Tümü":
            data = [r for r in data if r.get('sorumlu_ekip') == ekip]
        
        # Ay
        if ay != "Tümü":
            data = [r for r in data if r.get('ay') == ay]
        
        return data
    
    def load_hatali_table(self, table, db_manager, jcl_text, ekip, ay, show_hatali):
        """Hatalı işler tablosunu yükle"""
        if not show_hatali:
            table.setRowCount(0)
            table.setColumnCount(0)
            return
        
        data = db_manager.get_all_hatali_isler()
        data = self.apply_filters(data, jcl_text, ekip, ay)
        
        table.clear()
        table.setRowCount(len(data))
        table.setColumnCount(11)
        
        headers = ['ID', 'JCL Adı', 'Ay', 'Sheet', 'Hatalı Sayı (Ay)', 
                   'Son Hatalı Tarih', 'Hatalı Sayı (Yıl)', 'Sorumlu Ekip',
                   'Yüklenme Tarihi', 'Güncelleme Tarihi', 'Kaynak Dosya']
        table.setHorizontalHeaderLabels(headers)
        
        for row_idx, record in enumerate(data):
            table.setItem(row_idx, 0, QTableWidgetItem(str(record['id'])))
            table.setItem(row_idx, 1, QTableWidgetItem(record['jcl_adi']))
            table.setItem(row_idx, 2, QTableWidgetItem(record['ay']))
            table.setItem(row_idx, 3, QTableWidgetItem(record['sheet_adi']))
            table.setItem(row_idx, 4, QTableWidgetItem(str(record['hatali_sayi_ay'] or '')))
            table.setItem(row_idx, 5, QTableWidgetItem(str(record['son_hatali_tarih'] or '')))
            table.setItem(row_idx, 6, QTableWidgetItem(str(record['hatali_sayi_yil'] or '')))
            table.setItem(row_idx, 7, QTableWidgetItem(record['sorumlu_ekip'] or ''))
            table.setItem(row_idx, 8, QTableWidgetItem(str(record['yuklenme_tarihi'])[:19]))
            table.setItem(row_idx, 9, QTableWidgetItem(str(record['guncelleme_tarihi'])[:19]))
            table.setItem(row_idx, 10, QTableWidgetItem(record['kaynak_dosya'] or ''))
        
        table.resizeColumnsToContents()
    
    def load_uzun_table(self, table, db_manager, jcl_text, ekip, ay, show_uzun):
        """Uzun süren işler tablosunu yükle"""
        if not show_uzun:
            table.setRowCount(0)
            table.setColumnCount(0)
            return
        
        data = db_manager.get_all_uzun_isler()
        data = self.apply_filters(data, jcl_text, ekip, ay)
        
        table.clear()
        table.setRowCount(len(data))
        table.setColumnCount(10)
        
        headers = ['ID', 'JCL Adı', 'Ay', 'Sheet', 'Çalışma Sayısı', 
                   'Çalışma Süresi', 'Sorumlu Ekip', 'Yüklenme Tarihi', 
                   'Güncelleme Tarihi', 'Kaynak Dosya']
        table.setHorizontalHeaderLabels(headers)
        
        for row_idx, record in enumerate(data):
            table.setItem(row_idx, 0, QTableWidgetItem(str(record['id'])))
            table.setItem(row_idx, 1, QTableWidgetItem(record['jcl_adi']))
            table.setItem(row_idx, 2, QTableWidgetItem(record['ay']))
            table.setItem(row_idx, 3, QTableWidgetItem(record['sheet_adi']))
            table.setItem(row_idx, 4, QTableWidgetItem(str(record['calisma_sayisi'] or '')))
            table.setItem(row_idx, 5, QTableWidgetItem(str(record['calisma_suresi'] or '')))
            table.setItem(row_idx, 6, QTableWidgetItem(record['sorumlu_ekip'] or ''))
            table.setItem(row_idx, 7, QTableWidgetItem(str(record['yuklenme_tarihi'])[:19]))
            table.setItem(row_idx, 8, QTableWidgetItem(str(record['guncelleme_tarihi'])[:19]))
            table.setItem(row_idx, 9, QTableWidgetItem(record['kaynak_dosya'] or ''))
        
        table.resizeColumnsToContents()
    
    def load_birlesik_table(self, table, db_manager, jcl_text, ekip, ay, show_hatali, show_uzun):
        """Birleşik görünüm tablosunu yükle"""
        hatali_data = db_manager.get_all_hatali_isler() if show_hatali else []
        uzun_data = db_manager.get_all_uzun_isler() if show_uzun else []
        
        hatali_data = self.apply_filters(hatali_data, jcl_text, ekip, ay)
        uzun_data = self.apply_filters(uzun_data, jcl_text, ekip, ay)
        
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
        
        table.clear()
        table.setRowCount(len(data_list))
        table.setColumnCount(7)
        
        headers = ['JCL Adı', 'Ay', 'Hatalı Sheets', 'Hatalı Ekipler', 
                   'Uzun Sheets', 'Uzun Ekipler', 'Durum']
        table.setHorizontalHeaderLabels(headers)
        
        for row_idx, item in enumerate(data_list):
            table.setItem(row_idx, 0, QTableWidgetItem(item['jcl_adi']))
            table.setItem(row_idx, 1, QTableWidgetItem(item['ay']))
            
            if item['hatali_kayitlar']:
                sheets_h = ', '.join(set([r['sheet_adi'] for r in item['hatali_kayitlar']]))
                ekipler_h = ', '.join(set([r['sorumlu_ekip'] for r in item['hatali_kayitlar'] if r['sorumlu_ekip']]))
                table.setItem(row_idx, 2, QTableWidgetItem(sheets_h))
                table.setItem(row_idx, 3, QTableWidgetItem(ekipler_h))
            
            if item['uzun_kayitlar']:
                sheets_u = ', '.join(set([r['sheet_adi'] for r in item['uzun_kayitlar']]))
                ekipler_u = ', '.join(set([r['sorumlu_ekip'] for r in item['uzun_kayitlar'] if r['sorumlu_ekip']]))
                table.setItem(row_idx, 4, QTableWidgetItem(sheets_u))
                table.setItem(row_idx, 5, QTableWidgetItem(ekipler_u))
            
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
            table.setItem(row_idx, 6, durum_item)
        
        table.resizeColumnsToContents()
    
    def update_stats(self, stats_label, hatali_table, uzun_table, birlesik_table, db_manager):
        """İstatistikleri güncelle"""
        stats = db_manager.get_tablo_istatistikleri()
        
        hatali_visible = hatali_table.rowCount()
        uzun_visible = uzun_table.rowCount()
        birlesik_visible = birlesik_table.rowCount()
        
        stats_label.setText(
            f"📊 İstatistikler: "
            f"Hatalı: {hatali_visible}/{stats['hatali_isler']} | "
            f"Uzun: {uzun_visible}/{stats['uzun_isler']} | "
            f"Birleşik: {birlesik_visible} | "
            f"Yükleme: {stats['yukleme_gecmisi']}"
        )