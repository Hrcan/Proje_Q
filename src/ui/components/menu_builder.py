"""
Menü Oluşturucu - Ana menü çubuğu yönetimi
Proje_Q - JCL Veri Yönetim Sistemi
"""
from PyQt5.QtWidgets import QAction


class MenuBuilder:
    """Ana pencere için menü çubuğu oluşturucu"""
    
    def __init__(self, parent):
        """
        Args:
            parent: Ana pencere (MainWindow) referansı
        """
        self.parent = parent
    
    def build_menu_bar(self):
        """Tüm menüleri oluştur ve ana pencereye ekle"""
        menubar = self.parent.menuBar()
        
        # Menüleri oluştur
        self.build_file_menu(menubar)
        self.build_edit_menu(menubar)
        self.build_view_menu(menubar)
        self.build_tools_menu(menubar)
        self.build_help_menu(menubar)
    
    def build_file_menu(self, menubar):
        """Dosya menüsünü oluştur"""
        file_menu = menubar.addMenu('📁 Dosya')
        
        # Excel Yükle
        load_action = QAction('📂 Excel Yükle...', self.parent)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.parent.load_excel)
        file_menu.addAction(load_action)
        
        # Excel'e Aktar
        export_action = QAction('📊 Excel\'e Aktar...', self.parent)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.parent.export_to_excel)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Yedek Oluştur
        backup_action = QAction('💾 Yedek Oluştur...', self.parent)
        backup_action.triggered.connect(self.parent.create_backup_dialog)
        file_menu.addAction(backup_action)
        
        # Yedekten Geri Yükle
        restore_action = QAction('📥 Yedekten Geri Yükle...', self.parent)
        restore_action.triggered.connect(self.parent.restore_backup_dialog)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        # Çıkış
        exit_action = QAction('❌ Çıkış', self.parent)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.parent.close)
        file_menu.addAction(exit_action)
    
    def build_edit_menu(self, menubar):
        """Düzenle menüsünü oluştur"""
        edit_menu = menubar.addMenu('✏️ Düzenle')
        
        # Yenile
        refresh_action = QAction('🔄 Yenile', self.parent)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.parent.refresh_all)
        edit_menu.addAction(refresh_action)
        
        # Filtreleri Temizle
        clear_filters_action = QAction('🧹 Filtreleri Temizle', self.parent)
        clear_filters_action.setShortcut('Ctrl+R')
        clear_filters_action.triggered.connect(self.parent.clear_filters)
        edit_menu.addAction(clear_filters_action)
        
        edit_menu.addSeparator()
        
        # Veritabanını Temizle
        clear_db_action = QAction('🗑️ Veritabanını Temizle...', self.parent)
        clear_db_action.triggered.connect(self.parent.clear_database)
        edit_menu.addAction(clear_db_action)
    
    def build_view_menu(self, menubar):
        """Görünüm menüsünü oluştur"""
        view_menu = menubar.addMenu('👁️ Görünüm')
        
        # Tema alt menüsü
        theme_menu = view_menu.addMenu('🎨 Tema')
        
        # Açık Tema
        light_theme = QAction('☀️ Açık Tema', self.parent)
        light_theme.triggered.connect(lambda: self.parent.change_theme('light'))
        theme_menu.addAction(light_theme)
        
        # Koyu Tema
        dark_theme = QAction('🌙 Koyu Tema', self.parent)
        dark_theme.triggered.connect(lambda: self.parent.change_theme('dark'))
        theme_menu.addAction(dark_theme)
        
        # Mavi Tema
        blue_theme = QAction('🔵 Mavi Tema', self.parent)
        blue_theme.triggered.connect(lambda: self.parent.change_theme('blue'))
        theme_menu.addAction(blue_theme)
        
        view_menu.addSeparator()
        
        # İstatistikler
        stats_action = QAction('📈 İstatistikler', self.parent)
        stats_action.triggered.connect(self.parent.show_statistics)
        view_menu.addAction(stats_action)
    
    def build_tools_menu(self, menubar):
        """Araçlar menüsünü oluştur"""
        tools_menu = menubar.addMenu('🔧 Araçlar')
        
        # Ayarlar
        settings_action = QAction('⚙️ Ayarlar...', self.parent)
        settings_action.setShortcut('Ctrl+,')
        settings_action.triggered.connect(self.parent.show_settings)
        tools_menu.addAction(settings_action)
        
        tools_menu.addSeparator()
        
        # Logları Görüntüle
        logs_action = QAction('📋 Logları Görüntüle...', self.parent)
        logs_action.triggered.connect(self.parent.show_logs)
        tools_menu.addAction(logs_action)
        
        tools_menu.addSeparator()
        
        # Veritabanını Optimize Et
        optimize_action = QAction('⚡ Veritabanını Optimize Et', self.parent)
        optimize_action.triggered.connect(self.parent.optimize_database)
        tools_menu.addAction(optimize_action)
    
    def build_help_menu(self, menubar):
        """Yardım menüsünü oluştur"""
        help_menu = menubar.addMenu('❓ Yardım')
        
        # Kullanım Kılavuzu
        guide_action = QAction('📖 Kullanım Kılavuzu', self.parent)
        guide_action.setShortcut('F1')
        guide_action.triggered.connect(self.parent.show_user_guide)
        help_menu.addAction(guide_action)
        
        help_menu.addSeparator()
        
        # Hakkında
        about_action = QAction('ℹ️ Hakkında', self.parent)
        about_action.triggered.connect(self.parent.show_about)
        help_menu.addAction(about_action)