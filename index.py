########## BUILD LINE
# pyinstaller index.py --name "Wallpaper Changer" --icon=icon/icon.ico --add-data "icon/;icon/" --noconsole    # doesnt work yet --onefile 
############
from pathlib import Path
import time
from changer import Changer
import tkinter
from gui import ChangeGui
from tray import Tray
from settings import Settings



##### SETTINGS
MONITOR_SIZE = "1920x1080"
NUM_OF_SCREENS = 3
IMAGES_FOLDER_PATH = Path("images")
WP_PATH = Path("wp")
#####


#####
KEY_CHANGEINTERVAL = "changeIntervalSecs"
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

def onChangeInterval(newIntervalInSeconds):
    global secs_changeInterval
    secs_changeInterval = newIntervalInSeconds
    settings.setData(KEY_CHANGEINTERVAL, secs_changeInterval)
    settings.save()

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
    global cg, icon
    if not cg:
        cg = ChangeGui(icon, NUM_OF_SCREENS, loadNew, loadAll, onGuiClosed, onChangeInterval)
    cg.loadImages(myChanger.currentImages)
    cg.show()

icon = Path("icon/icon.png")
closing = False
lastChangeTime = 0
trayIcon:Tray = None
myChanger = Changer(IMAGES_FOLDER_PATH, WP_PATH)
cg:ChangeGui = None
settings = Settings(Path("."))
secs_changeInterval = settings.getData(KEY_CHANGEINTERVAL)
if not secs_changeInterval:
    onChangeInterval(60*60)
    print("Set default interval")

def main():
    global trayIcon, lastChangeTime, closing
    # CREATE TRAY ICON
    trayIcon = Tray(icon, openGui, loadAll, close)
    trayIcon.start()
    # MAIN CHECK LOOP
    print("Go into main check loop")
    while not closing:
        if time.time() >= lastChangeTime + secs_changeInterval:
            loadAll()
        time.sleep(1)
    print("Closed")

main()