from pathlib import Path
import json
from .filePers import readStr, saveStr
from change.changer import Changer
from appSettings import *
from loadNew.imageDler import ImageDler


class Persister:
    __KEY_CHANGER = "changer"
    __KEY_IMGDLER = "imgDler"

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

    def load(self, persistable:'Persistable'):
        data = self.__getData(self.__getClassName(persistable))
        if data:
            persistable.loadFromJson(data)

    def addForSave(self, persistable:'Persistable'):
        self.__setData(self.__getClassName(persistable), persistable.getSaveDataJson())

    def __getClassName(self, obj:object):
        return obj.__class__.__name__

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

## Just a class for typing
class Persistable:
    def getSaveDataJson(self):
        pass

    def loadFromJson(self, data):
        pass