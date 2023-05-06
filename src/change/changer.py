from pathlib import Path
import ctypes
from .imageUtil import getImageWithHighestHeight, getImagesWidthSum
from PIL import Image
import io
from .wpcImage import WpcImage
from typing import List
from change.screen import Screen
from .wpcImageContainer import WpcImageContainer
from .changerGUI import ChangerGUI
import time


class Changer:
    __CUR_WP = Path("wp")
    # win api constants
    __SPI_SETDESKWALLPAPER = 20

    def __init__(self, imageContainer:WpcImageContainer, screens: List[Screen]) -> None:
        self.__imageContainer = imageContainer
        self.__screens = screens
        self.__gui:ChangerGUI = None
        self.__lastChangeTime = 0
        self.changeIntervalSecs = 3600 # 1 hour
        # try load change interval

    def changeWallpaper(self, screen:Screen):
        newImages = self.__imageContainer.getRandomImages(1, self.__getCurrentImages())
        if len(newImages) > 0:
            screen.setWpcImage(newImages[0])

    def changeAllWallpaper(self):
        newImages = self.__imageContainer.getRandomImages(3, self.__getCurrentImages())
        for screen in self.__screens:
            if len(newImages) <= 0:
                return
            screen.setWpcImage(newImages.pop())

    def openGui(self):
        if not self.__gui:
            self.__gui = ChangerGUI(self, self.__screens)
            self.__gui.onClose = self.__onWpcGuiClosed
            self.__gui.refreshAllImages()
            self.__gui.show()

    def stop(self):
        if self.__gui:
            self.__gui.close()

    def doChanges(self):
        if time.time() - self.__lastChangeTime >= self.changeIntervalSecs:
            self.changeAllWallpaper()
        wpChanged = False
        for screen in self.__screens:
            if screen.hasWpcChanged():
                wpChanged = True
            screen.resetWpcChanged()
        if wpChanged:
            self.__imagesToWallpaper()
            if self.__gui:
                self.__gui.refreshAllImages()
            self.__lastChangeTime = time.time()
    
    def __onWpcGuiClosed(self):
        self.__gui = None
    
    def __getCurrentImages(self):
        curImages = []
        for screen in self.__screens:
            curImages.append(screen.getWpcImage())
        return curImages

    def __imagesToWallpaper(self):
        mergedImage = self.__mergeImagesHorizontal(self.__getCurrentImages())
        self.__setWallpaperImage(mergedImage)

    def __mergeImagesHorizontal(self, images: List[WpcImage]) -> WpcImage:
        highestHeightImage = getImageWithHighestHeight(images)
        widthSum = getImagesWidthSum(images)
        mergedPILImage = Image.new("RGB", (widthSum, highestHeightImage.size.height))
        startPos = 0
        for image in images:
            pilImage = image.asPilImage()
            mergedPILImage.paste(pilImage, [startPos,0])
            startPos += image.size.width
        mergedImage = WpcImage()
        bytesIO = io.BytesIO()
        mergedImage.extension = "jpg"
        mergedPILImage.save(bytesIO, Image.EXTENSION["." + mergedImage.extension])
        mergedImage.data = bytesIO.getvalue()
        mergedImage.type = WpcImage.Type.JPG
        mergedImage.name = "merged"
        mergedImage.size = WpcImage.Size(widthSum, highestHeightImage)
        return mergedImage

    def __setWallpaperImage(self, image:WpcImage):
        image.name = self.__CUR_WP.name
        image.move(self.__CUR_WP.parent)
        # print("Set image as wallpaper...")
        # print("Full image path: " + image..absolute().__str__())
        success = ctypes.windll.user32.SystemParametersInfoW(self.__SPI_SETDESKWALLPAPER, 0, image.getFullPathStr(), 0)

    __KEY_CHANGEINTERVAL = "changeIntervalSecs"
    def loadFromJson(self, json:dict):
        self.changeIntervalSecs = int(json[self.__KEY_CHANGEINTERVAL])

    def getSaveDataJson(self):
        saveData = {}
        saveData[self.__KEY_CHANGEINTERVAL] = self.changeIntervalSecs
        return saveData