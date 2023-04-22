from wallpaperChanger import WallpaperChanger, ICON_PNG_PATH
from trayIcon.tray import Tray, TrayItem

class WpcTray:
    def __init__(self, wallpaperChanger:WallpaperChanger) -> None:
        self.wallpaperChanger = wallpaperChanger
        self.tray = Tray(ICON_PNG_PATH, self.__createTrayItems())
        self.tray.start()

    def stop(self):
        self.tray.stop()

    def __createTrayItems(self):
        trayItems = []
        # trayItems.append(TrayItem("Open", self.wallpaperChanger....))