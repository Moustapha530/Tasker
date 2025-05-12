"""
    Module for managing tsk and json files, for saving and editing tasklists.
"""
from pathlib import Path
from json import load
from os import remove, rename

def loadJsonData(jsonPath : str) -> dict:
        with open(jsonPath, "r") as file:
            return load(file)

def listTaskListName() -> list[str]:
    taskListsFolder = Path("data\\taskLists")
    return [f.stem for f in taskListsFolder.iterdir() if f.is_file() and f.name.endswith(".json")]

def removeTaskList(name : str) -> None:
    try:
        remove(f"data\\taskLists\\{name}.json")
    except:
        pass

def renameTaskList(oldName : str, newName : str) -> None:
    try:
        rename(f"data\\taskLists\\{oldName}.json", f"data\\taskLists\\{newName}.json")
    except:
        pass