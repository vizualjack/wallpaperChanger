import re
from re import Match
import requests
from pathlib import Path
from random import randint

WALLPAPER_SIZE = "1920x1080"
WALLPAPER_PAGE = "https://wallpaperscraft.com/catalog/anime/" + WALLPAPER_SIZE
DOMAIN = WALLPAPER_PAGE.split("/catalog")[0]



def downloadImages(savePath, numOfImage) -> list[Path]:
    images = []
    for i in range(numOfImage):
        images.append(downloadImage(savePath))
    print("Downloaded all images")
    return images


def downloadImage(savePath):
    path = savePath
    if not isinstance(path, Path):
        path = Path(savePath)
    if not path.exists():
        path.mkdir()
    response = requests.get(WALLPAPER_PAGE)
    lastPageSearch = WALLPAPER_PAGE.replace(DOMAIN, "") + "/page([0-9]*)"
    matches = re.findall(lastPageSearch, response.text)
    if not matches:
        print("Found no pages")
    lastPage = __getLastPage(matches)
    page = randint(1, lastPage)
    searchPage = f"{WALLPAPER_PAGE}/page{page}"
    response = requests.get(searchPage)
    imageSearch = f'/download/([^"/]*)/{WALLPAPER_SIZE}'
    matches = re.findall(imageSearch, response.text)
    if not matches or len(matches) == 0:
        print("Found no images")
    imageIndex = randint(0,len(matches)-1)
    imageName = matches[imageIndex]
    fullImageName = f"{imageName}_{WALLPAPER_SIZE}.jpg"
    downloadLink = f"https://images.wallpaperscraft.com/image/single/{fullImageName}"
    response = requests.get(downloadLink)
    if not response:
        print("Can't load image")
    fullImagePath = path.joinpath(fullImageName)
    f = open(fullImagePath.__str__(), "wb")
    f.write(response.content)
    f.flush()
    f.close()
    print("Image downloaded")
    return fullImagePath


def __getLastPage(matches: list[Match]):
    lastPage = -1
    for match in matches:
        page = int(match)
        if page > lastPage:
            lastPage = page
    return lastPage