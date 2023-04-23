########## BUILD LINE
# pyinstaller src/index.py --name "Wallpaper Changer" --icon=src/icon/icon.ico --add-data "src/icon/;src/icon/" --noconsole    # doesnt work yet --onefile 
############

from wallpaperChanger import WallpaperChanger

wpChanger = WallpaperChanger()
wpChanger.run()