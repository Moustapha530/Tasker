from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QColor

class ShadowFrame(QFrame):
    def __init__(self,
                 shadowColor : QColor = QColor(0, 0, 0, 100),  # Default black semi-transparent shadow
                 blurRadius : int = 20,
                 offset : int = 10,
                 sides : str | list[str] = 'bottom',  # Can be 'all' or a list like ['left', 'bottom']
                 parent : QWidget | None = None) -> None:
        super().__init__(parent)

        # Create the drop shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blurRadius)
        shadow.setColor(shadowColor)

        # Support both string and list input for sides
        if isinstance(sides, str):
            if sides.lower() == 'all':
                offset_x, offset_y = 0, 0
            else:
                sides = [sides.lower()]
        else:
            sides = [s.lower() for s in sides]

        # Compute combined offset for multiple sides
        offset_x, offset_y = 0, 0
        if 'top' in sides:
            offset_y -= offset
        if 'bottom' in sides:
            offset_y += offset
        if 'left' in sides:
            offset_x -= offset
        if 'right' in sides:
            offset_x += offset

        # Apply the computed offset
        shadow.setOffset(offset_x, offset_y)

        # Assign the effect to this widget
        self.setGraphicsEffect(shadow)
