from .image import Image
from .imageUtil import checkIfImageAlreadyExist
from typing import List
import re
from web.webLoader import loadBytes, loadStr


WALLPAPER_CATALOG_PAGE = "https://wallpaperscraft.com/catalog/anime/"
DOMAIN = WALLPAPER_CATALOG_PAGE.split("/catalog")[0]

class ImageDler:
    def __init__(self, imageSize: Image.Size) -> None:
        self.imageSize = imageSize
        self.page = 1
        self.index = 0
        self.lastPage = self.__getLastPage()
        if not self.lastPage:
            print("Page currently scuffed or so...")

    def downloadImages(self, numOfImage) -> List[Image]:
        images = []
        if not self.lastPage:
            self.lastPage = self.__getLastPage()
        if not self.lastPage:
            print("Page currently scuffed or so...")
            return images
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
        if not self.lastPage:
            self.lastPage = self.__getLastPage()
        if not self.lastPage:
            print("Page currently scuffed or so...")
            return None
        fullImageName = None
        while not fullImageName:
            pageLink = self.__getPageLink()
            if not pageLink:
                return None
            images = self.__loadImageNamesFromLink(pageLink)
            if not images:
                print("Page currently scuffed or so...")
                break
            fullImageName = self.__getNextImageName(images)
            if not fullImageName:
                self.page += 1
        if not fullImageName:
            return None
        image = self.__downloadImageByFullName(fullImageName)
        return image

    def __downloadImageByFullName(self, fullImageName) -> Image:
        downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
        imageBytes = loadBytes(downloadLink)        
        if not imageBytes:
            print("__downloadImageByFullName: No or error response")
            return None
        image = Image()
        try:
            image.data = imageBytes
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
            fullImageName = f"{imageName}_{self.__getImageSizeStr()}.jpg"
            self.index += 1
        return fullImageName
    
    def __getPageLink(self) -> str:
        lastPage = self.__getLastPage()
        if not lastPage:
            return None
        if self.page > lastPage:
            self.page = 1
            self.index = 0
        pageLink = self.__getWallpaperPage()
        if self.page > 1:
            pageLink += f"/page{self.page}"
        return pageLink
    
    def __getLastPage(self) -> int:
        #### LOAD LINKS IN PAGE
        page = loadStr(self.__getWallpaperPage())
        if not page:
            print("Can't load wallpaper page...scuffed or so")
            return None
        lastPageSearch = self.__getWallpaperPage().replace(DOMAIN, "") + "/page([0-9]*)"
        matches = re.findall(lastPageSearch, page)
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
        page = loadStr(searchPage)
        if not page:
            print("__loadImagesFromLink: Failed response")
            return None
        imageSearch = f'/download/([^"/]*)/{self.__getImageSizeStr()}'
        matches = re.findall(imageSearch, page)
        if not matches or len(matches) == 0:
            print("__loadImagesFromLink: No matches")
            return None
        return matches
    
    def __getImageSizeStr(self) -> str:
        return f"{self.imageSize.width}x{self.imageSize.height}"
    
    def __getWallpaperPage(self) -> str:
        return f"{WALLPAPER_CATALOG_PAGE}{self.__getImageSizeStr()}"