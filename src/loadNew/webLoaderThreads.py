from collections.abc import Callable, Iterable, Mapping
from threading import Thread
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from .loader import loadBytes, loadStr


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