from pathlib import Path
import json


class Persister:
    def __init__(self, dataFilePath:Path) -> None:
        self.dataFilePath = dataFilePath
        self.data = {}
        self.load()

    def load(self):
        if not self.dataFilePath.exists():
            return
        f = open(self.dataFilePath.absolute().__str__())
        self.data = json.loads(f.read())
        f.close()

    def save(self):
        f = open(self.dataFilePath.absolute().__str__(), "w")
        f.write(json.dumps(self.data))
        f.flush()
        f.close()

    def getData(self,key):
        if not key in self.data:
            return None
        return self.data[key]
    
    def setData(self, key, value):
        self.data[key] = value