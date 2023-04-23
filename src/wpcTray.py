from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from wallpaperChanger import WallpaperChanger
######
from trayIcon.tray import Tray, TrayItem
import subprocess


class WpcTray:
    def __init__(self, wallpaperChanger:WallpaperChanger) -> None:
        self.wallpaperChanger = wallpaperChanger
        self.tray = Tray(self.wallpaperChanger.ICON_PNG_PATH, self.__createTrayItems())
        self.tray.start()

    def stop(self):
        self.tray.stop()

    def __createTrayItems(self):
        trayItems = []
        trayItems.append(TrayItem("Open", self.wallpaperChanger.openWpcGui))
        trayItems.append(TrayItem("Change all", self.__changeAll))
        trayItems.append(TrayItem("Open images", self.__openImageFolder))
        trayItems.append(TrayItem("Close", self.wallpaperChanger.stop))
        return trayItems
        
    def __changeAll(self):
        self.wallpaperChanger.changeAll()

    def __openImageFolder(self):
        subprocess.Popen(f'explorer \"{self.wallpaperChanger.IMAGE_CONTAINER_PATH.absolute().__str__()}\"')
        
