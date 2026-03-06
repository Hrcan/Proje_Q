"""
Toplu Arama Dialogu
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt


class BulkSearchDialog(QDialog):
    """Toplu JCL arama dialogu"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.jcl_list = []
        
        self.setWindowTitle("🔍 Toplu JCL Arama")
        self.setModal(True)
        self.setMinimumSize(600, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("🔍 Toplu JCL Arama")
        title.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Açıklama
        info = QLabel(
            "📝 Aramak istediğiniz JCL adlarını girin.\n"
            "Her satıra bir JCL veya virgül/boşlukla ayırarak yazabilirsiniz."
        )
        info.setStyleSheet("""
            padding: 10px;
            background-color: #E3F2FD;
            border-radius: 5px;
            color: #1976D2;
        """)
        info.setWordWrap(True)
        layout.addWidget(info)
        
        # Metin alanı
        text_label = QLabel("JCL Listesi:")
        text_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(text_label)
        
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText(
            "Örnek:\n"
            "PKRBI330\n"
            "PKRBI340\n"
            "PCRMU102\n\n"
            "veya virgül/boşlukla:\n"
            "PKRBI330, PKRBI340, PCRMU102\n\n"
            "veya karışık:\n"
            "PKRBI330\n"
            "PKRBI340, PCRMU102"
        )
        self.text_area.setStyleSheet("""
            QTextEdit {
                border: 2px solid #2196F3;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
            }
            QTextEdit:focus {
                border: 2px solid #1976D2;
            }
        """)
        layout.addWidget(self.text_area)
        
        # İstatistik
        self.count_label = QLabel("JCL Sayısı: 0")
        self.count_label.setStyleSheet("""
            padding: 5px;
            background-color: #f0f0f0;
            border-radius: 3px;
            font-weight: bold;
        """)
        layout.addWidget(self.count_label)
        
        # Metin değiştiğinde sayı güncelle
        self.text_area.textChanged.connect(self.update_count)
        
        # Hızlı işlemler
        quick_layout = QHBoxLayout()
        
        btn_clear = QPushButton("🗑️ Temizle")
        btn_clear.clicked.connect(self.clear_text)
        btn_clear.setToolTip("Metni temizle")
        
        btn_example = QPushButton("📋 Örnek Yükle")
        btn_example.clicked.connect(self.load_example)
        btn_example.setToolTip("Örnek JCL listesi yükle")
        
        btn_unique = QPushButton("🔧 Tekrarları Temizle")
        btn_unique.clicked.connect(self.remove_duplicates)
        btn_unique.setToolTip("Tekrar eden JCL'leri kaldır")
        
        quick_layout.addWidget(btn_clear)
        quick_layout.addWidget(btn_example)
        quick_layout.addWidget(btn_unique)
        quick_layout.addStretch()
        
        layout.addLayout(quick_layout)
        
        # Alt butonlar
        button_layout = QHBoxLayout()
        
        btn_search = QPushButton("🔍 Ara")
        btn_search.clicked.connect(self.do_search)
        btn_search.setStyleSheet("""
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
        
        btn_cancel = QPushButton("❌ İptal")
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setStyleSheet("""
            QPushButton {
                padding: 12px 30px;
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(btn_search)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
    
    def update_count(self):
        """JCL sayısını güncelle"""
        text = self.text_area.toPlainText().strip()
        if not text:
            self.count_label.setText("JCL Sayısı: 0")
            return
        
        jcl_list = self.parse_jcl_list(text)
        unique_count = len(set(jcl_list))
        total_count = len(jcl_list)
        
        if unique_count == total_count:
            self.count_label.setText(f"JCL Sayısı: {total_count}")
        else:
            self.count_label.setText(
                f"JCL Sayısı: {total_count} (Benzersiz: {unique_count}, Tekrar: {total_count - unique_count})"
            )
            self.count_label.setStyleSheet("""
                padding: 5px;
                background-color: #FFF3CD;
                border-radius: 3px;
                font-weight: bold;
                color: #856404;
            """)
    
    def parse_jcl_list(self, text):
        """Metinden JCL listesi çıkar"""
        # Satırlara ayır
        lines = text.split('\n')
        
        jcl_list = []
        for line in lines:
            # Virgül veya boşlukla ayır
            parts = line.replace(',', ' ').split()
            for part in parts:
                part = part.strip().upper()
                if part:
                    jcl_list.append(part)
        
        return jcl_list
    
    def clear_text(self):
        """Metni temizle"""
        self.text_area.clear()
    
    def load_example(self):
        """Örnek liste yükle"""
        example = (
            "PKRBI330\n"
            "PKRBI340\n"
            "PCRMU102\n"
            "MAGQVSAM\n"
            "ILHS7BSS"
        )
        self.text_area.setPlainText(example)
    
    def remove_duplicates(self):
        """Tekrarları kaldır"""
        text = self.text_area.toPlainText().strip()
        if not text:
            return
        
        jcl_list = self.parse_jcl_list(text)
        unique_jcls = sorted(set(jcl_list))
        
        self.text_area.setPlainText('\n'.join(unique_jcls))
        
        QMessageBox.information(
            self, "Başarılı",
            f"✅ Tekrarlar temizlendi!\n\n"
            f"Önceki: {len(jcl_list)} JCL\n"
            f"Sonraki: {len(unique_jcls)} JCL"
        )
    
    def do_search(self):
        """Aramayı başlat"""
        text = self.text_area.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, "Uyarı", "Lütfen en az bir JCL adı girin!")
            return
        
        self.jcl_list = self.parse_jcl_list(text)
        
        if not self.jcl_list:
            QMessageBox.warning(self, "Uyarı", "Geçerli JCL adı bulunamadı!")
            return
        
        # Onay
        unique_count = len(set(self.jcl_list))
        reply = QMessageBox.question(
            self, "Arama Onayı",
            f"🔍 {len(self.jcl_list)} JCL aranacak (Benzersiz: {unique_count})\n\n"
            "Devam edilsin mi?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.accept()
    
    def get_jcl_list(self):
        """Aranacak JCL listesini döndür"""
        return self.jcl_list