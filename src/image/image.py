from enum import Enum
from pathlib import Path
from PIL import Image as PILImage

class Image:
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
    def fromPath(path:Path):
        image = Image()
        nameParts = path.name.split(".")
        image.name = nameParts[0]
        image.extension = nameParts[1]
        image.saveFolder = path.parent
        pilImage = PILImage.open(path)
        image.data = pilImage.tobytes()
        width = pilImage.size[0]
        height = pilImage.size[1]
        image.imageSize = Image.Size(width, height)
        # image.imageType = pilImage.format  # ???
        extension = image.extension.lower()
        if extension == "jpg" or extension == "jpeg":
            image.type = Image.Type.JPG
        elif extension == "png":
            image.type = Image.Type.PNG
    
    # @staticmethod
    # def fromData(bytes:bytes):
    #     pass
    # from ...
    ########

    def __init__(self) -> None:
        self.type = Image.Type.UNKNOWN
        self.name = ""
        self.extension = ""
        self.saveFolder:Path = None
        self.data = bytes()
        self.size:Image.Size = None

    def getFullName(self):
        return f"{self.name}.{self.extension}"
    
    def move(self, newFolder:Path):
        if not self.saveFolder is None:
            currentFullPath = self.saveFolder.joinpath(self.getFullName())
            newFullPath = newFolder.joinpath(self.getFullName())
            currentFullPath.replace(newFullPath)
            self.saveFolder = newFolder
        else:
            self.saveFolder = newFolder
            self.save()

    def save(self):
        if self.saveFolder is None:
            return
        fullPathStr = self.saveFolder.joinpath(self.getFullName()).__str__()
        f = open(fullPathStr, "wb")
        f.write(self.data)
        f.flush()
        f.close()
        