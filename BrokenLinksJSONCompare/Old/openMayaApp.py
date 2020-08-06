import sys
import re
import os
import subprocess


def mayaReady(location=None):
    if re.match("maya\\.exe", os.path.basename(sys.executable), re.I):
        print("Running in Maya.")
    else:
        print("loading maya ...")
        mayaPath = r"C:\Program Files\Autodesk\Maya2019\bin\maya.exe"
        openMayaCmd = subprocess.Popen(
            [mayaPath, "-batch", "-file", location ,"-command", "python(\"print(loading maya...)\")"])
        openMayaCmd.wait()