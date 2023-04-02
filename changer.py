from pathlib import Path
from imageLoader import ImageLoader
from imageMerger import mergeImages, mergeRandomImagesInFolder, pickImages
from wpChanger import setImageAsWallpaper


class Changer:
    def __init__(self, imageFolder:Path, wpFolder:Path) -> None:
        self.loader = ImageLoader(imageFolder)
        self.wpFolder = wpFolder
        self.currentImages = []

    def fullImageChange(self, numOfScreens):
        self.currentImages = self.loader.downloadImages(numOfScreens)
        # self.currentImages = pickImages(self.loader.baseFolder, numOfScreens)
        self.__mergeAndSetGivenImages()

    def changeOne(self, index):
        if index >= len(self.currentImages) or index < 0:
            print("Index out of range")
            return
        newImage = self.loader.downloadImage()
        self.currentImages[index] = newImage
        self.__mergeAndSetGivenImages()


    # def __mergeAndSetRandomImages(self, numOfScreens):
    #     mergedImage = mergeRandomImagesInFolder(self.wpFolder, self.loader.baseFolder, numOfScreens)
    #     setImageAsWallpaper(mergedImage)

    def __mergeAndSetGivenImages(self):
        mergedImage = mergeImages(self.wpFolder, self.currentImages)
        setImageAsWallpaper(mergedImage)