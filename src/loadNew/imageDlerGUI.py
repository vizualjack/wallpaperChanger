from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from change.baseGUI import BaseGUI
from appSettings import APPLICATION_TITLE, ICON_PNG_PATH
from change.wpcImage import WpcImage
from change.wpcImageContainer import WpcImageContainer
from .imageDler import ImageDler
from PIL import Image, ImageTk


_IMAGE_WIDTH = 300
_WINDOW_HEIGHT = 270

class ImageDlerGUI(BaseGUI):
    def __init__(self, imageSize: WpcImage.Size, imageContainer:WpcImageContainer) -> None:
        self.__imageDler = ImageDler(imageSize)
        self.__imageContainer = imageContainer
        self.__saveableImageElements = []
        super().__init__(ICON_PNG_PATH, None, APPLICATION_TITLE, True, 1000, 500)
        self.imageHolderWrapper = Scrollbar(self.window)
        self.imageHolderWrapper.pack(side=RIGHT, fill = Y)
        self.imageHolder = Frame(self.window)
        self.__newImages()
        self.imageHolder.pack(side = LEFT, fill = BOTH)
        self.window.pack()
        # self.imageHolderWrapper.config(command = self.imageHolder.yview)

    def __newImages(self):
        for image in self.__imageContainer.getRandomImages(3):
            self.__saveableImageElements.append(SaveableImageElement(image, self))
        print("new image loaded")

class SaveableImageElement:
    def __init__(self, wpcImage:WpcImage, imageDlerGUI:ImageDlerGUI) -> None:
        self.__imageDlerGUI = imageDlerGUI
        self.__wpcImage = wpcImage
        img = self.__wpcImage.asPilImage()
        scalingFactor = img.size[1] / img.size[0]
        height = int(scalingFactor * _IMAGE_WIDTH)
        resized = img.resize((_IMAGE_WIDTH, height), Image.LANCZOS)
        self.__pi = ImageTk.PhotoImage(resized)
        s = Style()
        s.configure('My.TFrame', background='red')
        self.__frame = Frame(self.__imageDlerGUI.imageHolder, style="My.TFrame")
        self.__frame.grid()
        self.__imageLabel = Label(self.__frame, image=self.__pi)
        self.__imageLabel.grid(row=0, column=0)
        self.__saveButton = Button(self.__frame, text="Save", command=self.__save)
        self.__saveButton.grid(row=1, column=0)
        # self.__frame.pack(side="top", expand=1, fill="both")
        # self.__frame.grid(row=0, column=0)

    def __save(self):
        print("image to save: " + self.__wpcImage.getFullName())