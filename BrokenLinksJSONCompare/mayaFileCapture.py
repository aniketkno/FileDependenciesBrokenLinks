import os
import sys
import json
import maya.cmds as cmds


class MayaOrganizer():
    def __init__(self ):
        self.shotLocationFromMain = ""

        with open("BrokenLinksJSONCompare\location.txt", "w+") as f:
            self.shotLocationFromMain = f.readline()
            print(self.shotLocationFromMain)
        
        print(self.shotLocationFromMain)

        self.listOfItemLocations = []
        self.jsonCreator = {}
        self.shotnumber = self.openscene(self.shotLocationFromMain)
        self.jsonShotandLocation()


    def jsonShotandLocation(self):
        print(self.ItemsNLocationToList())
        self.jsonCreator = {self.shotnumber: self.ItemsNLocationToList()}
        with open("BrokenLinksJSONCompare\location.json", "w+") as shotNLocations:
            json.dump(self.jsonCreator, shotNLocations)
        print(self.jsonCreator)

    def openscene(self, sceneFileLocation2):
        fileExtensions = [".ma", ".mb"]
        shotName = os.path.basename(str(sceneFileLocation2))
        shot = shotName.split("_maya_")[0]

        print(shot)

        if os.path.exists(str(sceneFileLocation2)) and shotName.lower() in fileExtensions:
            opened_file = cmds.file(maya_file_to_open, o=True)
            print("you have opened " + shotName)
        return shot

    def texLocationInScene(self):
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
        print(texDirs)
        return texDirs

    def abcLocationInScene(self):
        abcDirs = []
        meshList = cmds.ls(type="gpuCache", dagObjects=True,
                           noIntermediate=True)
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

    def ItemsNLocationToList(self):
        for p in self.texLocationInScene():
            # texture for item in location
            fileName = os.path.basename(p)
            pTup = (fileName.split(r"_texture_")[0], p)
            print(pTup)
            self.listOfItemLocations.append(pTup)
        for abc in self.abcLocationInScene():
            # alembic for Item in location
            fileName = abc.split(r"/cache")
            pTup = (os.path.basename(fileName[1]), abc)
            print(pTup)
            self.listOfItemLocations.append(pTup)
        print self.listOfItemLocations
        return self.listOfItemLocations


MO = MayaOrganizer()
