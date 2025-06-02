"""
    Module that contains customed widgets for the application.
"""
from PyQt5.QtCore import QEasingCurve, Qt, QPoint, QPropertyAnimation, QRect, QSize
from PyQt5.QtGui import QColor, QIcon, QMouseEvent, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton, 
    QSizePolicy,
    QTabBar,
    QTabWidget, 
    QVBoxLayout,
    QWidget
)
# Locals importations
from themes import get_theme, getCurrentTheme

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

class CustomTabBar(QTabBar): 
    
    def __init__(self): 
        super().__init__() 
        self.setDrawBase(False) 
        self.setElideMode(Qt.TextElideMode.ElideRight) 
        self.setTabsClosable(True) 
        self.setMovable(True) 
        self.theme = get_theme(getCurrentTheme()) 
        self.setMouseTracking(True)

    def tabSizeHint(self, index: int) -> QSize:
        return QSize(128, 36)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.drawTabBarBackground(painter)

        for i in range(self.count()):
            rect = self.tabRect(i)
            is_selected = (i == self.currentIndex())
            self.drawTab(painter, rect, i, is_selected)

    def drawTab(self, painter: QPainter, rect: QRect, index: int, is_selected: bool):
        tab_color = QColor(self.theme['secondaryColor'])
        border_color = QColor(self.theme['primaryTextColor'])
        text_color = QColor(self.theme['primaryTextColor'])
        selected_color = QColor(self.theme['secondaryDarkColor'])

        path = QPainterPath()
        path.moveTo(rect.left() + 10, rect.bottom())
        path.lineTo(rect.left() + 4, rect.top() + 12)
        path.quadTo(rect.left(), rect.top(), rect.left() + 10, rect.top())
        path.lineTo(rect.right() - 10, rect.top())
        path.quadTo(rect.right(), rect.top(), rect.right() - 4, rect.top() + 12)
        path.lineTo(rect.right() - 10, rect.bottom())

        painter.setPen(Qt.NoPen)
        painter.setBrush(selected_color if is_selected else tab_color)
        painter.drawPath(path)

        if not is_selected and index < self.count() - 1:
            sep_x = rect.right() - 1
            painter.setPen(QPen(border_color, 1))
            painter.drawLine(sep_x, rect.top() + 10, sep_x, rect.bottom() - 6)

        painter.setPen(QPen(text_color))
        font = painter.font()
        font.setBold(is_selected)
        painter.setFont(font)
        text = self.tabText(index)
        painter.drawText(rect.adjusted(12, 6, -12, -6), Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, text)

    def drawTabBarBackground(self, painter: QPainter):
        bg_rect = QRect(0, 0, self.width(), self.height() + 6)
        painter.fillRect(bg_rect, QColor(self.theme['secondaryColor']))

class CustomTabWidget(QTabWidget): 
    
    def __init__(self, parent = None): 
        super().__init__(parent) 
        self.setTabBar(CustomTabBar()) 
        self.setTabPosition(QTabWidget.TabPosition.North) 
        self.setObjectName("CTabWidget") 
        self.setStyleSheet("QTabWidget::pane { border: none; margin-top: -6px; background: none; }") 
        self.tabCloseRequested.connect(self.closeAnimatedTab)

    def addAnimatedTab(self, new_tab : QWidget | None = None, name : str = "New Tab"):
        if new_tab is None:
            new_tab = QWidget()
            layout = QVBoxLayout(new_tab)
            layout.setContentsMargins(0, 0, 0, 0)
            
        self.addTab(new_tab, name)

        index = self.indexOf(new_tab)
        self.setCurrentIndex(index)

        tab_rect = self.tabBar().tabRect(index)
        start_x = self.tabBar().width()

        anim = QPropertyAnimation(self.tabBar(), b"pos")
        anim.setStartValue(QPoint(start_x, tab_rect.y()))
        anim.setEndValue(QPoint(0, 0))
        anim.setDuration(300)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._tab_add_anim = anim  # Prevent GC

    def closeAnimatedTab(self, index : int):
        widget = self.widget(index)
        if not widget:
            return
        anim = QPropertyAnimation(widget, b"maximumWidth")
        anim.setStartValue(widget.width())
        anim.setEndValue(0)
        anim.setDuration(200)
        anim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        anim.finished.connect(lambda: self.removeTab(index))
        anim.start()
        self._tab_close_anim = anim    

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
        parent.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(50)
        self.setObjectName("CTitleBar")
        self.setStyleSheet(self.applyCTheme())
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

    def applyCTheme(self) -> str:
        theme = get_theme(getCurrentTheme())
        return f"""
        #CTitleBar{{
            background-color: {theme['secondaryColor']};
            border-radius: 0px;
            border-bottom-right-radius: 15px;
            border-top-right-radius: 15px;
        }}

        #CTitleBar QFrame{{
            background-color: {theme['secondaryColor']};
        }}

        #CloseBtn:hover{{
            background-color: red;
        }}
        """

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

class SideBar(QFrame):
    """
    Sidebar widget with navigation buttons and sliding animation.
    """

    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.setFixedWidth(60)
        self.setMaximumWidth(60)
        self.setMinimumWidth(0)

        self.setObjectName("CSideBar")
        self.setStyleSheet(self.applyCTheme())
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

        buttons = {
            "Close side bar": ["ressources\\icons\\left.png", "ctrl+shift+t"],
            "Show task lists": ["ressources\\icons\\tasklists.png", "ctrl+shift+e"],
            "Add task list": ["ressources\\icons\\new_tasklist.png", "ctrl+shift+n"],
            "Settings": ["ressources\\icons\\settings.png", "ctrl+shift+s"],
        }
        self.buttons : dict[str, QPushButton] = dict()

        for name, value in buttons.items():
            btn = QPushButton("", self)
            btn.setIcon(QIcon(value[0]))
            btn.setFixedSize(50, 50)
            btn.setShortcut(value[1])
            btn.setToolTip(f"{name} ({btn.shortcut().toString()})")

            if name == "Close side bar":
                btn.clicked.connect(self.toggleSidebar)
                

            self.layout.addWidget(btn)
            self.buttons[name] = btn

        # Animation for sidebar
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)  # 300ms animation speed

    def applyCTheme(self) -> str:
        theme = get_theme(getCurrentTheme())
        return f"""
        #CSideBar{{
            background-color: {theme['secondaryColor']};
            border-radius: 0px;
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
        }}        
        """


    def toggleSidebar(self) -> None:
        """
        Slide the sidebar in or out using width animation (layout-friendly).
        """
        target_width = 0 if self.width() > 30 else 60
        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(target_width)
        self.animation.start()

class SectionTitle(QWidget):
    def __init__(self, text: str):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setObjectName("SectionTitle")
        self.setStyleSheet(self.applyCTheme())
        self.label = QLabel(text.upper())
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedSize(90, 8)
        line.setObjectName("line")
        layout.addWidget(self.label)
        layout.addWidget(line)

    def applyCTheme(self) -> str:
        theme = get_theme(getCurrentTheme())
        return f"""
        #SectionTitle QLabel{{
            background-color: transparent;
            font-weight: bold; 
            font-size: 16px;
        }}

        #SectionTitle #line{{
            background-color: {theme['primaryColor']};
            border-radius: 3px;
        }}
        """