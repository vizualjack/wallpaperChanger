from PIL import Image as PILImage
from io import BytesIO
from img.imageUtil import loadPILImage

baseImg = PILImage.open("images/pic.jpg")
bytesIO = BytesIO()
baseImg.save(bytesIO, "JPEG")
data = bytesIO.getvalue()

width,height = baseImg.size
print(width)
print(height)
# imageViaBytes = PILImage.frombytes("RGB", (width,height), data)
imageViaBytes = loadPILImage("pic.jpg", data)
imageViaBytes.save("aa.jpg")