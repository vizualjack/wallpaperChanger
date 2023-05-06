from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from wpc import Wpc
######
import subprocess
from pystray import Icon, Menu, MenuItem
from pystray._util import win32
from ctypes import wintypes
import ctypes
from PIL import Image
from pathlib import Path
from typing import List
from appSettings import *


class WpcTray:
    def __init__(self, wpc:Wpc) -> None:
        self.__wpc = wpc
        self.tray = Tray(ICON_PNG_PATH, self.__createTrayItems())
        self.tray.start()

    def stop(self):
        self.tray.stop()

    def __createTrayItems(self):
        trayItems = []
        trayItems.append(TrayItem("Open", self.__wpc.changer.openGui))
        trayItems.append(TrayItem("Change all", self.__changeAll))
        trayItems.append(TrayItem("Open images", self.__openImageFolder))
        trayItems.append(TrayItem("Close", self.__wpc.stop))
        return trayItems
        
    def __changeAll(self):
        self.__wpc.changer.changeAllWallpaper()

    def __openImageFolder(self):
        subprocess.Popen(f'explorer \"{IMAGE_FOLDER.absolute().__str__()}\"')
        
    
########## HELPER CLASSES ###########
class TrayItem:
    def __init__(self, displayText:str, onClickFunc) -> None:
        self.displayText = displayText
        self.onClickFunc = onClickFunc


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
    

class CustomIcon(Icon):
    def __init__(self, name, icon=None, title=None, menu=None,onDoubleClick=None, **kwargs):
        super().__init__(name, icon, title, menu, **kwargs)
        self.onDoubleClick = onDoubleClick

    def _on_notify(self, wparam, lparam):
        """Handles ``WM_NOTIFY``.

        If this is a left button click, this icon will be activated. If a menu
        is registered and this is a right button click, the popup menu will be
        displayed.
        """
        if lparam == 515 and self.onDoubleClick:
            self.onDoubleClick()
        if lparam == win32.WM_LBUTTONUP:
            self()

        elif self._menu_handle and lparam == win32.WM_RBUTTONUP:
            # TrackPopupMenuEx does not behave unless our systray window is the
            # foreground window
            win32.SetForegroundWindow(self._hwnd)

            # Get the cursor position to determine where to display the menu
            point = wintypes.POINT()
            win32.GetCursorPos(ctypes.byref(point))

            # Display the menu and get the menu item identifier; the identifier
            # is the menu item index
            hmenu, descriptors = self._menu_handle
            index = win32.TrackPopupMenuEx(
                hmenu,
                win32.TPM_RIGHTALIGN | win32.TPM_BOTTOMALIGN
                | win32.TPM_RETURNCMD,
                point.x,
                point.y,
                self._menu_hwnd,
                None)
            if index > 0:
                descriptors[index - 1](self)
