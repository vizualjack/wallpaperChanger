from pathlib import Path
from change.wpcImageContainer import WpcImageContainer
from typing import List
from wpcTray import WpcTray
import time
from util.persister import Persister
import tkinter.messagebox
from util.exceptionSaver import saveException
from screen import Screen
from screeninfo import get_monitors
from change.changer import Changer
from appSettings import *



class Wpc:
    def __init__(self) -> None:
        self.persister = Persister()
        self.screens:List[Screen] = []
        for monitor in get_monitors():
            self.screens.append(Screen(monitor.width, monitor.height))
        self.imageContainer = WpcImageContainer(IMAGE_FOLDER)
        # self.imageDler = persist.imageDlerPersist.loadFromPersister(self.persister)
        self.changer = Changer(self.imageContainer, self.screens)
        self.persister.loadChanger(self.changer)
        self.running = False

    def start(self):
        self.tray = WpcTray(self)
        self.__mainLoop()

    def stop(self):
        self.running = False

    def __mainLoop(self):
        self.running = True
        while self.running:
            try:
                self.changer.doChanges()
                time.sleep(1)
            except:
                self.__saveException()
        self.__save()
        self.changer.stop()
        self.tray.stop()

    def __saveException(self):
        additionalInfo = f"Current images:\n"
        for screen in self.screens:
            additionalInfo += f"\t{screen.getWpcImage().getFullName()}\n"
        logFilePath = saveException(additionalInfo)
        logFileName = logFilePath.name
        tkinter.messagebox.showerror(APPLICATION_TITLE, f"Error thrown in main thread! See {logFileName} for more details!")      

    def __save(self):
        self.persister.addChangerForSave(self.changer)
        self.persister.save()
