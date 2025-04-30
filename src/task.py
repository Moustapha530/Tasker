"""
    Task module: contains Task and SubTask classes used in Tasker app.
"""

from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QCheckBox, QPushButton, QVBoxLayout,
    QLineEdit, QScrollArea, QStackedLayout, QWidget, QGraphicsOpacityEffect
)
from themes import applyTaskTheme


class Task(QFrame):
    """
    Represents a task item with optional subtasks.
    Supports renaming, subtask management, and visual status sync.
    """

    def __init__(self, name: str, parentList) -> None:
        super().__init__()
        self.name = name
        self.parentList = parentList
        self.subtasks: list[SubTask] = []
        self.isExpanded = False

        self.setObjectName("Task")
        self.setStyleSheet(applyTaskTheme())

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 8, 10, 8)

        # --- Header section ---
        header = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.label = QLabel(name)
        self.labelEdit = QLineEdit(name)
        self.labelEdit.setStyleSheet("background-color: transparent")
        self.labelEdit.hide()

        self.renameBtn = QPushButton()
        self.renameBtn.setIcon(QIcon("ressources/icons/edit.png"))
        self.renameBtn.setToolTip("Rename task")

        self.addBtn = QPushButton()
        self.addBtn.setIcon(QIcon("ressources/icons/new.png"))
        self.addBtn.setToolTip("Add sub-task")

        self.deleteBtn = QPushButton()
        self.deleteBtn.setObjectName("DeleteBtn")
        self.deleteBtn.setIcon(QIcon("ressources/icons/delete.png"))
        self.deleteBtn.setToolTip("Delete task")

        self.dropdownBtn = QPushButton()
        self.dropdownBtn.setIcon(QIcon("ressources/icons/down.png"))
        self.dropdownBtn.setToolTip("Show/Hide subtasks")

        self.labelContainer = QWidget()
        labelStack = QStackedLayout(self.labelContainer)
        labelStack.setStackingMode(QStackedLayout.StackAll)
        labelStack.addWidget(self.label)
        labelStack.addWidget(self.labelEdit)

        header.addWidget(self.dropdownBtn)
        header.addWidget(self.checkbox)
        header.addWidget(self.labelContainer)
        header.addStretch()
        header.addWidget(self.renameBtn)
        header.addWidget(self.addBtn)
        header.addWidget(self.deleteBtn)

        mainLayout.addLayout(header)

        # --- Subtask container with scroll ---
        self.scrollBar = QScrollArea()
        self.scrollBar.setWidgetResizable(True)
        self.scrollBar.setMinimumHeight(10)
        self.scrollBar.setMaximumHeight(0)

        self.subtaskContainer = QWidget()
        self.subtaskLayout = QVBoxLayout(self.subtaskContainer)
        self.subtaskLayout.setContentsMargins(54, 4, 8, 4)  # Indentation for sub-tasks
        self.scrollBar.setWidget(self.subtaskContainer)

        mainLayout.addWidget(self.scrollBar)

        # --- Connections ---
        self.addBtn.clicked.connect(self.addSubtask)
        self.deleteBtn.clicked.connect(self.deleteSelf)
        self.renameBtn.clicked.connect(self.showRenameInput)
        self.labelEdit.returnPressed.connect(self.commitRename)
        self.checkbox.stateChanged.connect(self.toggleSubtasks)
        self.dropdownBtn.clicked.connect(self.toggleSubtaskVisibility)

        # Initial state
        self.scrollBar.setVisible(False)
        self.addBtn.setVisible(False)
        self.renameBtn.setVisible(False)
        self.deleteBtn.setVisible(False)

    def addSubtask(self) -> None:
        """
        Add a subtask (as a SubTask).
        """
        sub = SubTask("Subtask", self)
        self.subtaskLayout.addWidget(sub)
        self.syncWithSubtasks()
        if len(self.subtasks) == 0:
            self.toggleSubtaskVisibility()
        self.subtasks.append(sub)

    def animateButtonFade(self, button: QPushButton, fade_in: bool) -> None:
        """Animate the opacity of a button."""
        if not button.graphicsEffect():
            effect = QGraphicsOpacityEffect(button)
            button.setGraphicsEffect(effect)
        else:
            effect = button.graphicsEffect()

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(900)
        anim.setStartValue(effect.opacity())
        anim.setEndValue(1.0 if fade_in else 0.0)
        anim.start()
        button.anim = anim  # Keep reference
        button.setVisible(True if fade_in else False)

    def animateLabel(self) -> None:
        """
        Fade animation when a label is updated.
        """
        effect = QGraphicsOpacityEffect(self.label)
        self.label.setGraphicsEffect(effect)

        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(500)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.start()
        self.label.anim = anim

    def animateSubtasks(self, expand: bool) -> None:
        """
        Animate opening or closing the subtask container.
        """
        anim = QPropertyAnimation(self.scrollBar, b"maximumHeight")
        anim.setDuration(500)
        if expand:
            self.scrollBar.setMaximumHeight(0)
            self.scrollBar.setVisible(True)
            height = self.subtaskContainer.sizeHint().height() + 20
            anim.setStartValue(0)
            anim.setEndValue(height)
            self.dropdownBtn.setIcon(QIcon("ressources/icons/top.png"))
        else:
            height = self.scrollBar.height()
            anim.setStartValue(height)
            anim.setEndValue(0)
            self.dropdownBtn.setIcon(QIcon("ressources/icons/down.png"))

        anim.start()
        self.scrollBar.anim = anim  # keep ref to prevent GC

    def commitRename(self) -> None:
        """
        Commit a renaming change.
        """
        new_name = self.labelEdit.text().strip()
        if new_name:
            self.name = new_name
            self.label.setText(new_name)
            self.labelEdit.hide()
            self.label.show()
            self.animateLabel()

    def deleteSelf(self) -> None:
        """
        Delete this task.
        """
        self.setParent(None)
        self.deleteLater()
        self.parentList.removeTask(self)

    def enterEvent(self, event) -> None:
        """Hover enter: animate fade-in of buttons."""
        super().enterEvent(event)
        for btn in [self.addBtn, self.renameBtn, self.deleteBtn]:
            self.animateButtonFade(btn, fade_in=True)

    def leaveEvent(self, event) -> None:
        """Hover leave: animate fade-out of buttons."""
        super().leaveEvent(event)
        for btn in [self.addBtn, self.renameBtn, self.deleteBtn]:
            self.animateButtonFade(btn, fade_in=False)

    def removeSubtask(self, sub) -> None:
        """
        Remove a specific subtask.
        """
        if sub in self.subtasks:
            self.subtasks.remove(sub)
            self.syncWithSubtasks()
        if len(self.subtasks) == 0:
            self.scrollBar.setVisible(False)

    def showRenameInput(self) -> None:
        """
        Show inline rename field.
        """
        self.labelEdit.setText(self.label.text())
        self.label.hide()
        self.labelEdit.show()
        self.labelEdit.setFocus()

    def syncWithSubtasks(self) -> None:
        """
        Update the main task checkbox according to subtasks.
        """
        if not self.subtasks:
            return
        done = all(sub.checkbox.isChecked() for sub in self.subtasks)
        self.checkbox.blockSignals(True)
        self.checkbox.setChecked(done)
        self.checkbox.blockSignals(False)
        try:
            self.parentList.updateProgress()
        except:
            return
    
    def toDict(self) -> dict:
        """
        Serialize the task to a dictionary.
        """
        return {
            "name": self.name,
            "done": self.checkbox.isChecked(),
            "subtasks": [s.toDict() for s in self.subtasks]
        }

    def toggleSubtaskVisibility(self) -> None:
        """
        Expand/collapse subtasks
        """
        expand = not self.isExpanded
        self.isExpanded = expand
        self.animateSubtasks(expand)

    def toggleSubtasks(self, state) -> None:
        """
        Mark all subtasks done/undone based on main checkbox.
        """
        for sub in self.subtasks:
            sub.checkbox.blockSignals(True)
            sub.checkbox.setChecked(bool(state))
            sub.checkbox.blockSignals(False)
        try:
            self.parentList.updateProgress()
        except:
            return None


