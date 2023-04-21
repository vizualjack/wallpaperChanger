from image import Image
from imageUtil import checkIfImageAlreadyExist
from typing import List
import re
import requests


WALLPAPER_CATALOG_PAGE = "https://wallpaperscraft.com/catalog/anime/"
DOMAIN = WALLPAPER_CATALOG_PAGE.split("/catalog")[0]

class ImageDler:
    def __init__(self, imageSize: Image.Size) -> None:
        self.imageSize = imageSize
        self.imageSizeStr = f"{self.imageSize.width}x{self.imageSize.height}"
        self.wallpaperPage = f"{WALLPAPER_CATALOG_PAGE}{self.imageSizeStr}"
        self.page = 1
        self.index = 0

    def downloadImages(self, numOfImage) -> List[Image]:
        images = []
        for i in range(numOfImage):
            image = None
            while not image:
                image = self.downloadImage()
                if not image:
                    break
                if checkIfImageAlreadyExist(image, images):
                    image = None
            if image:
                images.append(image)
        print("downloadImages: Images downloaded")
        if numOfImage > len(images):
            print("downloadImages: Not enough images")
        return images

    def downloadImage(self) -> Image:
        fullImageName = None
        while not fullImageName:
            pageLink = self.__getPageLink()
            if not pageLink:
                return None
            images = self.__loadImageNamesFromLink(pageLink)
            fullImageName = self.__getNextImageName(images)
            if not fullImageName:
                self.page += 1
        if not fullImageName:
            return None
        image = self.__downloadImageByFullName(fullImageName)
        return image

    def __downloadImageByFullName(self, fullImageName) -> Image:
        downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
        response = requests.get(downloadLink)
        if not response:
            print("__downloadImageByFullName: No or error response")
            return None
        image = Image()
        try:
            image.data = response.content
            nameParts = fullImageName.split(".")
            image.name = nameParts[0]
            image.extension = nameParts[1]
            image.size = self.imageSize
            image.type = Image.getTypeForExtension(image.extension)
            print("__downloadImageByFullName: Image downloaded")
        except Exception as ex:
            print("__downloadImageByFullName: Got an error")
            print(ex)
            print(ex.with_traceback())
            image = None
        return image

    def __getNextImageName(self, imagesNames: List[str]) -> str:
        fullImageName = None
        while not fullImageName:
            if self.index >= len(imagesNames):
                return None
            imageName = imagesNames[self.index]
            fullImageName = f"{imageName}_{self.imageSizeStr}.jpg"
            self.index += 1
        return fullImageName
    
    def __getPageLink(self) -> str:
        lastPage = self.__getLastPage()
        if not lastPage:
            return None
        if self.page > lastPage:
            self.page = 1
            self.index = 0
        return f"{self.wallpaperPage}/page{self.page}"
    
    def __getLastPage(self) -> int:
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

    def __loadImageNamesFromLink(self, searchPage) -> List[str]:
        response = requests.get(searchPage)
        if not response:
            print("__loadImagesFromLink: Got no response")
            return None
        imageSearch = f'/download/([^"/]*)/{self.imageSizeStr}'
        matches = re.findall(imageSearch, response.text)
        if not matches or len(matches) == 0:
            print("__loadImagesFromLink: No matches")
            return None
        return matches


############ SHOULD HANDLE WHERE ELSE
    # class LoadPosition:
    #     _POSITION_SAVE_NAME = "loaderPos.json"
    #     _KEY_PAGE = "page"
    #     _KEY_IMAGE_INDEX = "imageIndex"
    #     def __init__(self, baseFolder:Path) -> None:
    #         self.savePath = baseFolder.joinpath(self._POSITION_SAVE_NAME)
    #         self.data = {}
    #         self.data[self._KEY_PAGE] = 1
    #         self.data[self._KEY_IMAGE_INDEX] = 0
    #         self.load()

    #     def getPage(self):
    #         return self.data[self._KEY_PAGE]
        
    #     def getImageIndex(self):
    #         return self.data[self._KEY_IMAGE_INDEX]
        
    #     def nextPage(self):
    #         self.data[self._KEY_PAGE] = self.data[self._KEY_PAGE] + 1
    #         self.data[self._KEY_IMAGE_INDEX] = 0

    #     def nextIndex(self):
    #         self.data[self._KEY_IMAGE_INDEX] = self.data[self._KEY_IMAGE_INDEX] + 1

    #     def setPos(self, page, imageIndex):
    #         self.data[self._KEY_PAGE] = page
    #         self.data[self._KEY_IMAGE_INDEX] = imageIndex
    # ######## POS CLASS #######