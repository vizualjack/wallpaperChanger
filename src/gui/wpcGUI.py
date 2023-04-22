from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial
from typing import List
from .baseGUI import BaseGUI
from wallpaperChanger import WallpaperChanger, ICON_PNG_PATH


IMAGE_WIDTH = 300

class WpcGUI(BaseGUI):
    def __init__(self, wallpaperChanger:WallpaperChanger, parent: Tk = None) -> None:
        super().__init__(ICON_PNG_PATH, parent)
        self.wallpaperChanger = wallpaperChanger
        self.root = Tk()
        fullWidth = IMAGE_WIDTH+4
        fullWidth *= self.wallpaperChanger.saveData.getNumOfScreens()
        self._setWindowToMidPos(fullWidth, 270)
        self._setTitle("Wallpaper Changer")
        self._setResizeable(False)
        # actual window stuff
        # self.shownImages = []
        # self.currentImages = []
        # self.currentImageLabels = []
        self.checkStates = []
        self.window.grid()
        ### top bar 
        allLoader = Frame(self.window)
        allLoader.grid(column=1,row=0)
        allLoader.grid()
        Button(allLoader, text="Load all new", command=partial(self.onLoadAll, False)).grid(column=0,row=0)
        Button(allLoader, text="All to blacklist", command=partial(self.onLoadAll, True)).grid(column=1,row=0)
        Button(self.window, text="Settings", command=self.openSettings).grid(column=2,row=0)
        ### settings for each screen
        for i in range(self.wallpaperChanger.saveData.getNumOfScreens()):
            checkState = IntVar(self.window)
            check = Checkbutton(self.window, variable=checkState)
            check.grid(column=i,row=2)
            self.checkStates.append(checkState)
        midVal = int(self.wallpaperChanger.saveData.getNumOfScreens() / 2)
        Button(self.window, text="New one", command=self.__onNewOneClick).grid(column=midVal,row=3)
        Button(self.window, text="To blacklist", command=self.__onToBlackListClick).grid(column=midVal,row=4)

    
    def __onNewOneClick(self):
        for index in range(len(self.checkStates)):
            checkState = (IntVar)(self.checkStates[index])
            if checkState.get() == 1:
                self.onLoadOne(index, False)

    def loadImages(self):
        # CLEAR CUR IMAGES
        if len(self.currentImages) > 0:
            for curLabel in self.currentImageLabels:
                curLabel.destroy()
            self.currentImages.clear()
            self.currentImageLabels.clear()
        self.shownImages = images
        index = 0
        for imgPath in self.shownImages:
            img = Image.open(imgPath)
            scalingFactor = img.size[1] / img.size[0]
            height = int(scalingFactor * IMAGE_WIDTH)
            resized = img.resize((IMAGE_WIDTH, height), Image.LANCZOS)
            pi = ImageTk.PhotoImage(resized)
            imageLabel = Label(self.mainFrame, image=pi)
            imageLabel.grid(column=index,row=1)
            index += 1
            self.currentImages.append(pi)
            self.currentImageLabels.append(imageLabel)