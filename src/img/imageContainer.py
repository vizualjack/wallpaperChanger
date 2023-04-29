from pathlib import Path
from random import randint
from typing import List
from .image import Image
import os


class ImageContainer:
    def __init__(self, imagesFolder) -> None:
        if isinstance(imagesFolder, str):
            imagesFolder = Path(imagesFolder)
        self.imagesFolder = imagesFolder
        # self.blackListFile = self.imagesFolder.joinpath(BLACKLIST_FILE_NAME)
        self.blackList = []
        ### CREATE FOLDER IF NOT EXIST
        if not self.imagesFolder.exists():
            self.imagesFolder.mkdir()

    def getRandomImages(self, numOfImages, blackList:List[Image]=None) -> List[Image]:
        allImages = []
        blackListPathsStr = self.__getBlackListAbsolutePathStr(blackList)
        for i in self.imagesFolder.iterdir():
            curAbsolutePathStr = i.absolute().__str__()
            if i.is_file() and not self.__checkIfInBlackList(curAbsolutePathStr, blackListPathsStr):
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
    
    def __checkIfInBlackList(self, absolutePath:str, blackListPathsStr:List[str]):
        if not blackListPathsStr:
            return False
        for blackListPath in blackListPathsStr:
            if absolutePath == blackListPath:
                return True
        return False
    
    def __getBlackListAbsolutePathStr(self, blackList:List[Image]=None):
        if not blackList:
            return None
        blackListPathsStr = []
        for blImage in blackList:
            if blImage and blImage.saveFolder:
                blackListPathsStr.append(blImage.getFullPathStr())
        return blackListPathsStr
    
    def add(self, image: Image) -> bool:
        if image.getFullName() in self.blackList:
            return False
        image.move(self.imagesFolder)
        return True

    def remove(self, image: Image):
        if image.saveFolder != self.imagesFolder:
            return False
        os.remove(image.getFullPath())
        return True

    def addToBlackList(self, image:Image):
        self.blackList.append(image.getFullName())

    def removeFromBlackList(self, image:Image):
        self.blackList.pop(image.getFullName())