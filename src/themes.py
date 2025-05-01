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


    QTabWidget::pane {{
        background-color: {theme['primaryColor']};
    }}

    QTabBar::tab {{
        background-color: {theme['secondaryColor']};
        color: {theme['primaryTextColor']};
        padding: 8px 16px;
        margin: 0px;
        min-width: 70px;
    }}

    QTabBar::tab:selected {{
        color: {theme['primaryLightColor']};
        border: none;
        border-top: 3px solid {theme['primaryColor']};
        background-color: transparent;
    }}

    QTabBar::tab:hover {{
        background-color: {theme['secondaryLightColor']}; 
        border: none;
    }}

    QTabBar::close-button {{
        image: url(ressources/icons/cross.png);
        subcontrol-position: right;
    }}

    QTabBar::close-button:hover {{
        background-color: red;
    }}

    #OnlyTab {{
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
    }}

    #ConerLeftTab {{
        border-bottom-left-radius: 15px;
    }}

    #ConerRightTab {{
        border-bottom-right-radius: 15px;
    }}
    """

def applyCTheme() -> str:
    theme = get_theme(getCurrentTheme())
    return f"""
    #CTitleBar{{
        background-color: {theme['secondaryColor']};
        border-radius: 0px;
        border-bottom-right-radius: 15px;
        border-top-right-radius: 15px;
    }}

    #CTitleBar QFrame{{
        background-color: {theme['secondaryColor']};
    }}

    #CloseBtn:hover{{
        background-color: red;
    }}

    #CSideBar{{
        background-color: {theme['secondaryColor']};
        border-radius: 0px;
        border-bottom-left-radius: 15px;
        border-bottom-right-radius: 15px;
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