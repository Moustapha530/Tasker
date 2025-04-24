"""
    Module for managing tsk and json files, for saving and editing tasklists.
"""
import os
from json import load

def loadJsonData(jsonPath : str) -> dict:
        with open(jsonPath, "r") as file:
            return load(file)

def listTaskListFiles() -> list[str]:
    taskListFiles : list[str] = list()

    for taskListFile in os.listdir("data\\taskLists"):
        if taskListFile.endswith('.json'):
            taskListFiles.append(taskListFile)

    return taskListFiles

