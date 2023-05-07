from __future__ import annotations
from typing import Any, List, TYPE_CHECKING
if TYPE_CHECKING:
    from .imageDler import ImageDler    
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path
from tkinter import *
from tkinter.ttk import *
from change.baseGUI import BaseGUI
from appSettings import APPLICATION_TITLE, ICON_PNG_PATH
from change.wpcImage import WpcImage
from change.wpcImageContainer import WpcImageContainer
from PIL import Image, ImageTk
from threading import Thread


_WINDOW_WIDTH = 1000
_WINDOW_HEIGHT = 600
_IMAGE_LOADING_BATCH = 10

class ImageDlerGUI(BaseGUI):
    def __init__(self, imageDler: ImageDler, imageContainer:WpcImageContainer) -> None:
        self.__imageDler = imageDler
        self.__imageContainer = imageContainer
        self.__loadedImages:List[WpcImage] = []
        self.__bgLoader:BgLoader = None
        super().__init__(ICON_PNG_PATH, None, APPLICATION_TITLE, True, _WINDOW_WIDTH, _WINDOW_HEIGHT)
        self.window.bind("<Configure>", lambda e: self.__onResizeWindow(e))
        self.window.pack(fill=BOTH)
        buttons = Frame(self.window)
        self.__prevBtn = Button(buttons, text="Prev", command=self.__prevImage)
        self.__prevBtn.grid(row=0, column=0)
        self.__saveBtn = Button(buttons, text="Save", command=self.__save)
        self.__saveBtn.grid(row=0, column=1)
        self.__nextBtn = Button(buttons, text="Next", command=self.__nextImage)
        self.__nextBtn.grid(row=0, column=2)
        buttons.grid(column=0,row=1)
        # visible image stuff
        self.__imageIndex = 0
        self.__imageElement = None
        self.__imageLabel = None
        self.__imageWidth = 0
        self.__imageHeight = 0
        ###
        self.__loadNewImages()
        self.__checkButtonStates()

    def __onResizeWindow(self, event):
        newWidth = event.width
        self.__showImage(newWidth-5)
        newHeight = self.__imageHeight + 30
        self.parent.geometry(f"{newWidth}x{newHeight}")

    def __save(self):
        print("save image: " + self.__getCurrentImage().getFullName())
        self.__imageContainer.add(self.__getCurrentImage())

    def __prevImage(self):
        self.__imageIndex -= 1
        self.__afterImageSwitch()

    def __nextImage(self):
        self.__imageIndex += 1
        self.__afterImageSwitch()

    def __afterImageSwitch(self):
        print("switch to image: " + self.__getCurrentImage().getFullName())
        self.__checkButtonStates()
        self.__showImage()
        restImages = (len(self.__loadedImages)-1) - self.__imageIndex
        if restImages < 5:
            self.__loadNewImagesBackground()

    def __checkButtonStates(self):
        if self.__imageIndex <= 0:
            self.__prevBtn["state"] = "disabled"
        else: 
            self.__prevBtn["state"] = "normal"
        if self.__imageIndex >= len(self.__loadedImages)-1:
            self.__nextBtn["state"] = "disabled"
        else: 
            self.__nextBtn["state"] = "normal"

    def __getCurrentImage(self) -> WpcImage:
        return self.__loadedImages[self.__imageIndex]
    
    def __loadNewImagesBackground(self):
        if self.__bgLoader and self.__bgLoader.is_alive():
            return
        self.__bgLoader = BgLoader(self.__imageDler, self.__loadedImages)
        self.__bgLoader.start()
        print("started loading new images")

    def __loadNewImages(self):
        self.__loadedImages.extend(self.__imageDler.downloadImages(_IMAGE_LOADING_BATCH))
        print("got new images")

    def __showImage(self, width=None):
        if not width:
            width = self.__imageWidth
        curImage = self.__getCurrentImage()
        if not curImage:
            return
        pilImg = curImage.asPilImage()
        scalingFactor = pilImg.size[1] / pilImg.size[0]
        self.__imageWidth = width
        self.__imageHeight = int(scalingFactor * self.__imageWidth)
        resized = pilImg.resize((self.__imageWidth, self.__imageHeight), Image.LANCZOS)
        self.__imageElement = ImageTk.PhotoImage(resized)
        if self.__imageLabel:
            self.__imageLabel.destroy()
        self.__imageLabel = Label(self.window, image=self.__imageElement)
        self.__imageLabel.grid(row=0, column=0)


class BgLoader(Thread):
    def __init__(self, imageDler: ImageDler, imageList:List[WpcImage], group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self.__imageDler = imageDler
        self.__imageList = imageList

    def run(self):
        newImages = self.__imageDler.downloadImages(_IMAGE_LOADING_BATCH)
        self.__imageList.extend(newImages)
        print("BgLoader done")