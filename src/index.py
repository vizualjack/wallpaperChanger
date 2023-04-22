# from trayIcon.tray import Tray, TrayItem
# from pathlib import Path
# from gui.settingsGUI import SettingsGUI
# from saveData import SaveData

# def onSettingsGuiClosed():
#     global saveData
#     print("I could close it :D")
#     print(saveData.getHeight())

# iconPath = Path("src/icon/icon.png")
# saveData = SaveData()
# print(saveData.getHeight())
# settingsGUI = SettingsGUI(iconPath, saveData)
# settingsGUI.onClose = onSettingsGuiClosed
# settingsGUI.show()

from wallpaperChanger import WallpaperChanger

wpChanger = WallpaperChanger()
wpChanger.run()