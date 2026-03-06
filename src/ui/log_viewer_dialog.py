"""
Log Görüntüleyici Dialogu
"""
import os
from datetime import datetime
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTextEdit, QLabel, QComboBox, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LogViewerDialog(QDialog):
    """Sistem loglarını görüntüle"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.log_dir = "logs"
        
        self.setWindowTitle("📋 Log Görüntüleyici")
        self.setModal(True)
        self.setMinimumSize(900, 600)
        
        self.init_ui()
        self.center_on_screen()
        self.load_logs()
    
    def center_on_screen(self):
        """Dialogu ekranın ortasında aç"""
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
        title = QLabel("📋 Sistem Logları")
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
        
        # Üst kontroller
        controls_layout = QHBoxLayout()
        
        # Log tipi seçimi
        type_label = QLabel("Log Tipi:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Tüm Loglar", "INFO", "WARNING", "ERROR"])
        self.type_combo.currentTextChanged.connect(self.filter_logs)
        
        # Yenile butonu
        btn_refresh = QPushButton("🔄 Yenile")
        btn_refresh.clicked.connect(self.load_logs)
        btn_refresh.setFixedWidth(100)
        
        # Temizle butonu
        btn_clear = QPushButton("🗑️ Temizle")
        btn_clear.clicked.connect(self.clear_logs)
        btn_clear.setFixedWidth(100)
        
        # Export butonu
        btn_export = QPushButton("💾 Export")
        btn_export.clicked.connect(self.export_logs)
        btn_export.setFixedWidth(100)
        
        controls_layout.addWidget(type_label)
        controls_layout.addWidget(self.type_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(btn_refresh)
        controls_layout.addWidget(btn_clear)
        controls_layout.addWidget(btn_export)
        
        layout.addLayout(controls_layout)
        
        # Log görüntüleme alanı
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 2px solid #2196F3;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.log_text)
        
        # Alt bilgi
        self.info_label = QLabel()
        self.info_label.setStyleSheet("padding: 5px; color: #666;")
        layout.addWidget(self.info_label)
        
        # Kapat butonu
        button_layout = QHBoxLayout()
        btn_close = QPushButton("✅ Kapat")
        btn_close.clicked.connect(self.accept)
        btn_close.setStyleSheet("""
            QPushButton {
                padding: 10px 30px;
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
        button_layout.addStretch()
        button_layout.addWidget(btn_close)
        layout.addLayout(button_layout)
    
    def load_logs(self):
        """Logları yükle - GERÇEKgerçek log dosyasından"""
        try:
            logs = []
            
            # Log dosyasını oku
            log_file = os.path.join(self.log_dir, "app.log")
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    file_logs = f.readlines()
                    logs = [line.strip() for line in file_logs if line.strip()]
                
                if not logs:
                    logs = [f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Log dosyası boş"]
            else:
                logs = [f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Log dosyası henüz oluşturulmamış"]
                logs.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Uygulama işlemlerini yapmaya başladığınızda loglar burada görünecek")
            
            # Ters sırada göster (en yeni üstte)
            logs.reverse()
            
            # Logları göster
            self.all_logs = logs
            self.filter_logs()
            
            # Bilgi güncelle
            self.info_label.setText(f"📊 Toplam {len(logs)} log kaydı yüklendi")
            
        except Exception as e:
            QMessageBox.warning(self, "Uyarı", f"Log yükleme hatası: {e}")
            self.log_text.setPlainText(f"⚠️ Log yüklenemedi: {e}")
    
    def filter_logs(self):
        """Logları filtrele"""
        filter_type = self.type_combo.currentText()
        
        if filter_type == "Tüm Loglar":
            filtered = self.all_logs
        else:
            # INFO, WARNING, ERROR
            filtered = [log for log in self.all_logs if f"[{filter_type}]" in log]
        
        # Renklendirme ile göster
        html_logs = []
        for log in filtered:
            if "[ERROR]" in log:
                html_logs.append(f'<span style="color: #ff6b6b;">{log}</span>')
            elif "[WARNING]" in log:
                html_logs.append(f'<span style="color: #ffa500;">{log}</span>')
            elif "[INFO]" in log:
                html_logs.append(f'<span style="color: #51cf66;">{log}</span>')
            else:
                html_logs.append(f'<span style="color: #d4d4d4;">{log}</span>')
        
        self.log_text.setHtml("<br>".join(html_logs))
        
        # Bilgi güncelle
        self.info_label.setText(
            f"📊 Toplam {len(self.all_logs)} log | Gösterilen: {len(filtered)}"
        )
    
    def clear_logs(self):
        """Logları temizle"""
        reply = QMessageBox.question(
            self, "Onay",
            "Tüm log kayıtlarını silmek istediğinize emin misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                log_file = os.path.join(self.log_dir, "app.log")
                if os.path.exists(log_file):
                    os.remove(log_file)
                
                self.log_text.clear()
                self.info_label.setText("✅ Loglar temizlendi")
                QMessageBox.information(self, "Başarılı", "Log kayıtları temizlendi!")
                
                # Yeniden yükle
                self.load_logs()
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Log temizleme hatası: {e}")
    
    def export_logs(self):
        """Logları dosyaya aktar"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Log Dosyası Kaydet",
                f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Text Files (*.txt);;All Files (*)"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.all_logs))
                
                QMessageBox.information(self, "Başarılı", f"Loglar kaydedildi:\n{file_path}")
                self.info_label.setText(f"✅ Loglar export edildi: {os.path.basename(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Export hatası: {e}")