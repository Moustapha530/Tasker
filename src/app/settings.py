"""
    Module for manage settings of the app and load json data.
"""
from json.encoder import JSONEncoder

from app.core import loadJsonData

def getSetting(name : str) -> str | dict | list:
        try:
            return settings[name]
        except KeyError:
            print(f"No setting {name} found")

def changeSettings(settingName : str, value : str | dict | list) -> None:
        settings[settingName] = value
        with open("data\\settings.json", "w") as file:
            jsonSettings = encoder.encode(settings)
            file.write(jsonSettings)


encoder = JSONEncoder(indent=4)
settings : dict = loadJsonData("data\\settings.json")