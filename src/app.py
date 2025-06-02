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
    QSizePolicy,
    QScrollArea,
    QStackedLayout
)
from qt_material import apply_stylesheet

# Local imports
from customWidgets import CustomTitleBar, CustomTabWidget, SideBar
from tasksList import TaskList, TaskListExplorer
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
        self.explorer = TaskListExplorer(self)
        # Top-level vertical layout
        mainLayout = QVBoxLayout(self.centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Custom Title Bar at the top
        self.titleBar = CustomTitleBar(self, "")
        self.titleBar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        mainLayout.addWidget(self.titleBar)

        # Tabs at the top on top of the title bar
        self.tabs = CustomTabWidget(self)
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        mainLayout.addWidget(self.tabs)
        self.tabs.raise_()

        # Sidebar (left)
        self.sideBar = SideBar(self)
        self.sideBar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.sideBar.buttons.get("Add task list").clicked.connect(self.addNewTaskList)
        self.sideBar.buttons.get("Show task lists").clicked.connect(self.showTaskListExplorer)
        mainLayout.addWidget(self.sideBar, alignment=Qt.AlignmentFlag.AlignLeft)

        self.addWelcomeTab()

    def addTaskList(self, taskList : TaskList, name = "Untitled") -> None:
        # Remove welcome tab if it's the only tab
        if self.tabs.count() == 1 and self.tabs.widget(0) == self.welcomeTab:
            self.tabs.removeTab(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(taskList)
        scroll.setWidget(container)

        self.tabs.addAnimatedTab(scroll, name)

    def addNewTaskList(self) -> None:
        # Remove welcome tab if it's the only tab
        if self.tabs.count() == 1 and self.tabs.widget(0) == self.welcomeTab:
            self.tabs.removeTab(0)

        taskList = TaskList()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(taskList)
        scroll.setWidget(container)

        self.tabs.addAnimatedTab(scroll, "Untitled")

    def addWelcomeTab(self) -> None:
        self.welcomeTab = QWidget()
        layout = QVBoxLayout(self.welcomeTab)
        label = QLabel("👋 Welcome to Tasker!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.tabs.addAnimatedTab(self.welcomeTab, "Welcome")

    def closeTab(self, index: int):
        widget = self.tabs.widget(index)

        # Prevent closing the welcome tab if it's the only one
        if widget == self.welcomeTab and self.tabs.count() == 1:
            return

        self.tabs.closeAnimatedTab(index)
        if widget:
            widget.deleteLater()

        # If all task tabs are closed, show the welcome tab again
        if self.tabs.count() == 0:
            self.addWelcomeTab()

    def mainLoop(self) -> None:
        """Start the application event loop."""
        self.show()
        self.qtApplication.exec_()

    def showTaskListExplorer(self) -> None:
        self.tabs.addAnimatedTab(self.explorer, "Explorer")