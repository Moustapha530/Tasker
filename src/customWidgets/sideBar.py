from PyQt5.QtWidgets import (
    QFrame,
    QMainWindow,
    QPushButton, 
    QVBoxLayout
)
from qtawesome import icon

class SideBar(QFrame):
    """
    Sidebar widget with navigation buttons.
    """

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(70)
        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 40, 10, 10)
        mainLayout.setSpacing(10)

        btnFrame = QFrame(self)
        btnFrame.setFixedWidth(50)
        btnFrame.setObjectName("BtnFrame")

        layout = QVBoxLayout(btnFrame)
        layout.setContentsMargins(0, 20, 0, 0)

        self.homeBtn = QPushButton()
        self.homeBtn.setIcon(icon("fa5s.home", color="white"))
        self.homeBtn.setObjectName("SidebarButton")
        self.homeBtn.setFixedSize(btnFrame.width(), btnFrame.width())
        layout.addWidget(self.homeBtn)

        self.taskListsBtn = QPushButton()
        self.taskListsBtn.setIcon(icon("fa5s.folder", color="white"))
        self.taskListsBtn.setObjectName("SidebarButton")
        self.taskListsBtn.setFixedSize(btnFrame.width(), btnFrame.width())
        layout.addWidget(self.taskListsBtn)

        self.taskCheckBtn = QPushButton()
        self.taskCheckBtn.setIcon(icon("fa5s.check-circle", color="white"))
        self.taskCheckBtn.setObjectName("SidebarButton")
        self.taskCheckBtn.setFixedSize(btnFrame.width(), btnFrame.width())
        layout.addWidget(self.taskCheckBtn)

        layout.addStretch() 

        self.settingsBtn = QPushButton()
        self.settingsBtn.setIcon(icon("fa5s.cog", color="white"))
        self.settingsBtn.setObjectName("SidebarButton")
        self.settingsBtn.setFixedSize(btnFrame.width(), btnFrame.width())
        layout.addWidget(self.settingsBtn)

        self.addItemBtn = QPushButton()
        self.addItemBtn.setIcon(icon("fa5s.plus-circle", color="white"))
        self.addItemBtn.setObjectName("AddItemButton")
        self.addItemBtn.setFixedSize(btnFrame.width(), btnFrame.width())
        layout.addWidget(self.addItemBtn)

        mainLayout.addWidget(btnFrame)
