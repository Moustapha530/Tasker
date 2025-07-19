from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QScrollArea,
)
from qframelesswindow import FramelessMainWindow
# Local imports
from customWidgets import CustomTitleBar, SideBar
from .tasksList import TaskList, TaskListExplorer

class Tasker(FramelessMainWindow):
    """The main application window with VSCode-like layout."""

    def __init__(self):
        """Initialize the main UI structure."""
        self.qtApplication = QApplication([])
        super().__init__()
        self.setWindowTitle("Tasker")
        self.setGeometry(10, 10, 500, 500)
        self.setContentsMargins(0, 0, 0, 0)

        centralWidget = QWidget()
        centralWidget.setObjectName("MainWindowContainer") 
        self.setCentralWidget(centralWidget)

        mainLayout = QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        
        self.titleBar = CustomTitleBar(self)
        mainLayout.addWidget(self.titleBar)

        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)

        sideBar = SideBar(self)
        contentLayout.addWidget(sideBar)

        sideBar.homeBtn.clicked.connect(self.addWelcomeTab)
        sideBar.taskListsBtn.clicked.connect(self.showTaskListExplorer)
        sideBar.taskCheckBtn.clicked.connect(self.settings)
        sideBar.settingsBtn.clicked.connect(self.settings)
        sideBar.addItemBtn.clicked.connect(self.addNewTaskList)

        mainContentArea = QWidget()
        mainContentAreaLayout = QVBoxLayout(mainContentArea)
        mainContentAreaLayout.setContentsMargins(0, 0, 0, 0)
        mainContentAreaLayout.setSpacing(0)
        mainContentAreaLayout.addWidget(self.titleBar.tabWidget.findChild(QStackedWidget)) 

        contentLayout.addWidget(mainContentArea)
        mainLayout.addLayout(contentLayout)
        self.titleBar.tabWidget.tabCloseRequested.connect(self.closeTab)
        self.applyStylesheet()
        self.addWelcomeTab()

    def addTaskList(self, taskList : TaskList, name = "Untitled") -> None:
        # Remove welcome tab if it's the only tab
        if self.titleBar.tabWidget.count() == 1 and self.titleBar.tabWidget.widget(0) == self.welcomeTab:
            self.titleBar.tabWidget.removeTab(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(taskList)
        scroll.setWidget(container)

        self.titleBar.tabWidget.addTab(scroll, name)

    def addNewTaskList(self) -> None:
        taskList = TaskList()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(taskList)
        scroll.setWidget(container)

        self.titleBar.tabWidget.addTab(scroll, "Untitled")

    def addWelcomeTab(self) -> None:
        self.welcomeTab = QWidget()
        layout = QVBoxLayout(self.welcomeTab)
        label = QLabel("👋 Welcome to Tasker!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.titleBar.tabWidget.addTab(self.welcomeTab, "Welcome")
    
    def applyStylesheet(self):
        stylesheet = """
        #MainWindowContainer {
            background-color: #273044; 
        }

        #BtnFrame {
            background-color: #2a3247;
            border-radius: 20px;
        }

        #Sidebar {
            background-color: #181f30; 
        }

        #SidebarButton {
            background-color: transparent;
            border: none;
            border-radius: 5px;
        }

        #SidebarButton:hover {
            background-color: #4c566a; 
        }

        #AddItemButton {
            background-color: #5e81ac; 
            color: white;
            font-size: 24px;
            font-weight: bold;
            border: none;
            border-radius: 25px; 
        }

        #AddItemButton:hover {
            background-color: #6a9ac9; 
        }

        /* --- CustomTitleBar --- */
        #CustomTitlebar {
            background-color: #181f30; 
        }

        #CustomTabWidget QTabBar::close-button {
            border-radius: 6px;
            image : url("ressources/images/cross.png");
            padding: 4px;
            subcontrol-position: right;
            width: 32px;
            height: 32px;
        }

        #CustomTabWidget QTabBar::close-button:hover {
            background-color: #6a9ac9; 
        }

        #Icon, #Icon:hover {
            background-color: #2a3247; 
            border-radius: 10px; 
            margin: 10px;
        }
 
        #MinButton, #MaxRestoreButton, #CloseButton {
            background-color: transparent;
            color: #eceff4;
            font-size: 16px;
            border: none;
            font-weight: bold;
        }

        #MinButton:hover, #MaxRestoreButton:hover {
            background-color: #4c566a;
        }

        #CloseButton:hover {
            background-color: #bf616a; 
        }

        /* Default style */
        QWidget {
            background-color: transparent;
            border: none;
        }

        QScrollBar:vertical {
            width: 12px;
            background: #2b2b2b;
        }

        QScrollBar::handle:vertical {
            background: #888;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical:hover {
            background: #aaa;
        }
        """
        self.setStyleSheet(stylesheet)

    def closeTab(self, index: int):
        widget = self.titleBar.tabWidget.widget(index)

        # Prevent closing the welcome tab if it's the only one
        if widget == self.welcomeTab and self.titleBar.tabWidget.count() == 1:
            return

        self.titleBar.tabWidget.removeTab(index)
        if widget:
            widget.deleteLater()

        # If all task tabs are closed, show the welcome tab again
        if self.titleBar.tabWidget.count() == 0:
            self.addWelcomeTab()

    def mainLoop(self) -> None:
        """Start the application event loop."""
        self.show()
        self.qtApplication.exec_()

    def settings(self) -> None:
        pass

    def showTaskListExplorer(self) -> None:
        explorer = TaskListExplorer(self)
        self.titleBar.tabWidget.addTab(explorer, "Explorer")