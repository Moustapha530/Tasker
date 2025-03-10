"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QMainWindow,
    QPushButton
)
# Locals importations
from filesManager import loadStyleSheet

class CustomTitleBar(QFrame):
    """Personnalized title bar"""
    def __init__(self, parent : QMainWindow):
        super().__init__(parent)
        parent.setWindowFlag(Qt.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QHBoxLayout(self)
        self.setStyleSheet(loadStyleSheet("titleBarStyle"))
        # Create minimize button
        self.minimizeBtn = QPushButton("", self)
        self.minimizeBtn.setIcon(QIcon("ressources\\icons\\minimize.png"))
        self.minimizeBtn.setFixedSize(35, 35)
        self.minimizeBtn.clicked.connect(self.window().showMinimized)
        self.minimizeBtn.setToolTip("Minimize window")
        # Create toogle minisize and maximize button
        self.toogleMaximizeBtn = QPushButton("", self)
        self.resizeIcon = QIcon("ressources\\icons\\resize.png")
        self.maximizeIcon = QIcon("ressources\\icons\\maximize.png")
        self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
        self.toogleMaximizeBtn.setFixedSize(35, 35)
        self.toogleMaximizeBtn.setToolTip("Toogle maximize")
        self.toogleMaximizeBtn.clicked.connect(self.toogleMaximize)
        # Create close button
        self.closeBtn = QPushButton("", self)
        self.closeBtn.setIcon(QIcon("ressources\\icons\\cross.png"))
        self.closeBtn.setFixedSize(35, 35)
        self.closeBtn.clicked.connect(self.window().close)
        self.closeBtn.setToolTip("Close app")
        # Add buttons to the layout
        for btn in [self.minimizeBtn, self.toogleMaximizeBtn, self.closeBtn]:
            self.layout.addWidget(btn)

    # Toogle maximize command
    def toogleMaximize(self) -> None:
        if self.window().isMaximized():
            self.toogleMaximizeBtn.setToolTip("Toogle maximize")
            self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
            self.window().showNormal()
        else:
            self.toogleMaximizeBtn.setToolTip("Toogle minimize")
            self.toogleMaximizeBtn.setIcon(self.resizeIcon)
            self.window().showMaximized()