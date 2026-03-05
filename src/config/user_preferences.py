"""
Kullanıcı Tercihleri Yönetimi
"""
import json
import os
from datetime import datetime


class UserPreferences:
    """Kullanıcı tercihlerini yöneten sınıf"""
    
    def __init__(self, config_file='config/user_prefs.json'):
        self.config_file = config_file
        self.preferences = self.load_preferences()
    
    def load_preferences(self):
        """Tercihleri yükle"""
        default_prefs = {
            'window': {
                'width': 1800,
                'height': 900,
                'x': 100,
                'y': 50
            },
            'filters': {
                'last_jcl': '',
                'last_ekip': 'Tümü',
                'last_ay': 'Tümü',
                'cb_hatali': True,
                'cb_uzun': True
            },
            'export': {
                'last_folder': '',
                'default_columns': []
            },
            'theme': 'light',
            'auto_backup': True,
            'backup_interval_days': 7,
            'last_backup': None
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Merge with defaults
                    for key in default_prefs:
                        if key not in loaded:
                            loaded[key] = default_prefs[key]
                    return loaded
            except Exception as e:
                print(f"Tercih yuklemede hata: {e}")
                return default_prefs
        
        return default_prefs
    
    def save_preferences(self):
        """Tercihleri kaydet"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.preferences, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Tercih kaydetmede hata: {e}")
            return False
    
    def get(self, key, default=None):
        """Tercih değeri al"""
        keys = key.split('.')
        value = self.preferences
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
    
    def set(self, key, value):
        """Tercih değeri ayarla"""
        keys = key.split('.')
        current = self.preferences
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
        self.save_preferences()
    
    def update_window_geometry(self, x, y, width, height):
        """Pencere geometrisini güncelle"""
        self.preferences['window'] = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        self.save_preferences()
    
    def update_filters(self, jcl='', ekip='Tümü', ay='Tümü', hatali=True, uzun=True):
        """Filtreleri güncelle"""
        self.preferences['filters'] = {
            'last_jcl': jcl,
            'last_ekip': ekip,
            'last_ay': ay,
            'cb_hatali': hatali,
            'cb_uzun': uzun
        }
        self.save_preferences()
    
    def update_backup_time(self):
        """Son yedekleme zamanını güncelle"""
        self.preferences['last_backup'] = datetime.now().isoformat()
        self.save_preferences()
    
    def needs_backup(self):
        """Yedekleme gerekli mi?"""
        if not self.preferences.get('auto_backup', True):
            return False
        
        last_backup = self.preferences.get('last_backup')
        if not last_backup:
            return True
        
        try:
            last_date = datetime.fromisoformat(last_backup)
            days_since = (datetime.now() - last_date).days
            interval = self.preferences.get('backup_interval_days', 7)
            return days_since >= interval
        except:
            return True