class SubTask(Task):
    """
    A lightweight task to be embedded inside another task.
    """

    def __init__(self, name: str, parentTask) -> None:
        super().__init__(name, parentTask)
        self.setObjectName("SubTask")
        self.parentTask = parentTask

        # Hide dropdown and add subtask for subtasks
        self.addBtn.hide()
        self.renameBtn.hide()
        self.dropdownBtn.hide()

        # Hide subtasks container
        self.scrollBar.setVisible(False)

        self.checkbox.stateChanged.connect(self.parentTask.syncWithSubtasks)

        self.deleteBtn.clicked.disconnect()
        self.deleteBtn.clicked.connect(self.deleteSelf)

    def deleteSelf(self) -> None:
        """
        Delete this subtask.
        """
        self.setParent(None)
        self.deleteLater()
        self.parentTask.removeSubtask(self)

    def enterEvent(self, event) -> None:
        """
        When mouse enters, show buttons and auto-expand subtasks.
        """
        for btn in [self.renameBtn, self.deleteBtn]:
            self.animateButtonFade(btn, fade_in=True)

    def leaveEvent(self, event) -> None:
        """
        When mouse leaves, hide buttons.
        """
        for btn in [self.renameBtn, self.deleteBtn]:
            self.animateButtonFade(btn, fade_in=False)

    def toDict(self) -> dict:
       """
       Serialize the task to a dictionary.
       """
       return {
           "name": self.name,
           "done": self.checkbox.isChecked(),
       }