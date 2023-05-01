from typing import Any
from .webLoader import loadStr
from .webLoaderThread import WebLoaderThread


class WebLoaderThreadStr(WebLoaderThread):    
    def getResult(self) -> str:
        return self._result

    def run(self):
        self._result = loadStr(self._link)
        self._finished = True