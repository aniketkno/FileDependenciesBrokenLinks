import re
import os
import sys
import json
import subprocess
import maya.cmds as cmds
sys.path.insert(0, r"C:\Python27\Lib\site-packages")
from PyQt4 import QtCore, QtGui, uic


def openMaya(sceneFileLocation=None):
    # Check if file exists
    mayaPath = r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe"
    pyScript = "C:/Users/anike/Documents/GitHub/FileDependenciesBrokenLinks/BrokenLinksJSONCompare/mayaFileCapture.py"

    # shotLocation = open("BrokenLinksJSONCompare\location.txt", "w+")
    # shotLocation.seek(0)
    # shotLocation.truncate()
    # print(str(sceneFileLocation))
    # shotLocation.write(str(sceneFileLocation))
    # shotLocation.close()
    jsonLocation = {str(sceneFileLocation): []}
    with open("BrokenLinksJSONCompare\location.json", "w+") as emptyShot:
        json.dump(jsonLocation, emptyShot)

    openMayaCmd = subprocess.Popen(
        [mayaPath, "-batch", "-file", str(sceneFileLocation), "-command", "python(\"execfile('{0}')\")".format(pyScript)])
    openMayaCmd.wait()
    dictLocations = {}
    with open("BrokenLinksJSONCompare\location.json", "r") as loadedLocation:
        dictLocations = json.load(loadedLocation)
    print(dictLocations.keys())
    print(dictLocations.values())
    shotNum = dictLocations.keys()[0]
    itemList = dictLocations.values()
    return shotNum, itemList


def validPath(filePath=None):
    if os.path.isfile(filePath):
        return True
    else:
        return False


def jsonParseData(root=None):
    print(root)
    with open(os.path.abspath(root), 'r') as f:
        jsonData = json.load(f)
    print jsonData
    return jsonData


'''
def ItemsNLocationToList():
    listOfItemLocations = []
    for p in texLocationInScene():
        # texture for item in location
        fileName = os.path.basename(p)
        pTup = (fileName.split(r"_texture_")[0], p)
        listOfItemLocations.append(pTup)
    for abc in abcLocationInScene():
        # alembic for Item in location
        fileName = os.path.normpath(os.path.basename(abc))
        hello = abc.split(r"/cache")
        pTup = (os.path.basename(hello[0]), os.path.normpath(abc))
        listOfItemLocations.append(pTup)
        print listOfItemLocations
    return listOfItemLocations
def texLocationInScene():

    texDirs = []
    fileList = cmds.ls(type="file")

    if not fileList:
        texDirs.append("There were no file paths found.")
        return texDirs

    for f in fileList:
        try:
            # handle error when no files are attached to shader
            fPath = cmds.getAttr(f+".fileTextureName")
        except AttributeError:
            print("there is no attribute: " + f+".fileTextureName")
        dirPath = os.path.splitext(fPath)[0]

        if fPath not in texDirs:
            texDirs.append(fPath)
        texDirs.sort()
    return texDirs
def abcLocationInScene():
    abcDirs = []
    meshList = cmds.ls(type="gpuCache", dagObjects=True, noIntermediate=True)
    animatedMeshes = cmds.ls(type="AlembicNode")

    if not meshList and not animatedMeshes:
        abcDirs.append("There were no file paths found.")
        return abcDirs

    for m in meshList:
        try:
            aPath = cmds.getAttr(m+'.cacheFileName')
        except AttributeError:
            print("there is no attribute: " + m+'.cacheFileName')
        location = os.path.split(aPath)[0]
        if aPath not in abcDirs:
            abcDirs.append(aPath)
        abcDirs.sort()

    for m in animatedMeshes:
        try:
            cache_path = cmds.getAttr(m + '.abc_File')
        except AttributeError:
            print("there is no attribute: " + m + '.abc_File')
        if cache_path not in abcDirs:
            abcDirs.append(cache_path)
    return abcDirs
'''


def checkItemInShot(jsonData=None, shotNumber=None, items=None):
    if not shotNumber:
        return "WARNING: This shot IS NOT in project."
    elif not jsonData:
        return "WARNING: JSON data was not loaded properly"
    wrongTexItemList = ""
    wrongAbcItemList = ""
    missingItemList = ""

    print(shotNumber)
    for shot, sh_dict in jsonData.items():
        if shotNumber == shot:
            for item in items:
                for itemName, location in item:
                    if not sh_dict.get(itemName.split("_")[0]) and location.split(".")[-1] == "abc":
                        wrongAbcItemList += '{0}'.format(
                            itemName, shotNumber) + "\n"
                    elif not sh_dict.get(itemName.split("_")[0]):
                        wrongTexItemList += '{0}'.format(
                            itemName, shotNumber) + "\n"
                    if not validPath(location):
                        missingItemList += '{0} is missing from: .......  {1}'.format(
                            itemName, location) + "\n"
    if not wrongTexItemList and not wrongAbcItemList and not missingItemList:
        return "There are no missing links"
    return "Alembic Files Not in Shot \n" + wrongAbcItemList + "\n" + "Texture Files Not in Shot \n" + wrongTexItemList + "\n" + "Files in shot, but are missing from location \n" + missingItemList


class Broken_Links_Form(QtGui.QMainWindow):
    def __init__(self, parent=QtGui.QApplication.instance()):
        super(Broken_Links_Form, self).__init__()
        uic.loadUi(
            r"C:\Users\anike\Documents\GitHub\FileDependenciesBrokenLinks\BrokenLinksJSONCompare\BrokenLinks.ui", self)
        self.toolButton_MayaLocation.clicked.connect(
            lambda: self.lineEdit_MayaLocation.setText(QtGui.QFileDialog.getOpenFileName()))
        self.toolButton_JSONLocation.clicked.connect(
            lambda: self.lineEdit_JSONLocation.setText(QtGui.QFileDialog.getOpenFileName()))
        self.pushButton_AnalyzeBrokenLinks.clicked.connect(
            lambda: self.findMissingLinks())

    def findMissingLinks(self):
        jsonDataDict = jsonParseData(self.lineEdit_JSONLocation.text())
        shotNumberValue, itemLocations = openMaya(
            self.lineEdit_MayaLocation.text())
        self.textEdit_missingLinks.setText(checkItemInShot(
            jsonData=jsonDataDict, shotNumber=shotNumberValue, items=itemLocations))


def main(*args):
    # python location\of\BrokenLinks.py location\of\shot.json location\of\maya\scene.ma
    print("")
    app = QtGui.QApplication(sys.argv)
    Form = Broken_Links_Form()
    Form.show()
    sys.exit(app.exec_())


main()
