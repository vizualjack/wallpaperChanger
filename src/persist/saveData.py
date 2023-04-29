from persist.persister import Persister

_SAVE_KEY = "saveData"
_INTERVAL_KEY = "changeIntervalSecs"
_NUMOFSCREENS_KEY = "numOfScreens"
_USEONLYSAVEDIMAGES_KEY = "useOnlySavedImages"

class SaveData:
    def __init__(self) -> None:
        self.dataDict = {}
        self.dataDict[_INTERVAL_KEY] = -1
        self.dataDict[_NUMOFSCREENS_KEY] = -1
        self.dataDict[_USEONLYSAVEDIMAGES_KEY] = False

    def getInterval(self):
        return self.__getData(_INTERVAL_KEY)
    
    def setInterval(self, newVal):
        self.__setData(_INTERVAL_KEY, newVal)
    
    def getNumOfScreens(self):
        return self.__getData(_NUMOFSCREENS_KEY)
    
    def setNumOfScreens(self, newVal):
        self.__setData(_NUMOFSCREENS_KEY, newVal)

    def getUseOnlySavedImages(self):
        return self.__getData(_USEONLYSAVEDIMAGES_KEY)
    
    def setUseOnlySavedImages(self, newVal):
        self.__setData(_USEONLYSAVEDIMAGES_KEY, newVal)

    @staticmethod
    def load(persister:Persister) -> 'SaveData':
        dataDict = persister.getData(_SAVE_KEY)
        if dataDict is None:
            return None
        saveData = SaveData()
        saveData.dataDict = dataDict
        return saveData
    
    def addToPersister(self, persister:Persister):
        persister.setData(_SAVE_KEY, self.dataDict)

    def __setData(self, key, newVal):
        self.dataDict[key] = newVal

    def __getData(self, key):
        if not key in self.dataDict:
            return None
        return self.dataDict[key]