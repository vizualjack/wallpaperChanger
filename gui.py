from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial

IMAGE_WIDTH = 300

class ChangeGui:
    def __init__(self, icon:Path, onLoadOne, onLoadAll, onClose, onChangeInterval) -> None:
        self.root = Tk()
        self.icon = PhotoImage(file=icon.absolute().__str__())
        self.root.iconphoto(False, self.icon)
        self.root.title("Wallpaper Changer")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.wm_resizable(False, False)
        self.onClose = onClose
        self.onChangeInterval = onChangeInterval
        self.frm = Frame(self.root)
        self.frm.grid()
        self.shownImages = []
        self.currentImages = []
        self.onLoadOne = onLoadOne
        self.onLoadAll = onLoadAll
        self.changeIntervalVal = StringVar()
        self.settingsWindow = None

    def show(self):
        self.root.mainloop()

    def closeSettings(self):
        if self.settingsWindow:
            self.settingsWindow.destroy()
            self.settingsWindow = None

    def openSettings(self):
        if self.settingsWindow:
            return
        self.settingsWindow = Toplevel(self.root)
        self.settingsWindow.iconphoto(False, self.icon)
        self.settingsWindow.title("Settings")
        self.settingsWindow.protocol("WM_DELETE_WINDOW", self.closeSettings)
        self.settingsWindow.resizable(False, False)
        self.settingsWindow.grid()
        self.changeIntervalVal.set("")
        Label(self.settingsWindow, text="Setting").grid(row=0,column=1)
        Label(self.settingsWindow, text="Change interval(secs)").grid(row=0,column=0)
        Entry(self.settingsWindow, textvariable=self.changeIntervalVal).grid(row=0, column=1)
        Button(self.settingsWindow, text="Save", command=self.saveSettings).grid(row=1, column=1)

    def saveSettings(self):
        try:
            intVal = int(self.changeIntervalVal.get())
            if intVal > 0:
                self.onChangeInterval(intVal)
            self.closeSettings()
        except:
            print("Fail to convert interval value")

    def loadImages(self, images: list[Path]):
        if len(self.currentImages) > 0:
            for key in self.frm.children.copy().keys():
                self.frm.children.get(key).destroy()                
            self.currentImages.clear()
        self.shownImages = images
        Button(self.frm, text="Load all new", command=self.onLoadAll).grid(column=1,row=0)
        Button(self.frm, text="Settings", command=self.openSettings).grid(column=2,row=0)
        index = 0
        for imgPath in self.shownImages:
            img = Image.open(imgPath)
            scalingFactor = img.size[1] / img.size[0]
            height = int(scalingFactor * IMAGE_WIDTH)
            resized = img.resize((IMAGE_WIDTH, height), Image.LANCZOS)
            pi = ImageTk.PhotoImage(resized)
            imageLabel = Label(self.frm, image=pi)
            imageLabel.grid(column=index,row=1)
            Button(self.frm, text="Load new", command=partial(self.onLoadOne, index)).grid(column=index,row=2)
            index += 1
            self.currentImages.append(pi)

    def close(self):        
        if self.onClose:
            self.onClose()
        self.root.destroy()
