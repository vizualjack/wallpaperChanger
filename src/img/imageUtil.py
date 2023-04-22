from .image import Image
from typing import List

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