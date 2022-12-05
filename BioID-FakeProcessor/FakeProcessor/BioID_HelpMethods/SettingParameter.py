import os
import json

# Start Path
# Save Coordinates
# Cameras
# Fake Folder Name
# Fake Image Name
# Picture Width
# Camera Preview Toplevel
# --------------------------
# Save new Settings
# Load Settings
# Reset Settings
# Default Settings

#region StartPath
startPath = os.path.expanduser('~')

def getStartPath():
    global startPath
    return startPath
def setStartPath(path):
    global startPath
    startPath = path
#endregion

#region SavedCords
savedCord = (0, 0)

def getCords():
    global savedCord
    return savedCord
def setCords(x, y):
    global savedCord
    savedCord = (x, y)
#endregion

#region Cameras
cameraIndex = 0

def getCamera():
    global cameraIndex
    return cameraIndex
def setCamera(index):
    global cameraIndex
    cameraIndex = index
#endregion

#region FakeFolderName
fakeFolderName=""

def getFakeFolderName():
    global fakeFolderName
    return fakeFolderName
def setFakeFolderName(string):
    global fakeFolderName
    fakeFolderName = string
#endregion

#region FakeImageName
fakeImageName=""

def getFakeImageName():
    global fakeImageName
    return fakeImageName
def setFakeImageName(string):
    global fakeImageName
    fakeImageName = string
#endregion

#region PictureWidth
picWidth = 600

def getPicWidth():
    global picWidth
    return picWidth
def setPicWidth(width):
    global picWidth
    picWidth = width
#endregion

#region PrevWindow
prevWin = True

def getPrevWin():
    global prevWin
    return prevWin
def setPrevWin(bool):
    global prevWin
    prevWin = bool
#endregion

# --------------------------

os.umask(0)
def opener(path, flags):
    return os.open(path, flags, 0o777)

import pathlib
fullPath = pathlib.Path().resolve()
print(fullPath)

#region SettingManagment
def loadDefaultSettings(setting):
    global prevWin, picWidth, fakeFolderName, fakeImageName, savedCord, startPath, cameraIndex
    if os.path.exists('DefaultSettings.json'):
        with open(str(fullPath) + '\\DefaultSettings.json', 'r+', opener=opener) as product:
            data = json.load(product)
            product.close()
            if setting == "startPath":
                    startPath = data["startPath"]
            elif setting == "prevWin":
                    prevWin = data["prevWin"]
            elif setting == "picWidth":
                    picWidth = data["picWidth"]
            elif setting == "fakeFolderName":
                    fakeFolderName = data["fakeFolderName"]
            elif setting == "fakeImageName":
                    fakeImageName = data["fakeImageName"]
            elif setting == "savedCord":
                    savedCord = tuple(data["savedCord"])
            elif setting == "cameraIndex":
                    cameraIndex = data["cameraIndex"]
            elif setting == "full":
                    startPath = data["startPath"]
                    prevWin = data["prevWin"]
                    picWidth = data["picWidth"]
                    fakeFolderName = data["fakeFolderName"]
                    fakeImageName = data["fakeImageName"]
                    savedCord = tuple(data["savedCord"])
                    cameraIndex = data["cameraIndex"]
            else:
                if setting == "startPath":
                        startPath = os.path.expanduser('~')
                elif setting == "prevWin":
                        prevWin = True
                elif setting == "picWidth":
                        picWidth = 600
                elif setting == "fakeFolderName":
                        fakeFolderName = ""
                elif setting == "fakeImageName":
                        fakeImageName = ""
                elif setting == "savedCord":
                        savedCord = (0, 0)
                elif setting == "cameraIndex":
                        cameraIndex = 0
                elif setting == "full":
                        startPath = os.path.expanduser('~')
                        prevWin = True
                        picWidth = 600
                        fakeFolderName = ""
                        fakeImageName = ""
                        savedCord = (0, 0)
                        cameraIndex = 0


def loadSettings():
    global prevWin, picWidth, fakeFolderName, fakeImageName, savedCord, startPath, cameraIndex
    if os.path.exists('Settings.json'):
        with open(str(fullPath) + '\\Settings.json', 'r+', opener=opener) as product:
            data = json.load(product)
            product.close()
            startPath = data['startPath']
            picWidth = data['picWidth']
            fakeFolderName = data['fakeFolderName']
            fakeImageName = data['fakeImageName']
            savedCord = tuple(data['savedCord'])
            cameraIndex = data['cameraIndex']
    else:
        resetSettings()

def saveSettings():
    global prevWin, picWidth, fakeFolderName, fakeImageName, savedCord, startPath, cameraIndex
    jsonDict = {"prevWin":prevWin,
                "picWidth":picWidth,
                "fakeFolderName":fakeFolderName,
                "fakeImageName":fakeImageName,
                "savedCord":savedCord,
                "startPath":startPath,
                "cameraIndex":cameraIndex
                }
    with open(str(fullPath) + '\\Settings.json', 'w+', opener=opener) as outfile:
        json.dump(jsonDict, outfile)
        outfile.close()

def saveDefaultSettings():
    global prevWin, picWidth, fakeFolderName, fakeImageName, savedCord, startPath, cameraIndex
    jsonDict = {"prevWin": prevWin,
                "picWidth": picWidth,
                "fakeFolderName": fakeFolderName,
                "fakeImageName": fakeImageName,
                "savedCord": savedCord,
                "startPath": startPath,
                "cameraIndex": cameraIndex
                }
    with open(str(fullPath) + '\\DefaultSettings.json', 'w+', opener=opener) as outfile:
        json.dump(jsonDict, outfile)
        outfile.close()

def resetSettings():
    loadDefaultSettings("full")
    saveSettings()
#endregion