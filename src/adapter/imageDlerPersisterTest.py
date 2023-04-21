from imageDlerPersister import addImageDler, loadImageDler
from ..persist.persister import Persister
from pathlib import Path
from ..img.imageDler import ImageDler
from ..img.image import Image

PERS_DATA_PATH = Path("./data.json")


### SAVE DATA
persister = Persister(PERS_DATA_PATH)
imgDler = ImageDler(Image.Size(1920, 1080))
img = imgDler.downloadImage()
print(img.getFullName())
addImageDler(imgDler, persister)
persister.save()
####
#### LOAD DATA
persister = Persister(PERS_DATA_PATH)
imgDler = loadImageDler(persister)
img = imgDler.downloadImage()
print(img.getFullName())