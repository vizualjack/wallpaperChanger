from pathlib import Path
from imageLoader import downloadImages
from imageEditer import mergeImages, mergeRandomImagesInFolder
from wpChanger import setImageAsWallpaper


NUM_OF_SCREENS = 3
IMAGES_FOLDER = Path("images")
WP_FOLDER = Path("wps")
dlImages = downloadImages(IMAGES_FOLDER, 3)
mergedImage = mergeImages(WP_FOLDER, dlImages)
setImageAsWallpaper(mergedImage)