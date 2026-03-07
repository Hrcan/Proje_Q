"""
Test Runner - Tüm unit testleri çalıştır
"""
import unittest
import sys
import os

# Proje root'unu sys.path'e ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_all_tests():
    """Tüm testleri çalıştır ve sonuçları göster"""
    
    # Test loader
    loader = unittest.TestLoader()
    
    # Test suite
    suite = unittest.TestSuite()
    
    # Tests dizinindeki tüm testleri bul
    tests = loader.discover('tests', pattern='test_*.py')
    suite.addTests(tests)
    
    # Test runner - verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("=" * 70)
    print("PROJE_Q - UNIT TEST ÇALIŞTIRILIYOR")
    print("=" * 70)
    print()
    
    # Testleri çalıştır
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("TEST SONUÇLARI")
    print("=" * 70)
    print(f"Toplam Test: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print("=" * 70)
    
    # Exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())