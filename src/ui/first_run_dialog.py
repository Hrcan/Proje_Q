"""
İlk Çalıştırma Setup Wizard
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QFileDialog, QTextEdit, QGroupBox, QCheckBox,
    QStackedWidget, QWidget, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import os


class FirstRunDialog(QDialog):
    """İlk çalıştırma setup wizard'ı - Adım adım kurulum"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Proje_Q Kurulum Sihirbazı")
        self.setMinimumSize(750, 600)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        
        # Ayarlar
        self.settings = {
            'install_dir': os.path.join(os.path.expanduser('~'), 'Proje_Q'),
            'excel_folder': '',
            'auto_load': True,
            'create_backup': True,
            'create_desktop_shortcut': True
        }
        
        self.current_step = 0
        self.total_steps = 4
        
        self.setup_ui()
        self.update_navigation()
        
    def setup_ui(self):
        """UI oluştur"""
        layout = QVBoxLayout()
        
        # Başlık
        title_label = QLabel("Proje_Q Kurulum Sihirbazı")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2196F3; margin: 10px;")
        layout.addWidget(title_label)
        
        # İlerleme çubuğu
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.total_steps)
        self.progress_bar.setValue(1)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Adım %v / %m")
        layout.addWidget(self.progress_bar)
        
        layout.addSpacing(10)
        
        # Adım başlığı
        self.step_title = QLabel()
        step_font = QFont()
        step_font.setPointSize(12)
        step_font.setBold(True)
        self.step_title.setFont(step_font)
        self.step_title.setStyleSheet("color: #333; margin-bottom: 15px;")
        layout.addWidget(self.step_title)
        
        # Stacked widget (adımlar)
        self.pages = QStackedWidget()
        
        # Adım 1: Hoşgeldiniz
        self.pages.addWidget(self.create_welcome_page())
        
        # Adım 2: Kurulum Dizini
        self.pages.addWidget(self.create_install_dir_page())
        
        # Adım 3: Ayarlar
        self.pages.addWidget(self.create_settings_page())
        
        # Adım 4: Özet
        self.pages.addWidget(self.create_summary_page())
        
        layout.addWidget(self.pages)
        
        # Navigasyon butonları
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()
        
        self.back_btn = QPushButton("< Geri")
        self.back_btn.setMinimumWidth(100)
        self.back_btn.clicked.connect(self.previous_step)
        
        self.next_btn = QPushButton("İleri >")
        self.next_btn.setMinimumWidth(100)
        self.next_btn.setDefault(True)
        self.next_btn.clicked.connect(self.next_step)
        
        self.finish_btn = QPushButton("Kurulumu Tamamla")
        self.finish_btn.setMinimumWidth(150)
        self.finish_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.finish_btn.clicked.connect(self.finish_setup)
        self.finish_btn.hide()
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.next_btn)
        nav_layout.addWidget(self.finish_btn)
        
        layout.addLayout(nav_layout)
        
        self.setLayout(layout)
    
    def create_welcome_page(self):
        """Hoşgeldiniz sayfası"""
        page = QWidget()
        layout = QVBoxLayout()
        
        welcome_text = QTextEdit()
        welcome_text.setReadOnly(True)
        welcome_text.setHtml("""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #2196F3;">🎉 Proje_Q'ya Hoşgeldiniz!</h1>
            <p style="font-size: 14pt;"><b>JCL Veri Yönetim Sistemi v1.0.0</b></p>
        </div>
        
        <div style="padding: 20px;">
            <h2 style="color: #2196F3;">📋 Özellikler:</h2>
            <ul style="font-size: 11pt; line-height: 1.8;">
                <li><b>Hatalı İşler Takibi:</b> Excel'den hatalı JCL işlerini içe aktarın</li>
                <li><b>Uzun Süren İşler:</b> Performans sorunlarını tespit edin</li>
                <li><b>Gelişmiş Arama:</b> 5 farklı arama modu</li>
                <li><b>Toplu JCL Sorgulama:</b> Wildcard desteği ile toplu sorgular</li>
                <li><b>Export:</b> Excel ve CSV formatında dışa aktarma</li>
            </ul>
            
            <div style="background: #E3F2FD; padding: 15px; border-left: 4px solid #2196F3; margin-top: 20px;">
                <p style="margin: 0;"><b>ℹ️ Kurulum Süreci:</b></p>
                <p style="margin: 5px 0;">Bu sihirbaz sizi 4 adımda kurulum sürecinde yönlendirecektir:</p>
                <ol style="margin: 5px 0;">
                    <li>Hoşgeldiniz</li>
                    <li>Kurulum Dizini Seçimi</li>
                    <li>Ayarlar</li>
                    <li>Kurulum Özeti</li>
                </ol>
            </div>
            
            <p style="text-align: center; margin-top: 30px; font-size: 12pt;">
                <b>Devam etmek için "İleri" butonuna tıklayın.</b>
            </p>
        </div>
        """)
        
        layout.addWidget(welcome_text)
        page.setLayout(layout)
        return page
    
    def create_install_dir_page(self):
        """Kurulum dizini seçimi sayfası"""
        page = QWidget()
        layout = QVBoxLayout()
        
        info = QLabel("Proje_Q'nun kurulacağı dizini seçin:")
        info.setStyleSheet("font-size: 11pt; margin-bottom: 10px;")
        layout.addWidget(info)
        
        # Kurulum dizini seçimi
        install_group = QGroupBox("📁 Kurulum Dizini")
        install_layout = QVBoxLayout()
        
        dir_layout = QHBoxLayout()
        self.install_dir_edit = QLineEdit()
        self.install_dir_edit.setText(self.settings['install_dir'])
        self.install_dir_edit.setPlaceholderText("Kurulum dizini...")
        
        browse_btn = QPushButton("Gözat...")
        browse_btn.clicked.connect(self.browse_install_dir)
        browse_btn.setMinimumWidth(100)
        
        dir_layout.addWidget(self.install_dir_edit)
        dir_layout.addWidget(browse_btn)
        install_layout.addLayout(dir_layout)
        
        # Bilgi
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setMaximumHeight(200)
        info_text.setHtml("""
        <div style="padding: 10px;">
            <p><b>ℹ️ Kurulum Hakkında:</b></p>
            <ul>
                <li>Seçilen dizinde <b>Proje_Q</b> klasörü oluşturulacak</li>
                <li>Aşağıdaki alt klasörler otomatik oluşturulacak:
                    <ul>
                        <li><b>database/</b> - Veritabanı dosyaları</li>
                        <li><b>logs/</b> - Log dosyaları</li>
                        <li><b>backup/</b> - Yedek dosyaları</li>
                        <li><b>config/</b> - Ayar dosyaları</li>
                    </ul>
                </li>
                <li>Toplam yaklaşık disk alanı: <b>100-150 MB</b></li>
            </ul>
        </div>
        """)
        install_layout.addWidget(info_text)
        
        install_group.setLayout(install_layout)
        layout.addWidget(install_group)
        
        # Desktop shortcut
        self.desktop_shortcut_check = QCheckBox("Masaüstü kısayolu oluştur")
        self.desktop_shortcut_check.setChecked(True)
        self.desktop_shortcut_check.setStyleSheet("font-size: 11pt; margin-top: 10px;")
        layout.addWidget(self.desktop_shortcut_check)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_settings_page(self):
        """Ayarlar sayfası"""
        page = QWidget()
        layout = QVBoxLayout()
        
        # Excel klasörü
        excel_group = QGroupBox("📂 Excel Dosyaları (İsteğe Bağlı)")
        excel_layout = QVBoxLayout()
        
        excel_info = QLabel("Excel dosyalarınızın varsayılan konumunu belirleyebilirsiniz:")
        excel_info.setStyleSheet("color: #666; margin-bottom: 5px;")
        excel_layout.addWidget(excel_info)
        
        folder_layout = QHBoxLayout()
        self.excel_folder_edit = QLineEdit()
        self.excel_folder_edit.setPlaceholderText("Belirtilmediyse her seferinde sorulacak...")
        
        excel_browse_btn = QPushButton("Gözat...")
        excel_browse_btn.clicked.connect(self.browse_excel_folder)
        excel_browse_btn.setMinimumWidth(100)
        
        folder_layout.addWidget(self.excel_folder_edit)
        folder_layout.addWidget(excel_browse_btn)
        excel_layout.addLayout(folder_layout)
        
        excel_group.setLayout(excel_layout)
        layout.addWidget(excel_group)
        
        # Genel ayarlar
        general_group = QGroupBox("⚙️ Genel Ayarlar")
        general_layout = QVBoxLayout()
        
        self.auto_load_check = QCheckBox("Başlangıçta son kullanılan veritabanını otomatik yükle")
        self.auto_load_check.setChecked(True)
        general_layout.addWidget(self.auto_load_check)
        
        self.backup_check = QCheckBox("Veri güncellemelerinde otomatik yedek oluştur")
        self.backup_check.setChecked(True)
        general_layout.addWidget(self.backup_check)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        layout.addStretch()
        page.setLayout(layout)
        return page
    
    def create_summary_page(self):
        """Özet sayfası"""
        page = QWidget()
        layout = QVBoxLayout()
        
        summary_label = QLabel("Kurulum özeti:")
        summary_label.setStyleSheet("font-size: 11pt; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(summary_label)
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)
        
        page.setLayout(layout)
        return page
    
    def browse_install_dir(self):
        """Kurulum dizini seç"""
        parent_dir = QFileDialog.getExistingDirectory(
            self,
            "Proje_Q Kurulum Dizinini Seçin",
            os.path.expanduser('~'),
            QFileDialog.ShowDirsOnly
        )
        if parent_dir:
            # Direkt seçilen dizini kullan (Proje_Q ekleme)
            self.install_dir_edit.setText(parent_dir)
    
    def browse_excel_folder(self):
        """Excel klasörü seç"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Excel Dosyaları Klasörünü Seçin",
            "",
            QFileDialog.ShowDirsOnly
        )
        if folder:
            self.excel_folder_edit.setText(folder)
    
    def update_navigation(self):
        """Navigasyon butonlarını güncelle"""
        self.pages.setCurrentIndex(self.current_step)
        self.progress_bar.setValue(self.current_step + 1)
        
        # Adım başlıklarını güncelle
        titles = [
            "Adım 1/4: Hoşgeldiniz",
            "Adım 2/4: Kurulum Dizini",
            "Adım 3/4: Ayarlar",
            "Adım 4/4: Kurulum Özeti"
        ]
        self.step_title.setText(titles[self.current_step])
        
        # Buton görünürlüğü
        self.back_btn.setEnabled(self.current_step > 0)
        
        if self.current_step == self.total_steps - 1:
            # Son adım - Özeti göster
            self.update_summary()
            self.next_btn.hide()
            self.finish_btn.show()
        else:
            self.next_btn.show()
            self.finish_btn.hide()
    
    def update_summary(self):
        """Özet sayfasını güncelle"""
        install_dir = self.install_dir_edit.text() or self.settings['install_dir']
        excel_folder = self.excel_folder_edit.text() or "Belirtilmedi"
        desktop_shortcut = "Evet" if self.desktop_shortcut_check.isChecked() else "Hayır"
        auto_load = "Evet" if self.auto_load_check.isChecked() else "Hayır"
        auto_backup = "Evet" if self.backup_check.isChecked() else "Hayır"
        
        summary_html = f"""
        <div style="padding: 15px;">
            <h2 style="color: #2196F3;">📋 Kurulum Özeti</h2>
            
            <div style="background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="color: #333; margin-top: 0;">📍 Kurulum Bilgileri</h3>
                <table style="width: 100%; font-size: 11pt;">
                    <tr>
                        <td style="padding: 5px;"><b>Kurulum Dizini:</b></td>
                        <td style="padding: 5px; color: #2196F3;">{install_dir}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Masaüstü Kısayolu:</b></td>
                        <td style="padding: 5px;">{desktop_shortcut}</td>
                    </tr>
                </table>
            </div>
            
            <div style="background: #E3F2FD; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <h3 style="color: #333; margin-top: 0;">⚙️ Ayarlar</h3>
                <table style="width: 100%; font-size: 11pt;">
                    <tr>
                        <td style="padding: 5px;"><b>Excel Klasörü:</b></td>
                        <td style="padding: 5px;">{excel_folder}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Otomatik Yükleme:</b></td>
                        <td style="padding: 5px;">{auto_load}</td>
                    </tr>
                    <tr>
                        <td style="padding: 5px;"><b>Otomatik Yedekleme:</b></td>
                        <td style="padding: 5px;">{auto_backup}</td>
                    </tr>
                </table>
            </div>
            
            <div style="background: #FFF3E0; padding: 15px; border-radius: 5px; border-left: 4px solid #FF9800;">
                <p style="margin: 0;"><b>⚡ Kurulum Yapılacak İşlemler:</b></p>
                <ul style="margin: 10px 0;">
                    <li>Kurulum dizini oluşturulacak</li>
                    <li>Program dosyaları kopyalanacak</li>
                    <li>Alt klasörler oluşturulacak (database, logs, backup, config)</li>
                    <li>Ayarlar kaydedilecek</li>
                    {f'<li>Masaüstü kısayolu oluşturulacak</li>' if desktop_shortcut == "Evet" else ''}
                </ul>
            </div>
            
            <p style="text-align: center; margin-top: 30px; font-size: 12pt; color: #4CAF50;">
                <b>✓ Kuruluma başlamak için "Kurulumu Tamamla" butonuna tıklayın.</b>
            </p>
        </div>
        """
        
        self.summary_text.setHtml(summary_html)
    
    def next_step(self):
        """Sonraki adım"""
        if self.current_step < self.total_steps - 1:
            # Adım 2'den 3'e geçerken (Kurulum Dizini -> Ayarlar)
            if self.current_step == 1:
                # Excel klasörünü otomatik doldur
                if not self.excel_folder_edit.text():
                    install_dir = self.install_dir_edit.text() or self.settings['install_dir']
                    data_excel_path = os.path.join(install_dir, 'Data', 'Excel')
                    self.excel_folder_edit.setText(data_excel_path)
                    self.excel_folder_edit.setPlaceholderText(data_excel_path)
            
            self.current_step += 1
            self.update_navigation()
    
    def previous_step(self):
        """Önceki adım"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_navigation()
    
    def finish_setup(self):
        """Kurulumu tamamla"""
        # Ayarları kaydet
        self.settings['install_dir'] = self.install_dir_edit.text() or self.settings['install_dir']
        self.settings['excel_folder'] = self.excel_folder_edit.text()
        self.settings['auto_load'] = self.auto_load_check.isChecked()
        self.settings['create_backup'] = self.backup_check.isChecked()
        self.settings['create_desktop_shortcut'] = self.desktop_shortcut_check.isChecked()
        
        # Kurulum dizinini oluştur
        install_dir = self.settings['install_dir']
        try:
            os.makedirs(install_dir, exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'database'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'logs'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'backup'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'config'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'Data'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'Data', 'Excel'), exist_ok=True)
            os.makedirs(os.path.join(install_dir, 'Data', 'TXT-jpeg'), exist_ok=True)
            
            # Excel default klasörünü Data/Excel yap
            if not self.settings['excel_folder']:
                self.settings['excel_folder'] = os.path.join(install_dir, 'Data', 'Excel')
            
            # Masaüstü kısayolu oluştur
            if self.settings['create_desktop_shortcut']:
                self.create_desktop_shortcut(install_dir)
                
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Hata", f"Kurulum dizini oluşturulamadı:\n{str(e)}")
            return
        
        self.accept()
    
    def create_desktop_shortcut(self, install_dir):
        """Masaüstü kısayolu oluştur"""
        try:
            import sys
            
            # EXE yolu
            if getattr(sys, 'frozen', False):
                # PyInstaller ile çalışıyorsa
                exe_path = sys.executable
            else:
                # Development modda
                exe_path = os.path.join(install_dir, 'Proje_Q.exe')
            
            # Masaüstü yolu
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            shortcut_path = os.path.join(desktop, 'Proje_Q.lnk')
            
            # Windows shortcut oluştur (win32com kullanarak)
            try:
                import win32com.client
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = exe_path
                shortcut.WorkingDirectory = install_dir
                shortcut.IconLocation = exe_path
                shortcut.Description = "Proje_Q - JCL Veri Yönetim Sistemi"
                shortcut.save()
            except ImportError:
                # win32com yoksa, basit bir batch scripti oluştur
                batch_path = os.path.join(desktop, 'Proje_Q.bat')
                with open(batch_path, 'w') as f:
                    f.write(f'@echo off\n')
                    f.write(f'cd /d "{install_dir}"\n')
                    f.write(f'start "" "{exe_path}"\n')
        except Exception:
            # Kısayol oluşturulamazsa sessizce geç (kritik değil)
            pass
    
    def get_settings(self):
        """Ayarları al"""
        return self.settings