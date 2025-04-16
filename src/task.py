"""
    Task module that contains task class implementation.
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QFrame, 
    QHBoxLayout,
    QLabel,
    QCheckBox, 
    QPushButton,
    QVBoxLayout,
    QScrollArea,
    QWidget,
)
from themes import applyTaskTheme


class SubTask(QFrame):
    def __init__(self, name: str, parentTask):
        super().__init__()
        self.setObjectName("SubTask")
        self.setStyleSheet(applyTaskTheme())
        self.name = name
        self.parentTask = parentTask

        layout = QHBoxLayout(self)
        self.checkbox = QCheckBox()
        self.label = QLabel(name)
        self.deleteBtn = QPushButton("")
        self.deleteBtn.setIcon(QIcon("ressources\\icons\\delete.png"))

        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.deleteBtn)

        self.deleteBtn.clicked.connect(self.deleteSelf)

    def deleteSelf(self):
        self.setParent(None)
        self.deleteLater()
        self.parentTask.removeSubtask(self)

    def toDict(self):
        return {"name": self.name, "done": self.checkbox.isChecked()}



class Task(QFrame):
    def __init__(self, name: str, parentList):
        super().__init__()
        self.name = name
        self.parentList = parentList
        self.subtasks : list[SubTask] = []
        self.setObjectName("Task")
        self.setStyleSheet(applyTaskTheme())
        main_layout = QVBoxLayout(self)

        # Header: checkbox + name + delete + add sub-task
        header = QHBoxLayout()
        header.setSpacing(0)
        self.checkbox = QCheckBox()
        self.label = QLabel(name)

        self.addBtn = QPushButton("")
        self.addBtn.setIcon(QIcon("ressources\\icons\\new.png"))
        self.addBtn.setToolTip("Add sub-task")

        self.deleteBtn = QPushButton("")
        self.deleteBtn.setIcon(QIcon("ressources\\icons\\delete.png"))
        self.deleteBtn.setToolTip("Delete")
        self.deleteBtn.setObjectName("DeleteBtn")

        header.addWidget(self.checkbox)
        header.addWidget(self.label)
        header.addStretch()
        header.addWidget(self.addBtn)
        header.addWidget(self.deleteBtn)
        main_layout.addLayout(header)


        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        subtask_container = QWidget()
        self.subtask_layout = QVBoxLayout(subtask_container)
        self.subtask_layout.setContentsMargins(8, 8, 8, 8)
        scroll.setWidget(subtask_container)

        main_layout.addWidget(scroll)

        self.addBtn.clicked.connect(self.addSubtask)
        self.deleteBtn.clicked.connect(self.deleteSelf)
        self.checkbox.stateChanged.connect(self.toggleSubtasks)

    def addSubtask(self):
        sub = SubTask("Subtask", self)
        self.subtask_layout.addWidget(sub)
        self.subtasks.append(sub)
        sub.checkbox.stateChanged.connect(self.syncWithSubtasks)
        self.syncWithSubtasks()

    def removeSubtask(self, sub):
        if sub in self.subtasks:
            self.subtasks.remove(sub)

    def deleteSelf(self):
        self.setParent(None)
        self.deleteLater()
        self.parentList.removeTask(self)

    def syncWithSubtasks(self):
        if not self.subtasks:
            return

        # If all subtasks are checked, check the task
        if all(sub.checkbox.isChecked() for sub in self.subtasks):
            self.checkbox.blockSignals(True)
            self.checkbox.setChecked(True)
            self.checkbox.blockSignals(False)
        else:
            self.checkbox.blockSignals(True)
            self.checkbox.setChecked(False)
            self.checkbox.blockSignals(False)

        self.parentList.updateProgress()


    def toDict(self):
        return {
            "name": self.name,
            "done": self.checkbox.isChecked(),
            "subtasks": [s.toDict() for s in self.subtasks]
        }

    def toggleSubtasks(self, state):
        for sub in self.subtasks:
            sub.checkbox.blockSignals(True)
            sub.checkbox.setChecked(bool(state))
            sub.checkbox.blockSignals(False)
        self.parentList.updateProgress()
