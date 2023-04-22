from pathlib import Path


CUR_WALLPAPER_NAME = "wp"

class Changer:
    def __init__(self, baseFolder:Path, screenSize:ScreenSize) -> None:
        self.screenSize = screenSize
        self.imageTank = ImageTank(baseFolder, screenSize)
        self.wpPath = baseFolder.joinpath(CUR_WALLPAPER_NAME)
        self.currentImages = []

    def fullImageChange(self, numOfScreens, currentToBlackList=False):
        if currentToBlackList:
            for currentImage in self.currentImages:
                self.imageTank.addToBlackList(currentImage)            
        self.currentImages = self.imageTank.getImages(numOfScreens)
        self.__mergeAndSetGivenImages()

    def changeOne(self, index, currentToBlackList=False):
        self.__changeImageOnIndex(index, currentToBlackList)
        self.__mergeAndSetGivenImages()
    
    def changeMultiple(self, indexes, currentToBlackList=False):
        for index in indexes:    
            self.__changeImageOnIndex(index, currentToBlackList)
        self.__mergeAndSetGivenImages()

    def __changeImageOnIndex(self, index, currentToBlackList=False):
        if index >= len(self.currentImages) or index < 0:
            print("Index out of range")
            return
        newImage = self.imageTank.getImages(1)[0]
        if currentToBlackList:
            self.imageTank.addToBlackList(self.currentImages[index])
        self.currentImages[index] = newImage

    def __mergeAndSetGivenImages(self):
        print("=== Merge images ===")
        print(self.currentImages)
        print("====================")
        mergedImage = mergeImages(self.wpPath, self.currentImages, self.screenSize)
        setImageAsWallpaper(mergedImage)