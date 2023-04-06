from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
from threading import Thread
from pystray._util import win32
from ctypes import wintypes
import ctypes
from pathlib import Path


class Tray:  #(Thread)
    def __init__(self,icon:Path, onOpen, onLoadAll, onClose):
        # super().__init__(None, None, None, None, None, daemon=None)
        menuItems = [MenuItem("Open", onOpen),MenuItem("Change all", onLoadAll), MenuItem("Close", onClose)]
        self.icon = CustomIcon(
            'wct',
            icon=Image.open(icon), 
            menu=menuItems,
            onDoubleClick=onOpen
        )
        self.icon.title = "Wallpaper Changer"
        
    def start(self):
        self.icon.run_detached()

    def stop(self):
        self.icon.stop()

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
