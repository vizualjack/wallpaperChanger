########## BUILD LINE
# pyinstaller index.py --name "Wallpaper Changer" --icon=icon/icon.ico --add-data "icon/;icon/" --noconsole    # doesnt work yet --onefile 
############
from pathlib import Path
import time
from changer import Changer
from gui import GUI
from tray import Tray
from userSettings import UserSettings
from screenSize import ScreenSize



##### APP SETTINGS
MONITOR_SIZE = ScreenSize(1920,1080)
NUM_OF_SCREENS = 3
BASE_FOLDER = Path()
#####


def loadAll(curToBlackList=False):
    global lastChangeTime
    lastChangeTime = time.time()
    myChanger.fullImageChange(NUM_OF_SCREENS, curToBlackList)
    refreshGui()

def loadNew(index, curToBlackList=False):
    myChanger.changeOne(index, curToBlackList)
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
    global cg, icon, userSettings
    if not cg:
        cg = GUI(icon, userSettings, loadNew, loadAll, onGuiClosed)
    if not cg.needSettings:
        cg.loadImages(myChanger.currentImages)
    cg.show()

icon = Path("icon/icon.png")
closing = False
lastChangeTime = 0
trayIcon:Tray = None
myChanger = Changer(BASE_FOLDER, MONITOR_SIZE)
cg:GUI = None
userSettings = UserSettings(BASE_FOLDER)

def main():
    global trayIcon, lastChangeTime, closing, userSettings, cg
    if not userSettings.getChangeInterval():
        openGui()
    if not userSettings.getChangeInterval():
        print("No user settings, can't initialize!")
        return
    # CREATE TRAY ICON
    trayIcon = Tray(icon, openGui, loadAll, close)
    trayIcon.start()
    # MAIN CHECK LOOP
    print("Go into main check loop")
    while not closing:
        if time.time() >= lastChangeTime + userSettings.getChangeInterval():
            loadAll()
        time.sleep(1)
    print("Closed")

main()