from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial
from typing import List
from userSettings import UserSettings


IMAGE_WIDTH = 300

class GUI:
    def __init__(self, icon:Path, userSettings:UserSettings, onLoadOne, onLoadAll, onClose) -> None:
        self.userSettings = userSettings
        self.root = Tk()
        if self.userSettings.getChangeInterval():
            fullWidth = IMAGE_WIDTH+4
            fullWidth *= self.userSettings.getNumOfScreens()
            self.root.geometry(self.__getMidGeometryForMidPos(fullWidth, 222))
        else:
            self.root.geometry(self.__getMidGeometryForMidPos(150, 20))
        self.icon = PhotoImage(file=icon.absolute().__str__())
        self.root.iconphoto(False, self.icon)
        self.root.title("Wallpaper Changer")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.wm_resizable(False, False)
        self.onClose = onClose
        self.mainFrame = Frame(self.root)
        self.mainFrame.grid()
        self.shownImages = []
        self.currentImages = []
        self.currentImageLabels = []
        self.onLoadOne = onLoadOne
        self.onLoadAll = onLoadAll
        self.changeIntervalVal = StringVar()
        self.monitorWidthVal = StringVar()
        self.monitorHeightVal = StringVar()
        self.numOfScreensVal = StringVar()
        self.settingsWindow = None
        self.needSettings = False
        self.initLabel = Label(self.mainFrame, text="Wait for settings...")
        self.initLabel.grid(row=0,column=0)
        if not self.userSettings.getChangeInterval():
            self.needSettings = True
            self.openSettings()
        else:
            self.__initMainWindow()

    def show(self):
        self.root.mainloop()

    #### SETTINGS
    def openSettings(self):
        if self.settingsWindow:
            return
        self.settingsWindow = Toplevel(self.root)
        self.settingsWindow.geometry(self.__getMidGeometryForMidPos(243,109))
        self.settingsWindow.iconphoto(False, self.icon)
        self.settingsWindow.title("Settings")
        self.settingsWindow.protocol("WM_DELETE_WINDOW", self.closeSettings)
        self.settingsWindow.resizable(False, False)
        self.settingsWindow.grid()
        self.changeIntervalVal.set(self.__getSettingsValue(self.userSettings.getChangeInterval()))
        self.monitorWidthVal.set(self.__getSettingsValue(self.userSettings.getMonitorWidth()))
        self.monitorHeightVal.set(self.__getSettingsValue(self.userSettings.getMonitorHeight()))
        self.numOfScreensVal.set(self.__getSettingsValue(self.userSettings.getNumOfScreens()))
        ## CHANGE INTERVAL
        Label(self.settingsWindow, text="Change interval(secs)").grid(row=0,column=0)
        Entry(self.settingsWindow, textvariable=self.changeIntervalVal).grid(row=0, column=1)
        ## WIDTH
        Label(self.settingsWindow, text="Monitor width(px)").grid(row=1,column=0)
        Entry(self.settingsWindow, textvariable=self.monitorWidthVal).grid(row=1, column=1)
        ## HEIGHT
        Label(self.settingsWindow, text="Monitor height(px)").grid(row=2,column=0)
        Entry(self.settingsWindow, textvariable=self.monitorHeightVal).grid(row=2, column=1)
        ## NUM OF SCREENS
        Label(self.settingsWindow, text="Number of screens").grid(row=3,column=0)
        Entry(self.settingsWindow, textvariable=self.numOfScreensVal).grid(row=3, column=1)
        ####
        Button(self.settingsWindow, text="Save", command=self.saveSettings).grid(row=4, column=1)

    def closeSettings(self):
        if self.settingsWindow:
            self.settingsWindow.destroy()
            self.settingsWindow = None
        if self.needSettings:
            if self.userSettings.getChangeInterval():
                self.__initMainWindow()
                self.needSettings = False
            self.close()    

    def saveSettings(self):
        try:
            print(self.root.winfo_width())
            print(self.root.winfo_height())
            self.userSettings.setChangeInterval(int(self.changeIntervalVal.get()))
            self.userSettings.setMonitorWidth(int(self.monitorWidthVal.get()))
            self.userSettings.setMonitorHeight(int(self.monitorHeightVal.get()))
            self.userSettings.setNumOfScreens(int(self.numOfScreensVal.get()))
            self.userSettings.save()
            self.closeSettings()
        except:
            print("Fail to save settings, check ur input")        

    def __getSettingsValue(self, settingsVal):
        if not settingsVal:
            return ""
        return settingsVal
    ###### ^ SETTINGS ^ 

    def loadImages(self, images: List[Path]):
        if len(images) != self.userSettings.getNumOfScreens():
            print("list of images not match with number of screens")
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

    def close(self):        
        if self.onClose:
            self.onClose()
        self.root.destroy()

    def __initMainWindow(self):
        self.initLabel.destroy()
        allLoader = Frame(self.mainFrame)
        allLoader.grid(column=1,row=0)
        allLoader.grid()
        Button(allLoader, text="Load all new", command=partial(self.onLoadAll, False)).grid(column=0,row=0)
        Button(allLoader, text="All to blacklist", command=partial(self.onLoadAll, True)).grid(column=1,row=0)
        Button(self.mainFrame, text="Settings", command=self.openSettings).grid(column=2,row=0)
        for i in range(self.userSettings.getNumOfScreens()):
            imageBtns = Frame(self.mainFrame)
            imageBtns.grid(column=i,row=2)
            imageBtns.grid()
            Button(imageBtns, text="New one", command=partial(self.onLoadOne, i, False)).grid(column=0,row=0)
            Button(imageBtns, text="To blacklist", command=partial(self.onLoadOne, i, True)).grid(column=1,row=0)

    def __getMidGeometryForMidPos(self, width, height):
        x = int((self.root.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.root.winfo_screenheight() / 2) - (height / 2))
        return f"{width}x{height}+{x}+{y}"
