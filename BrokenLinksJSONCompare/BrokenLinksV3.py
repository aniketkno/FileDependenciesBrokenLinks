import re
import os
import sys
import json
import subprocess
import maya.cmds as cmds
sys.path.insert(0, r"C:\Python27\Lib\site-packages")
from PyQt4 import QtCore, QtGui, uic


def openMaya(sceneFileLocation=None):
    '''
    dumps json file with scene location for maya to open
    opens maya and runs mayaFileCapture.py internally in maya batch
    load json file to dictionary shot number and items tuples

    input: scene file location
    returns: shot number, list of tuples containing items and location
    '''
    mayaPath = r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe"
    pyScript = "C:/Users/anike/Documents/GitHub/FileDependenciesBrokenLinks/BrokenLinksJSONCompare/mayaFileCapture.py"

    jsonLocation = {str(sceneFileLocation): []}
    with open("BrokenLinksJSONCompare\location.json", "w+") as emptyShot:
        json.dump(jsonLocation, emptyShot)

    openMayaCmd = subprocess.Popen(
        [mayaPath, "-batch", "-file", str(sceneFileLocation), "-command", "python(\"execfile('{0}')\")".format(pyScript)])
    openMayaCmd.wait()

    dictLocations = {}
    with open("BrokenLinksJSONCompare\location.json", "r") as loadedLocation:
        dictLocations = json.load(loadedLocation)


    shotNum = dictLocations.keys()[0]
    itemList = dictLocations.values()
    return shotNum, itemList


def validPath(filePath=None):
    '''
    makes sure if paths are actual files
    input: file path
    output: bool
    '''
    if os.path.isfile(filePath):
        return True
    else:
        return False


def jsonParseData(root=None):
    '''
    loads json file into a dictionary
    input: location of json file
    output: dictionary
    '''

    with open(os.path.abspath(root), 'r') as f:
        jsonData = json.load(f)
    return jsonData


def checkItemInShot(jsonData=None, shotNumber=None, items=None):
    '''
    check if shotnumber, jsonData are loaded
    feeds key as shot into json directory and checks if files are located
    if Item is not suppose to be in shot then item is listed. 
    if Item is part of the scene however the file is not located in file directory it gets listed.
    input: Dictionary from json file, shotnumber and items from maya scene 
    output: string of location that are not meeting criteria if files are missing
    '''
    if not shotNumber:
        return "WARNING: This shot IS NOT in project."
    elif not jsonData:
        return "WARNING: JSON data was not loaded properly"
    wrongTexItemList = ""
    wrongAbcItemList = ""
    missingItemList = ""

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
    '''
    runs gui for parsing scenes for missing texture/alembic files
    input: qtgui object
    output: visual gui
    '''

    def __init__(self, parent=QtGui.QApplication.instance()):
        '''
        initializes gui and connects buttons to text
        input: location of maya scens and project json file
        output: list of missing links in gui
        '''
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
        '''
        loads json data from file
        loads shot and item location 
        connects data into the textedit
        input: analyze button click connected , no other data
        output: data to textedit in gui
        '''

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
