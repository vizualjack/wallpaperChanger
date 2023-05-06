from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from .changer import Changer
######
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from .baseGUI import BaseGUI


_WINDOW_TITLE = "Settings"
_WINDOW_WIDTH = 243
_WINDOW_HEIGHT = 50

class SettingsGUI(BaseGUI):
    def __init__(self, icon: Path, changer:Changer, parent: Tk = None) -> None:
        super().__init__(icon, parent, _WINDOW_TITLE, False, _WINDOW_WIDTH, _WINDOW_HEIGHT)
        self.__changer = changer
        ### init window content
        self.window.grid()
        self.changeIntervalVal = StringVar(value = self.__changer.changeIntervalSecs)
        ## CHANGE INTERVAL
        Label(self.window, text="Change interval(secs)").grid(row=0,column=0)
        Entry(self.window, textvariable=self.changeIntervalVal).grid(row=0, column=1)
        ####
        Button(self.window, text="Save", command=self.__saveSettings).grid(row=1, column=1)

    def __saveSettings(self):
        if not self.__validValues():
            return
        self.__changer.changeIntervalSecs = int(self.changeIntervalVal.get())
        self._close()

    def __validValues(self):
        try:
            if not self.__valueBiggerThanZero(int(self.changeIntervalVal.get())):
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