from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent 
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton, 
    QSizePolicy,
)
from qtawesome import icon
# Locals importations
from .tab import CustomTabWidget

class CustomTitleBar(QFrame):
    """
    Custom title bar with the tab widget. 
    """
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40) 
        self.setupUi()
        self.setObjectName("CustomTitlebar")

    def setupUi(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.checkBtn = QPushButton("")
        self.checkBtn.setIcon(icon("fa5s.check", color="white"))
        self.checkBtn.setObjectName("Icon")
        self.checkBtn.setFixedSize(70, 40)
        layout.addWidget(self.checkBtn)
        
        self.tabWidget = CustomTabWidget(radius=10,
                activeColor="#273044",
                inactiveColor="#181f30",
                hoverColor="#344058",
                tabHeight=42,
                borderWidth=0,
                padding=8,
                margin=0,
                tabWidth=140)
        self.tabWidget.setObjectName("CustomTabWidget")
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        layout.addWidget(self.tabWidget)

        layout.addStretch() 

        self.minButton = QPushButton("")
        self.minButton.setIcon(icon("fa5s.window-minimize", color="white"))
        self.minButton.setObjectName("MinButton")
        self.minButton.setFixedSize(self.height(), self.height())
        self.minButton.clicked.connect(self.minimizeWindow)
        layout.addWidget(self.minButton)

        self.maxRestoreButton = QPushButton("")
        self.maxRestoreButton.setIcon(icon("mdi.window-maximize", color="white"))
        self.maxRestoreButton.setObjectName("MaxRestoreButton")
        self.maxRestoreButton.setFixedSize(self.height(), self.height())
        self.maxRestoreButton.clicked.connect(self.maximizeRestoreWindow)
        layout.addWidget(self.maxRestoreButton)

        self.closeButton = QPushButton("")
        self.closeButton.setIcon(icon("mdi.close", color="white"))
        self.closeButton.setObjectName("CloseButton")
        self.closeButton.setFixedSize(self.height(), self.height())
        self.closeButton.clicked.connect(self.closeWindow)
        layout.addWidget(self.closeButton)

        self.startPos = None

    def mousePressEvent(self, event : QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.startPos = event.globalPos() - self.window().frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event : QMouseEvent):
        if self.startPos is not None and event.buttons() == Qt.MouseButton.LeftButton:
            self.window().move(event.globalPos() - self.startPos)
            event.accept()

    def mouseReleaseEvent(self, event : QMouseEvent):
        self.startPos = None
        event.accept()

    def minimizeWindow(self):
        if self.window():
            self.window().showMinimized()

    def maximizeRestoreWindow(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.maxRestoreButton.setIcon(icon("mdi.window-maximize", color="white"))
        else:
            self.window().showMaximized()
            self.maxRestoreButton.setIcon(icon("mdi.window-restore", color="white"))

    def closeWindow(self):
        if self.window():
            self.window().close()
