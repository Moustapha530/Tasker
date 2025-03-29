"""
    The app module for managing the application.
    This is an open-source project made by [SalemMalola](https://github.com/Salem530)
"""

# Dependencies importation
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QTabWidget,
    QWidget,
    QFrame,
    QSizePolicy
)

# Local importations
from customWidgets import AppLogo, CustomTitleBar, loadStyleSheet


class Tasker(QMainWindow):
    """The main application manager."""

    def __init__(self):
        """Initialize the application window and UI components."""
        # Create the Qt application
        self.qtApplication = QApplication([])
        super().__init__()

        # Set window properties
        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle("Tasker")
        self.setStyleSheet(loadStyleSheet("style"))

        # Central widget and main layout
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create and add the app logo
        self.appLogo = AppLogo(self, "ressources/images/tasker.png")
        self.layout.addWidget(
            self.appLogo, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        # Create the tab widget
        self.tabs = QTabWidget(self)
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Make tabs responsive
        self.layout.addWidget(self.tabs, alignment=Qt.AlignmentFlag.AlignTop)

        # Create the title bar
        self.titleBar = CustomTitleBar(self)
        self.layout.addWidget(
            self.titleBar, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight
        )

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
        tab_frame.setStyleSheet("background-color: white; border-radius: 5px;")  # Basic styling
        tab_layout.addWidget(tab_frame)  # Add the frame to the layout

        self.tabs.addTab(tab, tab_name)  # Add the tab to the QTabWidget

    def mainLoop(self) -> None:
        """Launch the application main loop."""
        self.show()
        self.qtApplication.exec_()
