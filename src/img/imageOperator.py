from PIL import Image as PILImage
from typing import List
from .image import Image
from .imageUtil import getImageWithHighestHeight, getImagesWidthSum


class ImageOperator:
    @staticmethod
    def mergeImagesHorizontal(images: List[Image]) -> Image:
        highestHeightImage = getImageWithHighestHeight(images)
        mergedPILImage = PILImage.new("RGB", (getImagesWidthSum(images), highestHeightImage.size.height))
        startPos = 0
        for image in images:
            # PILImage.frombytes(data=image.data)
            # pilImageFromImage = PILImage.frombytes("RGB", (image.size.width, image.size.height), image.data)
            pilImageFromImage = PILImage.open(image.getFullPath())
            mergedPILImage.paste(pilImageFromImage, [startPos,0])            
            startPos += image.size.width
        mergedPILImage.save("test.jpg")
        mergedImage = Image()
        mergedImage.data = mergedPILImage.tobytes()
        mergedImage.extension = images[0].extension
        mergedImage.type = images[0].type
        mergedImage.name = "merged"
        return mergedImage