# -*- mode: python ; coding: utf-8 -*-
"""
Proje_Q - PyInstaller Specification File
Version: 1.0.0
Build: Production Release
"""

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('config', 'config'),
        ('VERSION', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'openpyxl',
        'openpyxl.cell',
        'openpyxl.styles',
        'sqlite3',
        # Src modülleri
        'ui',
        'ui.main_window',
        'ui.advanced_search_dialog',
        'ui.bulk_search_dialog',
        'ui.bulk_search_results_dialog',
        'ui.export_dialog',
        'ui.log_viewer_dialog',
        'ui.settings_dialog',
        'ui.statistics_dialog',
        'ui.themes',
        'ui.components',
        'ui.components.dialog_manager',
        'ui.components.menu_builder',
        'ui.components.search_panel',
        'ui.components.table_manager',
        'ui.components.toolbar_builder',
        'database',
        'database.db_manager',
        'utils',
        'utils.backup_manager',
        'utils.excel_reader',
        'utils.logger',
        'config',
        'config.constants',
        'config.user_preferences',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
        'unittest',
        'test',
        'tests',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Proje_Q',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path if available
    version_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Proje_Q',
)