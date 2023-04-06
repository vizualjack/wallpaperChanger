from PIL import Image
from pathlib import Path
from random import randint
from uuid import uuid4
from typing import List


def mergeRandomImagesInFolder(savePath, imagesPath, numOfImages) -> Path:
    path = imagesPath
    if not isinstance(path, Path):
        path = Path(imagesPath)    
    images = pickImages(path, numOfImages)
    if len(images) < numOfImages:
        print("There are not enough images")
    return mergeImages(savePath, images)


def mergeImages(savePath, images: List[Path]):
    path = savePath
    if not isinstance(path, Path):
        path = Path(path)
    mergedImage = Image.new("RGB", (1920*len(images),1080))
    for i in range(len(images)):
        image = images[i]
        mergedImage.paste(Image.open(image.absolute().__str__()), [1920*i,0])
    mergedImagePath = Path(path.__str__() + ".jpg") #path.joinpath(f"{uuid4().__str__()}")
    mergedImage.save(mergedImagePath)
    return mergedImagePath


def pickImages(imageFolder: Path, numOfImages) -> List[Path]:
    allImages = []
    for i in imageFolder.iterdir():
        if i.is_file():
            allImages.append(i)
    images = []
    for i in range(numOfImages):
        if len(allImages) == 0:
            break
        pickIndex = randint(0,len(allImages)-1)
        images.append(allImages.pop(pickIndex))
    return images