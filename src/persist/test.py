from persister import Persister
from pathlib import Path

PERSISTER_DATA_PATH = Path("./persisterData")

persister = Persister(PERSISTER_DATA_PATH)
dict1 = {}
dict1["abc"] = "asdasd"
dict2 = {}
dict2["asdasd"] = 2323
innerDict = {}
innerDict["test"] = "stuff"
dict2["innerDict"] = innerDict
persister.setData("dict1", dict1)
persister.setData("dict2", dict2)
persister.save()

persister = Persister(PERSISTER_DATA_PATH)
persister.load()
ldict2 = persister.getData("dict2")
print(ldict2["innerDict"]["test"])