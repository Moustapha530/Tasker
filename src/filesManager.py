"""
    Module for managing tsk and json files, for saving and editing tasklists.
"""
from json import load

def loadStyleSheet(name : str) -> str:
    with open(f"style\\{name}.qss") as style:
        return style.read()

def loadJsonData(jsonPath : str) -> dict:
        with open(jsonPath, "r") as file:
            return load(file)