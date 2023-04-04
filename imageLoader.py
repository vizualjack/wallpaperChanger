import re
from re import Match
import requests
from pathlib import Path
from random import randint
import os


WALLPAPER_SIZE = "1920x1080"
WALLPAPER_PAGE = "https://wallpaperscraft.com/catalog/anime/" + WALLPAPER_SIZE
DOMAIN = WALLPAPER_PAGE.split("/catalog")[0]
BLACKLIST_FOLDER_NAME = "blackList"


class ImageLoader:
    def __init__(self, baseFolder:Path) -> None:
        self.baseFolder = baseFolder
        self.blackListFolder = baseFolder.joinpath(BLACKLIST_FOLDER_NAME)
        ### CREATE FOLDER IF NOT EXIST
        if not self.baseFolder.exists():
            self.baseFolder.mkdir()
        if not self.blackListFolder.exists():
            self.blackListFolder.mkdir()

        
    def downloadImages(self, numOfImage) -> list[Path]:
        images = []
        for i in range(numOfImage):
            images.append(self.downloadImage())
        print("Downloaded all images")
        return images


    def downloadImage(self):
        ## GET PAGES
        response = requests.get(WALLPAPER_PAGE)
        lastPageSearch = WALLPAPER_PAGE.replace(DOMAIN, "") + "/page([0-9]*)"
        matches = re.findall(lastPageSearch, response.text)
        if not matches:
            print("Found no pages")
        lastPage = self.__getLastPage(matches)
        fullImageName = None
        while not fullImageName:
            ## GET RANDOM IMAGE PAGE
            page = randint(1, lastPage)
            searchPage = f"{WALLPAPER_PAGE}/page{page}"
            ## LOAD IMAGES FROM ROLLED PAGE
            response = requests.get(searchPage)
            imageSearch = f'/download/([^"/]*)/{WALLPAPER_SIZE}'
            matches = re.findall(imageSearch, response.text)
            if not matches or len(matches) == 0:
                print("Found no images")        
            ## SEARCH FOR IMAGE THAT'S NOT BLACKLISTED AND ALREADY LOADED
            while len(matches) > 0 and not fullImageName:
                imageIndex = randint(0,len(matches)-1)
                imageName = matches.pop(imageIndex)
                fullImageName = f"{imageName}_{WALLPAPER_SIZE}.jpg"
                if self.__checkBlackList(fullImageName) or self.__checkImageFolder(fullImageName):
                    print("Image already exists")
                    fullImageName = None
        ## DOWNLOAD AND SAVING OF IMAGE
        downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
        response = requests.get(downloadLink)
        if not response:
            print("Can't load image")
        fullImagePath = self.baseFolder.joinpath(fullImageName)
        f = open(fullImagePath.__str__(), "wb")
        f.write(response.content)
        f.flush()
        f.close()
        print("Image downloaded")
        return fullImagePath


    def addToBlackList(self, image:Path):
        parent1 = self.blackListFolder.parent
        parent2 = image.parent
        if parent1.absolute().__str__() != parent2.absolute().__str__():
            print("Image is outside of my image folder")
        else:
            image.replace(self.blackListFolder.joinpath(image.name))


    def __checkBlackList(self, fullImageName):
        self.__checkFolderForItem(self.blackListFolder, fullImageName)

    
    def __checkImageFolder(self, fullImageName):
        self.__checkFolderForItem(self.baseFolder, fullImageName)
    

    def __checkFolderForItem(self, folder:Path, fullItemName):
        for file in folder.iterdir():
            if fullItemName == file.name:
                return True
        return False


    def __getLastPage(self, matches: list[Match]):
        lastPage = -1
        for match in matches:
            page = int(match)
            if page > lastPage:
                lastPage = page
        return lastPage