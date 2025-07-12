from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton, 
    QSizePolicy,
)
from qframelesswindow import TitleBarBase
from qtawesome import icon
# Locals importations
from .tab import CustomTabWidget

class CustomTitleBar(QFrame, TitleBarBase):
    """
    Custom title bar with the tab widget. 
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.parentWindow = parent
        self.setFixedHeight(40) 
        self.setupUi()
        self.setObjectName("CustomTitlebar")

    def eventFilter(self, obj, e : QEvent) -> bool:
        if obj is self.parentWindow:
            if e.type() == QEvent.Type.WindowStateChange:
                self.updateMaxRestoreButton()
                return False

        return super().eventFilter(obj, e)

    def maximizeRestoreWindow(self) -> None:
        self.updateMaxRestoreButton()
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def setupUi(self) -> None:
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
                borderWidth=8,
                padding=8,
                tabHeight=42,
                tabWidth=140)
        self.tabWidget.setObjectName("CustomTabWidget")
        self.tabWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        layout.addWidget(self.tabWidget)

        layout.addStretch() 

        self.minButton = QPushButton("")
        self.minButton.setIcon(icon("fa5s.window-minimize", color="white"))
        self.minButton.setObjectName("MinButton")
        self.minButton.setFixedSize(self.height(), self.height())
        self.minButton.clicked.connect(self.window().showMinimized)
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
        self.closeButton.clicked.connect(self.window().close)
        layout.addWidget(self.closeButton)

        self.startPos = None

    def updateMaxRestoreButton(self) -> None:
        if self.window().isMaximized():
            self.maxRestoreButton.setIcon(icon("mdi.window-restore", color="white"))
        else:
            self.maxRestoreButton.setIcon(icon("mdi.window-maximize", color="white"))