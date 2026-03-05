"""
Excel Okuyucu
Excel dosyalarını okuyup veritabanına hazır hale getiren modül
"""
import pandas as pd
import re
from typing import List, Dict, Tuple
from datetime import datetime


class ExcelReader:
    """Excel dosyalarını okuyan sınıf"""
    
    def __init__(self, file_path: str):
        """
        Args:
            file_path: Excel dosya yolu
        """
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1].split('\\')[-1]
        self.rapor_tipi = self._detect_rapor_tipi()
        self.ay = self._extract_ay()
    
    def _detect_rapor_tipi(self) -> str:
        """Dosya adından rapor tipini belirle"""
        if 'Hatalı' in self.file_name or 'Hatali' in self.file_name:
            return 'HATALI'
        elif 'Uzun' in self.file_name:
            return 'UZUN'
        return 'BILINMEYEN'
    
    def _extract_ay(self) -> str:
        """Dosya adından ay bilgisini çıkar (YYYY-MM formatında)"""
        # Türkçe ay isimleri
        aylar = {
            'OCAK': '01', 'SUBAT': '02', 'ŞUBAT': '02',
            'MART': '03', 'NISAN': '04', 'MAYIS': '05',
            'HAZIRAN': '06', 'TEMMUZ': '07', 'AGUSTOS': '08', 'AĞUSTOS': '08',
            'EYLUL': '09', 'EYLÜL': '09', 'EKIM': '10', 'EKİM': '10',
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
        
        return f"{yil}-01"  # Default
    
    def get_sheet_names(self) -> List[str]:
        """Sheet isimlerini getir"""
        xl_file = pd.ExcelFile(self.file_path)
        return xl_file.sheet_names
    
    def read_hatali_isler_sheet(self, sheet_name: str) -> List[Dict]:
        """Hatalı işler sheet'ini oku"""
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=0)
        
        kayitlar = []
        for _, row in df.iterrows():
            # NaN kontrolü
            if pd.isna(row.iloc[0]):  # JCL adı boşsa atla
                continue
            
            kayit = {
                'jcl_adi': str(row.iloc[0]).strip(),
                'ay': self.ay,
                'sheet_adi': sheet_name,
                'hatali_sayi_ay': int(row.iloc[1]) if pd.notna(row.iloc[1]) else None,
                'son_hatali_tarih': str(row.iloc[2])[:10] if pd.notna(row.iloc[2]) else None,
                'hatali_sayi_yil': int(row.iloc[3]) if pd.notna(row.iloc[3]) else None,
                'sorumlu_ekip': str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else None,
                'kaynak_dosya': self.file_name
            }
            kayitlar.append(kayit)
        
        return kayitlar
    
    def read_uzun_isler_sheet(self, sheet_name: str) -> List[Dict]:
        """Uzun süren işler sheet'ini oku"""
        df = pd.read_excel(self.file_path, sheet_name=sheet_name, header=0)
        
        kayitlar = []
        for _, row in df.iterrows():
            # NaN kontrolü
            if pd.isna(row.iloc[0]):  # JCL adı boşsa atla
                continue
            
            kayit = {
                'jcl_adi': str(row.iloc[0]).strip(),
                'ay': self.ay,
                'sheet_adi': sheet_name,
                'calisma_sayisi': int(row.iloc[1]) if pd.notna(row.iloc[1]) else None,
                'calisma_suresi': int(row.iloc[2]) if pd.notna(row.iloc[2]) else None,
                'sorumlu_ekip': str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else None,
                'kaynak_dosya': self.file_name
            }
            kayitlar.append(kayit)
        
        return kayitlar
    
    def read_all_sheets(self) -> Tuple[List[Dict], str]:
        """
        Tüm sheet'leri oku
        Returns:
            (kayitlar_listesi, hata_mesaji)
        """
        try:
            sheet_names = self.get_sheet_names()
            all_kayitlar = []
            
            for sheet_name in sheet_names:
                if self.rapor_tipi == 'HATALI':
                    kayitlar = self.read_hatali_isler_sheet(sheet_name)
                elif self.rapor_tipi == 'UZUN':
                    kayitlar = self.read_uzun_isler_sheet(sheet_name)
                else:
                    continue
                
                all_kayitlar.extend(kayitlar)
            
            return all_kayitlar, None
            
        except Exception as e:
            return [], str(e)