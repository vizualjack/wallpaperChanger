from typing import List, Tuple
import requests
from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from typing import Any


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

def loadMultipleStr(links:List[str]) -> List['LoadResult']:
    webLoaders:List[WebLoaderThreadStr] = []
    for link in links:
        webLoaders.append(WebLoaderThreadStr(link))
    return __getResultsFromWebLoaders(webLoaders)

def loadMultipleBytes(links:List[str]) -> List['LoadResult']:
    webLoaders:List[WebLoaderThreadBytes] = []
    for link in links:
        webLoaders.append(WebLoaderThreadBytes(link))
    return __getResultsFromWebLoaders(webLoaders)


class LoadResult():
    def __init__(self, link, result) -> None:
        self.link = link
        self.result = result

def __getResultsFromWebLoaders(webLoaders:List['WebLoaderThreadBytes']) -> List[LoadResult]:
    results = []
    for webLoader in webLoaders:
        webLoader.start()
    for webLoader in webLoaders:
        webLoader.join()
        if webLoader.getResult():
            results.append(LoadResult(webLoader.getLink(),webLoader.getResult()))
    return results

class WebLoaderThreadBytes(Thread):
    def __init__(self, link, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)
        self._link = link
        self._finished = False
        self._result = None

    def isFinished(self):
        return self._finished
    
    def getResult(self) -> bytes:
        return self._result
    
    def getLink(self) -> str:
        return self._link

    def run(self):
        self._result = loadBytes(self._link)
        self._finished = True


class WebLoaderThreadStr(WebLoaderThreadBytes):    
    def getResult(self) -> str:
        return self._result

    def run(self):
        self._result = loadStr(self._link)
        self._finished = True