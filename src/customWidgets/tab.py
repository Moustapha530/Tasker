from PyQt5.QtWidgets import QTabWidget, QTabBar, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QFontMetrics
from PyQt5.QtCore import Qt, QSize, QVariantAnimation, QEasingCurve, QRect


class CustomTabBar(QTabBar):
    def __init__(self,
                 radius=8,
                 activeColor="#ffffff",
                 inactiveColor="#e0e0e0",
                 hoverColor="#f1f3f4",
                 borderWidth=1,
                 padding=8,
                 tabWidth=None,
                 tabHeight=32):
        super().__init__()

        self.radius = radius
        self.activeColor = QColor(activeColor)
        self.inactiveColor = QColor(inactiveColor)
        self.hoverColor = QColor(hoverColor)

        self.borderWidth = borderWidth
        

        self.padding = padding

        self.fixedTabWidth = tabWidth
        self.fixedTabHeight = tabHeight


        self.hoverIndex = -1
        self.hoverAnim = QVariantAnimation(self)
        self.hoverAnim.setDuration(150)
        self.hoverAnim.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.hoverAnim.valueChanged.connect(self.update)
        self.hoverProgress = 0.0

        self.setMouseTracking(True)
        self.setUsesScrollButtons(False)
        self.setExpanding(False)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setContentsMargins(0, 0, 0, 0)

    def tabSizeHint(self, index):
        if self.fixedTabWidth is not None:
            width = self.fixedTabWidth
        else:
            metrics = QFontMetrics(self.font())
            text = self.tabText(index)
            width = metrics.horizontalAdvance(text) + 2 * self.padding

        return QSize(width, self.fixedTabHeight)

    def enterEvent(self, event):
        super().enterEvent(event)
        self.update()

    def leaveEvent(self, event):
        self.hoverIndex = -1
        self.hoverAnim.setDirection(self.hoverAnim.Backward)
        self.hoverAnim.start()
        super().leaveEvent(event)

    def mouseMoveEvent(self, event):
        idx = self.tabAt(event.pos())
        if idx != self.hoverIndex:
            self.hoverIndex = idx
            self.hoverAnim.setDirection(self.hoverAnim.Forward)
            self.hoverAnim.start()
        super().mouseMoveEvent(event)

    def roundedRectPath(self, rect : QRect, r1 : int, r2 : int , r3 : int, r4 : int) -> None:
        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        path = QPainterPath()
        path.moveTo(x + r1, y)
        path.lineTo(x + w - r2, y)
        path.quadTo(x + w, y, x + w, y + r2)
        path.lineTo(x + w, y + h - r3)
        path.quadTo(x + w, y + h, x + w - r3, y + h)
        path.lineTo(x + r4, y + h)
        path.quadTo(x, y + h, x, y + h - r4)
        path.lineTo(x, y + r1)
        path.quadTo(x, y, x + r1, y)
        path.closeSubpath()
        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        current = self.currentIndex()

        for idx in range(self.count()):
            rect = self.tabRect(idx)
            isActive = (idx == current)

            
            if isActive:
                r1, r2, r3, r4 = self.radius, self.radius, 0, 0
            elif idx == current - 1:
                r1, r2, r3, r4 = 0, 0, self.radius, 0
            elif idx == current + 1:
                r1, r2, r3, r4 = 0, 0, 0, self.radius
            elif idx == self.hoverIndex:
                r1 = r2 = r3 = r4 = self.radius
            else:
                r1 = r2 = r3 = r4 = 0
            

            if isActive:
                color = self.activeColor
            elif idx == self.hoverIndex:
                color = QColor(self.hoverColor)
                color.setAlphaF(self.hoverAnim.currentValue() or 0)
            else:
                color = self.inactiveColor if (idx == current - 1 or idx == current + 1) else QColor(0, 0, 0, 0)

            path = self.roundedRectPath(rect, r1, r2, r3, r4)

            painter.setPen(Qt.NoPen)
            painter.setBrush(color)
            painter.drawPath(path)

            painter.setPen(QPen(self.inactiveColor, self.borderWidth))
            painter.drawLine(rect.topLeft(), rect.topRight())

            painter.setPen(Qt.GlobalColor.white)
            font = QFont()
            font.setBold(isActive)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.tabText(idx))

        painter.end()

class CustomTabWidget(QTabWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setTabBar(CustomTabBar(**kwargs))
        self.setDocumentMode(True)
        self.setElideMode(Qt.TextElideMode.ElideRight)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.setUsesScrollButtons(False)
        self.setContentsMargins(0, 0, 0, 0)