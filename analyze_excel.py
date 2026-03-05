# -*- coding: utf-8 -*-
import pandas as pd
import os
import sys

# Windows encoding fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("="*80)
print("EXCEL DOSYALARI DETAYLI ANALİZİ")
print("="*80)

excel_dir = 'Data/Excel'
excel_files = sorted([f for f in os.listdir(excel_dir) if f.endswith('.xlsx')])

print(f"\nToplam Excel Dosyasi: {len(excel_files)}\n")

for file_idx, excel_file in enumerate(excel_files, 1):
    file_path = os.path.join(excel_dir, excel_file)
    
    print("\n" + "="*80)
    print(f"DOSYA {file_idx}: {excel_file}")
    print("="*80)
    
    try:
        # Excel dosyasını aç
        xl_file = pd.ExcelFile(file_path)
        sheet_names = xl_file.sheet_names
        
        print(f"\nToplam Sheet Sayisi: {len(sheet_names)}")
        print(f"Sheet Isimleri: {', '.join(sheet_names)}")
        
        # Her sheet'i analiz et
        for sheet_idx, sheet_name in enumerate(sheet_names, 1):
            print(f"\n  [{sheet_idx}] SHEET: {sheet_name}")
            print("  " + "-"*76)
            
            # İlk 10 satırı header olmadan oku
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, nrows=10)
            
            print(f"  Toplam Kolon Sayisi: {len(df.columns)}")
            
            # İlk birkaç satırı göster
            print(f"\n  ILK 7 SATIR (ilk 10 kolon):")
            for idx in range(min(7, len(df))):
                row_data = df.iloc[idx].head(10).tolist()
                # NaN değerleri boş string yap
                row_data = [str(x) if pd.notna(x) else "" for x in row_data]
                print(f"    Satir {idx+1}: {row_data}")
            
            # Kolon başlıklarını bulmaya çalış (ilk 10 satırda)
            print(f"\n  OLASI KOLON BASLIKLARI:")
            for idx in range(min(10, len(df))):
                row = df.iloc[idx]
                # Eğer satırda "JCL" veya "EKIP" gibi anahtar kelimeler varsa
                row_str = ' '.join([str(x).upper() for x in row if pd.notna(x)])
                if 'JCL' in row_str or 'EKIP' in row_str or 'JOB' in row_str:
                    print(f"    Satir {idx+1} (potansiyel baslik):")
                    for col_idx, val in enumerate(row):
                        if pd.notna(val):
                            print(f"      Kolon {col_idx+1}: {val}")
                            
    except Exception as e:
        print(f"  HATA: {str(e)}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("ANALIZ TAMAMLANDI")
print("="*80)