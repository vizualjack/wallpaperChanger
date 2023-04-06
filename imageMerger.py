from PIL import Image
from pathlib import Path
from random import randint
from uuid import uuid4
from typing import List
from screenSize import ScreenSize


def mergeImages(savePath, images: List[Path], screenSize:ScreenSize):
    path = savePath
    if not isinstance(path, Path):
        path = Path(path)
    mergedImage = Image.new("RGB", (screenSize.width*len(images),screenSize.height))
    for i in range(len(images)):
        image = images[i]
        mergedImage.paste(Image.open(image.absolute().__str__()), [screenSize.width*i,0])
    mergedImagePath = Path(path.__str__() + ".jpg") #path.joinpath(f"{uuid4().__str__()}")
    mergedImage.save(mergedImagePath)
    return mergedImagePath

# def mergeRandomImagesInFolder(savePath, imagesPath, numOfImages) -> Path:
#     path = imagesPath
#     if not isinstance(path, Path):
#         path = Path(imagesPath)    
#     images = pickImages(path, numOfImages)
#     if len(images) < numOfImages:
#         print("There are not enough images")
#     return mergeImages(savePath, images)