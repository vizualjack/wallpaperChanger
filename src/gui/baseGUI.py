from pathlib import Path
from tkinter import *
from tkinter.ttk import *

class BaseGUI:
    def __init__(self, icon:Path, parent:Tk=None) -> None:
        self.parent = parent
        self.window = None
        if parent:
            self.window = Toplevel(parent)
        else:
            self.parent = Tk()
            self.window = Frame(self.parent)
        self.__initWindow__(icon)
        self.onClose = None

    def show(self):
        if isinstance(self.window, Frame):
            self.parent.mainloop()

    def __initWindow__(self, icon:Path):
        self.icon = PhotoImage(file=icon.absolute().__str__())
        changeObj = self._getChangeableWindow()
        changeObj.iconphoto(False, self.icon)
        changeObj.protocol("WM_DELETE_WINDOW", self._close)

    def _getChangeableWindow(self):
        changeableWindow = self.window
        if isinstance(changeableWindow, Frame):
            changeableWindow = self.parent
        return changeableWindow        

    def _canBeClosed(self):
        return True

    def _close(self):
        toClose = self.window
        if isinstance(self.window, Frame):
            toClose = self.parent
        if not self._canBeClosed():
            return
        self.onClose()
        toClose.destroy()

    def _setTitle(self, title):
        self._getChangeableWindow().title(title)
            
    def _setWindowToMidPos(self, width, height):
        x = int((self.window.winfo_screenwidth() / 2) - (width / 2))
        y = int((self.window.winfo_screenheight() / 2) - (height / 2))
        self._setPosAndSize(x, y, width, height)

    def _setResizeable(self, resizable:bool):
        self._getChangeableWindow().resizable(resizable, resizable)

    def _setPosAndSize(self, x, y, width, height):
        geometryStr = f"{width}x{height}+{x}+{y}"
        self._getChangeableWindow().geometry(geometryStr)