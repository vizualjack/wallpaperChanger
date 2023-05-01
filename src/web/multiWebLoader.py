from typing import List, Tuple
from .webLoaderThreadStr import WebLoaderThread, WebLoaderThreadStr

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
    webLoaders:List[WebLoaderThread] = []
    for link in links:
        webLoaders.append(WebLoaderThread(link))
    return __getResultsFromWebLoaders(webLoaders)

def __getResultsFromWebLoaders(webLoaders:List[WebLoaderThread]) -> List[LoadResult]:
    results = []
    for webLoader in webLoaders:
        webLoader.start()
    for webLoader in webLoaders:
        webLoader.join()
        if webLoader.getResult():
            results.append(LoadResult(webLoader.getLink(),webLoader.getResult()))
    return results