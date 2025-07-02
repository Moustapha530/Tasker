from PyQt5.QtWidgets import QTabWidget, QTabBar, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPainterPath, QFontMetrics
from PyQt5.QtCore import Qt, QRect, QSize, QVariantAnimation, QEasingCurve


class CustomTabBar(QTabBar):
    def __init__(self,
                 radius=8,
                 activeColor="#ffffff",
                 inactiveColor="#e0e0e0",
                 hoverColor="#f1f3f4",
                 borderColor="#dcdcdc",
                 borderWidth=1,
                 padding=8,
                 margin=0,
                 tabWidth=None,
                 tabHeight=32,
                 borderTop=True,
                 borderBottom=True,
                 borderLeft=True,
                 borderRight=True,
                 borderTopColor=None,
                 borderBottomColor=None,
                 borderLeftColor=None,
                 borderRightColor=None,
                 roundCorners=True):
        super().__init__()

        self.radius = radius
        self.activeColor = QColor(activeColor)
        self.inactiveColor = QColor(inactiveColor)
        self.hoverColor = QColor(hoverColor)

        self.borderWidth = borderWidth
        self.borderTop = borderTop
        self.borderBottom = borderBottom
        self.borderLeft = borderLeft
        self.borderRight = borderRight

        defaultColor = QColor(borderColor)
        self.borderTopColor = QColor(borderTopColor) if borderTopColor else defaultColor
        self.borderBottomColor = QColor(borderBottomColor) if borderBottomColor else defaultColor
        self.borderLeftColor = QColor(borderLeftColor) if borderLeftColor else defaultColor
        self.borderRightColor = QColor(borderRightColor) if borderRightColor else defaultColor

        self.padding = padding
        self.margin = margin

        self.fixedTabWidth = tabWidth
        self.fixedTabHeight = tabHeight

        self.roundCorners = roundCorners

        self.hoverIndex = -1
        self.hoverAnim = QVariantAnimation(self)
        self.hoverAnim.setDuration(150)
        self.hoverAnim.setEasingCurve(QEasingCurve.InOutCubic)
        self.hoverAnim.valueChanged.connect(self.update)
        self.hoverProgress = 0.0

        self.setMouseTracking(True)
        self.setUsesScrollButtons(True)
        self.setExpanding(False)

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

    def roundedRectPath(self, rect, r1, r2, r3, r4):
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
        painter.setRenderHint(QPainter.Antialiasing)
        current = self.currentIndex()

        for idx in range(self.count()):
            rect = self.tabRect(idx).adjusted(self.margin, self.margin,
                                               -self.margin, -self.margin)
            isActive = (idx == current)

            if self.roundCorners:
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

            # Dessin de chaque bordure via un QPainterPath personnalisé
            border_path = QPainterPath()
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

            if self.borderTop:
                painter.setPen(QPen(self.borderTopColor, self.borderWidth))
                border_path.moveTo(x + r1, y)
                border_path.lineTo(x + w - r2, y)
                if r2 > 0:
                    border_path.quadTo(x + w, y, x + w, y + r2)
            if self.borderRight:
                painter.setPen(QPen(self.borderRightColor, self.borderWidth))
                border_path.moveTo(x + w, y + r2)
                border_path.lineTo(x + w, y + h - r3)
                if r3 > 0:
                    border_path.quadTo(x + w, y + h, x + w - r3, y + h)
            if self.borderBottom:
                painter.setPen(QPen(self.borderBottomColor, self.borderWidth))
                border_path.moveTo(x + w - r3, y + h)
                border_path.lineTo(x + r4, y + h)
                if r4 > 0:
                    border_path.quadTo(x, y + h, x, y + h - r4)
            if self.borderLeft:
                painter.setPen(QPen(self.borderLeftColor, self.borderWidth))
                border_path.moveTo(x, y + h - r4)
                border_path.lineTo(x, y + r1)
                if r1 > 0:
                    border_path.quadTo(x, y, x + r1, y)
                    
            if self.borderWidth:
                painter.drawPath(border_path)

            painter.setPen(Qt.black)
            font = QFont()
            font.setBold(isActive)
            painter.setFont(font)
            painter.drawText(rect, Qt.AlignCenter, self.tabText(idx))

        painter.end()


class CustomTabWidget(QTabWidget):
    def __init__(self, **kwargs):
        super().__init__()
        self.setTabBar(CustomTabBar(**kwargs))
        self.setDocumentMode(True)
        self.setElideMode(Qt.ElideRight)

    def addPage(self, widget: QWidget, title: str):
        self.addTab(widget, title)