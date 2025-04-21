"""
    The app module for managing the application.
    This is an open-source project made by [SalemMalola](https://github.com/Salem530)
"""

# Dependencies importation
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QFrame,
    QSizePolicy,
    QScrollArea,
)
from qt_material import apply_stylesheet

# Local imports
from customWidgets import CustomTitleBar, SideBar
from tasksList import TaskList
from themes import applyTheme

class Tasker(QMainWindow):
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
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        contentLayout.addWidget(self.tabs)

        # Add horizontal layout into the main vertical layout
        mainLayout.addLayout(contentLayout)
        self.addWelcomeTab()

    def addTaskList(self):
        name = self.sideBar.showTaskListDialog()
        # Remove welcome tab if it's the only tab
        if self.tabs.count() == 1 and self.tabs.widget(0) == self.welcomeTab:
            self.tabs.removeTab(0)

        task_list = TaskList(name)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(task_list)
        scroll.setWidget(container)

        self.tabs.addTab(scroll, name)
        self.tabs.setCurrentWidget(scroll)


    def addWelcomeTab(self) -> None:
        self.welcomeTab = QWidget()
        layout = QVBoxLayout(self.welcomeTab)
        label = QLabel("👋 Welcome to Tasker!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.tabs.addTab(self.welcomeTab, "Welcome")

    def closeTab(self, index: int):
        widget = self.tabs.widget(index)

        # Prevent closing the welcome tab if it's the only one
        if widget == self.welcomeTab and self.tabs.count() == 1:
            return

        self.tabs.removeTab(index)
        if widget:
            widget.deleteLater()

        # If all task tabs are closed, show the welcome tab again
        if self.tabs.count() == 0:
            self.addWelcomeTab()

    def mainLoop(self) -> None:
        """Start the application event loop."""
        self.show()
        self.qtApplication.exec_()
