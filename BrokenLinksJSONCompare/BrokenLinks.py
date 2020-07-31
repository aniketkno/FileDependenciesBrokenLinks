import sys
import Github.pfx_dev.PFX.JSONParserForItems.ItemsInShotsV5 as IIS

## parse through JSON 
## gather shot and asset location
## compare and gather items from each shot 
## if not in intersection of the dependant files 
## list as broken links
## 

def texLocationInScene():
    '''locates all texture files in scene 
    must have a scene open
    filters results that lack textures in scene 
    lists file types by location

    output: location or lack of location 
    '''
    texDirs = []
    fileList = mc.ls(type="file")

    if not fileList:
        texDirs.append("There were no file paths found.")
        return texDirs

    for f in fileList:
        try:
            # handle error when no files are attached to shader
            fPath = mc.getAttr(f+".fileTextureName")
        except AttributeError:
            print("there is no attribute: " + f+".fileTextureName")
        dirPath = os.path.split(fPath)[0]

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
    meshList = mc.ls(type="gpuCache", dagObjects=True, noIntermediate=True)
    animatedMeshes = mc.ls(type="AlembicNode")

    if not meshList and not animatedMeshes:
        abcDirs.append("There were no file paths found.")
        return abcDirs

    for m in meshList:
        try:
            aPath = mc.getAttr(m+'.cacheFileName')
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

def main(*args):
    jsonPath=os.path.normpath(sys.argv[1])
    keyForItem=sys.argv[2]
    assetName=sys.argv[3]
    jsonData={}
    if not IIS.isValidJSON(root=jsonPath):
        return
    jsonData=IIS.jsonParseData(root=jsonPath)

    while not IIS.isValidItemKey(key=keyForItem):
        keyForItem=input(
            "Key not valid. input (Character, Prop, Environment, Shot): ")
        IIS.isValidItemKey(key=keyForItem)

    mayaScenePath=IIS.checkItemInShot()
    IIS.isValidMayaScene()
