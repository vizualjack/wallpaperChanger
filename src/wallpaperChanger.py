from saveData import SaveData
from persist.persister import Persister
from pathlib import Path
from gui.settingsGUI import SettingsGUI
from trayIcon.tray import Tray, TrayItem
from img.image import Image
from img.imageContainer import ImageContainer
from img.imageDler import ImageDler
from img.imageOperator import ImageOperator
from typing import List
import ctypes


PERSISTER_SAVE_PATH = Path("data.json")
ICON_PNG_PATH = Path("src/icon/icon.png")
IMAGE_CONTAINER_PATH = Path("images")
WP_PATH = Path("wp")
# win api constants
SPI_SETDESKWALLPAPER = 20

class WallpaperChanger:
    def __init__(self) -> None:
        self.images:List[Image] = []
        self.persister = Persister(PERSISTER_SAVE_PATH)
        self.saveData = SaveData.load(self.persister)
        if not self.saveData:
            self.__startInitSettings()
        else:
            self.__initWpc()

    def changeMultiple(self, indexes, currentToBlacklist=False):
        for index in indexes:
            imageToChange = self.images[index]
            if currentToBlacklist:
                self.imageContainer.addToBlackList(imageToChange)
            newImage = self.imageDler.downloadImage()
            self.imageContainer.add(newImage)
            self.imageContainer[index] = newImage
        self.__imagesToWallpaper()

    def __imagesToWallpaper(self):
        mergedImage = ImageOperator.mergeImagesHorizontal(self.images)
        self.__setImageAsWallpaper(mergedImage)
        pass

    def __setImageAsWallpaper(self, image:Image):
        if not isinstance(imagePath, Path):
            path = Path(imagePath)
        if not path.exists() or not path.is_file():
            print("No image found")
            return False
        print("Set image as wallpaper...")
        print("Full image path: " + imagePath.absolute().__str__())
        print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath.absolute().__str__() , 0))

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
        pass

    def __mainLoop(self):
        pass