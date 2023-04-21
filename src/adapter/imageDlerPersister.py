from ..img.imageDler import ImageDler
from ..img.image import Image
from ..persist.persister import Persister

PERS_KEY = "imageDler"
INDEX_KEY = "index"
PAGE_KEY = "page"
WIDTH_KEY = "width"
HEIGHT_KEY = "height"

def addImageDler(imageDler: ImageDler, persister:Persister):
    saveData = {}
    saveData[PAGE_KEY] = imageDler.page
    saveData[INDEX_KEY] = imageDler.index
    saveData[WIDTH_KEY] = imageDler.imageSize.width
    saveData[HEIGHT_KEY] = imageDler.imageSize.height
    persister.setData(PERS_KEY, saveData)

def loadImageDler(persister:Persister) -> ImageDler | None:
    saveData = persister.getData(PERS_KEY)
    if saveData is None:
        return None
    imageDler = ImageDler(Image.Size(saveData[WIDTH_KEY], saveData[HEIGHT_KEY]))
    imageDler.page = saveData[PAGE_KEY]
    imageDler.index = saveData[INDEX_KEY]
    return imageDler