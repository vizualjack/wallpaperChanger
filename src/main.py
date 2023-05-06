########## BUILD LINE
# pyinstaller src/main.py --name "Wallpaper Changer" --icon=res/icon.ico --add-data "res/;res/" --noconsole    # doesnt work yet --onefile 
############

from wpc import Wpc

wpChanger = Wpc()
wpChanger.start()