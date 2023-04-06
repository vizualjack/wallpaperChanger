from settings import Settings
from pathlib import Path
from screenSize import ScreenSize

### KEYS
WIDTH = "winWidth"
HEIGHT = "winHeight"
NUM_OF_SCREENS = "numOfScreens"
CHANGE_INTERVAL = "changeIntervalSecs"

class UserSettings(Settings):
    def __init__(self, baseFolder: Path) -> None:
        super().__init__(baseFolder)

    def getMonitorSize(self):
        return ScreenSize(self.getMonitorWidth(), self.getMonitorHeight())

    def getMonitorWidth(self):
        return self.getData(WIDTH)

    def setMonitorWidth(self, newWidth:int):
        self.setData(WIDTH, newWidth)

    def getMonitorHeight(self):
        return self.getData(HEIGHT)

    def setMonitorHeight(self, newHeight:int):
        self.setData(HEIGHT, newHeight)

    def getNumOfScreens(self):
        return self.getData(NUM_OF_SCREENS)

    def setNumOfScreens(self, newNumOfScreens:int):
        self.setData(NUM_OF_SCREENS, newNumOfScreens)

    def getChangeInterval(self):
        return self.getData(CHANGE_INTERVAL)

    def setChangeInterval(self, newChangeInterval:int):
        self.setData(CHANGE_INTERVAL, newChangeInterval)