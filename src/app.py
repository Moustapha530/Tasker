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
    QTabWidget,
    QWidget,
    QFrame,
    QSizePolicy,
    QVBoxLayout,
)

# Local importations
from customWidgets import CustomTitleBar, loadStyleSheet


class Tasker(FramelessMainWindow):
    """The main application manager."""

    def __init__(self):
        """Initialize the application window and UI components."""
        # Create the Qt application
        self.qtApplication = QApplication([])
        super().__init__()

        # Set window properties
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet(loadStyleSheet("style"))

        # Central widget and main layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create the title bar
        self.titleBar = CustomTitleBar(self, "Ts - Tasker")
        self.titleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.addWidget(self.titleBar, alignment=Qt.AlignmentFlag.AlignTop)

        # Create the tab widget
        self.tabs = QTabWidget(self)
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make tabs responsive
        self.layout.addWidget(self.tabs, alignment=Qt.AlignmentFlag.AlignTop)

        # Add the default welcome tab
        self.addTab("Welcome")

    def addTab(self, tab_name: str) -> None:
        """
        Add a new tab with a QFrame as its content.

        Args:
            tab_name (str): The name of the tab to be added.
        """
        tab = QWidget()  # Create a new tab widget
        tab_layout = QHBoxLayout(tab)  # Set a layout for the tab
        tab_frame = QFrame()  # Create a frame inside the tab
        tab_layout.addWidget(tab_frame)  # Add the frame to the layout

        self.tabs.addTab(tab, tab_name)  # Add the tab to the QTabWidget

    def mainLoop(self) -> None:
        """Launch the application main loop."""
        self.show()
        self.qtApplication.exec_()
