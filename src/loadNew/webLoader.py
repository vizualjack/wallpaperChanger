import requests

__USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
# User-Agent

def loadBytes(link:str) -> bytes:
    response = requests.get(link, headers={"User-Agent": __USER_AGENT})
    if not response:
        print("loadBytes: failed...")
        return None
    return response.content

def loadStr(link:str) -> str:
    response = requests.get(link, headers={"User-Agent": __USER_AGENT})
    if not response:
        print("loadStr: failed...")
        return None
    return response.text