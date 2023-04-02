from pathlib import Path
from imageLoader import ImageLoader
from imageMerger import mergeImages, mergeRandomImagesInFolder
from wpChanger import setImageAsWallpaper


class Changer:
    def __init__(self, imageFolder:Path, wpFolder:Path) -> None:
        self.loader = ImageLoader(imageFolder)
        self.wpFolder = wpFolder
        self.currentImages = []

    def fullImageChange(self, numOfScreens):
        # self.currentImages = self.loader.downloadImages(numOfScreens)
        self.__mergeAndSet(numOfScreens)

    def changeOne(self, index):
        if index >= len(self.currentImages) or index < 0:
            print("Index out of range")
            return
        newImage = self.loader.downloadImage()
        self.currentImages[index] = newImage
        self.__mergeAndSet()

    def __mergeAndSet(self, numOfScreens):
        # mergedImage = mergeImages(self.wpFolder, self.currentImages)
        mergedImage = mergeRandomImagesInFolder(self.wpFolder, self.loader.baseFolder, numOfScreens)
        setImageAsWallpaper(mergedImage)