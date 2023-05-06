from pathlib import Path
from io import TextIOWrapper
from typing import List


def saveStrList(filePath:Path|str, dataList:List[str]):
    listAsOneStr = "\n".join(dataList)
    saveStr(filePath, listAsOneStr)

def readStrList(filePath:Path|str) -> List[str]:
    listAsOneStr = readStr(filePath)
    return listAsOneStr.split("\n")

def saveStr(filePath:Path|str, data:str):
    __writeAndCloseFile(__openWriteStrFile(filePath), data)

def readStr(filePath:Path|str) -> str:
    return __readAndCloseFile(__openReadStrFile(filePath))

def saveBytes(filePath:Path|str, data:bytes):
    __writeAndCloseFile(__openWriteBytesFile(filePath), data)

def readBytes(filePath:Path|str) -> bytes:
    return __readAndCloseFile(__openReadBytesFile(filePath))

def __readAndCloseFile(file:TextIOWrapper) -> any:
    data = file.read()
    file.flush()
    file.close()
    return data

def __writeAndCloseFile(file:TextIOWrapper, data):
    file.write(data)
    file.flush()
    file.close()

def __openReadStrFile(filePath):
    return __openFile(filePath, "r")

def __openWriteStrFile(filePath):
    return __openFile(filePath, "w")

def __openReadBytesFile(filePath):
    return __openFile(filePath, "rb")

def __openWriteBytesFile(filePath):
    return __openFile(filePath, "wb")

def __openFile(filePath, mode):
    return open(filePath, mode)