"""
    Module for managing tsk and json files, for saving and editing tasklists.
"""
from pathlib import Path
from json import load

def loadJsonData(jsonPath : str) -> dict:
        with open(jsonPath, "r") as file:
            return load(file)

def listTaskListName() -> list[str]:
    taskListsFolder = Path("data\\taskLists")
    return [f.stem for f in taskListsFolder.iterdir() if f.is_file() and f.name.endswith(".json")]
