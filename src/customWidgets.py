"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import QEasingCurve, Qt, QPoint, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QColor, QIcon, QMouseEvent 
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton, 
    QVBoxLayout,
    QSizePolicy,
    QWidget
)

# Locals importations
from tab import CustomTabWidget

class CustomTitleBar(QWidget):
    """
    Custom title bar with the tab widget. 
    """
    def __init__(self, parent : QMainWindow):
        super().__init__(parent)
        self.parentWindow = parent
        self.setFixedHeight(40) 
        self.setupUi()
        self.setObjectName("CustomTitlebar")

    def setupUi(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.checkBtn = QPushButton("")
        self.checkBtn.setIcon(QIcon("ressources\\icons\\checked.png"))
        self.checkBtn.setObjectName("Icon")
        self.checkBtn.setFixedSize(50, self.height())
        layout.addWidget(self.checkBtn)
        
        self.tabWidget = CustomTabWidget(radius=10,
                activeColor="#282c36",
                borderTop=True,
                borderLeft=False,
                borderRight=False,
                borderBottom=False,
                roundCorners=True,
                inactiveColor="#3b4252",
                hoverColor="#4c566a",
                tabHeight=40,
                borderColor="#3b4252",
                borderWidth=10,
                padding=8,
                margin=0,
                tabWidth=120)
        self.tabWidget.setObjectName("CustomTabWidget")
        layout.addWidget(self.tabWidget)

        layout.addStretch() 

        self.minButton = QPushButton("")
        self.minButton.setIcon(QIcon("ressources\\icons\\minimize.png"))
        self.minButton.setObjectName("MinButton")
        self.minButton.setFixedSize(self.height(), self.height())
        self.minButton.clicked.connect(self.minimizeWindow)
        layout.addWidget(self.minButton)

        self.maxRestoreButton = QPushButton("")
        self.maxRestoreButton.setIcon(QIcon("ressources\\icons\\maximize.png"))
        self.maxRestoreButton.setObjectName("MaxRestoreButton")
        self.maxRestoreButton.setFixedSize(self.height(), self.height())
        self.maxRestoreButton.clicked.connect(self.maximizeRestoreWindow)
        layout.addWidget(self.maxRestoreButton)

        self.closeButton = QPushButton("")
        self.closeButton.setIcon(QIcon("ressources\\icons\\cross.png"))
        self.closeButton.setObjectName("CloseButton")
        self.closeButton.setFixedSize(self.height(), self.height())
        self.closeButton.clicked.connect(self.closeWindow)
        layout.addWidget(self.closeButton)

        self.startPos = None

    def mousePressEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPos() - self.parentWindow.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event : QMouseEvent):
        if self.startPos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.parentWindow.move(event.globalPos() - self.startPos)
            event.accept()

    def mouseReleaseEvent(self, event : QMouseEvent):
        self.startPos = None
        event.accept()

    def minimizeWindow(self):
        if self.parentWindow:
            self.parentWindow.showMinimized()

    def maximizeRestoreWindow(self):
        if self.parentWindow:
            if self.parentWindow.isMaximized():
                self.parentWindow.showNormal()
                self.maxRestoreButton.setIcon(QIcon("ressources\\icons\\maximize.png")) 
            else:
                self.parentWindow.showMaximized()
                self.maxRestoreButton.setIcon(QIcon("ressources\\icons\\resize.png"))

    def closeWindow(self):
        if self.parentWindow:
            self.parentWindow.close()

class SideBar(QFrame):
    """
    Sidebar widget with navigation buttons.
    """

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(50) 
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 10)
        layout.setSpacing(10)

        self.homeBtn = QPushButton()
        self.homeBtn.setIcon(QIcon("ressources\\icons\\home.png"))
        self.homeBtn.setObjectName("SidebarButton")
        self.homeBtn.setFixedSize(50, 50)
        layout.addWidget(self.homeBtn)

        self.taskListsBtn = QPushButton()
        self.taskListsBtn.setIcon(QIcon("ressources\\icons\\taskLists.png"))
        self.taskListsBtn.setObjectName("SidebarButton")
        self.taskListsBtn.setFixedSize(50, 50)
        layout.addWidget(self.taskListsBtn)

        self.taskCheckBtn = QPushButton()
        self.taskCheckBtn.setIcon(QIcon("ressources\\icons\\task_check.png"))
        self.taskCheckBtn.setObjectName("SidebarButton")
        self.taskCheckBtn.setFixedSize(50, 50)
        layout.addWidget(self.taskCheckBtn)

        layout.addStretch() 

        self.settingsBtn = QPushButton()
        self.settingsBtn.setIcon(QIcon("ressources\\icons\\settings.png"))
        self.settingsBtn.setObjectName("SidebarButton")
        self.settingsBtn.setFixedSize(50, 50)
        layout.addWidget(self.settingsBtn)

        self.addItemBtn = QPushButton()
        self.addItemBtn.setIcon(QIcon("ressources\\icons\\new.png"))
        self.addItemBtn.setObjectName("AddItemButton")
        self.addItemBtn.setFixedSize(50, 50)
        layout.addWidget(self.addItemBtn)

class SectionTitle(QWidget):
    def __init__(self, text: str):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setObjectName("SectionTitle")
        self.label = QLabel(text.upper())
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedSize(90, 8)
        line.setObjectName("line")
        layout.addWidget(self.label)
        layout.addWidget(line)

   