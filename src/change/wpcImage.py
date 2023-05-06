from enum import Enum
from pathlib import Path
from PIL import Image
from util.filePers import saveBytes, readBytes
from io import BytesIO


class WpcImage:
    class Type(Enum):
        UNKNOWN = 0
        JPG = 1
        PNG = 2

    class Size:
        def __init__(self, width, height) -> None:
            self.width = width
            self.height = height

    #### STATIC CONSTRUCTORS
    @staticmethod
    def fromPath(path: Path|str) -> 'WpcImage':
        if isinstance(path, str):
            path = Path(path)
        image = WpcImage()
        nameParts = path.name.split(".")
        image.name = nameParts[0]
        image.extension = nameParts[1]
        image.saveFolder = path.parent
        pilImage = Image.open(path)
        image.data = readBytes(path)
        width = pilImage.size[0]
        height = pilImage.size[1]
        image.size = WpcImage.Size(width, height)
        image.type = WpcImage.getTypeForExtension(image.extension)
        return image
    
    @staticmethod
    def getTypeForExtension(extension:str) -> Type:
        extension = extension.lower()
        if extension == "jpg" or extension == "jpeg":
            return WpcImage.Type.JPG
        elif extension == "png":
            return WpcImage.Type.PNG
        return WpcImage.Type.UNKNOWN
    # from ...
    ########

    def __init__(self) -> None:
        self.type = WpcImage.Type.UNKNOWN
        self.name = ""
        self.extension = ""
        self.saveFolder:Path = None
        self.data = bytes()
        self.size:WpcImage.Size = None

    def getFullName(self):
        return f"{self.name}.{self.extension}"
    
    def move(self, newFolder:Path):
        if not self.saveFolder is None:
            currentFullPath = self.getFullPath()
            newFullPath = newFolder.joinpath(self.getFullName()).absolute()
            currentFullPath.replace(newFullPath)
            self.saveFolder = newFolder
        else:
            self.saveFolder = newFolder
            self.save()

    def save(self, saveFolder:Path=None):
        if saveFolder:
            self.saveFolder = saveFolder
        if self.saveFolder is None:
            return
        saveBytes(self.getFullPath(), self.data)

    def getFullPath(self) -> Path:
        if not self.saveFolder:
            return Path(self.getFullName()).absolute()
        return self.saveFolder.joinpath(self.getFullName()).absolute()
    
    def getFullPathStr(self) -> str:
        return self.getFullPath().__str__()
    
    def asPilImage(self) -> Image:
        formats = Image.ID
        fp = BytesIO(self.data)
        prefix = fp.read(16)
        Image.preinit()
        def _open_core(fp, filename, prefix, formats):
            for i in formats:
                i = i.upper()
                if i not in Image.OPEN:
                    Image.init()
                try:
                    factory, accept = Image.OPEN[i]
                    result = not accept or accept(prefix)
                    if result:
                        fp.seek(0)
                        im = factory(fp, filename)
                        Image._decompression_bomb_check(im.size)
                        return im
                except (SyntaxError, IndexError, TypeError):
                    continue
                except BaseException:
                    fp.close()
                    raise
            return None
        im = _open_core(fp, self.getFullName(), prefix, formats)
        if im:
            im._exclusive_fp = True
            return im
        return None