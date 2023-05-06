from .wpcImage import WpcImage
from typing import List
from PIL import Image

def getImageWithHighestHeight(images: List[WpcImage]):
    highestHeightImage = None
    for image in images:
        if highestHeightImage is None:
            highestHeightImage = image
        if image.size.height > highestHeightImage.size.height:
            highestHeightImage = image
    return highestHeightImage

def getImageWithHighestWidth(images: List[WpcImage]):
    highestWidthImage = None
    for image in images:
        if highestWidthImage is None:
            highestWidthImage = image
        if image.size.width > highestWidthImage.size.width:
            highestWidthImage = image
    return highestWidthImage

def getImagesWidthSum(images: List[WpcImage]):
    width = 0
    for image in images:
        width += image.size.width
    return width

def checkIfImageAlreadyExist(newImage:Image, images:List[WpcImage]):
    for image in images:
        if image.getFullName() == newImage.getFullName():
            return True
    return False