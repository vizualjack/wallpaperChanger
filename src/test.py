# from imageContainer import ImageContainer
# from imageDler import ImageDler
# from image import Image


# # imageContainer = ImageContainer("./images")
# # imageDler = ImageDler(Image.Size(1920, 1080))
# # newImage = imageDler.downloadImage()
# # print(f"loaded image: {newImage.getFullName()}")
# # imageContainer.add(newImage)
# # print("put into image container")

# imageContainer = ImageContainer("./images")
# for randImg in imageContainer.getRandomImages(2):
#     print(randImg.name)
#     imageContainer.addToBlackList(randImg)


# ### multi str load test
# from web.multiWebLoader import loadMultipleStr
# import time

# TEST_LINKS = [
#     r"https://realpython.com/iterate-through-dictionary-python/#iterating-through-values",
#     r"https://www.startpage.com/do/dsearch?query=python+loop+through+dict&language=english&cat=web&pl=ext-ff&extVersion=1.1.7",
#     ]

# counter = 1
# for loadResult in loadMultipleStr(TEST_LINKS):
#     print("Result for: " + loadResult.link)
#     f = open(f"page{counter}.html", "w", encoding="utf-8")
#     f.write(loadResult.result)
#     f.flush()
#     f.close()
#     counter += 1
# print("Done")



#### bytes load test
# from web.webLoaderThreadBytes import WebLoaderThreadBytes
# import time

# TEST_LINK = r"https://www.startpage.com/av/proxy-image?piurl=https%3A%2F%2Fstatic.boredpanda.com%2Fblog%2Fwp-content%2Fuploads%2F2017%2F11%2FMy-most-popular-pic-since-I-started-dog-photography-5a0b38cbd5e1e__880.jpg&sp=1682959839T1bb3471c120792504b1db6dd983cd62c7f456b4abcea8bb2e80af863644fefd8"

# webLoader = WebLoaderThreadBytes(TEST_LINK)
# while not webLoader.isFinished():
#     print("Waiting...")
#     time.sleep(1)
# print("Saving...")
# f = open("test.jpg", "wb")
# f.write(webLoader.getResult())
# f.flush()
# f.close()
# print("Done")



### image load test
# from PIL import Image as PILImage
# from io import BytesIO
# from img.imageUtil import

# baseImg = PILImage.open("images/pic.jpg")
# bytesIO = BytesIO()
# baseImg.save(bytesIO, "JPEG")
# data = bytesIO.getvalue()

# width,height = baseImg.size
# print(width)
# print(height)
# # imageViaBytes = PILImage.frombytes("RGB", (width,height), data)
# imageViaBytes = loadPILImage("pic.jpg", data)
# imageViaBytes.save("aa.jpg")