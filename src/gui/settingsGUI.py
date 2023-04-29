from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from wallpaperChanger import WallpaperChanger
######
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from saveData import SaveData
from .baseGUI import BaseGUI


_WINDOW_TITLE = "Settings"

class SettingsGUI(BaseGUI):
    def __init__(self, icon: Path, wpc:WallpaperChanger, parent: Tk = None) -> None:
        super().__init__(icon, parent)
        self.wpc = wpc
        self.saved = False
        self._setTitle(_WINDOW_TITLE)
        self._setWindowToMidPos(243,109)
        self._setResizeable(False)
        ### init window content
        self.window.grid()
        self.changeIntervalVal = StringVar(value=self.__getSettingsValue(self.wpc.saveData.getInterval()))
        self.monitorWidthVal = StringVar(value=self.__getSettingsValue(self.wpc.imageDler.imageSize.width))
        self.monitorHeightVal = StringVar(value=self.__getSettingsValue(self.wpc.imageDler.imageSize.height))
        self.numOfScreensVal = StringVar(value=self.__getSettingsValue(self.wpc.saveData.getNumOfScreens()))
        ## CHANGE INTERVAL
        Label(self.window, text="Change interval(secs)").grid(row=0,column=0)
        Entry(self.window, textvariable=self.changeIntervalVal).grid(row=0, column=1)
        ## WIDTH
        Label(self.window, text="Monitor width(px)").grid(row=1,column=0)
        Entry(self.window, textvariable=self.monitorWidthVal).grid(row=1, column=1)
        ## HEIGHT
        Label(self.window, text="Monitor height(px)").grid(row=2,column=0)
        Entry(self.window, textvariable=self.monitorHeightVal).grid(row=2, column=1)
        ## NUM OF SCREENS
        Label(self.window, text="Number of screens").grid(row=3,column=0)
        Entry(self.window, textvariable=self.numOfScreensVal).grid(row=3, column=1)
        ####
        Button(self.window, text="Save", command=self.__saveSettings).grid(row=4, column=1)

    def __saveSettings(self):
        if not self.__validValues():
            return
        self.wpc.saveData.setInterval(int(self.changeIntervalVal.get()))
        self.wpc.imageDler.imageSize.width = int(self.monitorWidthVal.get())
        self.wpc.imageDler.imageSize.height = int(self.monitorHeightVal.get())
        self.wpc.saveData.setNumOfScreens(int(self.numOfScreensVal.get()))
        self.saved = True
        self._close()

    def __validValues(self):
        try:
            if not self.__valueBiggerThanZero(int(self.changeIntervalVal.get())):
                return False
            if not self.__valueBiggerThanZero(int(self.monitorWidthVal.get())):
                return False
            if not self.__valueBiggerThanZero(int(self.monitorHeightVal.get())):
                return False
            if not self.__valueBiggerThanZero(int(self.numOfScreensVal.get())):
                return False
            return True
        except:
            print("Some values aren't numbers")
            return False

    def __valueBiggerThanZero(self, value:int):
        if value > 0:
            return True
        return False

    def _canBeClosed(self):
        if isinstance(self.window, Frame) and not self.saved:
            return False
        return True
    
    def __getSettingsValue(self, settingsVal):
        if not settingsVal:
            return ""
        elif settingsVal < 0:
            return ""
        return settingsVal