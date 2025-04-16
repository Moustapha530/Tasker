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
from tasksList import TaskList
from themes import applyTheme

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
        self.titleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mainLayout.addWidget(self.titleBar)

        # Bottom layout (horizontal): SideBar + TabWidget
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        # Sidebar (left)
        self.sideBar = SideBar(self)
        self.sideBar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.sideBar.buttons.get("Add Task List").clicked.connect(self.addTaskList)
        contentLayout.addWidget(self.sideBar)

        # Tabs (main content)
        self.tabs = QTabWidget(self)
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        contentLayout.addWidget(self.tabs)

        # Add horizontal layout into the main vertical layout
        mainLayout.addLayout(contentLayout)

    def addTaskList(self) -> None:
        name = self.sideBar.showTaskListDialog()
        self.tabs.addTab(TaskList(name), name)

    def mainLoop(self) -> None:
        """Start the application event loop."""
        self.show()
        self.qtApplication.exec_()
