from wallpaperChanger import WallpaperChanger, ICON_PNG_PATH, IMAGE_CONTAINER_PATH
from trayIcon.tray import Tray, TrayItem
import subprocess


class WpcTray:
    def __init__(self, wallpaperChanger:WallpaperChanger) -> None:
        self.wallpaperChanger = wallpaperChanger
        self.tray = Tray(ICON_PNG_PATH, self.__createTrayItems())
        self.tray.start()

    def stop(self):
        self.tray.stop()

    def __createTrayItems(self):
        trayItems = []
        trayItems.append(TrayItem("Open", self.wallpaperChanger.openWpcGui))
        trayItems.append(TrayItem("Change all", self.wallpaperChanger.changeAll))
        trayItems.append(TrayItem("Open images", self.__openImageFolder))
        trayItems.append(TrayItem("Close", self.wallpaperChanger.stop))
        
    def __openImageFolder(self):
        subprocess.Popen(f'explorer \"{IMAGE_CONTAINER_PATH.absolute().__str__()}\"')
        
