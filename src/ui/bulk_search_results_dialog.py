"""
Toplu Arama Sonuçları Dialogu
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QTabWidget, QGroupBox, QWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class BulkSearchResultsDialog(QDialog):
    """Toplu arama sonuçlarını gösterir"""
    
    def __init__(self, parent, jcl_list, hatali_results, uzun_results):
        super().__init__(parent)
        self.jcl_list = jcl_list
        self.hatali_results = hatali_results
        self.uzun_results = uzun_results
        
        self.setWindowTitle("🔍 Toplu Arama Sonuçları")
        self.setModal(True)
        self.setMinimumSize(1200, 700)
        
        self.init_ui()
        self.center_on_screen()
    
    def center_on_screen(self):
        """Dialogu ekranın tam ortasında aç"""
        from PyQt5.QtWidgets import QDesktopWidget
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(
            (screen.width() - size.width()) // 2,
            (screen.height() - size.height()) // 2
        )
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("🔍 Toplu Arama Sonuçları")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 15px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Özet istatistikler
        summary_layout = QHBoxLayout()
        
        # Aranan JCL'ler
        searched_group = self.create_summary_card(
            "📋 Aranan JCL",
            str(len(self.jcl_list)),
            f"Benzersiz: {len(set(self.jcl_list))}",
            "#2196F3"
        )
        summary_layout.addWidget(searched_group)
        
        # Bulunan Hatalı
        hatali_group = self.create_summary_card(
            "❌ Hatalı İşler",
            str(len(self.hatali_results)),
            f"Kayıt bulundu",
            "#f44336"
        )
        summary_layout.addWidget(hatali_group)
        
        # Bulunan Uzun
        uzun_group = self.create_summary_card(
            "⏱️ Uzun İşler",
            str(len(self.uzun_results)),
            f"Kayıt bulundu",
            "#FF9800"
        )
        summary_layout.addWidget(uzun_group)
        
        # Toplam
        total = len(self.hatali_results) + len(self.uzun_results)
        total_group = self.create_summary_card(
            "📊 Toplam",
            str(total),
            "Sonuç",
            "#4CAF50"
        )
        summary_layout.addWidget(total_group)
        
        layout.addLayout(summary_layout)
        
        # JCL Bulunamadılar listesi
        not_found = self.get_not_found_jcls()
        if not_found:
            warning_label = QLabel(
                f"⚠️ {len(not_found)} JCL için sonuç bulunamadı: {', '.join(not_found[:10])}"
                + ("..." if len(not_found) > 10 else "")
            )
            warning_label.setStyleSheet("""
                padding: 10px;
                background-color: #FFF3CD;
                color: #856404;
                border-radius: 5px;
                border-left: 4px solid #ffc107;
            """)
            warning_label.setWordWrap(True)
            layout.addWidget(warning_label)
        
        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("""
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
        if self.hatali_results:
            hatali_table = self.create_results_table(self.hatali_results, 'hatali')
            tabs.addTab(hatali_table, f"❌ HATALI İŞLER ({len(self.hatali_results)})")
        
        # Tab 2: Uzun İşler
        if self.uzun_results:
            uzun_table = self.create_results_table(self.uzun_results, 'uzun')
            tabs.addTab(uzun_table, f"⏱️ UZUN İŞLER ({len(self.uzun_results)})")
        
        # Tab 3: JCL Özeti
        summary_table = self.create_jcl_summary()
        tabs.addTab(summary_table, "📋 JCL ÖZETİ")
        
        layout.addWidget(tabs)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        
        btn_close = QPushButton("✅ Kapat")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_close)
        
        layout.addLayout(button_layout)
    
    def create_summary_card(self, title, value, subtitle, color):
        """Özet kartı oluştur"""
        group = QGroupBox()
        group.setStyleSheet(f"""
            QGroupBox {{
                border: 2px solid {color};
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 12px; color: {color}; font-weight: bold;")
        title_label.setAlignment(Qt.AlignCenter)
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("font-size: 10px; color: #666;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)
        
        group.setLayout(layout)
        return group
    
    def create_results_table(self, data, table_type):
        """Sonuç tablosu oluştur"""
        table = QTableWidget()
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        
        if table_type == 'hatali':
            table.setColumnCount(7)
            headers = ['JCL Adı', 'Ay', 'Sheet', 'Hatalı Sayı (Ay)', 
                      'Hatalı Sayı (Yıl)', 'Sorumlu Ekip', 'Son Hatalı Tarih']
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(data))
            
            for row_idx, record in enumerate(data):
                table.setItem(row_idx, 0, QTableWidgetItem(record['jcl_adi']))
                table.setItem(row_idx, 1, QTableWidgetItem(record['ay']))
                table.setItem(row_idx, 2, QTableWidgetItem(record['sheet_adi']))
                table.setItem(row_idx, 3, QTableWidgetItem(str(record['hatali_sayi_ay'] or '')))
                table.setItem(row_idx, 4, QTableWidgetItem(str(record['hatali_sayi_yil'] or '')))
                table.setItem(row_idx, 5, QTableWidgetItem(record['sorumlu_ekip'] or ''))
                table.setItem(row_idx, 6, QTableWidgetItem(str(record['son_hatali_tarih'] or '')))
        
        else:  # uzun
            table.setColumnCount(6)
            headers = ['JCL Adı', 'Ay', 'Sheet', 'Çalışma Sayısı', 
                      'Çalışma Süresi', 'Sorumlu Ekip']
            table.setHorizontalHeaderLabels(headers)
            table.setRowCount(len(data))
            
            for row_idx, record in enumerate(data):
                table.setItem(row_idx, 0, QTableWidgetItem(record['jcl_adi']))
                table.setItem(row_idx, 1, QTableWidgetItem(record['ay']))
                table.setItem(row_idx, 2, QTableWidgetItem(record['sheet_adi']))
                table.setItem(row_idx, 3, QTableWidgetItem(str(record['calisma_sayisi'] or '')))
                table.setItem(row_idx, 4, QTableWidgetItem(str(record['calisma_suresi'] or '')))
                table.setItem(row_idx, 5, QTableWidgetItem(record['sorumlu_ekip'] or ''))
        
        table.resizeColumnsToContents()
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
        """)
        
        return table
    
    def create_jcl_summary(self):
        """JCL özet tablosu - Tüm bulunan gerçek JCL'leri göster"""
        table = QTableWidget()
        table.setColumnCount(6)
        headers = ['JCL Adı', 'Hatalı Kayıt', 'Hatalı Ekipler', 'Uzun Kayıt', 'Uzun Ekipler', 'Durum']
        table.setHorizontalHeaderLabels(headers)
        
        # Tüm bulunan benzersiz JCL'leri al
        found_jcls = set()
        for r in self.hatali_results:
            found_jcls.add(r['jcl_adi'])
        for r in self.uzun_results:
            found_jcls.add(r['jcl_adi'])
        
        # Her gerçek JCL için özet oluştur
        jcl_summary = {}
        for jcl in found_jcls:
            hatali_records = [r for r in self.hatali_results if r['jcl_adi'] == jcl]
            uzun_records = [r for r in self.uzun_results if r['jcl_adi'] == jcl]
            
            hatali_ekipler = set([r['sorumlu_ekip'] for r in hatali_records if r.get('sorumlu_ekip')])
            uzun_ekipler = set([r['sorumlu_ekip'] for r in uzun_records if r.get('sorumlu_ekip')])
            
            jcl_summary[jcl] = {
                'hatali': len(hatali_records),
                'hatali_ekipler': ', '.join(sorted(hatali_ekipler)) if hatali_ekipler else '-',
                'uzun': len(uzun_records),
                'uzun_ekipler': ', '.join(sorted(uzun_ekipler)) if uzun_ekipler else '-'
            }
        
        table.setRowCount(len(jcl_summary))
        
        for row_idx, (jcl, counts) in enumerate(sorted(jcl_summary.items())):
            table.setItem(row_idx, 0, QTableWidgetItem(jcl))
            table.setItem(row_idx, 1, QTableWidgetItem(str(counts['hatali'])))
            table.setItem(row_idx, 2, QTableWidgetItem(counts['hatali_ekipler']))
            table.setItem(row_idx, 3, QTableWidgetItem(str(counts['uzun'])))
            table.setItem(row_idx, 4, QTableWidgetItem(counts['uzun_ekipler']))
            
            # Durum
            if counts['hatali'] == 0 and counts['uzun'] == 0:
                durum = "Bulunamadı"
                color = QColor(255, 200, 200)
            elif counts['hatali'] > 0 and counts['uzun'] > 0:
                durum = "Her İkisi"
                color = QColor(144, 238, 144)
            elif counts['hatali'] > 0:
                durum = "Sadece Hatalı"
                color = QColor(255, 230, 200)
            else:
                durum = "Sadece Uzun"
                color = QColor(200, 220, 255)
            
            durum_item = QTableWidgetItem(durum)
            durum_item.setBackground(color)
            table.setItem(row_idx, 5, durum_item)
        
        table.resizeColumnsToContents()
        
        # İlk kolonu sabitle (freeze)
        table.horizontalHeader().setSectionResizeMode(0, table.horizontalHeader().Fixed)
        table.setColumnWidth(0, 150)
        
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
        """)
        
        return table
    
    def get_not_found_jcls(self):
        """Bulunamayan pattern'leri döndür"""
        # Hiç sonuç bulunamayan pattern'leri listele
        not_found = []
        
        # Eğer hiç sonuç yoksa tüm pattern'leri göster
        if not self.hatali_results and not self.uzun_results:
            return sorted(set(self.jcl_list))
        
        # Her pattern için en az bir sonuç var mı kontrol et
        for pattern in set(self.jcl_list):
            pattern_upper = pattern.upper()
            has_result = False
            
            # Pattern'e uyan herhangi bir sonuç var mı?
            for record in self.hatali_results + self.uzun_results:
                jcl_adi_upper = record['jcl_adi'].upper()
                
                if '*' in pattern_upper:
                    # Wildcard pattern
                    pattern_parts = pattern_upper.split('*')
                    if len(pattern_parts) == 2:
                        prefix, suffix = pattern_parts
                        if prefix and suffix:
                            if jcl_adi_upper.startswith(prefix) and jcl_adi_upper.endswith(suffix):
                                has_result = True
                                break
                        elif prefix:
                            if jcl_adi_upper.startswith(prefix):
                                has_result = True
                                break
                        elif suffix:
                            if jcl_adi_upper.endswith(suffix):
                                has_result = True
                                break
                    elif pattern_upper == '*':
                        has_result = True
                        break
                else:
                    # Normal arama
                    if pattern_upper in jcl_adi_upper:
                        has_result = True
                        break
            
            if not has_result:
                not_found.append(pattern)
        
        return sorted(not_found)
