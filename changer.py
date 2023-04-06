from pathlib import Path
from imageTank import ImageTank
from imageMerger import mergeImages
from wpChanger import setImageAsWallpaper
from screenSize import ScreenSize

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
        if index >= len(self.currentImages) or index < 0:
            print("Index out of range")
            return
        newImage = self.imageTank.getImages(1)[0]
        if currentToBlackList:
            self.imageTank.addToBlackList(self.currentImages[index])
        self.currentImages[index] = newImage
        self.__mergeAndSetGivenImages()

    def __mergeAndSetGivenImages(self):
        mergedImage = mergeImages(self.wpPath, self.currentImages, self.screenSize)
        setImageAsWallpaper(mergedImage)
    
    # def __mergeAndSetRandomImages(self, numOfScreens):
    #     mergedImage = mergeRandomImagesInFolder(self.wpFolder, self.loader.baseFolder, numOfScreens)
    #     setImageAsWallpaper(mergedImage)