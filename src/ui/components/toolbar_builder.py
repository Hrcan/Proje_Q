"""
Toolbar Oluşturucu - Ana toolbar yönetimi
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import QAction, QToolBar


class ToolbarBuilder:
    """Ana pencere için toolbar oluşturucu"""
    
    def __init__(self, parent):
        """
        Args:
            parent: Ana pencere (MainWindow) referansı
        """
        self.parent = parent
    
    def build_toolbar(self):
        """Toolbar'ı oluştur ve ana pencereye ekle"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(toolbar.iconSize() * 1.5)
        self.parent.addToolBar(toolbar)
        
        # Toolbar butonlarını ekle
        self.add_file_actions(toolbar)
        toolbar.addSeparator()
        self.add_view_actions(toolbar)
    
    def add_file_actions(self, toolbar):
        """Dosya işlemleri butonları"""
        # Gelişmiş Arama - YENİ v0.6.0
        advanced_search_btn = QAction('🔍 Gelişmiş Arama', self.parent)
        advanced_search_btn.setToolTip('Gelişmiş arama penceresi (Ctrl+F)')
        advanced_search_btn.triggered.connect(self.parent.show_advanced_search)
        toolbar.addAction(advanced_search_btn)
        
        toolbar.addSeparator()
        
        # Excel Yükle
        load_btn = QAction('📂 Yükle', self.parent)
        load_btn.setToolTip('Excel dosyası yükle (Ctrl+O)')
        load_btn.triggered.connect(self.parent.load_excel)
        toolbar.addAction(load_btn)
        
        # Yenile
        refresh_btn = QAction('🔄 Yenile', self.parent)
        refresh_btn.setToolTip('Tabloları yenile (F5)')
        refresh_btn.triggered.connect(self.parent.refresh_all)
        toolbar.addAction(refresh_btn)
        
        toolbar.addSeparator()
        
        # Excel'e Aktar
        export_btn = QAction('📊 Aktar', self.parent)
        export_btn.setToolTip('Excel\'e aktar (Ctrl+E)')
        export_btn.triggered.connect(self.parent.export_to_excel)
        toolbar.addAction(export_btn)
        
        # Yedek Oluştur
        backup_btn = QAction('💾 Yedekle', self.parent)
        backup_btn.setToolTip('Veritabanı yedeği oluştur')
        backup_btn.triggered.connect(self.parent.create_backup_dialog)
        toolbar.addAction(backup_btn)
    
    def add_view_actions(self, toolbar):
        """Görünüm işlemleri butonları"""
        # İstatistikler
        stats_btn = QAction('📈 İstatistik', self.parent)
        stats_btn.setToolTip('İstatistikleri görüntüle')
        stats_btn.triggered.connect(self.parent.show_statistics)
        toolbar.addAction(stats_btn)
        
        # Ayarlar
        settings_btn = QAction('⚙️ Ayarlar', self.parent)
        settings_btn.setToolTip('Ayarları aç (Ctrl+,)')
        settings_btn.triggered.connect(self.parent.show_settings)
        toolbar.addAction(settings_btn)