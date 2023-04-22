from PIL import Image as PILImage
from typing import List
from image import Image
from imageUtil import getImageWithHighestHeight, getImagesWidthSum


class ImageOperator:
    @staticmethod
    def mergeImagesHorizontal(images: List[Image]) -> Image:
        height = getImageWithHighestHeight(images)
        mergedImage = PILImage.new("RGB", (getImagesWidthSum(images),height))
        startPos = 0
        for image in images:
            mergedImage.paste(PILImage.open(image.data), [startPos,0])
            startPos += image.size.width
        return mergedImage