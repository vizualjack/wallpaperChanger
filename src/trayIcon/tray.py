from PIL import Image
from pathlib import Path
from typing import List
from pystray import MenuItem
from .trayItem import TrayItem
from .customIcon import CustomIcon


class Tray:
    def __init__(self,icon:Path, trayItems: List[TrayItem]): 
        self.icon = CustomIcon(
            'wct',
            icon=Image.open(icon), 
            menu=self.__getMenuItemFromTrayItems(trayItems),
            onDoubleClick=trayItems[0].onClickFunc
        )
        self.icon.title = "Wallpaper Changer"
        
    def start(self):
        self.icon.run_detached()

    def stop(self):
        self.icon.stop()

    def __getMenuItemFromTrayItems(self, trayItems: List[TrayItem]):
        menuItems = []
        for trayItem in trayItems:
            menuItems.append(MenuItem(trayItem.displayText, trayItem.onClickFunc))
        return menuItems
