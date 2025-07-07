
__all__ = ["sideBar", "titleBar", "tab"]

from .sideBar import SideBar
from .titleBar import CustomTitleBar
from .tab import CustomTabWidget

from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget
)


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