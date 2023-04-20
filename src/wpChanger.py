from pathlib import Path
import ctypes

SPI_SETDESKWALLPAPER = 20

def setImageAsWallpaper(imagePath):
    path = imagePath
    if not isinstance(imagePath, Path):
        path = Path(imagePath)
    if not path.exists() or not path.is_file():
        print("No image found")
        return False
    print("Set image as wallpaper...")
    print("Full image path: " + imagePath.absolute().__str__())
    print(ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, imagePath.absolute().__str__() , 0))