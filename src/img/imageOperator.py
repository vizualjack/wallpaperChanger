from PIL import Image as PILImage
from typing import List
from .image import Image
from .imageUtil import getImageWithHighestHeight, getImagesWidthSum
import io


class ImageOperator:
    @staticmethod
    def mergeImagesHorizontal(images: List[Image]) -> Image:
        highestHeightImage = getImageWithHighestHeight(images)
        widthSum = getImagesWidthSum(images)
        mergedPILImage = PILImage.new("RGB", (widthSum, highestHeightImage.size.height))
        startPos = 0
        for image in images:
            # PILImage.frombytes(data=image.data)
            # pilImageFromImage = PILImage.frombytes("RGB", (image.size.width, image.size.height), image.data)
            pilImageFromImage = PILImage.open(image.getFullPath())
            mergedPILImage.paste(pilImageFromImage, [startPos,0])
            startPos += image.size.width
        mergedImage = Image()
        bytesIO = io.BytesIO()
        mergedImage.extension = images[0].extension
        mergedPILImage.save(bytesIO, PILImage.EXTENSION["." + mergedImage.extension])
        mergedImage.data = bytesIO.getvalue()
        mergedImage.type = images[0].type
        mergedImage.name = "merged"
        mergedImage.size = Image.Size(widthSum, highestHeightImage)
        return mergedImage