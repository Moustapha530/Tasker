"""
    The task list module used to manage task group.
"""
import json
import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout, 
    QGridLayout,
    QLabel,
    QScrollArea,
    QPushButton,
    QFrame, 
    QProgressBar,
    QInputDialog, 
    QMessageBox,
    QMenu,
    QVBoxLayout, 
    QWidget, 
)
from qtawesome import icon
from .core import listTaskListName, removeTaskList, renameTaskList
from .task import SubTask, Task
from customWidgets import SectionTitle

class TaskList(QFrame):

    def __init__(self, name: str = "Untitled"):
        super().__init__()
        self.name = name
        self.tasks : list[Task] = []

        self.setObjectName("TaskList")
        self.setStyleSheet(self.applyStyleSheet())

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header with name and progress bar 
        header = QHBoxLayout()
        header.setAlignment(Qt.AlignmentFlag.AlignTop)

        toolsLayout = QHBoxLayout()
        toolsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.nameLabel = SectionTitle(name)
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        self.addTaskBtn = QPushButton("")
        self.addTaskBtn.setIcon(icon("fa5s.plus", color="white"))
        self.addTaskBtn.setToolTip("Add task")
        self.addTaskBtn.setFixedSize(32, 32)

        header.addWidget(self.nameLabel)
        toolsLayout.addWidget(self.progress)
        toolsLayout.addWidget(self.addTaskBtn)

        layout.addLayout(header)
        layout.addLayout(toolsLayout)

        # Tasks area
        self.taskLayout = QVBoxLayout()
        self.taskLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addLayout(self.taskLayout)

        self.addTaskBtn.clicked.connect(self.addTask)

    def addTask(self):
        task = Task("New Task", self)
        self.taskLayout.addWidget(task)
        self.tasks.append(task)
        self.updateProgress()

    def applyStyleSheet(self) -> str:
        return """
        #TaskList QLabel {
            color: white;
        }

        #TaskList QPushButton:hover {
            background-color: #4c566a;
            border-radius: 10px;
            padding: 5px;
        }

        #TaskList QProgressBar {
            background-color: #2e3b5b;
            border-radius: 10px;
        }

        #TaskList QProgressBar::chunk {
            background-color: green;
            border-radius: 10px;
        }
        """

    def loadFromFile(self, name: str):
        """
        Load a task list from a JSON file and reconstruct the task list.

        Args:
            name (str): Path to the JSON file.
        """
        if not os.path.exists(f"data\\taskLists\\{name}.json"):
            print(f"File \"data\\taskLists\\{name}\" does not exist.")
            return

        with open(f"data\\taskLists\\{name}.json", "r") as f:
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
        self.nameLabel.label.setText(self.name)

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
        self.setStyleSheet(self.applyStyleSheet())

        mainLayout = QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 5, 10, 5)

        self.icon = QLabel()
        self.icon.setPixmap(icon("fa5s.tasks", color="white").pixmap(32, 32))

        self.label = QLabel(name)
        self.optionsBtn = QPushButton("")
        self.optionsBtn.setIcon(icon("fa5s.ellipsis-v", color="white"))
        self.optionsBtn.setFixedSize(32, 32)
        self.optionsBtn.setVisible(False)

        mainLayout.addWidget(self.icon, alignment=Qt.AlignmentFlag.AlignHCenter)
        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        bottomLayout.addWidget(self.optionsBtn, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        
        mainLayout.addLayout(bottomLayout)

        self.optionsBtn.clicked.connect(self.showOptions)
        self.setFixedSize(125, 95)

    def applyStyleSheet(self) -> str:
        return """
        #TaskListPreview QLabel {
            color: white;
        }

        #TaskListPreview QPushButton:hover {
            background-color: #4c566a;
            border-radius: 10px;
            padding: 5px;
        }
        """

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
        self.tasker = parent 

        self.setObjectName("TaskListExplorer")
        self.setStyleSheet(self.applyStyleSheet())

        self.maxCol = 10
        self.currentIndex = 0
        layout = QVBoxLayout(self)
        title = SectionTitle("Task Lists")
        layout.addWidget(title)
        layout.setSpacing(0)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)

        self.container = QWidget()
        self.listLayout = QGridLayout(self.container)
        self.scrollArea.setWidget(self.container)

        layout.addWidget(self.scrollArea)
        self.showTaskLists()

    def addTaskListPreview(self, name: str):
        preview = TaskListPreview(name)
        preview.openRequested.connect(self.openList)
        preview.renameRequested.connect(self.renameList)
        preview.deleteRequested.connect(self.removeList)
        row = self.currentIndex // self.maxCol
        col = self.currentIndex % self.maxCol
        self.listLayout.addWidget(preview, row, col)
        self.currentIndex += 1

    def applyStyleSheet(self) -> str:
        return """
        #TaskListExplorer QLabel {
            color: white;
        }
        """

    def openList(self, name: str):
        if self.tasker is None:
            return
        taskLists = TaskList()
        taskLists.loadFromFile(name)
        self.tasker.addTaskList(taskLists, name)

    def renameList(self, old_name: str):
        new_name, ok = QInputDialog.getText(self, "Rename Task List", "New name:", text=old_name)
        if ok and new_name.strip():
            # Remplace le widget
            for i in range(self.listLayout.count()):
                item = self.listLayout.itemAt(i).widget()
                if item.name == old_name:
                    item.name = new_name
                    item.label.setText(new_name)
                    renameTaskList(old_name, new_name)
                    break

    def removeList(self, name: str):
        confirm = QMessageBox.question(self, "Delete", f"Delete task list '{name}'?")
        if confirm == QMessageBox.Yes:
            for i in range(self.listLayout.count()):
                item = self.listLayout.itemAt(i).widget()
                if item.name == name:
                    item.setParent(None)
                    item.deleteLater()
                    removeTaskList(name)
                    break

    def showTaskLists(self) -> None:
        for file in listTaskListName():
            self.addTaskListPreview(file)