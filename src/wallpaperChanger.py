from saveData import SaveData
from persist.persister import Persister
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


PERSISTER_SAVE_PATH = Path("data.json")
ICON_PNG_PATH = Path("src/icon/icon.png")
IMAGE_CONTAINER_PATH = Path("images")
WP_PATH = Path("wp")
# win api constants
SPI_SETDESKWALLPAPER = 20

class WallpaperChanger:
    class Change:
        def __init__(self, index, currentToBlackList) -> None:
            self.index = index
            self.currentToBlackList = currentToBlackList

    def __init__(self) -> None:
        self.images:List[Image] = []
        self.persister = Persister(PERSISTER_SAVE_PATH)
        self.saveData = SaveData.load(self.persister)
        self.lastChangeTime = 0
        self.changes = []
        self.running = False
        self.gui:WpcGUI = None
        if not self.saveData:
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

    def __imagesToWallpaper(self):
        mergedImage = ImageOperator.mergeImagesHorizontal(self.images)
        self.__setImageAsWallpaper(mergedImage)

    def __setImageAsWallpaper(self, image:Image):
        image.move(WP_PATH.parent)
        print("Set image as wallpaper...")
        # print("Full image path: " + image..absolute().__str__())
        print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image.getFullPath(), 0))

    def __startInitSettings(self):
        settingsGui = SettingsGUI(ICON_PNG_PATH, self.saveData)
        settingsGui.onClose = self.__initSettings()

    def __initSettings(self):
        # set non user settings
        self.saveData.setPage(1)
        self.saveData.setIndex(0)
        # initial save to save at least the user settings
        self.saveData.save(self.persister)
        # le go
        self.__initWpc()

    def __initWpc(self):
        self.imageContainer = ImageContainer(IMAGE_CONTAINER_PATH)
        self.imageDler = ImageDler(Image.Size(self.saveData.getWidth(), self.saveData.getHeight()))
        self.__initTray()
        self.__mainLoop()

    def __initTray(self):
        self.tray = WpcTray(self)

    def __doChanges(self, changes:List[Change]):
        for change in changes:
            imageToChange = self.images[change.index]
            if change.currentToBlackList:
                self.imageContainer.addToBlackList(imageToChange)
            newImage = self.imageDler.downloadImage()
            self.imageContainer.add(newImage)
            self.imageContainer[change.index] = newImage
        self.__imagesToWallpaper()

    def __mainLoop(self):
        self.running = True
        while self.running:
            if time.time() - self.lastChangeTime >= self.saveData.getInterval():
                self.changeAll()
            if len(self.changes):
                self.__doChanges()
                self.lastChangeTime = time.time()
            time.sleep(1)
        self.saveData.save(self.persister)
        self.tray.stop()
        if self.gui:
            self.gui.close()
        