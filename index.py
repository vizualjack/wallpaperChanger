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
from typing import List


##### APP SETTINGS
BASE_FOLDER = Path()
#####
class ChangeInfo:
    def __init__(self, index, curToBlackList) -> None:
        self.index = index
        self.curToBlackList = curToBlackList


def loadAll(curToBlackList=False):
    global changeAll, toBlackList
    changeAll = True
    toBlackList = curToBlackList

def loadNew(index, curToBlackList=False):
    changeInfos.append(ChangeInfo(index, curToBlackList))

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
cg:GUI = None
userSettings = UserSettings(BASE_FOLDER)
myChanger:Changer = None
# NEXT CHANGE DATA
changeInfos:List[ChangeInfo] = []
changeAll = False
toBlackList = False

def main():
    global trayIcon, lastChangeTime, closing, userSettings, cg, myChanger, changeAll, toBlackList, changeInfos
    if not userSettings.getChangeInterval():
        openGui()
    if not userSettings.getChangeInterval():
        print("No user settings, can't initialize!")
        return
    # Changer init
    myChanger = Changer(BASE_FOLDER, userSettings.getMonitorSize())
    # CREATE TRAY ICON
    trayIcon = Tray(icon, openGui, loadAll, close)
    trayIcon.start()
    # MAIN CHECK LOOP
    print("Go into main check loop")
    while not closing:
        # CHECK AND DO CHANGE
        if len(changeInfos) > 0 or changeAll:
            if changeAll:
                myChanger.fullImageChange(userSettings.getNumOfScreens(), toBlackList)
                changeInfos.clear()
            for changeInfo in changeInfos:
                myChanger.changeOne(changeInfo.index, changeInfo.curToBlackList)
            changeInfos.clear()
            refreshGui()
            global lastChangeTime
            lastChangeTime = time.time()
            changeAll = False
        ## FULL CHANGE CHECK
        if time.time() >= lastChangeTime + userSettings.getChangeInterval():
            loadAll()
        time.sleep(1)
    print("Closed")

main()