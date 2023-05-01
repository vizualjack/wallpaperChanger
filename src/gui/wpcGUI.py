from __future__ import annotations 
from typing import TYPE_CHECKING
if TYPE_CHECKING:  # here goes just the stuff only for type checking
    from wallpaperChanger import WallpaperChanger
######
from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial
from typing import List
from .baseGUI import BaseGUI
from .settingsGUI import SettingsGUI
from img.imageUtil import loadPILImage
from .guiUtil import destroyAllChildren


IMAGE_WIDTH = 300

class WpcGUI(BaseGUI):
    def __init__(self, wallpaperChanger:WallpaperChanger, parent: Tk = None) -> None:
        super().__init__(wallpaperChanger.ICON_PNG_PATH, parent)
        self.wallpaperChanger = wallpaperChanger
        self.settingsWindow:SettingsGUI = None
        fullWidth = IMAGE_WIDTH+4
        fullWidth *= self.wallpaperChanger.saveData.getNumOfScreens()
        self._setWindowToMidPos(fullWidth, 270)
        self._setTitle("Wallpaper Changer")
        self._setResizeable(False)
        # actual window stuff
        # self.shownImages = []
        self.currentImages = []
        self.currentImageLabels:List[Label] = []
        self.checkStates = []
        self.window.grid()
        self.__createBaseLayout()

    def refreshAllImages(self):
        for index in range(len(self.wallpaperChanger.images)):
            self.refreshImage(index)

    def refreshImages(self, indexes:List[int]):
        for index in indexes:
            self.refreshImage(index)

    def refreshImage(self, index):
        image = self.wallpaperChanger.images[index]
        ## new one
        img = loadPILImage(image.getFullName(), image.data)  # Image.open(image.getFullPath())
        scalingFactor = img.size[1] / img.size[0]
        height = int(scalingFactor * IMAGE_WIDTH)
        resized = img.resize((IMAGE_WIDTH, height), Image.LANCZOS)
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
        ### top bar 
        onlySavedImages = Frame(self.window)
        onlySavedImages.grid(column=0,row=0)
        onlySavedImages.grid()
        self.onlySavedImages = IntVar(self.window)
        if self.wallpaperChanger.saveData.getUseOnlySavedImages():
            self.onlySavedImages.set(1)
        Checkbutton(onlySavedImages, command=self.__onSwitchOnlySavedImagesCheck, variable=self.onlySavedImages, text="Only saved images").grid(column=0,row=0)
        allLoader = Frame(self.window)
        allLoader.grid(column=1,row=0)
        allLoader.grid()
        if self.wallpaperChanger.saveData.getUseOnlySavedImages():
            Button(allLoader, text="Change all", command=self.__onAllChange).grid(column=0,row=0)
        else:
            Button(allLoader, text="All save & new", command=self.__onAllSave).grid(column=0,row=0)
            Button(allLoader, text="All blacklist & new", command=self.__onAllBlacklist).grid(column=1,row=0)
        Button(self.window, text="Settings", command=self.__openSettings).grid(column=2,row=0)
        ### settings for each screen
        for i in range(self.wallpaperChanger.saveData.getNumOfScreens()):
            checkState = IntVar(self.window)
            check = Checkbutton(self.window, variable=checkState)
            check.grid(column=i,row=2)
            self.checkStates.append(checkState)
            self.currentImages.append(None)
            self.currentImageLabels.append(None)
        midVal = int(self.wallpaperChanger.saveData.getNumOfScreens() / 2)
        if self.wallpaperChanger.saveData.getUseOnlySavedImages():
            Button(self.window, text="Change", command=self.__onChangeClick).grid(column=midVal,row=3)
        else:
            Button(self.window, text="Save & new", command=self.__onSaveClick).grid(column=midVal,row=3)
            Button(self.window, text="To blacklist & new", command=self.__onToBlackListClick).grid(column=midVal,row=4)

    def __onSwitchOnlySavedImagesCheck(self):
        newUseOnlyVal = False
        if self.onlySavedImages.get() == 1:
            newUseOnlyVal = True
        self.wallpaperChanger.saveData.setUseOnlySavedImages(newUseOnlyVal)
        self.__createBaseLayout()
        self.refreshAllImages()

    def __openSettings(self):
        self.settingsWindow = SettingsGUI(self.wallpaperChanger.ICON_PNG_PATH, self.wallpaperChanger.saveData, self.parent)
        self.settingsWindow.onClose = self.__onCloseSettings
        self.settingsWindow.show()

    def __onCloseSettings(self):
        self.settingsWindow = None

    
    def __onAllChange(self):
        self.wallpaperChanger.changeAll(self.wallpaperChanger.Change.ChangeType.NOTHING)

    def __onAllSave(self):
        self.wallpaperChanger.changeAll(self.wallpaperChanger.Change.ChangeType.SAVE)

    def __onAllBlacklist(self):
        self.wallpaperChanger.changeAll(self.wallpaperChanger.Change.ChangeType.TO_BLACKLIST)
    
    def __onChangeClick(self):
        self.wallpaperChanger.changeMultiple(self.__getIndexes(), self.wallpaperChanger.Change.ChangeType.NOTHING)
    
    def __onSaveClick(self):
        self.wallpaperChanger.changeMultiple(self.__getIndexes(), self.wallpaperChanger.Change.ChangeType.SAVE)

    def __onToBlackListClick(self):
        self.wallpaperChanger.changeMultiple(self.__getIndexes(), self.wallpaperChanger.Change.ChangeType.TO_BLACKLIST)

    def __getIndexes(self):
        indexes = []
        for index in range(len(self.checkStates)):
            checkState = self.checkStates[index]
            if checkState.get() == 1:
                indexes.append(index)
        return indexes