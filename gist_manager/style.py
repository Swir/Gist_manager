PALETTES = {
    "Midnight Blue": {
        "bg": "#070B16", "panel": "#0D1426", "panel2": "#111C33",
        "border": "#1E3154", "text": "#EAF2FF", "muted": "#8292AD",
        "accent": "#1F8FFF", "accent2": "#55B8FF", "danger": "#FF5D73",
        "input": "#0A1121", "hover": "#142746",
    },
    "Graphite": {
        "bg": "#0E1014", "panel": "#171A20", "panel2": "#1E222A",
        "border": "#303640", "text": "#F2F4F8", "muted": "#9299A5",
        "accent": "#6EA8FE", "accent2": "#9CC2FF", "danger": "#FF6B7D",
        "input": "#111419", "hover": "#262C35",
    },
    "Light": {
        "bg": "#F3F7FC", "panel": "#FFFFFF", "panel2": "#F8FAFD",
        "border": "#D8E2EE", "text": "#172033", "muted": "#66758C",
        "accent": "#087CF0", "accent2": "#3F9BFF", "danger": "#D74255",
        "input": "#FFFFFF", "hover": "#EAF3FF",
    },
}


def theme_css(name):
    p = PALETTES.get(name, PALETTES["Midnight Blue"])
    return f"""
    * {{ font-family:'Segoe UI','Inter',sans-serif; font-size:10pt; }}
    QMainWindow, QWidget#root {{ background:{p['bg']}; color:{p['text']}; }}
    QWidget {{ color:{p['text']}; }}
    QFrame#hero, QFrame#card {{ background:{p['panel']}; border:1px solid {p['border']}; border-radius:14px; }}
    QLabel#title {{ color:{p['text']}; font-size:24pt; font-weight:700; }}
    QLabel#subtitle, QLabel#muted, QLabel#caption {{ color:{p['muted']}; }}
    QLabel#sectionTitle {{ font-size:12pt; font-weight:700; }}
    QLabel#badge {{ color:{p['accent2']}; background:{p['hover']}; border:1px solid {p['border']}; border-radius:10px; padding:4px 9px; font-weight:600; }}
    QPushButton {{ background:{p['panel2']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:9px; padding:8px 13px; font-weight:600; }}
    QPushButton:hover {{ background:{p['hover']}; border-color:{p['accent']}; }}
    QPushButton:pressed {{ padding-top:9px; padding-bottom:7px; }}
    QPushButton#primary {{ background:{p['accent']}; color:white; border-color:{p['accent']}; }}
    QPushButton#primary:hover {{ background:{p['accent2']}; border-color:{p['accent2']}; }}
    QPushButton#danger {{ color:{p['danger']}; border-color:{p['danger']}; background:transparent; }}
    QPushButton#danger:hover {{ background:{p['danger']}; color:white; }}
    QLineEdit, QTextEdit, QTextBrowser, QComboBox {{ background:{p['input']}; color:{p['text']}; border:1px solid {p['border']}; border-radius:9px; padding:8px 10px; selection-background-color:{p['accent']}; }}
    QLineEdit:focus, QTextEdit:focus, QTextBrowser:focus, QComboBox:focus {{ border:1px solid {p['accent']}; }}
    QLineEdit[readOnly="true"] {{ color:{p['muted']}; background:{p['panel2']}; }}
    QComboBox::drop-down {{ border:none; width:24px; }}
    QComboBox QAbstractItemView {{ background:{p['panel']}; color:{p['text']}; border:1px solid {p['border']}; selection-background-color:{p['accent']}; }}
    QCheckBox {{ spacing:8px; }}
    QCheckBox::indicator {{ width:18px; height:18px; border-radius:5px; border:1px solid {p['border']}; background:{p['input']}; }}
    QCheckBox::indicator:checked {{ background:{p['accent']}; border-color:{p['accent']}; }}
    QTabWidget::pane {{ border:none; background:transparent; margin-top:8px; }}
    QTabBar::tab {{ background:transparent; color:{p['muted']}; border:none; border-bottom:2px solid transparent; padding:10px 18px; font-weight:600; }}
    QTabBar::tab:selected {{ color:{p['accent2']}; border-bottom:2px solid {p['accent']}; }}
    QTabBar::tab:hover {{ color:{p['text']}; }}
    QTableWidget {{ background:{p['panel']}; alternate-background-color:{p['panel2']}; gridline-color:transparent; border:1px solid {p['border']}; border-radius:10px; selection-background-color:{p['hover']}; selection-color:{p['text']}; outline:none; }}
    QTableWidget::item {{ padding:7px; border-bottom:1px solid {p['border']}; }}
    QHeaderView::section {{ background:{p['panel2']}; color:{p['muted']}; border:none; border-bottom:1px solid {p['border']}; padding:9px 8px; font-weight:700; }}
    QScrollBar:vertical {{ background:transparent; width:10px; margin:3px; }}
    QScrollBar::handle:vertical {{ background:{p['border']}; min-height:26px; border-radius:4px; }}
    QScrollBar::handle:vertical:hover {{ background:{p['accent']}; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height:0; }}
    QMenuBar {{ background:{p['bg']}; color:{p['muted']}; }}
    QMenuBar::item:selected {{ background:{p['hover']}; color:{p['text']}; }}
    QMenu {{ background:{p['panel']}; color:{p['text']}; border:1px solid {p['border']}; padding:6px; }}
    QMenu::item {{ padding:7px 24px 7px 12px; border-radius:6px; }}
    QMenu::item:selected {{ background:{p['hover']}; }}
    QStatusBar {{ background:{p['panel']}; color:{p['muted']}; border-top:1px solid {p['border']}; }}
    QProgressBar {{ background:{p['panel2']}; border:1px solid {p['border']}; border-radius:7px; text-align:center; min-height:18px; }}
    QProgressBar::chunk {{ background:{p['accent']}; border-radius:6px; }}
    QToolTip {{ background:{p['panel']}; color:{p['text']}; border:1px solid {p['border']}; padding:5px; }}
    """
