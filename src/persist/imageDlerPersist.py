from persist.persister import Persister
from img.imageDler import ImageDler
from img.image import Image

__SAVE_KEY = "imageDler"
__INDEX_KEY = "index"
__PAGE_KEY = "page"
__WIDTH_KEY = "width"
__HEIGHT_KEY = "height"

def addToPersister(persister:Persister, imgDler: ImageDler):
    dataDict = {}
    dataDict[__INDEX_KEY] = imgDler.index
    dataDict[__PAGE_KEY] = imgDler.page
    dataDict[__WIDTH_KEY] = imgDler.imageSize.width
    dataDict[__HEIGHT_KEY] = imgDler.imageSize.height
    persister.setData(__SAVE_KEY, dataDict)

def loadFromPersister(persister:Persister) -> ImageDler | None:
    dataDict = persister.getData(__SAVE_KEY)
    if not dataDict:
        return None
    imgDler = ImageDler(Image.Size(dataDict[__WIDTH_KEY], dataDict[__HEIGHT_KEY]))
    imgDler.index = dataDict[__INDEX_KEY]
    imgDler.page = dataDict[__PAGE_KEY]
    return imgDler