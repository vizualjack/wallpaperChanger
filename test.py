from imageTank import ImageTank
from screenSize import ScreenSize
from pathlib import Path

##### SETTINGS
MONITOR_SIZE = ScreenSize(1920,1080)
NUM_OF_SCREENS = 3
BASE_FOLDER = Path()
#####

imageTank = ImageTank(BASE_FOLDER, MONITOR_SIZE)
imageTank.downloadImages(NUM_OF_SCREENS)