from pathlib import Path
from imageLoader import ImageLoader
from imageMerger import mergeImages, mergeRandomImagesInFolder, pickImages
from wpChanger import setImageAsWallpaper
from screenSize import ScreenSize

class Changer:
    def __init__(self, imageFolder:Path, wpPath:Path, screenSize:ScreenSize) -> None:
        self.loader = ImageLoader(imageFolder, screenSize)
        self.wpPath = wpPath
        self.currentImages = []

    def fullImageChange(self, numOfScreens, currentToBlackList=False):
        if currentToBlackList:
            for currentImage in self.currentImages:
                self.loader.addToBlackList(currentImage)            
        self.currentImages = self.loader.downloadImages(numOfScreens)
        neededRest = len(self.currentImages) - len(self.currentImages)
        if neededRest > 0:
            self.currentImages.extend(pickImages(self.loader.baseFolder, neededRest))
        self.__mergeAndSetGivenImages()

    def changeOne(self, index, currentToBlackList=False):
        if index >= len(self.currentImages) or index < 0:
            print("Index out of range")
            return
        newImage = self.loader.downloadImage()
        if currentToBlackList:
            self.loader.addToBlackList(self.currentImages[index])
        self.currentImages[index] = newImage
        self.__mergeAndSetGivenImages()

    # def __mergeAndSetRandomImages(self, numOfScreens):
    #     mergedImage = mergeRandomImagesInFolder(self.wpFolder, self.loader.baseFolder, numOfScreens)
    #     setImageAsWallpaper(mergedImage)

    def __mergeAndSetGivenImages(self):
        mergedImage = mergeImages(self.wpPath, self.currentImages)
        setImageAsWallpaper(mergedImage)