from tkinter import *
from tkinter.ttk import *
from pathlib import Path
from PIL import Image, ImageTk
from functools import partial

IMAGE_WIDTH = 300

class ChangeGui:
    def __init__(self, onLoadOne, onLoadAll, onClose) -> None:
        self.root = Tk()
        self.root.title("Wallpaper Changer")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.wm_resizable(False, False)
        self.onClose = onClose
        self.frm = Frame(self.root)
        self.frm.grid()
        self.shownImages = []
        self.currentImages = []
        self.onLoadOne = onLoadOne
        self.onLoadAll = onLoadAll

    def show(self):
        self.root.mainloop()

    def loadImages(self, images: list[Path]):
        if len(self.currentImages) > 0:
            for key in self.frm.children.copy().keys():
                self.frm.children.get(key).destroy()                
            self.currentImages.clear()
        self.shownImages = images
        Button(self.frm, text="Load all new", command=self.onLoadAll).grid(column=1,row=0)
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
