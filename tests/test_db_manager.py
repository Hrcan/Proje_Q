"""
DatabaseManager Unit Tests
"""
import unittest
import os
import sqlite3
from src.database.db_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """DatabaseManager test sınıfı"""
    
    def setUp(self):
        """Her test öncesi çalışır"""
        # Test için in-memory database kullan
        self.db = DatabaseManager(':memory:')
        self.db.connect()
        self.db.create_tables()
    
    def tearDown(self):
        """Her test sonrası çalışır"""
        self.db.disconnect()
    
    def test_create_tables(self):
        """Tabloların doğru oluşturulduğunu test et"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabloları kontrol et
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN ('hatali_isler', 'uzun_isler', 'yukleme_gecmisi')
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            self.assertEqual(len(tables), 3)
            self.assertIn('hatali_isler', tables)
            self.assertIn('uzun_isler', tables)
            self.assertIn('yukleme_gecmisi', tables)
    
    def test_insert_hatali_is(self):
        """Hatalı iş eklemeyi test et"""
        data = {
            'jcl_adi': 'TEST_JCL_001',
            'ay': '2024-12',
            'sheet_adi': 'Sheet1',
            'hatali_sayi_ay': 5,
            'sorumlu_ekip': 'Test Ekip'
        }
        
        result = self.db.insert_hatali_is(data)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)
        
        # Verinin eklendiğini kontrol et
        records = self.db.get_all_hatali_isler()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['jcl_adi'], 'TEST_JCL_001')
    
    def test_insert_uzun_is(self):
        """Uzun iş eklemeyi test et"""
        data = {
            'jcl_adi': 'TEST_JCL_002',
            'ay': '2024-12',
            'sheet_adi': 'Sheet1',
            'calisma_sayisi': 10,
            'calisma_suresi': 120,
            'sorumlu_ekip': 'Test Ekip'
        }
        
        result = self.db.insert_uzun_is(data)
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)
        
        # Verinin eklendiğini kontrol et
        records = self.db.get_all_uzun_isler()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['jcl_adi'], 'TEST_JCL_002')
    
    def test_duplicate_insert(self):
        """Duplicate insert durumunu test et (REPLACE)"""
        data = {
            'jcl_adi': 'TEST_JCL_003',
            'ay': '2024-12',
            'sheet_adi': 'Sheet1',
            'hatali_sayi_ay': 5
        }
        
        # İlk insert
        self.db.insert_hatali_is(data)
        
        # Aynı kayıt (güncelleme)
        data['hatali_sayi_ay'] = 10
        self.db.insert_hatali_is(data)
        
        # Hala 1 kayıt olmalı (REPLACE)
        records = self.db.get_all_hatali_isler()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['hatali_sayi_ay'], 10)
    
    def test_missing_required_fields(self):
        """Gerekli alanların eksik olması durumunu test et"""
        data = {
            'jcl_adi': 'TEST_JCL_004',
            # 'ay' eksik
            'sheet_adi': 'Sheet1'
        }
        
        with self.assertRaises(ValueError):
            self.db.insert_hatali_is(data)
    
    def test_get_tablo_istatistikleri(self):
        """İstatistik fonksiyonunu test et"""
        # Birkaç kayıt ekle
        self.db.insert_hatali_is({
            'jcl_adi': 'JCL_1',
            'ay': '2024-12',
            'sheet_adi': 'Sheet1'
        })
        
        self.db.insert_uzun_is({
            'jcl_adi': 'JCL_2',
            'ay': '2024-12',
            'sheet_adi': 'Sheet1'
        })
        
        stats = self.db.get_tablo_istatistikleri()
        
        self.assertEqual(stats['hatali_isler'], 1)
        self.assertEqual(stats['uzun_isler'], 1)
        self.assertEqual(stats['yukleme_gecmisi'], 0)
    
    def test_lock_mechanism(self):
        """
        Lock mekanizmasını test et
        
        Not: Threading.Lock()'un varlığını kontrol ediyoruz.
        Gerçek thread-safety production ortamında test edilir.
        """
        # Lock objesinin var olduğunu kontrol et
        self.assertTrue(hasattr(self.db, '_lock'))
        self.assertIsInstance(self.db._lock, type(__import__('threading').Lock()))
        
        # Context manager'ın çalıştığını kontrol et
        with self.db.get_connection() as conn:
            self.assertIsNotNone(conn)
            # Connection'ın cursor oluşturabildiğini kontrol et
            cursor = conn.cursor()
            self.assertIsNotNone(cursor)


if __name__ == '__main__':
    unittest.main()