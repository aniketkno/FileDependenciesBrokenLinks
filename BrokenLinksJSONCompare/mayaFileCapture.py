import os
import sys
import json
import maya.cmds as cmds


class MayaOrganizer():
    '''
    opens json shot data and takes location of maya scene
    opens maya scene
    finds texture/alembic files in scene
    dumps back json file to main script
    input: json file for communication scene location
    output: json file for communication shot name, items in scene and their location
    '''

    def __init__(self ):
        '''
        input location json data 
        opens scene from location data as shotname
        outputs dictionary of shot: list of tuples containing file name and location 

        input: json file for communication scene location
        output: json file for communication shot name, items in scene and their location
        '''
        self.shotLocationFromMain = ""

        with open("BrokenLinksJSONCompare\location.json", "r") as f:
            self.shotLocationFromMain = json.load(f).keys()[0]
        
        print(self.shotLocationFromMain)
        self.listOfItemLocations = []
        self.jsonCreator = {}
        self.shotnumber = self.openscene(self.shotLocationFromMain)
        self.jsonShotandLocation()


    def jsonShotandLocation(self):
        '''
        creates dictionary shot number: items in shot
        dumps data into json file
        input: class property shot number and list of tuples of items/locations
        output: json file
        '''
        self.jsonCreator = {self.shotnumber: self.ItemsNLocationToList()}
        with open("BrokenLinksJSONCompare\location.json", "w+") as shotNLocations:
            json.dump(self.jsonCreator, shotNLocations)

    def openscene(self, sceneFileLocation2):
        '''
        checks if file is a maya scene file
        opens scene and returns shot name else returns ""
        
        input: with maya open method takes scenelocation
        output: shotnumber in the name of the file
        '''
        fileExtensions = [".ma", ".mb"]
        shotName = os.path.basename(str(sceneFileLocation2))
        if "_maya_" in shotName:
            shot = shotName.split("_maya_")[0]
        else: shot = ""

        if os.path.exists(str(sceneFileLocation2)) and shotName.lower() in fileExtensions:
            opened_file = cmds.file(maya_file_to_open, o=True)
            print("you have opened " + shotName)
        return shot

    def texLocationInScene(self):
        '''
        initializes search in maya to find all texture files
        input: maya open
        output: list of texture location
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

    def abcLocationInScene(self):
        '''
        initializes search in maya to find all alembic files
        input: maya open
        output: list of alembic/gpu cache location
        '''
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
        '''
        calls for texture and alembic location items crops their names as file name and 
        returns list of tuples to parse
        input: maya open
        output: list of tuples item name, item location 
        '''
        for p in self.texLocationInScene():
            # texture for item in location
            fileName = os.path.basename(p)
            pTup = (fileName.split(r"_texture_")[0], p)
            self.listOfItemLocations.append(pTup)
        for abc in self.abcLocationInScene():
            # alembic for Item in location
            fileName = abc.split(r"/cache")
            pTup = (os.path.basename(fileName[1]), abc)
            self.listOfItemLocations.append(pTup)
        return self.listOfItemLocations

## Initialize script with no args
MO = MayaOrganizer()
