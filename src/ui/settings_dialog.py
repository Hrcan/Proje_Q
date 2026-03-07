"""
Ayarlar Dialogu
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpinBox, QCheckBox, QGroupBox,
                             QFormLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    """Uygulama ayarları"""
    
    def __init__(self, parent, preferences):
        super().__init__(parent)
        self.preferences = preferences
        
        self.setWindowTitle("⚙️ Ayarlar")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        self.init_ui()
    
    def init_ui(self):
        """Arayüzü oluştur"""
        layout = QVBoxLayout(self)
        
        # Başlık
        title = QLabel("⚙️ Uygulama Ayarları")
        title.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            padding: 10px;
            background-color: #2196F3;
            color: white;
            border-radius: 5px;
        """)
        layout.addWidget(title)
        
        # Görünüm Ayarları
        view_group = QGroupBox("🎨 Görünüm")
        view_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['light', 'dark', 'blue'])
        current_theme = self.preferences.get('theme', 'light')
        self.theme_combo.setCurrentText(current_theme)
        
        view_layout.addRow("Tema:", self.theme_combo)
        
        view_group.setLayout(view_layout)
        layout.addWidget(view_group)
        
        # Yedekleme Ayarları
        backup_group = QGroupBox("💾 Otomatik Yedekleme")
        backup_layout = QVBoxLayout()
        
        self.auto_backup_cb = QCheckBox("Otomatik yedeklemeyi etkinleştir")
        self.auto_backup_cb.setChecked(self.preferences.get('auto_backup', True))
        
        interval_layout = QHBoxLayout()
        interval_label = QLabel("Yedekleme aralığı (gün):")
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(1, 30)
        self.backup_interval.setValue(self.preferences.get('backup_interval_days', 7))
        
        interval_layout.addWidget(interval_label)
        interval_layout.addWidget(self.backup_interval)
        interval_layout.addStretch()
        
        backup_layout.addWidget(self.auto_backup_cb)
        backup_layout.addLayout(interval_layout)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        # Performans Ayarları
        perf_group = QGroupBox("⚡ Performans")
        perf_layout = QFormLayout()
        
        self.cache_size = QSpinBox()
        self.cache_size.setRange(16, 256)
        self.cache_size.setSingleStep(16)
        self.cache_size.setValue(64)
        self.cache_size.setSuffix(" MB")
        
        perf_layout.addRow("Cache boyutu:", self.cache_size)
        
        perf_group.setLayout(perf_layout)
        layout.addWidget(perf_group)
        
        # Bilgi
        info_label = QLabel(
            "ℹ️ Ayarlar değiştirildiğinde uygulamanın yeniden başlatılması gerekebilir."
        )
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Butonlar
        button_layout = QHBoxLayout()
        
        btn_reset = QPushButton("🔄 Varsayılana Dön")
        btn_reset.clicked.connect(self.reset_to_defaults)
        
        btn_save = QPushButton("💾 Kaydet")
        btn_save.clicked.connect(self.save_settings)
        btn_save.setStyleSheet("""
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
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        
        layout.addLayout(button_layout)
    
    def reset_to_defaults(self):
        """Varsayılan ayarlara dön"""
        reply = QMessageBox.question(
            self, "Onay",
            "Tüm ayarlar varsayılan değerlere döndürülsün mü?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.theme_combo.setCurrentText('light')
            self.auto_backup_cb.setChecked(True)
            self.backup_interval.setValue(7)
            self.cache_size.setValue(64)
    
    def save_settings(self):
        """Ayarları kaydet"""
        from utils.logger import app_logger
        
        old_theme = self.preferences.get('theme', 'light')
        new_theme = self.theme_combo.currentText()
        
        # Tema değişti mi?
        if old_theme != new_theme:
            app_logger.info(f"Tema değiştirildi: {old_theme} -> {new_theme}")
            self.preferences.set('theme', new_theme)
            # Parent'ın change_theme metodunu çağır
            if hasattr(self.parent(), 'change_theme'):
                self.parent().change_theme(new_theme)
        
        self.preferences.set('auto_backup', self.auto_backup_cb.isChecked())
        self.preferences.set('backup_interval_days', self.backup_interval.value())
        
        app_logger.info("Ayarlar kaydedildi")
        
        QMessageBox.information(self, "Başarılı", "✅ Ayarlar kaydedildi!")
        self.accept()
