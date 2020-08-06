def checkItemInShot(jsonData=None, shotNumber=None, items=None):
    if not shotNumber:
        return "WARNING: This shot IS NOT in project."
    elif not jsonData:
        return "WARNING: JSON data was not loaded properly"
    ShotList = ""
    for sh_dict in jsonData[shotNumber]:
        for itemName, location in items:
            if not sh_dict.get(str(itemName.split("_")[0])):
                ShotList.append('The item, {0}, is not in {1}'.format(
                    itemName, shotNumber))
    if not ShotList:
        return "There are no missing links"
    return ShotList


def checkItemInShot(jsonData=None, shotNumber=None, items=None):
    if not shotNumber:
        return "WARNING: This shot IS NOT in project."
    elif not jsonData:
        return "WARNING: JSON data was not loaded properly"
    # wrongItemList = ""
    missingItemList = ""
    for shot, sh_dict in jsonData.items():
        if shotNumber == shot:
            print(shotNumber)
            for item in items:
                for itemName, location in item:
                    if not validPath(location):
                        missingItemList += 'The {1} is not located at {0}'.format(
                            itemName, location) + "\n"
                    # if not sh_dict.get(itemName.split("_")[0]):
                    #     WrongItemList += 'The {1} does not contain {0}'.format(
                    #         itemName, shotNumber) + "\n"
        else:
            print(shotNumber)
    if not WrongItemList:
        return "There are no missing links"
    return WrongItemList + "\n" + missingItemList
