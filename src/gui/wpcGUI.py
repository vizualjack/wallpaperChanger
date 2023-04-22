from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial
from typing import List
from .baseGUI import BaseGUI
from .settingsGUI import SettingsGUI
# from wallpaperChanger import WallpaperChanger   # just for coding help


IMAGE_WIDTH = 300

class WpcGUI(BaseGUI):             # :WallpaperChanger   # for coding help
    def __init__(self, wallpaperChanger, parent: Tk = None) -> None:
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
        ### top bar 
        allLoader = Frame(self.window)
        allLoader.grid(column=1,row=0)
        allLoader.grid()
        Button(allLoader, text="Load all new", command=self.__onAllNew).grid(column=0,row=0)
        Button(allLoader, text="All to blacklist", command=self.__onAllBlacklist).grid(column=1,row=0)
        Button(self.window, text="Settings", command=self.__openSettings).grid(column=2,row=0)
        ### settings for each screen
        for i in range(self.wallpaperChanger.saveData.getNumOfScreens()):
            checkState = IntVar(self.window)
            check = Checkbutton(self.window, variable=checkState)
            check.grid(column=i,row=2)
            self.checkStates.append(checkState)
        midVal = int(self.wallpaperChanger.saveData.getNumOfScreens() / 2)
        Button(self.window, text="New one", command=self.__onNewOneClick).grid(column=midVal,row=3)
        Button(self.window, text="To blacklist", command=self.__onToBlackListClick).grid(column=midVal,row=4)


    def loadImages(self):
        # clear current images and labels
        if len(self.currentImages) > 0:
            for curLabel in self.currentImageLabels:
                curLabel.destroy()
            self.currentImages.clear()
            self.currentImageLabels.clear()
        # add new images
        index = 0
        for image in self.wallpaperChanger.images:
            img = Image.open(image.data)
            scalingFactor = img.size[1] / img.size[0]
            height = int(scalingFactor * IMAGE_WIDTH)
            resized = img.resize((IMAGE_WIDTH, height), Image.LANCZOS)
            pi = ImageTk.PhotoImage(resized)
            imageLabel = Label(self.window, image=pi)
            imageLabel.grid(column=index,row=1)
            index += 1
            self.currentImages.append(pi)
            self.currentImageLabels.append(imageLabel)

    def __openSettings(self):
        self.settingsWindow = SettingsGUI(self.wallpaperChanger.ICON_PNG_PATH, self.wallpaperChanger.saveData, self.parent)
        self.settingsWindow.onClose = self.__onCloseSettings
        self.settingsWindow.show()

    def __onCloseSettings(self):
        self.settingsWindow = None

    def __onAllNew(self):
        self.wallpaperChanger.changeAll(False)

    def __onAllBlacklist(self):
        self.wallpaperChanger.changeAll(True)
    
    def __onNewOneClick(self):
        self.wallpaperChanger.changeMultiple(self.__getIndexes(), False)

    def __onToBlackListClick(self):
        self.wallpaperChanger.changeMultiple(self.__getIndexes(), True)

    def __getIndexes(self):
        indexes = []
        for index in range(len(self.checkStates)):
            checkState = (IntVar)(self.checkStates[index])
            if checkState.get() == 1:
                indexes.append(index)
        return indexes