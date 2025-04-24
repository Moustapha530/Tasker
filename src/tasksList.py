"""
    The task list module used to manage task group.
"""
import json
import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QScrollArea,
    QPushButton, 
    QProgressBar,
    QInputDialog, 
    QMessageBox,
    QMenu,
)
from filesManager import listTaskListFiles
from task import SubTask, Task
from themes import applyTaskTheme

class TaskList(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.tasks : list[Task] = []
        self.setObjectName("TaskList")
        self.setStyleSheet(applyTaskTheme())
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header with name and progress bar 
        top = QHBoxLayout()
        top.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.nameLabel = QLabel(name)
        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.addTaskBtn = QPushButton("")
        self.addTaskBtn.setIcon(QIcon("ressources\\icons\\new.png"))
        self.addTaskBtn.setToolTip("Add task")
        self.saveBtn = QPushButton("")
        self.saveBtn.setIcon(QIcon("ressources\\icons\\save.png"))
        self.saveBtn.setToolTip("Save")


        top.addWidget(self.nameLabel)
        top.addWidget(self.progress)
        top.addWidget(self.addTaskBtn)
        top.addWidget(self.saveBtn)

        layout.addLayout(top)

        # Tasks area
        self.taskLayout = QVBoxLayout()
        self.taskLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.taskLayout)

        self.addTaskBtn.clicked.connect(self.addTask)
        self.saveBtn.clicked.connect(self.saveToFile)

    def addTask(self):
        task = Task("New Task", self)
        self.taskLayout.addWidget(task)
        self.tasks.append(task)
        self.updateProgress()

    def loadFromFile(self, name: str):
        """
        Load a task list from a JSON file and reconstruct the task list.

        Args:
            name (str): Path to the JSON file.
        """
        if not os.path.exists(f"data\\taskList\\{name}"):
            print(f"File \"data\\taskList\\{name}\" does not exist.")
            return

        with open(f"data\\taskLists\\{name}", "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON: {e}")
                return

        # Clear current tasks
        for task in self.tasks:
            task.setParent(None)
            task.deleteLater()
        self.tasks.clear()

        # Restore title
        self.name = data.get("name", "Unnamed List")
        self.nameLabel.setText(self.name)

        for task_data in data.get("tasks", []):
            task_name = task_data.get("name", "Unnamed Task")
            task = Task(task_name, self)
            task.checkbox.setChecked(task_data.get("done", False))

            # Add subtasks if any
            for sub_data in task_data.get("subtasks", []):
                sub_name = sub_data.get("name", "Unnamed Subtask")
                sub = SubTask(sub_name, task)
                sub.checkbox.setChecked(sub_data.get("done", False))
                task.subtask_layout.addWidget(sub)
                task.subtasks.append(sub)

            self.taskLayout.addWidget(task)
            self.tasks.append(task)

        self.updateProgress()


    def removeTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)
        self.updateProgress()

    def updateProgress(self):
        if not self.tasks:
            self.progress.setValue(0)
            return
        done_count = sum(1 for t in self.tasks if t.checkbox.isChecked())
        percent = int((done_count / len(self.tasks)) * 100)
        self.progress.setValue(percent)
        self.saveToFile()

    def saveToFile(self):
        data = {
            "name": self.name,
            "tasks": [t.toDict() for t in self.tasks]
        }
        with open(f"data\\taskLists\\{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)

class TaskListPreview(QWidget):
    openRequested = pyqtSignal(str)
    renameRequested = pyqtSignal(str)
    deleteRequested = pyqtSignal(str)

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.setObjectName("TaskListPreview")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        icon = QLabel()
        icon.setPixmap(QIcon("ressources\\icons\\checkList.png").pixmap(24, 24))

        self.label = QLabel(name)
        self.optionsBtn = QPushButton("⋯")
        self.optionsBtn.setFixedWidth(30)
        self.optionsBtn.setVisible(False)

        layout.addWidget(icon)
        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.optionsBtn)

        self.optionsBtn.clicked.connect(self.showOptions)

    def showOptions(self):
        menu = QMenu(self)
        rename_action = menu.addAction("Rename")
        delete_action = menu.addAction("Delete")
        action = menu.exec_(self.optionsBtn.mapToGlobal(self.optionsBtn.rect().bottomRight()))
        if action == rename_action:
            self.renameRequested.emit(self.name)
        elif action == delete_action:
            self.deleteRequested.emit(self.name)

    def enterEvent(self, event):
        self.optionsBtn.setVisible(True)

    def leaveEvent(self, event):
        self.optionsBtn.setVisible(False)

    def mouseDoubleClickEvent(self, event):
        self.openRequested.emit(self.name)

class TaskListExplorer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TaskListExplorer")

        layout = QVBoxLayout(self)
        title = QLabel("Task Lists")
        title.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(title)

        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.container = QWidget()
        self.listLayout = QVBoxLayout(self.container)
        self.scrollArea.setWidget(self.container)

        layout.addWidget(self.scrollArea)
        self.showTaskLists()

    def addTaskListPreview(self, name: str):
        preview = TaskListPreview(name)
        preview.openRequested.connect(self.openList)
        preview.renameRequested.connect(self.renameList)
        preview.deleteRequested.connect(self.removeList)

        self.listLayout.addWidget(preview)

    def openList(self, name: str):
        try:
            taskList = TaskList("Untitled task list")
            taskList.loadFromFile(name)
        except:
            pass

    def renameList(self, old_name: str):
        new_name, ok = QInputDialog.getText(self, "Rename Task List", "New name:", text=old_name)
        if ok and new_name.strip():
            # Remplace le widget
            for i in range(self.listLayout.count()):
                item = self.listLayout.itemAt(i).widget()
                if item.name == old_name:
                    item.name = new_name
                    item.label.setText(new_name)
                    break

    def removeList(self, name: str):
        confirm = QMessageBox.question(self, "Delete", f"Delete task list '{name}'?")
        if confirm == QMessageBox.Yes:
            for i in range(self.listLayout.count()):
                item = self.listLayout.itemAt(i).widget()
                if item.name == name:
                    item.setParent(None)
                    item.deleteLater()
                    break

    def showTaskLists(self) -> None:
        for file in listTaskListFiles():
            taskList = TaskList("Untitled task list")
            taskList.loadFromFile(file)
            self.addTaskListPreview(taskList)