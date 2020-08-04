import os
import sys
import json
import subprocess
import maya.cmds as cmds
sys.path.insert(0, r"C:\Python27\Lib\site-packages")
from PyQt4 import QtCore, QtGui, uic





# Open Maya scene files.
def openMayaScene(root=None):
    # Check if file exists
    print("maya Opened")
    fileExtensions = [".ma", ".mb"]
    shotName = os.path.basename(str(root))
    shot = shotName.split("_maya_")[0]
    mayaPath = r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe"
    openMayaCmd = subprocess.Popen(
        [mayaPath, "-batch", "-file", "", "-command", "python(\"execfile('{0}')\")"])
    openMayaCmd.wait()

    if os.path.exists(str(root)) and shotName.lower() in fileExtensions:
        cmds.file(new=True, force=True)
        cmds.file(root, open=True)
        print("you have opened " + shotName)
    return shot

def jsonParseData(root=None):
    # parse through JSON
    print(root)
    with open(os.path.abspath(root), 'r') as f:
        jsonData = json.load(f)
    print jsonData
    return jsonData


def ItemsNLocationToList():
    # check if texture/alembic files are within scene
    # compare and gather items from each shot
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
    '''locates all texture files in scene
    must have a scene open
    filters results that lack textures in scene
    lists file types by location

    output: location or lack of location
    '''
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
    '''locates all alembic cache files in scene
    must have a scene open
    filters results that lacks alembic cache files in scene
    lists alembicNodes or gpuCache types by location

    output: location or lack of location of alembic cache
    '''
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


def checkItemInShot(jsonData=None, shotNumber=None):
    ShotList = []
    for shot, sh_dict in jsonData.items():
        if shotNumber == shot:
            for itemName, location in ItemsNLocationToList():
                if not sh_dict.get(itemName.split("_")[0]):
                    continue
                if itemName in sh_dict.get(itemName.split("_")[0]):
                    pass
                else:
                    print('The item, {0}, is not in {1}'.format(
                        itemName, shotNumber))
                    ShotList.append({itemName, shotNumber})
    if not ShotList:
        return "There are no missing links"
    return ShotList


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


    def validPath(self, filePath=None):
        if os.path.isfile(filePath):
            return filePath

    def findMissingLinks(self):
        print(self.lineEdit_JSONLocation.text())
        jsonDataDict = jsonParseData(self.lineEdit_JSONLocation.text())
        shotNumberValue = openMayaScene(str(self.lineEdit_MayaLocation.text()))
        self.textEdit_missingLinks.setText(checkItemInShot(
            jsonData=jsonDataDict, shotNumber=shotNumberValue))


def main(*args):
    # python location\of\BrokenLinks.py location\of\shot.json location\of\maya\scene.ma
    print("")

    app = QtGui.QApplication(sys.argv)
    Form = Broken_Links_Form()
    Form.show()
    sys.exit(app.exec_())


main()
