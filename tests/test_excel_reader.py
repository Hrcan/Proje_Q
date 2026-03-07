"""
ExcelReader Unit Tests
"""
import unittest
import os
from src.utils.excel_reader import (
    ExcelReader, 
    ExcelReaderError, 
    InvalidFileFormatError,
    EmptySheetError
)


class TestExcelReader(unittest.TestCase):
    """ExcelReader test sınıfı"""
    
    def test_invalid_file_path(self):
        """Geçersiz dosya yolu test et"""
        with self.assertRaises(FileNotFoundError):
            ExcelReader('nonexistent_file.xlsx')
    
    def test_invalid_file_format(self):
        """Geçersiz dosya formatı test et"""
        with self.assertRaises(InvalidFileFormatError):
            ExcelReader('test.txt')
    
    def test_detect_rapor_tipi_hatali(self):
        """Hatalı rapor tipinin algılanması"""
        # Test için geçici bir dosya yolu (var olmasa bile)
        reader = ExcelReader.__new__(ExcelReader)
        reader.file_name = 'SAO_Hatalı_Biten_İşler.xlsx'
        rapor_tipi = reader._detect_rapor_tipi()
        self.assertEqual(rapor_tipi, 'HATALI')
    
    def test_detect_rapor_tipi_uzun(self):
        """Uzun rapor tipinin algılanması"""
        reader = ExcelReader.__new__(ExcelReader)
        reader.file_name = 'SAO_Uzun_Süren_İşler.xlsx'
        rapor_tipi = reader._detect_rapor_tipi()
        self.assertEqual(rapor_tipi, 'UZUN')
    
    def test_extract_ay_aralik(self):
        """Ay çıkarma - ARALIK"""
        reader = ExcelReader.__new__(ExcelReader)
        reader.file_name = 'Rapor_ARALIK_2024.xlsx'
        ay = reader._extract_ay()
        self.assertEqual(ay, '2024-12')
    
    def test_extract_ay_ocak(self):
        """Ay çıkarma - OCAK"""
        reader = ExcelReader.__new__(ExcelReader)
        reader.file_name = 'Rapor_OCAK_2025.xlsx'
        ay = reader._extract_ay()
        self.assertEqual(ay, '2025-01')
    
    def test_safe_int_valid(self):
        """_safe_int - geçerli değer"""
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_int(42)
        self.assertEqual(result, 42)
    
    def test_safe_int_none(self):
        """_safe_int - None değer"""
        import pandas as pd
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_int(pd.NA)
        self.assertIsNone(result)
    
    def test_safe_int_invalid(self):
        """_safe_int - geçersiz değer"""
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_int('invalid')
        self.assertIsNone(result)
    
    def test_safe_str_valid(self):
        """_safe_str - geçerli değer"""
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_str('  test  ')
        self.assertEqual(result, 'test')
    
    def test_safe_str_none(self):
        """_safe_str - None değer"""
        import pandas as pd
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_str(pd.NA)
        self.assertIsNone(result)
    
    def test_safe_date_valid(self):
        """_safe_date - geçerli tarih"""
        import pandas as pd
        reader = ExcelReader.__new__(ExcelReader)
        date = pd.Timestamp('2024-12-15')
        result = reader._safe_date(date)
        self.assertEqual(result, '2024-12-15')
    
    def test_safe_date_none(self):
        """_safe_date - None değer"""
        import pandas as pd
        reader = ExcelReader.__new__(ExcelReader)
        result = reader._safe_date(pd.NA)
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()