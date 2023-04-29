from enum import Enum
from pathlib import Path
from PIL import Image as PILImage
from persist.filePers import saveBytes

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
    def fromPath(path) -> 'Image':
        if isinstance(path, str):
            path = Path(path)
        image = Image()
        nameParts = path.name.split(".")
        image.name = nameParts[0]
        image.extension = nameParts[1]
        image.saveFolder = path.parent
        pilImage = PILImage.open(path)
        image.data = pilImage.tobytes()
        width = pilImage.size[0]
        height = pilImage.size[1]
        image.size = Image.Size(width, height)
        # image.imageType = pilImage.format  # ???
        image.type = Image.getTypeForExtension(image.extension)
        return image
    
    @staticmethod
    def getTypeForExtension(extension:str) -> Type:
        extension = extension.lower()
        if extension == "jpg" or extension == "jpeg":
            return Image.Type.JPG
        elif extension == "png":
            return Image.Type.PNG
        return Image.Type.UNKNOWN
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
        return self.saveFolder.joinpath(self.getFullName()).absolute()
    
    def getFullPathStr(self) -> str:
        return self.getFullPath().__str__()