from pathlib import Path
import json
from .filePers import readStr, saveStr


class Persister:
    def __init__(self, dataFilePath:Path) -> None:
        self.dataFilePath = dataFilePath
        self.data = {}
        self.load()

    def load(self):
        if not self.dataFilePath.exists():
            return
        jsonStr = readStr(self.dataFilePath.absolute())
        self.data = json.loads(jsonStr)

    def save(self):
        jsonStr = json.dumps(self.data)
        saveStr(self.dataFilePath.absolute(), jsonStr)

    def getData(self,key):
        if not key in self.data:
            return None
        return self.data[key]
    
    def setData(self, key, value):
        self.data[key] = value