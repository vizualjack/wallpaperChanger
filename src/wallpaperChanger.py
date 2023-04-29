from saveData import SaveData
from persist.persister import Persister
import persist.imageContainerPersist
import persist.imageDlerPersist
from pathlib import Path
from gui.settingsGUI import SettingsGUI
from gui.wpcGUI import WpcGUI
from trayIcon.tray import Tray, TrayItem
from img.image import Image
from img.imageContainer import ImageContainer
from img.imageDler import ImageDler
from img.imageOperator import ImageOperator
from typing import List
import ctypes
from wpcTray import WpcTray
import time



class WallpaperChanger:
    ICON_PNG_PATH = Path("src/icon/icon.png")
    PERSISTER_SAVE_PATH = Path("data.json")
    IMAGE_CONTAINER_PATH = Path("images")
    WP_PATH = Path("wp")
    # win api constants
    SPI_SETDESKWALLPAPER = 20

    class Change:
        def __init__(self, index, currentToBlackList) -> None:
            self.index = index
            self.currentToBlackList = currentToBlackList        

    def __init__(self) -> None:
        self.images:List[Image] = []
        self.persister = Persister(self.PERSISTER_SAVE_PATH)
        self.saveData = SaveData.load(self.persister)        
        self.imageContainer = persist.imageContainerPersist.loadFromPersister(self.persister)
        self.imageDler = persist.imageDlerPersist.loadFromPersister(self.persister)
        self.lastChangeTime = 0
        self.changes:List[WallpaperChanger.Change] = []
        self.running = False
        self.gui:WpcGUI = None

    def run(self):
        if not self.saveData or not self.imageContainer or not self.imageDler:
            self.saveData = SaveData()
            self.imageContainer = ImageContainer(self.IMAGE_CONTAINER_PATH)
            self.imageDler = ImageDler(Image.Size(0,0))
            self.__startInitSettings()
        else:
            self.__initWpc()

    def changeMultiple(self, indexes, currentToBlackList=False):
        for index in indexes:
            self.changes.append(WallpaperChanger.Change(index, currentToBlackList))

    def changeAll(self, currentToBlackList=False):
        for index in range(len(self.images)):
            self.changes.append(WallpaperChanger.Change(index, currentToBlackList))

    def stop(self):
        self.running = False

    def openWpcGui(self):
        if not self.gui:
            self.gui = WpcGUI(self)
            self.gui.onClose = self.__onWpcGuiClosed
            self.gui.loadImages()
            self.gui.show()
        
    def __onWpcGuiClosed(self):
        self.gui = None

    def __imagesToWallpaper(self):
        mergedImage = ImageOperator.mergeImagesHorizontal(self.images)
        self.__setImageAsWallpaper(mergedImage)

    def __setImageAsWallpaper(self, image:Image):
        image.name = self.WP_PATH.name
        image.move(self.WP_PATH.parent)
        print("Set image as wallpaper...")
        # print("Full image path: " + image..absolute().__str__())
        print(ctypes.windll.user32.SystemParametersInfoW(self.SPI_SETDESKWALLPAPER, 0, image.getFullPathStr(), 0))

    def __startInitSettings(self):
        settingsGui = SettingsGUI(self.ICON_PNG_PATH, self)
        settingsGui.onClose = self.__initSettings
        settingsGui.show()

    def __initSettings(self):
        # initial save to save at least the user settings
        self.__save()
        # le go
        self.__initWpc()

    def __initWpc(self):
        for i in range(self.saveData.getNumOfScreens()):
            self.images.append(Image())
        self.__initTray()
        self.__mainLoop()

    def __initTray(self):
        self.tray = WpcTray(self)

    def __doChanges(self):
        for change in self.changes:
            imageToChange = self.images[change.index]
            if change.currentToBlackList:
                self.imageContainer.addToBlackList(imageToChange)
            newImage = self.imageDler.downloadImage()
            if newImage:
                self.imageContainer.add(newImage)
            else:
                randomImages = self.imageContainer.getRandomImages(1,self.images)
                if len(randomImages) > 0:
                    newImage = randomImages[0]
            if newImage:
                self.images[change.index] = newImage
        self.changes.clear()
        self.__imagesToWallpaper()
        if self.gui:
            self.gui.loadImages()

    def __mainLoop(self):
        self.running = True
        while self.running:
            if time.time() - self.lastChangeTime >= self.saveData.getInterval():
                self.changeAll()
            if len(self.changes):
                self.__doChanges()
                self.lastChangeTime = time.time()
            time.sleep(1)
        self.__save()
        self.tray.stop()
        if self.gui:
            self.gui.close()

    def __save(self):
        self.saveData.addToPersister(self.persister)
        persist.imageContainerPersist.addToPersister(self.persister, self.imageContainer)
        persist.imageDlerPersist.addToPersister(self.persister, self.imageDler)
        self.persister.save()