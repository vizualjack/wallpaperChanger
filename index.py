from pathlib import Path
import time
from changer import Changer
import tkinter
from gui import ChangeGui
from tray import Tray



##### SETTINGS
MONITOR_SIZE = "1920x1080"
NUM_OF_SCREENS = 3
IMAGES_FOLDER = Path("images")
WP_FOLDER = Path("wps")
CHANGE_INTERVAL_SECS = 10
#####


#####
closing = False
nextChangeTime = time.time()
trayIcon:Tray = None
myChanger = Changer(IMAGES_FOLDER, WP_FOLDER)
cg:ChangeGui = None


def loadAll():
    myChanger.fullImageChange(NUM_OF_SCREENS)
    refreshGui()

def loadNew(index):
    myChanger.changeOne(index)
    refreshGui()

def refreshGui():
    if not cg:
        return
    cg.loadImages(myChanger.currentImages)

def onGuiClosed():
    global cg
    cg = None

def close():
    print("Closing...")
    global closing, trayIcon, cg
    # DESTROY TRAY
    trayIcon.stop()
    # DESTROY GUI
    if cg:
        cg.close()
    closing = True

def openGui():
    global cg
    if not cg:
        cg = ChangeGui(loadNew, loadAll, onGuiClosed)
    cg.loadImages(myChanger.currentImages)
    cg.show()

def main():
    global trayIcon, nextChangeTime, closing
    # CREATE TRAY ICON
    trayIcon = Tray(openGui, close)
    trayIcon.start()
    # MAIN CHECK LOOP
    print("Go into main check loop")
    while not closing:
        if time.time() >= nextChangeTime:
            nextChangeTime = time.time() + CHANGE_INTERVAL_SECS
            loadAll()
        time.sleep(1)
    print("Closed")

main()