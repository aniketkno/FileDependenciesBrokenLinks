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
