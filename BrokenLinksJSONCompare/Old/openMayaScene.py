import maya.cmds as cmds
import os


def openMayaScene(root, shotName):
    fileExtensions = [".ma", ".mb"]
    if os.path.exists(str(root)) and shotName.lower() in fileExtensions:
        cmds.file(new=True, force=True)
        cmds.file(root, open=True)
        print("you have opened " + shotName)
    return "done"
