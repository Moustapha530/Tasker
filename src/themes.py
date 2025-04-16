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
    }}

    QTabWidget::pane {{
        background-color: {theme['primaryColor']};
    }}

    QTabBar{{
        border-bottom: 1px solid {theme['primaryTextColor']};
    }}

    QTabBar::tab {{
        background-color: {theme['secondaryColor']};
        border-bottom: 1px solid {theme['primaryTextColor']};
        color: {theme['primaryTextColor']};
        padding: 8px 16px;
        margin: 0px;
    }}

    QTabBar::tab:selected {{
        color: {theme['primaryLightColor']};
        border: none;
        border-top: 3px solid {theme['primaryColor']}; /* Line at top like VSCode */
        background-color: transparent;
    }}

    QTabBar::tab:hover {{
        background-color: {theme['secondaryLightColor']}; /* Light hover effect */
    }}
    """

def applyCTheme() -> str:
    theme = get_theme(getCurrentTheme())
    return f"""
   #CTitleBar{{
        border-bottom: 1px solid {theme['primaryTextColor']};
    }}

    #CloseBtn:hover{{
        background-color: red;
    }}

    #CSideBar{{
        border: 1px solid {theme['primaryTextColor']};
    }}
    """

def getCurrentTheme() -> str:
    return f"{getSetting("apparence")["theme"]}.xml"