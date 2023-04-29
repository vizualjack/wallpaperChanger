from .image import Image
from typing import List
from PIL import Image as PILImage
from io import BytesIO

def getImageWithHighestHeight(images: List[Image]):
    highestHeightImage = None
    for image in images:
        if highestHeightImage is None:
            highestHeightImage = image
        if image.size.height > highestHeightImage.size.height:
            highestHeightImage = image
    return highestHeightImage

def getImageWithHighestWidth(images: List[Image]):
    highestWidthImage = None
    for image in images:
        if highestWidthImage is None:
            highestWidthImage = image
        if image.size.width > highestWidthImage.size.width:
            highestWidthImage = image
    return highestWidthImage

def getImagesWidthSum(images: List[Image]):
    width = 0
    for image in images:
        width += image.size.width
    return width

def checkIfImageAlreadyExist(newImage:Image, images:List[Image]):
    for image in images:
        if image.getFullName() == newImage.getFullName():
            return True
    return False


def loadPILImage(imageName:str, imageBytes:bytes) -> PILImage:
    formats = PILImage.ID
    fp = BytesIO(imageBytes)
    prefix = fp.read(16)
    PILImage.preinit()
    def _open_core(fp, filename, prefix, formats):
        for i in formats:
            i = i.upper()
            if i not in PILImage.OPEN:
                PILImage.init()
            try:
                factory, accept = PILImage.OPEN[i]
                result = not accept or accept(prefix)
                if result:
                    fp.seek(0)
                    im = factory(fp, filename)
                    PILImage._decompression_bomb_check(im.size)
                    return im
            except (SyntaxError, IndexError, TypeError):
                continue
            except BaseException:
                fp.close()
                raise
        return None
    im = _open_core(fp, imageName, prefix, formats)
    if im:
        im._exclusive_fp = True
        return im
    return None