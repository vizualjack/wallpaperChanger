from tkinter import Misc, Widget
from typing import List

def destroyAllChildren(guiElement:Misc):
    elementsToDestroy:List[Widget] = []
    for childElement in guiElement.children.values():
        elementsToDestroy.append(childElement)
    for elementToDestroy in elementsToDestroy:
        elementToDestroy.destroy()
