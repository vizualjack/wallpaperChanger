from .filePers import saveStr
from pathlib import Path
import traceback
from datetime import datetime
from appSettings import *


def saveException(additionalInfo:str=None) -> Path:
    global initSuccessful, exceptionPath
    if not initSuccessful:
        __init()
    if not initSuccessful:
        print("Can't save exception, init wasn't successful")
        return None
    # actual save here
    exceptionInfo = f"{traceback.format_exc()}\n"
    if additionalInfo:
        exceptionInfo += f"=== Additional info===\n{additionalInfo}\n"
    dtAsStr = datetime.now().strftime(f"%Y%m%d%H%M%S")
    logFileName = f"exception_{dtAsStr}.log"
    logFilePath = exceptionPath.joinpath(logFileName)
    saveStr(logFilePath, exceptionInfo)
    print(exceptionInfo)
    return logFilePath

def __init():
    global initSuccessful, exceptionPath
    print("Check if initialize is needed for exception saver")
    if exceptionPath:
        return
    # if exceptionPath and not exceptionPath.is_file():
    #     initSuccessful = True
    #     return
    exceptionPath = Path(EXCEPTION_FOLDER)
    print("Initialize exception saver")
    if exceptionPath.is_file():
        print("Can't inititalize exception saver")
        return
    if not exceptionPath.exists():
        exceptionPath.mkdir()
    initSuccessful = True
    print("Exception saver initialized")

## init stuff (create exceptions folder)
initSuccessful = False
exceptionPath = None
__init()