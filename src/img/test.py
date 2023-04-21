from imageContainer import ImageContainer
from imageDler import ImageDler
from image import Image


# imageContainer = ImageContainer("./images")
# imageDler = ImageDler(Image.Size(1920, 1080))
# newImage = imageDler.downloadImage()
# print(f"loaded image: {newImage.getFullName()}")
# imageContainer.add(newImage)
# print("put into image container")

imageContainer = ImageContainer("./images")
for randImg in imageContainer.getRandomImages(2):
    print(randImg.name)
    imageContainer.addToBlackList(randImg)