from .persister import Persister
# from ..img.imageContainer import ImageContainer
from img.imageContainer import ImageContainer

__SAVE_KEY = "imageContainer"
__BLACKLIST_KEY = "blackList"
__IMAGEFOLDER_KEY = "imageFolder"

def addToPersister(persister:Persister, imageContainer: ImageContainer):
    dataDict = {}
    dataDict[__BLACKLIST_KEY] = imageContainer.blackList
    dataDict[__IMAGEFOLDER_KEY] = imageContainer.imagesFolder.__str__()
    persister.setData(__SAVE_KEY, dataDict)

def loadFromPersister(persister:Persister) -> ImageContainer | None:
    dataDict = persister.getData(__SAVE_KEY)
    if not dataDict:
        return None
    imageContainer = ImageContainer(dataDict[__IMAGEFOLDER_KEY])
    imageContainer.blackList = dataDict[__BLACKLIST_KEY]
    return imageContainer