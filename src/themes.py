from qt_material import get_theme
from settings import getSetting



def applyTheme() -> str:
    """
    Returns a stylesheet string for QTabWidget customized and general widgets
    based on the theme.
    """
    theme = get_theme(getCurrentTheme())
    return f"""
    *{{
        border: none;
    }}

    QPushButton{{
        background-color: transparent;
    }}

    QPushButton:hover{{
        background-color: {theme['secondaryLightColor']};
        border-radius: 5px;
    }}

    QProgressBar, QProgressBar::chunk{{
        color: {theme['primaryColor']};
        border-radius: 10px;
    }}

    QScrollBar:vertical {{
        width: 12px;
        background: #2b2b2b;
    }}

    QScrollBar::handle:vertical {{
        background: #888;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: #aaa;
    }}
    """

def applyTaskTheme() -> str:
    theme = get_theme(getCurrentTheme())
    return f"""
    #DeleteBtn:hover{{
        background-color: red;
    }}

    #Task{{
        background-color: transparent;  
    }}

    #TaskList{{
        background-color: transparent;
    }}
    """

def getCurrentTheme() -> str:
    return f"{getSetting("apparence")["theme"]}.xml"