ItemsNLocationToList= ["Hello","Dave","Dude"]

shotNLocations = open("location.txt", "w+")
shotNLocations.writelines(ItemsNLocationToList + "\n")
shotNLocations.close()
