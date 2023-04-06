import re
from re import Match
import requests
from pathlib import Path
from random import randint
import os
import json
from typing import List
from screenSize import ScreenSize


WALLPAPER_CATALOG_PAGE = "https://wallpaperscraft.com/catalog/anime/"
DOMAIN = WALLPAPER_CATALOG_PAGE.split("/catalog")[0]
BLACKLIST_FOLDER_NAME = "blackList"
IMAGES_FOLDER_NAME = "images"


class ImageTank:
    class LoadPosition:
        _POSITION_SAVE_NAME = "loaderPos.json"
        _KEY_PAGE = "page"
        _KEY_IMAGE_INDEX = "imageIndex"
        def __init__(self, baseFolder:Path) -> None:
            self.savePath = baseFolder.joinpath(self._POSITION_SAVE_NAME)
            self.data = {}
            self.data[self._KEY_PAGE] = 1
            self.data[self._KEY_IMAGE_INDEX] = 0
            self.load()

        def getPage(self):
            return self.data[self._KEY_PAGE]
        
        def getImageIndex(self):
            return self.data[self._KEY_IMAGE_INDEX]
        
        def nextPage(self):
            self.data[self._KEY_PAGE] = self.data[self._KEY_PAGE] + 1
            self.data[self._KEY_IMAGE_INDEX] = 0

        def nextIndex(self):
            self.data[self._KEY_IMAGE_INDEX] = self.data[self._KEY_IMAGE_INDEX] + 1

        def setPos(self, page, imageIndex):
            self.data[self._KEY_PAGE] = page
            self.data[self._KEY_IMAGE_INDEX] = imageIndex

        def load(self):
            if not self.savePath.exists():
                return
            f = open(self.savePath.absolute().__str__())
            self.data = json.loads(f.read())
            f.close()

        def save(self):
            f = open(self.savePath.absolute().__str__(), "w")
            f.write(json.dumps(self.data))
            f.flush()
            f.close()
    ######## POS CLASS #######

    def __init__(self, baseFolder:Path, screenSize: ScreenSize) -> None:
        self.baseFolder = baseFolder
        self.imagesFolder = baseFolder.joinpath(IMAGES_FOLDER_NAME)
        self.blackListFolder = self.imagesFolder.joinpath(BLACKLIST_FOLDER_NAME)
        self.position = self.LoadPosition(baseFolder)
        self.screenSizeStr = f"{screenSize.width}x{screenSize.height}"
        self.wallpaperPage = f"{WALLPAPER_CATALOG_PAGE}{self.screenSizeStr}"
        ### CREATE FOLDER IF NOT EXIST
        if not self.imagesFolder.exists():
            self.imagesFolder.mkdir()
        if not self.blackListFolder.exists():
            self.blackListFolder.mkdir()

    def getImages(self, numOfImages):
        imagePaths = self.downloadImages(numOfImages)
        neededRest = numOfImages - len(imagePaths)
        if neededRest > 0:
            self.currentImages.extend(self.getRandomImages(neededRest))

    def getRandomImages(self, numOfImages) -> List[Path]:
        allImages = []
        for i in self.imagesFolder.iterdir():
            if i.is_file():
                allImages.append(i)
        images = []
        for i in range(numOfImages):
            if len(allImages) == 0:
                break
            pickIndex = randint(0,len(allImages)-1)
            images.append(allImages.pop(pickIndex))
        return images
        
    def downloadImages(self, numOfImage) -> List[Path]:
        images = []
        for i in range(numOfImage):
            image = self.downloadImage()
            if image:
                images.append(image)
        print("downloadImages: Images downloaded")
        if numOfImage > len(images):
            print("downloadImages: Not enough images")
        return images

    def downloadImage(self):
        fullImageName = None
        while not fullImageName:
            pageLink = self.__getPageLink()
            if not pageLink:
                return None
            images = self.__loadImageNamesFromLink(pageLink)
            fullImageName = self.__getNextImageName(images)
            if not fullImageName:
                self.position.nextPage()
        if not fullImageName:
            return None
        fullImagePath = self.__downloadImageByFullName(fullImageName)
        self.position.save()
        return fullImagePath
    
    def addToBlackList(self, image:Path):
        parent1 = self.blackListFolder.parent
        parent2 = image.parent
        if parent1.absolute().__str__() != parent2.absolute().__str__():
            print("Image is outside of my image folder")
        else:
            image.replace(self.blackListFolder.joinpath(image.name))
    
    def __downloadImageByFullName(self,fullImageName):
        downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
        response = requests.get(downloadLink)
        if not response:
            print("__downloadImageByFullName: No or error response")
            return None
        fullImagePath = self.imagesFolder.joinpath(fullImageName)
        try:
            f = open(fullImagePath.__str__(), "wb")
            f.write(response.content)
            f.flush()
            f.close()
            print("__downloadImageByFullName: Image downloaded")
        except:
            print("__downloadImageByFullName: Can't save image")
            fullImagePath = None
        return fullImagePath

    def __getNextImageName(self, imagesNames: List[str]):
        fullImageName = None
        while not fullImageName:
            imageIndex = self.position.getImageIndex()
            if imageIndex >= len(imagesNames):
                return None
            imageName = imagesNames[imageIndex]
            fullImageName = f"{imageName}_{self.screenSizeStr}.jpg"
            self.position.nextIndex()
            if self.__checkBlackList(fullImageName) or self.__checkImageFolder(fullImageName):
                print("Image already exists")
                fullImageName = None
        return fullImageName
    
    def __getPageLink(self):
        lastPage = self.__getLastPage()
        if not lastPage:
            return None
        page = self.position.getPage()
        if page > lastPage:
            return None
        return f"{self.wallpaperPage}/page{page}"

    def __loadImageNamesFromLink(self, searchPage):
        response = requests.get(searchPage)
        if not response:
            print("__loadImagesFromLink: Got no response")
            return None
        imageSearch = f'/download/([^"/]*)/{self.screenSizeStr}'
        matches = re.findall(imageSearch, response.text)
        if not matches or len(matches) == 0:
            print("__loadImagesFromLink: No matches")
            return None
        return matches

    def __checkBlackList(self, fullImageName):
        self.__checkFolderForItem(self.blackListFolder, fullImageName)
    
    def __checkImageFolder(self, fullImageName):
        self.__checkFolderForItem(self.imagesFolder, fullImageName)    

    def __checkFolderForItem(self, folder:Path, fullItemName):
        for file in folder.iterdir():
            if fullItemName == file.name:
                return True
        return False

    def __getLastPage(self):
        #### LOAD LINKS IN PAGE
        response = requests.get(self.wallpaperPage)
        lastPageSearch = self.wallpaperPage.replace(DOMAIN, "") + "/page([0-9]*)"
        matches = re.findall(lastPageSearch, response.text)
        if not matches:
            print("Found no pages")
            return None
        #### SEARCH FOR HIGHEST
        lastPage = -1
        for match in matches:
            page = int(match)
            if page > lastPage:
                lastPage = page
        return lastPage