import subprocess
import os
import sys


def mayaCallout():
    mayaPath = r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe"
    openMayaCmd = subprocess.Popen([mayaPath,"-batch", "-file", "", "-command", "python(\"execfile('{0}')\")"])
    openMayaCmd.wait()
    print("maya Opened")



mayaCallout()