"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import Qt, QPoint, QPropertyAnimation, QRect
from PyQt5.QtGui import QIcon, QFont, QPixmap, QMouseEvent
from PyQt5.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton, 
    QSizePolicy,
    QVBoxLayout,
)
# Locals importations
from themes import applyCTheme

class AppLogo(QFrame):
    """ 
    Custom widget that represents the application's title for
    custom titlte bar, it allows the user to move the main window by 
    dragging it.
    
    Attributes:
        title (QLabel): The app title
        _old_pos (QPoint | None): Stores the last known mouse position 
                                  for window movement.
    """

    def __init__(self, parent: QMainWindow, title : str) -> None:
        """
        Initializes the title widget with an image and enables window dragging.

        Args:
            parent (QMainWindow): The main application window.
            title (str): The app title text.
        """
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName("CAppLogo")
        self.setFixedHeight(50)
        self.layout = QHBoxLayout(self)
        self.title = QLabel(f"<h1>{title}</h1>", self) # Create the title label
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter) # Add the to the layout
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
        appLogo (AppLogo) : The dragable zone widget. 
        minimizeBtn (QPushButton) : The button to minimize the window.
        toogleMaximizeBtn (QPushButton) : The button to maximize or set the window normal.
        closeBtn (QPushButton) : The button to close the window.

        resizeIcon (QIcon) : The toogleMaximizeBtn icon.
        maximizeIcon (QIcon) : The toogleMaximizeBtn icon.
        layout (QHBoxLayout) : The layout to place buttons.
    """
    def __init__(self, parent : QMainWindow, title : str) -> None:
        """
        Create a instance of the CustomTitleBar for the given parent window.

        Args:
            parent (QMainWindow): The object window parent.
            title (str): The title for the app logo. 
        """
        super().__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.setObjectName("CTitleBar")
        self.setStyleSheet(applyCTheme())
        self.layout = QHBoxLayout(self)

        # Create the dragable zone
        self.appLogo = AppLogo(self, title)
        self.appLogo.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding) # Expland this
        self.layout.addWidget(self.appLogo)
        # Create the dragable zone
        self.btnFrame = QFrame(self)
        self.layout.addWidget(self.btnFrame)
        # Create minimize button
        self.minimizeBtn = QPushButton("", self.btnFrame)
        self.minimizeBtn.setIcon(QIcon("ressources\\icons\\minimize.png"))
        self.minimizeBtn.setFixedSize(35, 35)
        self.minimizeBtn.clicked.connect(self.window().showMinimized)
        self.minimizeBtn.setToolTip("Minimize window")
        # Create toogle minisize and maximize button
        self.toogleMaximizeBtn = QPushButton("", self.btnFrame)
        self.resizeIcon = QIcon("ressources\\icons\\resize.png")
        self.maximizeIcon = QIcon("ressources\\icons\\maximize.png")
        self.toogleMaximizeBtn.setIcon(self.maximizeIcon)
        self.toogleMaximizeBtn.setFixedSize(35, 35)
        self.toogleMaximizeBtn.setToolTip("Toogle maximize")
        self.toogleMaximizeBtn.clicked.connect(self.toogleMaximize)
        # Create close button
        self.closeBtn = QPushButton("", self.btnFrame)
        self.closeBtn.setIcon(QIcon("ressources\\icons\\cross.png"))
        self.closeBtn.setObjectName("CloseBtn")
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

class TaskListDialog(QDialog):
    """
    A modern dialog box for creating a new task list.

    Attributes:
        taskNameInput (QLineEdit): Input field for the task list name.
        confirmButton (QPushButton): Button to confirm task list creation.
        cancelButton (QPushButton): Button to cancel the dialog.
    """

    def __init__(self, parent=None):
        """
        Initialize the task list dialog.

        Args:
            parent (QWidget, optional): The parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("New Task List")
        self.setFixedSize(400, 200)


        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title Label
        titleLabel = QLabel("Create a New Task List")
        titleLabel.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(titleLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        # Task Name Input
        self.taskNameInput = QLineEdit()
        self.taskNameInput.setPlaceholderText("Enter task list name...")
        layout.addWidget(self.taskNameInput)

        # Buttons Layout
        buttonLayout = QHBoxLayout()

        # Cancel Button
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.reject)  # Close dialog on cancel
        buttonLayout.addWidget(self.cancelButton)

        # Confirm Button
        self.confirmButton = QPushButton("Create")
        self.confirmButton.clicked.connect(self.accept)  # Confirm action
        buttonLayout.addWidget(self.confirmButton)

        layout.addLayout(buttonLayout)

class SideBar(QFrame):
    """
    Sidebar widget with navigation buttons and sliding animation.
    """

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setFixedWidth(60)

        self.setObjectName("CSideBar")
        self.setStyleSheet(applyCTheme())
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        buttons = {
            "Close": "ressources\\icons\\left.png",
            "Task lists": "ressources\\icons\\tasklists.png",
            "Add Task List": "ressources\\icons\\new_tasklist.png",
            "Edit Task": "ressources\\icons\\edit.png",
            "Settings": "ressources\\icons\\settings.png",
        }
        self.buttons : dict[str, QPushButton] = dict()

        for name, icon_path in buttons.items():
            btn = QPushButton("", self)
            btn.setIcon(QIcon(icon_path))
            btn.setFixedSize(50, 50)
            btn.setToolTip(name)

            if name == "Close":
                btn.clicked.connect(self.toggleSidebar)
            elif name == "Add Task List":
                btn.clicked.connect(self.showTaskListDialog)

            self.layout.addWidget(btn)
            self.buttons[name] = btn

        # Animation for sidebar
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 300ms animation speed

    def showTaskListDialog(self) -> str | None:
        """
        Display the 'New Task List' dialog.
        """
        dialog = TaskListDialog(self)
        if dialog.exec_():  # If 'Create' is clicked
            task_name = dialog.taskNameInput.text().strip()
            if task_name:
                return task_name
            else:
                QMessageBox.warning(self, "Invalid Name", "Task list name cannot be empty.")

    def toggleSidebar(self) -> None:
        """
        Open or close the sidebar using an animation.
        """
        if self.width() == 60:  # If sidebar is open
            self.animation.setStartValue(QRect(self.x(), self.y(), 60, self.height()))
            self.animation.setEndValue(QRect(self.x(), self.y(), 0, self.height()))
        else:  # If sidebar is closed
            self.animation.setStartValue(QRect(self.x(), self.y(), 0, self.height()))
            self.animation.setEndValue(QRect(self.x(), self.y(), 60, self.height()))

        self.animation.start()