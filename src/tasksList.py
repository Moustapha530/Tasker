"""
    The task list module used to manage task group.
"""
import json
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QPushButton, 
    QProgressBar
)
from task import SubTask, Task


class TaskList(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.tasks : list[Task] = []

        layout = QVBoxLayout(self)

        # Header with name and progress bar 
        top = QHBoxLayout()
        self.nameLabel = QLabel(name)
        self.progress = QProgressBar()
        self.progress.setValue(0)

        self.addTaskBtn = QPushButton("")
        self.addTaskBtn.setIcon(QIcon("ressources\\icons\\new.png"))
        self.saveBtn = QPushButton("")
        self.saveBtn.setIcon(QIcon("ressources\\icons\\new.png"))

        top.addWidget(self.nameLabel)
        top.addStretch()
        top.addWidget(self.progress)
        top.addWidget(self.addTaskBtn)
        top.addWidget(self.saveBtn)

        layout.addLayout(top)

        # Tasks area
        self.taskLayout = QVBoxLayout()
        layout.addLayout(self.taskLayout)

        self.addTaskBtn.clicked.connect(self.addTask)
        self.saveBtn.clicked.connect(self.saveToFile)

    def addTask(self):
        task = Task("New Task", self)
        self.taskLayout.addWidget(task)
        self.tasks.append(task)
        self.updateProgress()

    

# Inside TaskListWidget class
    def load_from_file(self, file_path: str):
        """
        Load a task list from a JSON file and reconstruct the task list.

        Args:
            file_path (str): Path to the JSON file.
        """
        if not os.path.exists(file_path):
            print(f"File '{file_path}' does not exist.")
            return

        with open(file_path, "r") as f:
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

    def saveToFile(self):
        data = {
            "name": self.name,
            "tasks": [t.toDict() for t in self.tasks]
        }
        with open(f"{self.name}.json", "w") as f:
            json.dump(data, f, indent=4)