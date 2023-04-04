from pathlib import Path
from imageLoader import ImageLoader
from imageMerger import mergeImages, mergeRandomImagesInFolder, pickImages
from wpChanger import setImageAsWallpaper


class Changer:
    def __init__(self, imageFolder:Path, wpPath:Path) -> None:
        self.loader = ImageLoader(imageFolder)
        self.wpPath = wpPath
        self.currentImages = []

    def fullImageChange(self, numOfScreens, currentToBlackList=False):
        if currentToBlackList:
            for currentImage in self.currentImages:
                self.loader.addToBlackList(currentImage)            
        self.currentImages = self.loader.downloadImages(numOfScreens)
        # self.currentImages = pickImages(self.loader.baseFolder, numOfScreens)
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