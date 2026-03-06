"""
Tema Sistemi - Light, Dark, Blue
"""


def get_theme_stylesheet(theme_name='light'):
    """Tema stilini döndür"""
    
    if theme_name == 'dark':
        return DARK_THEME
    elif theme_name == 'blue':
        return BLUE_THEME
    else:
        return LIGHT_THEME


# ===== LIGHT THEME =====
LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    background-color: #ffffff;
    color: #333333;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11px;
}

QPushButton {
    padding: 8px 15px;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit {
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 3px;
    background-color: white;
    color: #333;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #2196F3;
}

QGroupBox {
    border: 2px solid #2196F3;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    color: #2196F3;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QTabWidget::pane {
    border: 1px solid #ddd;
    background: white;
}

QTabBar::tab {
    padding: 10px 20px;
    background: #f0f0f0;
    border: 1px solid #ddd;
    border-bottom: none;
}

QTabBar::tab:selected {
    background: #2196F3;
    color: white;
}

QTableWidget {
    alternate-background-color: #f9f9f9;
    gridline-color: #ddd;
    background-color: white;
}

QHeaderView::section {
    background-color: #2196F3;
    color: white;
    padding: 5px;
    border: 1px solid #1976D2;
    font-weight: bold;
}

QMenuBar {
    background-color: #f0f0f0;
    color: #333;
}

QMenuBar::item:selected {
    background-color: #2196F3;
    color: white;
}

QMenu {
    background-color: white;
    border: 1px solid #ddd;
}

QMenu::item:selected {
    background-color: #2196F3;
    color: white;
}

QToolBar {
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
    spacing: 5px;
    padding: 5px;
}

QStatusBar {
    background-color: #f0f0f0;
    color: #333;
    border-top: 1px solid #ddd;
}

QProgressBar {
    border: 1px solid #ddd;
    border-radius: 3px;
    text-align: center;
    background-color: #f0f0f0;
}

QProgressBar::chunk {
    background-color: #4CAF50;
    border-radius: 2px;
}

QCheckBox {
    spacing: 5px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #2196F3;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #2196F3;
    image: url(none);
}

QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #2196F3;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""


# ===== DARK THEME =====
DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
}

QWidget {
    background-color: #2d2d2d;
    color: #e0e0e0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11px;
}

QPushButton {
    padding: 8px 15px;
    background-color: #FF9800;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #F57C00;
}

QPushButton:pressed {
    background-color: #E65100;
}

QPushButton:disabled {
    background-color: #555555;
    color: #888888;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit {
    padding: 5px 10px;
    border: 1px solid #444;
    border-radius: 3px;
    background-color: #3d3d3d;
    color: #e0e0e0;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #FF9800;
}

QGroupBox {
    border: 2px solid #FF9800;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    color: #FF9800;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QTabWidget::pane {
    border: 1px solid #444;
    background: #2d2d2d;
}

QTabBar::tab {
    padding: 10px 20px;
    background: #3d3d3d;
    border: 1px solid #444;
    border-bottom: none;
    color: #e0e0e0;
}

QTabBar::tab:selected {
    background: #FF9800;
    color: white;
}

QTableWidget {
    alternate-background-color: #353535;
    gridline-color: #444;
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QHeaderView::section {
    background-color: #FF9800;
    color: white;
    padding: 5px;
    border: 1px solid #F57C00;
    font-weight: bold;
}

QMenuBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
}

QMenuBar::item:selected {
    background-color: #FF9800;
    color: white;
}

QMenu {
    background-color: #2d2d2d;
    border: 1px solid #444;
    color: #e0e0e0;
}

QMenu::item:selected {
    background-color: #FF9800;
    color: white;
}

QToolBar {
    background-color: #2d2d2d;
    border-bottom: 1px solid #444;
    spacing: 5px;
    padding: 5px;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #e0e0e0;
    border-top: 1px solid #444;
}

