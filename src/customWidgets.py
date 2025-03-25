"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLabel,
    QMainWindow,
    QPushButton, 
)
# Locals importations
from filesManager import loadStyleSheet

from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QPoint

class AppLogo(QLabel):
    """ 
    Custom widget that represents the application's logo and allows 
    the user to move the main window by dragging it.
    
    Attributes:
        _old_pos (QPoint | None): Stores the last known mouse position 
                                  for window movement.
    """

    def __init__(self, parent: QMainWindow, logo_path: str) -> None:
        """
        Initializes the logo widget with an image and enables window dragging.

        Args:
            parent (QMainWindow): The main application window.
            logo_path (str): Path to the image file for the logo.
        """
        super().__init__(parent)

        # Load and display the logo image
        self.setPixmap(QPixmap(logo_path))
        self.setScaledContents(True)  # Enable automatic scaling
        self.setFixedSize(50, 50)  # Set a fixed size (adjustable)
        self.setCursor(Qt.CursorShape.OpenHandCursor)  # Change cursor to indicate dragging

        # Store the last known position of the mouse (None when idle)
        self._old_pos: QPoint | None = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Captures the mouse position when the user presses the left button.

        Args:
            event (QMouseEvent): The mouse event containing position data.
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPos()  # Store initial position

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Moves the application window when the user drags the logo.

        Args:
            event (QMouseEvent): The mouse movement event.
        """
        if self._old_pos is not None:
            # Calculate the movement delta (difference between old and new position)
            delta: QPoint = event.globalPos() - self._old_pos
            
            # Move the main window to the new position
            self.window().move(self.window().pos() + delta)
            
            # Update the stored position for smooth movement
            self._old_pos = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """
        Resets the stored position when the user releases the mouse button.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        self._old_pos = None  # Reset the stored position



class CustomTitleBar(QFrame):
    """ 
    Custom title bar for the application.
    
    Attributes:
        minimizeBtn (QPushButton) : The button to minimize the window.
        toogleMaximizeBtn (QPushButton) : The button to maximize or set the window normal.
        closeBtn (QPushButton) : The button to close the window.

        resizeIcon (QIcon) : The toogleMaximizeBtn icon.
        maximizeIcon (QIcon) : The toogleMaximizeBtn icon.
        layout (QHBoxLayout) : The layout to place buttons.
    """
    def __init__(self, parent : QMainWindow) -> None:
        """
        Create a instance of the CustomTitleBar for the given parent window.

        Args:
            parent (QMainWindow): The object window parent.
        """
        super().__init__(parent)
        parent.setWindowFlag(Qt.WindowType.FramelessWindowHint)
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
        """
        Toogle parent window maximed or normal.

        Args: No args
        """
        if self.window().isMaximized():
            self.toogleMaximizeBtn.setToolTip("Toogle maximize")
            self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
            self.window().showNormal()
        else:
            self.toogleMaximizeBtn.setToolTip("Toogle minimize")
            self.toogleMaximizeBtn.setIcon(self.resizeIcon)
            self.window().showMaximized()