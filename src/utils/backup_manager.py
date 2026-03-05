"""
Veritabanı Yedekleme ve Geri Yükleme
"""
import os
import shutil
import sqlite3
from datetime import datetime
import zipfile


class BackupManager:
    """Veritabanı backup/restore yöneticisi"""
    
    def __init__(self, db_path='database/jcl_data.db', backup_dir='backup'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
    
    def create_backup(self, description=''):
        """Yedek oluştur"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"backup_{timestamp}.zip"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Veritabanını kopyala
            temp_db = f"temp_{timestamp}.db"
            shutil.copy2(self.db_path, temp_db)
            
            # Zip dosyası oluştur
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_db, 'jcl_data.db')
                
                # Metadata ekle
                metadata = {
                    'timestamp': timestamp,
                    'description': description,
                    'db_size': os.path.getsize(self.db_path)
                }
                zipf.writestr('metadata.txt', str(metadata))
            
            # Temp dosyayı sil
            os.remove(temp_db)
            
            return True, backup_path
        except Exception as e:
            return False, str(e)
    
    def restore_backup(self, backup_file):
        """Yedekten geri yükle"""
        try:
            # Önce mevcut veritabanını yedekle
            safety_backup = f"{self.db_path}.safety_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(self.db_path, safety_backup)
            
            # Zip'ten çıkar
            with zipfile.ZipFile(backup_file, 'r') as zipf:
                zipf.extract('jcl_data.db', 'temp_restore')
            
            # Veritabanını değiştir
            restored_db = 'temp_restore/jcl_data.db'
            shutil.copy2(restored_db, self.db_path)
            
            # Temp klasörü temizle
            shutil.rmtree('temp_restore')
            
            return True, "Başarılı"
        except Exception as e:
            # Hata durumunda eski veritabanını geri yükle
            if os.path.exists(safety_backup):
                shutil.copy2(safety_backup, self.db_path)
            return False, str(e)
    
    def list_backups(self):
        """Yedekleri listele"""
        backups = []
        
        if not os.path.exists(self.backup_dir):
            return backups
        
        for file in os.listdir(self.backup_dir):
            if file.endswith('.zip') and file.startswith('backup_'):
                file_path = os.path.join(self.backup_dir, file)
                stat = os.stat(file_path)
                
                # Timestamp'i parse et
                try:
                    timestamp_str = file.replace('backup_', '').replace('.zip', '')
                    timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                except:
                    timestamp = datetime.fromtimestamp(stat.st_mtime)
                
                backups.append({
                    'filename': file,
                    'path': file_path,
                    'size': stat.st_size,
                    'date': timestamp,
                    'date_str': timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
        
        # En yeni önce
        backups.sort(key=lambda x: x['date'], reverse=True)
        return backups
    
    def delete_backup(self, backup_file):
        """Yedek sil"""
        try:
            os.remove(backup_file)
            return True, "Silindi"
        except Exception as e:
            return False, str(e)
    
    def get_db_stats(self):
        """Veritabanı istatistikleri"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tablo sayıları
            cursor.execute("SELECT COUNT(*) FROM hatali_isler")
            hatali_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM uzun_isler")
            uzun_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM yukleme_gecmisi")
            yukleme_count = cursor.fetchone()[0]
            
            conn.close()
            
            # Dosya boyutu
            db_size = os.path.getsize(self.db_path)
            
            return {
                'hatali_isler': hatali_count,
                'uzun_isler': uzun_count,
                'yukleme_gecmisi': yukleme_count,
                'db_size': db_size,
                'db_size_mb': round(db_size / (1024 * 1024), 2)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def auto_cleanup_old_backups(self, keep_count=10):
        """Eski yedekleri temizle (en son X tanesini tut)"""
        backups = self.list_backups()
        
        if len(backups) <= keep_count:
            return 0
        
        deleted = 0
        for backup in backups[keep_count:]:
            success, _ = self.delete_backup(backup['path'])
            if success:
                deleted += 1
        
        return deleted