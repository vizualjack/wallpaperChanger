from change.wpcImage import WpcImage
from change.imageUtil import checkIfImageAlreadyExist
from typing import List
import re
from .loader import loadBytes, loadStr, loadMultipleBytes
from util.exceptionSaver import saveException
from change.screen import Screen
from change.wpcImageContainer import WpcImageContainer
from .imageDlerGUI import ImageDlerGUI


WALLPAPER_CATALOG_PAGE = "https://wallpaperscraft.com/catalog/anime/"
DOMAIN = WALLPAPER_CATALOG_PAGE.split("/catalog")[0]

class ImageDler:
    def __init__(self, imageContainer:WpcImageContainer, screens: List[Screen]) -> None:
        screen = screens[0]
        self.imageSize = WpcImage.Size(screen.width, screen.height)
        self.__imageContainer = imageContainer
        self.page = 1
        self.index = 0
        self.lastPage = self.__getLastPage()
        self.allPageImageNames = None
        self.__gui = None
        if not self.lastPage:
            print("Page currently scuffed or so...")

    def downloadImages(self, numOfImages) -> List[WpcImage]:
        imageNames = self.__getNextImageNames(numOfImages)
        links = self.__getLinksForImageNames(imageNames)
        images = []
        for loadResult in loadMultipleBytes(links):
            imageNameIndex = links.index(loadResult.link)
            imageName = imageNames[imageNameIndex]
            try:
                image = WpcImage()
                image.data = loadResult.result
                nameParts = imageName.split(".")
                image.name = nameParts[0]
                image.extension = nameParts[1]
                image.size = self.imageSize
                image.type = WpcImage.getTypeForExtension(image.extension)
                images.append(image)
                print("__downloadImageByFullName: Image downloaded and converted")
            except:
                additionalInfo = "ImageDler.downloadImages: Error on converting to an image\n"
                additionalInfo += f"link: {loadResult.link}"
                additionalInfo += f"size of result: {len(loadResult.result)}"
                saveException(additionalInfo)
        return images
    
    def openGui(self):
        if self.__gui:
            return
        self.__gui = ImageDlerGUI(self, self.__imageContainer)
        self.__gui.onClose = self.__onGuiClosed
        self.__gui.show()

    def stop(self):
        if self.__gui:
            self.__gui.close()

    def __onGuiClosed(self):
        self.__gui = None

    def __getNextImageNames(self, numOfImageNames:int):
        imageNames = []
        while len(imageNames) < numOfImageNames:
            ## make sure currentImageNames is filled
            if not self.allPageImageNames:
                pageLink = self.__getPageLink()
                if not pageLink:
                    print("page scuffed")
                    return imageNames
                self.allPageImageNames = self.__loadImageNamesFromLink(pageLink)
                if not self.allPageImageNames:
                    print("page scuffed")
                    return imageNames
            ## load image names from currentImageNames as long as possible
            while True:
                curImageName = self.__getNextImageName(self.allPageImageNames)
                if not curImageName:
                    self.page += 1
                    self.index = 0
                    self.allPageImageNames = None
                    break
                imageNames.append(curImageName)
                if len(imageNames) >= numOfImageNames:
                    break
        return imageNames
    
    def __getLinksForImageNames(self, imageNames:List[str]):
        links = []
        for imageName in imageNames:
            downloadLink = f"https://images.wallpaperscraft.com/image/single/{imageName}"
            links.append(downloadLink)
        return links

    def old_downloadImages(self, numOfImage) -> List[WpcImage]:
        images = []
        if not self.lastPage:
            self.lastPage = self.__getLastPage()
        if not self.lastPage:
            print("Page currently scuffed or so...")
            return images
        for i in range(numOfImage):
            image = None
            while not image:
                image = self.__downloadImage()
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

    def __downloadImage(self) -> WpcImage:
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

    def __downloadImageByFullName(self, fullImageName) -> WpcImage:
        downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
        imageBytes = loadBytes(downloadLink)        
        if not imageBytes:
            print("__downloadImageByFullName: No or error response")
            return None
        image = WpcImage()
        try:
            image.data = imageBytes
            nameParts = fullImageName.split(".")
            image.name = nameParts[0]
            image.extension = nameParts[1]
            image.size = self.imageSize
            image.type = WpcImage.getTypeForExtension(image.extension)
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

    __KEY_INDEX = "index"
    __KEY_PAGE = "page"
    def getSaveDataJson(self):
        data = {}
        data[self.__KEY_INDEX] = self.index
        data[self.__KEY_PAGE] = self.page
        return data

    def loadFromJson(self, data):
        self.index = data[self.__KEY_INDEX]
        self.page = data[self.__KEY_PAGE]