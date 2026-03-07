"""
Excel Okuyucu - İyileştirilmiş Error Handling + Type Hints
Excel dosyalarını okuyup veritabanına hazır hale getiren modül
"""
import pandas as pd
import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import os


class ExcelReaderError(Exception):
    """Excel okuma ile ilgili özel hata sınıfı"""
    pass


class InvalidFileFormatError(ExcelReaderError):
    """Geçersiz dosya formatı hatası"""
    pass


class EmptySheetError(ExcelReaderError):
    """Boş sheet hatası"""
    pass


class ExcelReader:
    """
    Excel dosyalarını okuyan sınıf - Type-safe ve Error-safe
    
    Features:
        - Automatic report type detection
        - Month extraction from filename
        - Type hints for all methods
        - Specific exception handling
        - Data validation
    
    Raises:
        FileNotFoundError: Dosya bulunamazsa
        InvalidFileFormatError: Geçersiz Excel formatı
        EmptySheetError: Boş sheet varsa
        pd.errors.EmptyDataError: Excel verisi boşsa
    """
    
    def __init__(self, file_path: str):
        """
        Args:
            file_path: Excel dosya yolu
            
        Raises:
            FileNotFoundError: Dosya mevcut değilse
            InvalidFileFormatError: Dosya Excel formatında değilse
        """
        # Önce format kontrolü yap (dosya yoksa bile)
        if not file_path.lower().endswith(('.xlsx', '.xls')):
            raise InvalidFileFormatError(
                f"Geçersiz dosya formatı: {file_path}. "
                "Sadece .xlsx ve .xls dosyaları desteklenir."
            )
        
        # Sonra dosya varlığını kontrol et
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")
        
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
        self.rapor_tipi = self._detect_rapor_tipi()
        self.ay = self._extract_ay()
    
    def _detect_rapor_tipi(self) -> str:
        """
        Dosya adından rapor tipini belirle
        
        Returns:
            str: 'HATALI', 'UZUN' veya 'BILINMEYEN'
        """
        file_upper = self.file_name.upper()
        
        if 'HATALI' in file_upper or 'HATALI' in file_upper:
            return 'HATALI'
        elif 'UZUN' in file_upper:
            return 'UZUN'
        
        return 'BILINMEYEN'
    
    def _extract_ay(self) -> str:
        """
        Dosya adından ay bilgisini çıkar (YYYY-MM formatında)
        
        Returns:
            str: Ay bilgisi (YYYY-MM formatında)
        
        Examples:
            >>> reader = ExcelReader('Rapor_ARALIK_2024.xlsx')
            >>> reader._extract_ay()
            '2024-12'
        """
        # Türkçe ay isimleri ve karşılıkları
        aylar = {
            'OCAK': '01', 'SUBAT': '02', 'ŞUBAT': '02',
            'MART': '03', 'NISAN': '04', 'MAYIS': '05',
            'HAZIRAN': '06', 'TEMMUZ': '07', 
            'AGUSTOS': '08', 'AĞUSTOS': '08',
            'EYLUL': '09', 'EYLÜL': '09', 
            'EKIM': '10', 'EKİM': '10',
            'KASIM': '11', 'ARALIK': '12'
        }
        
        # Yıl bul (4 basamaklı sayı)
        yil_match = re.search(r'(20\d{2})', self.file_name)
        yil = yil_match.group(1) if yil_match else '2024'
        
        # Ay bul
        file_upper = self.file_name.upper()
        for ay_adi, ay_no in aylar.items():
            if ay_adi in file_upper:
                return f"{yil}-{ay_no}"
        
        # Bulunamazsa varsayılan
        return f"{yil}-01"
    
    def get_sheet_names(self) -> List[str]:
        """
        Sheet isimlerini getir
        
        Returns:
            List[str]: Sheet isimlerinin listesi
            
        Raises:
            pd.errors.EmptyDataError: Excel dosyası boşsa
            ValueError: Excel dosyası okunamazsa
        """
        try:
            xl_file = pd.ExcelFile(self.file_path)
            return xl_file.sheet_names
        
        except pd.errors.EmptyDataError as e:
            raise EmptySheetError(f"Excel dosyası boş: {self.file_name}") from e
        
        except Exception as e:
            raise ValueError(
                f"Excel dosyası okunamadı: {self.file_name}. Hata: {str(e)}"
            ) from e
    
    def read_hatali_isler_sheet(self, sheet_name: str) -> List[Dict]:
        """
        Hatalı işler sheet'ini oku
        
        Args:
            sheet_name: Sheet adı
            
        Returns:
            List[Dict]: Kayıt listesi
            
        Raises:
            ValueError: Sheet okunamazsa
            KeyError: Beklenen kolonlar yoksa
        """
        try:
            df = pd.read_excel(
                self.file_path, 
                sheet_name=sheet_name, 
                header=0
            )
            
            # Kolon sayısı kontrolü
            if len(df.columns) < 5:
                raise ValueError(
                    f"Sheet '{sheet_name}' yetersiz kolon sayısına sahip. "
                    f"Beklenen: en az 5, Bulunan: {len(df.columns)}"
                )
            
            kayitlar = []
            for idx, row in df.iterrows():
                try:
                    # NaN kontrolü - JCL adı boşsa atla
                    if pd.isna(row.iloc[0]):
                        continue
                    
                    # Veri validasyonu
                    jcl_adi = str(row.iloc[0]).strip()
                    if not jcl_adi or len(jcl_adi) == 0:
                        continue
                    
                    kayit = {
                        'jcl_adi': jcl_adi,
                        'ay': self.ay,
                        'sheet_adi': sheet_name,
                        'hatali_sayi_ay': self._safe_int(row.iloc[1]),
                        'son_hatali_tarih': self._safe_date(row.iloc[2]),
                        'hatali_sayi_yil': self._safe_int(row.iloc[3]),
                        'sorumlu_ekip': self._safe_str(row.iloc[4]),
                        'kaynak_dosya': self.file_name
                    }
                    kayitlar.append(kayit)
                
                except Exception as e:
                    # Satır hatalarını logla ama devam et
                    print(f"Satır {idx} atlandı: {str(e)}")
                    continue
            
            return kayitlar
        
        except pd.errors.EmptyDataError as e:
            raise EmptySheetError(
                f"Sheet '{sheet_name}' boş: {self.file_name}"
            ) from e
        
        except Exception as e:
            raise ValueError(
                f"Sheet '{sheet_name}' okunamadı: {str(e)}"
            ) from e
    
    def read_uzun_isler_sheet(self, sheet_name: str) -> List[Dict]:
        """
        Uzun süren işler sheet'ini oku
        
        Args:
            sheet_name: Sheet adı
            
        Returns:
            List[Dict]: Kayıt listesi
            
        Raises:
            ValueError: Sheet okunamazsa
            KeyError: Beklenen kolonlar yoksa
        """
        try:
            df = pd.read_excel(
                self.file_path, 
                sheet_name=sheet_name, 
                header=0
            )
            
            # Kolon sayısı kontrolü
            if len(df.columns) < 4:
                raise ValueError(
                    f"Sheet '{sheet_name}' yetersiz kolon sayısına sahip. "
                    f"Beklenen: en az 4, Bulunan: {len(df.columns)}"
                )
            
            kayitlar = []
            for idx, row in df.iterrows():
                try:
                    # NaN kontrolü - JCL adı boşsa atla
                    if pd.isna(row.iloc[0]):
                        continue
                    
                    # Veri validasyonu
                    jcl_adi = str(row.iloc[0]).strip()
                    if not jcl_adi or len(jcl_adi) == 0:
                        continue
                    
                    kayit = {
                        'jcl_adi': jcl_adi,
                        'ay': self.ay,
                        'sheet_adi': sheet_name,
                        'calisma_sayisi': self._safe_int(row.iloc[1]),
                        'calisma_suresi': self._safe_int(row.iloc[2]),
                        'sorumlu_ekip': self._safe_str(row.iloc[3]),
                        'kaynak_dosya': self.file_name
                    }
                    kayitlar.append(kayit)
                
                except Exception as e:
                    # Satır hatalarını logla ama devam et
                    print(f"Satır {idx} atlandı: {str(e)}")
                    continue
            
            return kayitlar
        
        except pd.errors.EmptyDataError as e:
            raise EmptySheetError(
                f"Sheet '{sheet_name}' boş: {self.file_name}"
            ) from e
        
        except Exception as e:
            raise ValueError(
                f"Sheet '{sheet_name}' okunamadı: {str(e)}"
            ) from e
    
    def read_all_sheets(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Tüm sheet'leri oku
        
        Returns:
            Tuple[List[Dict], Optional[str]]: (kayitlar_listesi, hata_mesaji)
            - Başarılı: (kayitlar, None)
            - Hatalı: ([], hata_mesaji)
            
        Examples:
            >>> reader = ExcelReader('test.xlsx')
            >>> kayitlar, hata = reader.read_all_sheets()
            >>> if hata:
            ...     print(f"Hata: {hata}")
            >>> else:
            ...     print(f"{len(kayitlar)} kayıt okundu")
        """
        try:
            # Rapor tipi kontrolü
            if self.rapor_tipi == 'BILINMEYEN':
                return [], "Rapor tipi belirlenemedi. Dosya adında 'Hatalı' veya 'Uzun' olmalı."
            
            sheet_names = self.get_sheet_names()
            
            if not sheet_names:
                return [], "Excel dosyasında sheet bulunamadı"
            
            all_kayitlar = []
            
            for sheet_name in sheet_names:
                try:
                    if self.rapor_tipi == 'HATALI':
                        kayitlar = self.read_hatali_isler_sheet(sheet_name)
                    elif self.rapor_tipi == 'UZUN':
                        kayitlar = self.read_uzun_isler_sheet(sheet_name)
                    else:
                        continue
                    
                    all_kayitlar.extend(kayitlar)
                
                except EmptySheetError as e:
                    # Boş sheet'i atla, devam et
                    print(f"Uyarı: {str(e)}")
                    continue
                
                except ValueError as e:
                    # Sheet okuma hatası, devam et
                    print(f"Uyarı: {str(e)}")
                    continue
            
            if not all_kayitlar:
                return [], "Hiç geçerli kayıt bulunamadı"
            
            return all_kayitlar, None
        
        except FileNotFoundError as e:
            return [], f"Dosya bulunamadı: {str(e)}"
        
        except InvalidFileFormatError as e:
            return [], f"Geçersiz dosya formatı: {str(e)}"
        
        except pd.errors.EmptyDataError as e:
            return [], f"Excel dosyası boş: {str(e)}"
        
        except Exception as e:
            return [], f"Beklenmeyen hata: {str(e)}"
    
    # Helper metodlar - Type-safe conversions
    def _safe_int(self, value) -> Optional[int]:
        """
        Güvenli integer dönüşümü
        
        Args:
            value: Dönüştürülecek değer
            
        Returns:
            Optional[int]: Integer değer veya None
        """
        if pd.isna(value):
            return None
        
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def _safe_str(self, value) -> Optional[str]:
        """
        Güvenli string dönüşümü
        
        Args:
            value: Dönüştürülecek değer
            
        Returns:
            Optional[str]: String değer veya None
        """
        if pd.isna(value):
            return None
        
        try:
            result = str(value).strip()
            return result if result else None
        except Exception:
            return None
    
    def _safe_date(self, value) -> Optional[str]:
        """
        Güvenli tarih dönüşümü (YYYY-MM-DD formatı)
        
        Args:
            value: Dönüştürülecek değer
            
        Returns:
            Optional[str]: Tarih string'i veya None
        """
        if pd.isna(value):
            return None
        
        try:
            # Pandas Timestamp ise
            if isinstance(value, pd.Timestamp):
                return value.strftime('%Y-%m-%d')
            
            # String ise parse et
            date_str = str(value)[:10]
            
            # Tarih formatı kontrolü
            if len(date_str) >= 10 and '-' in date_str:
                return date_str
            
            return None
        
        except Exception:
            return None