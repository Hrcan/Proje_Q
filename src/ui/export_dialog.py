"""
Excel Export Dialogu - Kolon Seçimi
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, 
                             QPushButton, QLabel, QScrollArea, QWidget, 
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
import pandas as pd


class ExportDialog(QDialog):
    """Excel export için kolon seçim dialogu"""
    
    def __init__(self, parent, table, default_name):
        super().__init__(parent)
        self.table = table
        self.default_name = default_name
        self.checkboxes = {}
        
        self.setWindowTitle("📊 Excel'e Aktar - Kolon Seçimi")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("📋 Excel'e aktarılacak kolonları seçin:")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 10px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        layout.addWidget(title)
        
        # Hızlı seçim butonları
        quick_select = QHBoxLayout()
        
        btn_all = QPushButton("✅ Tümünü Seç")
        btn_all.clicked.connect(self.select_all)
        
        btn_none = QPushButton("❌ Hiçbirini Seçme")
        btn_none.clicked.connect(self.select_none)
        
        btn_important = QPushButton("⭐ Önemli Kolonlar")
        btn_important.clicked.connect(self.select_important)
        
        quick_select.addWidget(btn_all)
        quick_select.addWidget(btn_none)
        quick_select.addWidget(btn_important)
        quick_select.addStretch()
        
        layout.addLayout(quick_select)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Önemli kolonlar listesi
        important_cols = {
            'JCL Adı', 'Ay', 'Sheet', 'Sorumlu Ekip',
            'Hatalı Sayı (Ay)', 'Son Hatalı Tarih', 'Hatalı Sayı (Yıl)',
            'Çalışma Sayısı', 'Çalışma Süresi',
            'Hatalı Sheets', 'Hatalı Ekipler', 'Uzun Sheets', 'Uzun Ekipler', 'Durum'
        }
        
        # Tüm kolonlar için checkbox oluştur
        for col in range(self.table.columnCount()):
            header = self.table.horizontalHeaderItem(col)
            if header:
                col_name = header.text()
                cb = QCheckBox(col_name)
                cb.setStyleSheet("padding: 5px;")
                
                # Önemli kolonları başlangıçta seçili yap
                if col_name in important_cols:
                    cb.setChecked(True)
                
                self.checkboxes[col_name] = cb
                scroll_layout.addWidget(cb)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        
        btn_export = QPushButton("✅ Dışa Aktar")
        btn_export.setStyleSheet("""
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
        btn_export.clicked.connect(self.do_export)
        
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
        btn_cancel.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_export)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
    
    def select_all(self):
        """Tümünü seç"""
        for cb in self.checkboxes.values():
            cb.setChecked(True)
    
    def select_none(self):
        """Hiçbirini seçme"""
        for cb in self.checkboxes.values():
            cb.setChecked(False)
    
    def select_important(self):
        """Önemli kolonları seç"""
        important_cols = {
            'JCL Adı', 'Ay', 'Sheet', 'Sorumlu Ekip',
            'Hatalı Sayı (Ay)', 'Son Hatalı Tarih', 'Hatalı Sayı (Yıl)',
            'Çalışma Sayısı', 'Çalışma Süresi',
            'Hatalı Sheets', 'Hatalı Ekipler', 'Uzun Sheets', 'Uzun Ekipler', 'Durum'
        }
        
        for col_name, cb in self.checkboxes.items():
            cb.setChecked(col_name in important_cols)
    
    def get_selected_columns(self):
        """Seçili kolonları döndür"""
        return [col for col, cb in self.checkboxes.items() if cb.isChecked()]
    
    def do_export(self):
        """Export işlemini yap"""
        selected_columns = self.get_selected_columns()
        
        if not selected_columns:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir kolon seçin!")
            return
        
        # Dosya kaydetme dialogu
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Excel Olarak Kaydet",
            f"{self.default_name}.xlsx",
            "Excel Files (*.xlsx)"
        )
        
        if not file_path:
            return
        
        try:
            # Tüm kolon başlıklarını al
            all_headers = []
            for col in range(self.table.columnCount()):
                header = self.table.horizontalHeaderItem(col)
                if header:
                    all_headers.append(header.text())
            
            # Seçili kolonların index'lerini bul
            selected_indices = [all_headers.index(col) for col in selected_columns]
            
            # Tablo verilerini al (sadece seçili kolonlar)
            data = []
            for row in range(self.table.rowCount()):
                row_data = []
                for col_idx in selected_indices:
                    item = self.table.item(row, col_idx)
                    row_data.append(item.text() if item else '')
                data.append(row_data)
            
            # DataFrame oluştur ve kaydet
            df = pd.DataFrame(data, columns=selected_columns)
            
            # Excel'e yaz
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Veri')
                
                # Worksheet'i al ve stil uygula
                worksheet = writer.sheets['Veri']
                
                # Başlık satırını formatla
                from openpyxl.styles import Font, PatternFill, Alignment
                
                header_fill = PatternFill(start_color='2196F3', end_color='2196F3', fill_type='solid')
                header_font = Font(bold=True, color='FFFFFF')
                
                for cell in worksheet[1]:
                    cell.fill = header_fill
                    cell.font = header_font
                    cell.alignment = Alignment(horizontal='center', vertical='center')
                
                # Kolon genişliklerini ayarla
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            QMessageBox.information(
                self, "✅ Başarılı",
                f"Veri başarıyla kaydedildi!\n\n"
                f"📁 Dosya: {file_path}\n"
                f"📊 Satır: {len(df)}\n"
                f"📋 Kolon: {len(selected_columns)}"
            )
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Hata", f"Export hatası:\n{str(e)}")