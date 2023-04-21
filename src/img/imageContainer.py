from pathlib import Path
from random import randint
from typing import List
from image import Image



BLACKLIST_FOLDER_NAME = "blackList"

class ImageContainer:
    def __init__(self, imagesFolder) -> None:
        if isinstance(imagesFolder, str):
            imagesFolder = Path(imagesFolder)
        self.imagesFolder = imagesFolder
        self.blackListFolder = self.imagesFolder.joinpath(BLACKLIST_FOLDER_NAME)
        ### CREATE FOLDER IF NOT EXIST
        if not self.imagesFolder.exists():
            self.imagesFolder.mkdir()
        if not self.blackListFolder.exists():
            self.blackListFolder.mkdir()

    def getRandomImages(self, numOfImages) -> List[Image]:
        allImages = []
        for i in self.imagesFolder.iterdir():
            if i.is_file():
                allImages.append(i)
        randomImagePaths = []
        for i in range(numOfImages):
            if len(allImages) == 0:
                break
            pickIndex = randint(0,len(allImages)-1)
            randomImagePaths.append(allImages.pop(pickIndex))
        images = []
        for imagePath in randomImagePaths:
            images.append(Image.fromPath(imagePath))
        return images
    
    def addToBlackList(self, image:Image):
        image.move(self.blackListFolder)

    def add(self, image: Image):
        image.move(self.imagesFolder)


    
    # def __checkBlackList(self, fullImageName):
    #     self.__checkFolderForItem(self.blackListFolder, fullImageName)
    
    # def __checkImageFolder(self, fullImageName):
    #     self.__checkFolderForItem(self.imagesFolder, fullImageName)    

    # def __checkFolderForItem(self, folder:Path, fullItemName):
    #     for file in folder.iterdir():
    #         if fullItemName == file.name:
    #             return True
    #     return False

