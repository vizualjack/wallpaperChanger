from typing import List, Tuple
from .webLoaderThreads import WebLoaderThreadBytes, WebLoaderThreadStr
import requests


__USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"


def loadBytes(link:str) -> bytes:
    response = requests.get(link, headers={"User-Agent": __USER_AGENT})
    if not response:
        print("loadBytes: failed...")
        return None
    return response.content

def loadStr(link:str) -> str:
    response = requests.get(link, headers={"User-Agent": __USER_AGENT})
    if not response:
        print("loadStr: failed...")
        return None
    return response.text

class LoadResult():
    def __init__(self, link, result) -> None:
        self.link = link
        self.result = result

def loadMultipleStr(links:List[str]) -> List[LoadResult]:
    webLoaders:List[WebLoaderThreadStr] = []
    for link in links:
        webLoaders.append(WebLoaderThreadStr(link))
    return __getResultsFromWebLoaders(webLoaders)

def loadMultipleBytes(links:List[str]) -> List[LoadResult]:
    webLoaders:List[WebLoaderThreadBytes] = []
    for link in links:
        webLoaders.append(WebLoaderThreadBytes(link))
    return __getResultsFromWebLoaders(webLoaders)

def __getResultsFromWebLoaders(webLoaders:List[WebLoaderThreadBytes]) -> List[LoadResult]:
    results = []
    for webLoader in webLoaders:
        webLoader.start()
    for webLoader in webLoaders:
        webLoader.join()
        if webLoader.getResult():
            results.append(LoadResult(webLoader.getLink(),webLoader.getResult()))
    return results