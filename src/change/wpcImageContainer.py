from pathlib import Path
from random import randint
from typing import List
from .wpcImage import WpcImage
import os


class WpcImageContainer:
    def __init__(self, imagesFolder) -> None:
        if isinstance(imagesFolder, str):
            imagesFolder = Path(imagesFolder)
        self.imagesFolder = imagesFolder
        # self.blackListFile = self.imagesFolder.joinpath(BLACKLIST_FILE_NAME)
        # self.blackList = []
        ### CREATE FOLDER IF NOT EXIST
        if not self.imagesFolder.exists():
            self.imagesFolder.mkdir()

    def getRandomImages(self, numOfImages:int, excludeImages:List[WpcImage]=None) -> List[WpcImage]:
        allImagePaths = self.__getAllImagePaths(self.__getExcludePathsStr(excludeImages))
        return self.__getRandomImages(allImagePaths, numOfImages)
    
    def __getRandomImages(self, imagePaths:List[str], numOfImages:int):
        randomImages = []
        for i in range(numOfImages):
            if len(imagePaths) == 0:
                break
            pickIndex = randint(0,len(imagePaths)-1)
            randomPath = imagePaths.pop(pickIndex)        
            randomImages.append(WpcImage.fromPath(randomPath))
        return randomImages
    
    def __getAllImagePaths(self, excludePaths:List[str]):
        allImagePaths = []
        for i in self.imagesFolder.iterdir():
            curPath = i.absolute().__str__()
            if i.is_file() and not self.__checkIfInExcludeList(curPath, excludePaths):
                allImagePaths.append(i)
        return allImagePaths
    
    def __checkIfInExcludeList(self, checkPath:str, excludePaths:List[str]):
        if not excludePaths:
            return False
        for blackListPath in excludePaths:
            if checkPath == blackListPath:
                return True
        return False
    
    def __getExcludePathsStr(self, excludeList:List[WpcImage]=None):
        if not excludeList:
            return None
        excludePaths = []
        for exImage in excludeList:
            if exImage and exImage.saveFolder:
                excludePaths.append(exImage.getFullPathStr())
        return excludePaths
    
    def add(self, image: WpcImage) -> bool:
        # if image.getFullName() in self.blackList:
        #     return False
        image.move(self.imagesFolder)
        return True

    def remove(self, image: WpcImage):
        if image.saveFolder != self.imagesFolder:
            return False
        os.remove(image.getFullPath())
        return True

    # def addToBlackList(self, image:WpcImage):
    #     self.blackList.append(image.getFullName())

    # def removeFromBlackList(self, image:WpcImage):
    #     self.blackList.pop(image.getFullName())