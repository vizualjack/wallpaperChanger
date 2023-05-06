from pathlib import Path
import json
from .filePers import readStr, saveStr
from change.changer import Changer
from appSettings import *


class Persister:
    __KEY_CHANGER = "changer"

    def __init__(self) -> None:
        self.__filePath = PERSISTER_SAVE_PATH
        self.__data = {}
        self.__load()

    def save(self):
        jsonStr = json.dumps(self.__data)
        saveStr(self.__filePath.absolute(), jsonStr)

    def loadChanger(self, changer:Changer):
        data = self.__getData(self.__KEY_CHANGER)
        if data:
            changer.loadFromJson(self.__getData(self.__KEY_CHANGER))

    def addChangerForSave(self, changer:Changer):
        self.__setData(self.__KEY_CHANGER, changer.getSaveDataJson())

    def __getData(self,key):
        if not key in self.__data:
            return None
        return self.__data[key]
    
    def __setData(self, key, value):
        self.__data[key] = value

    def __load(self):
        if not self.__filePath.exists():
            return
        jsonStr = readStr(self.__filePath.absolute())
        self.__data = json.loads(jsonStr)