QProgressBar {
    border: 1px solid #444;
    border-radius: 3px;
    text-align: center;
    background-color: #3d3d3d;
    color: #e0e0e0;
}

QProgressBar::chunk {
    background-color: #FF9800;
    border-radius: 2px;
}

QCheckBox {
    spacing: 5px;
    color: #e0e0e0;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #FF9800;
    border-radius: 3px;
    background-color: #3d3d3d;
}

QCheckBox::indicator:checked {
    background-color: #FF9800;
    image: url(none);
}

QScrollBar:vertical {
    border: none;
    background: #3d3d3d;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #FF9800;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QLabel {
    color: #e0e0e0;
}

QComboBox QAbstractItemView {
    background-color: #3d3d3d;
    color: #e0e0e0;
    selection-background-color: #FF9800;
}
"""


# ===== BLUE THEME =====
BLUE_THEME = """
QMainWindow {
    background-color: #e3f2fd;
}

QWidget {
    background-color: #bbdefb;
    color: #0d47a1;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 11px;
}

QPushButton {
    padding: 8px 15px;
    background-color: #1976D2;
    color: white;
    border: none;
    border-radius: 5px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1565C0;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #90caf9;
    color: #e3f2fd;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit {
    padding: 5px 10px;
    border: 1px solid #64b5f6;
    border-radius: 3px;
    background-color: white;
    color: #0d47a1;
}

QLineEdit:focus, QComboBox:focus {
    border: 2px solid #1976D2;
}

QGroupBox {
    border: 2px solid #1976D2;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    font-weight: bold;
}

QGroupBox::title {
    color: #1976D2;
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QTabWidget::pane {
    border: 1px solid #64b5f6;
    background: white;
}

QTabBar::tab {
    padding: 10px 20px;
    background: #90caf9;
    border: 1px solid #64b5f6;
    border-bottom: none;
    color: #0d47a1;
}

QTabBar::tab:selected {
    background: #1976D2;
    color: white;
}

QTableWidget {
    alternate-background-color: #e3f2fd;
    gridline-color: #90caf9;
    background-color: white;
    color: #0d47a1;
}

QHeaderView::section {
    background-color: #1976D2;
    color: white;
    padding: 5px;
    border: 1px solid #1565C0;
    font-weight: bold;
}

QMenuBar {
    background-color: #90caf9;
    color: #0d47a1;
}

QMenuBar::item:selected {
    background-color: #1976D2;
    color: white;
}

QMenu {
    background-color: white;
    border: 1px solid #64b5f6;
    color: #0d47a1;
}

QMenu::item:selected {
    background-color: #1976D2;
    color: white;
}

QToolBar {
    background-color: #90caf9;
    border-bottom: 1px solid #64b5f6;
    spacing: 5px;
    padding: 5px;
}

QStatusBar {
    background-color: #90caf9;
    color: #0d47a1;
    border-top: 1px solid #64b5f6;
}

QProgressBar {
    border: 1px solid #64b5f6;
    border-radius: 3px;
    text-align: center;
    background-color: #e3f2fd;
    color: #0d47a1;
}

QProgressBar::chunk {
    background-color: #1976D2;
    border-radius: 2px;
}

QCheckBox {
    spacing: 5px;
    color: #0d47a1;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #1976D2;
    border-radius: 3px;
    background-color: white;
}

QCheckBox::indicator:checked {
    background-color: #1976D2;
    image: url(none);
}

QScrollBar:vertical {
    border: none;
    background: #e3f2fd;
    width: 12px;
    margin: 0px;
}

QScrollBar::handle:vertical {
    background: #1976D2;
    min-height: 20px;
    border-radius: 6px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QLabel {
    color: #0d47a1;
}

QComboBox QAbstractItemView {
    background-color: white;
    color: #0d47a1;
    selection-background-color: #1976D2;
    selection-color: white;
}
"""