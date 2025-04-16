"""
    The app module for managing the application.
    This is an open-source project made by [SalemMalola](https://github.com/Salem530)
"""

# Dependencies importation
from pyqt_frameless_window import FramelessMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QFrame,
    QSizePolicy,
)
from qt_material import apply_stylesheet

# Local imports
from customWidgets import CustomTitleBar, SideBar
from themes import applyTheme, applyCTheme

class Tasker(FramelessMainWindow):
    """The main application window with VSCode-like layout."""

    def __init__(self):
        """Initialize the main UI structure."""
        self.qtApplication = QApplication([])
        apply_stylesheet(self.qtApplication, "dark_blue.xml")
        super().__init__()

        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(applyTheme())

        # Central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Top-level vertical layout
        mainLayout = QVBoxLayout(self.centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Custom Title Bar at the top
        self.titleBar = CustomTitleBar(self, "Ts - Tasker")
        self.titleBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        mainLayout.addWidget(self.titleBar)

        # Bottom layout (horizontal): SideBar + TabWidget
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        # Sidebar (left)
        self.sideBar = SideBar(self)
        self.sideBar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        contentLayout.addWidget(self.sideBar)

        # Tabs (main content)
        self.tabs = QTabWidget(self)
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contentLayout.addWidget(self.tabs)

        # Add horizontal layout into the main vertical layout
        mainLayout.addLayout(contentLayout)

        # Add the default welcome tab
        self.addTab("Welcome")

    def addTab(self, tab_name: str) -> None:
        """Add a new tab with a frame inside."""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        tab_frame = QFrame()
        layout.addWidget(tab_frame)
        self.tabs.addTab(tab, tab_name)

    def mainLoop(self) -> None:
        """Start the application event loop."""
        self.show()
        self.qtApplication.exec_()
