from persist.persister import Persister


PERS_KEY = "saveData"
INDEX_KEY = "index"
PAGE_KEY = "page"
WIDTH_KEY = "width"
HEIGHT_KEY = "height"
INTERVAL_KEY = "changeIntervalSecs"
NUMOFSCREENS_KEY = "numOfScreens"

class SaveData:
    def __init__(self) -> None:
        self.dataDict = {}
        self.dataDict[PAGE_KEY] = -1
        self.dataDict[INDEX_KEY] = -1
        self.dataDict[WIDTH_KEY] = -1
        self.dataDict[HEIGHT_KEY] = -1
        self.dataDict[INTERVAL_KEY] = -1
        self.dataDict[NUMOFSCREENS_KEY] = -1

    def getPage(self):
        return self.__getData(PAGE_KEY)
    
    def setPage(self, newVal):
        self.__setData(PAGE_KEY, newVal)

    def getIndex(self):
        return self.__getData(INDEX_KEY)
    
    def setIndex(self, newVal):
        self.__setData(INDEX_KEY, newVal)

    def getWidth(self):
        return self.__getData(WIDTH_KEY)
    
    def setWidth(self, newVal):
        self.__setData(WIDTH_KEY, newVal)
    
    def getHeight(self):
        return self.__getData(HEIGHT_KEY)
    
    def setHeight(self, newVal):
        self.__setData(HEIGHT_KEY, newVal)

    def getInterval(self):
        return self.__getData(INTERVAL_KEY)
    
    def setInterval(self, newVal):
        self.__setData(INTERVAL_KEY, newVal)
    
    def getNumOfScreens(self):
        return self.__getData(NUMOFSCREENS_KEY)
    
    def setNumOfScreens(self, newVal):
        self.__setData(NUMOFSCREENS_KEY, newVal)

    @staticmethod
    def load(persister:Persister) -> 'SaveData':
        dataDict = persister.getData(PERS_KEY)
        if dataDict is None:
            return None
        saveData = SaveData()
        saveData.dataDict = dataDict
        return saveData
    
    def addToPersister(self, persister:Persister):
        persister.setData(PERS_KEY, self.dataDict)

    def __setData(self, key, newVal):
        self.dataDict[key] = newVal

    def __getData(self, key):
        if not key in self.dataDict:
            return None
        return self.dataDict[key]