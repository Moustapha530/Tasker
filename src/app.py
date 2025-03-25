"""
    The app module for manage application.
    This an opensource code made by [SalemMalola](https://github.com/Salem530)
"""
# Depencies importations
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QWidget,
)
# Locals importations
from customWidgets import AppLogo, CustomTitleBar, loadStyleSheet

class Tasker(QMainWindow):
    """The app manager"""
    def __init__(self):
        self.qtApplication = QApplication([])
        super().__init__()
        self.setGeometry(100, 100, 900, 600)
        self.setWindowTitle("Tasker")
        self.setStyleSheet(loadStyleSheet("style"))
        # Central widget
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        # Main layout
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        # Create the app logo
        self.appLogo = AppLogo(self, "ressources//images//tasker.png")
        self.layout.addWidget(self.appLogo, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        # Title bar
        self.titleBar = CustomTitleBar(self)
        self.layout.addWidget(self.titleBar, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

    def mainLoop(self) -> None:
        self.show()
        self.qtApplication.exec_()