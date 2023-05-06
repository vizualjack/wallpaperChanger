from change.wpcImage import WpcImage

class Screen:
    def __init__(self, width, height, wpcImage:WpcImage = None) -> None:
        self.width = width
        self.height = height
        self.__wpcImage = wpcImage
        self.__hasChanged = False

    def setWpcImage(self, newWpcImage:WpcImage):
        self.__wpcImage = newWpcImage
        self.__hasChanged = True

    def getWpcImage(self) -> WpcImage:
        return self.__wpcImage
    
    def hasWpcChanged(self) -> bool:
        return self.__hasChanged
    
    def resetWpcChanged(self):
        self.__hasChanged = False