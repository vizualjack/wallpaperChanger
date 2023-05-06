from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from .changer import Changer
######
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from typing import List
from .baseGUI import BaseGUI
from .settingsGUI import SettingsGUI
from .guiUtil import destroyAllChildren
from screen import Screen
from appSettings import *


_IMAGE_WIDTH = 300
_WINDOW_HEIGHT = 270

class ChangerGUI(BaseGUI):
    def __init__(self, changer:Changer, screens:List[Screen], parent:Tk = None) -> None:
        self.currentImages = []
        self.currentImageLabels:List[Label] = []
        self.checkStates = []
        self.__changer = changer
        self.__screens:List[Screen] = screens
        self.__settingsWindow:SettingsGUI = None
        fullWidth = _IMAGE_WIDTH + 4
        fullWidth *= len(self.__screens)
        super().__init__(ICON_PNG_PATH, parent, APPLICATION_TITLE, False, fullWidth, _WINDOW_HEIGHT)
        self.__createBaseLayout()

    def refreshAllImages(self):
        for index in range(len(self.__screens)):
            screen = self.__screens[index]
            ## new one
            img = screen.getWpcImage().asPilImage()
            scalingFactor = img.size[1] / img.size[0]
            height = int(scalingFactor * _IMAGE_WIDTH)
            resized = img.resize((_IMAGE_WIDTH, height), Image.LANCZOS)
            pi = ImageTk.PhotoImage(resized)
            imageLabel = Label(self.window, image=pi)
            ## destroy old one
            if self.currentImageLabels[index]:
                self.currentImageLabels[index].destroy()
            ## place new one
            imageLabel.grid(column=index,row=1)
            ## set to lists
            self.currentImages[index] = pi
            self.currentImageLabels[index] = imageLabel

    def __createBaseLayout(self):
        ### clear up
        destroyAllChildren(self.window)
        self.checkStates.clear()
        self.currentImages.clear()
        self.currentImageLabels.clear()
        ### activates grid
        self.window.grid()
        ### top bar 
        allLoader = Frame(self.window)
        allLoader.grid(column=1,row=0)
        allLoader.grid()
        Button(allLoader, text="Change all", command=self.__onAllChange).grid(column=0,row=0)
        Button(self.window, text="Settings", command=self.__openSettings).grid(column=2,row=0)
        ### settings for each screen
        for i in range(len(self.__screens)):
            checkState = IntVar(self.window)
            check = Checkbutton(self.window, variable=checkState)
            check.grid(column=i,row=2)
            self.checkStates.append(checkState)
            self.currentImages.append(None)
            self.currentImageLabels.append(None)
        midVal = int(len(self.__screens) / 2)
        Button(self.window, text="Change", command=self.__onChangeClick).grid(column=midVal,row=3)

    def __openSettings(self):
        self.__settingsWindow = SettingsGUI(ICON_PNG_PATH, self.__changer, self.parent)
        self.__settingsWindow.onClose = self.__onCloseSettings
        self.__settingsWindow.show()

    def __onCloseSettings(self):
        self.__settingsWindow = None
    
    def __onAllChange(self):
        self.__changer.changeAllWallpaper()
    
    def __onChangeClick(self):
        for index in self.__getIndexes():
            self.__changer.changeWallpaper(self.__screens[index])

    def __getIndexes(self):
        indexes = []
        for index in range(len(self.checkStates)):
            checkState = self.checkStates[index]
            if checkState.get() == 1:
                indexes.append(index)
        return indexes