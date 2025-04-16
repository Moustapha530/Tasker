"""
    Task module that contains task class implementation.
"""
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, 
    QHBoxLayout,
    QLabel,
    QCheckBox, 
    QPushButton,
    QVBoxLayout,
)


class SubTask(QWidget):
    def __init__(self, name: str, parentTask):
        super().__init__()
        self.name = name
        self.parentTask = parentTask

        layout = QHBoxLayout(self)
        self.checkbox = QCheckBox()
        self.label = QLabel(name)
        self.deleteBtn = QPushButton("")
        self.deleteBtn.setIcon(QIcon("ressources\\icons\\new.png"))

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



class Task(QWidget):
    def __init__(self, name: str, parentList):
        super().__init__()
        self.name = name
        self.parentList = parentList
        self.subtasks : list[SubTask] = []

        main_layout = QVBoxLayout(self)

        # Header: checkbox + name + delete + add sub-task
        header = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.label = QLabel(name)

        self.addBtn = QPushButton("")
        self.addBtn.setIcon(QIcon("ressources\\icons\\new.png"))

        self.deleteBtn = QPushButton("")
        self.addBtn.setIcon(QIcon("ressources\\icons\\delete.png"))

        header.addWidget(self.checkbox)
        header.addWidget(self.label)
        header.addStretch()
        header.addWidget(self.addBtn)
        header.addWidget(self.deleteBtn)
        main_layout.addLayout(header)

        # Subtasks area
        self.subtask_layout = QVBoxLayout()
        main_layout.addLayout(self.subtask_layout)

        self.addBtn.clicked.connect(self.addSubtask)
        self.deleteBtn.clicked.connect(self.deleteSelf)
        self.checkbox.stateChanged.connect(self.parentList.updateProgress)

    def addSubtask(self):
        sub = SubTask("Subtask", self)
        self.subtask_layout.addWidget(sub)
        self.subtasks.append(sub)

    def removeSubtask(self, sub):
        if sub in self.subtasks:
            self.subtasks.remove(sub)

    def deleteSelf(self):
        self.setParent(None)
        self.deleteLater()
        self.parentList.removeTask(self)

    def toDict(self):
        return {
            "name": self.name,
            "done": self.checkbox.isChecked(),
            "subtasks": [s.toDict() for s in self.subtasks]
        }