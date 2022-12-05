import os
import concurrent.futures
import time
import re
from multiprocessing import Manager
import glob
from functools import partial
from PIL import Image
from FakeProcessor.BioID_HelpMethods.SettingParameter import getStartPath, getPicWidth

resetPath = os.path.expanduser("~")
pictures = []
picDict = {}

def getDict():
    global picDict
    return picDict

def checkDirFiles(dirName):
    list_of_files = sorted(filter(os.path.isfile,
                                  glob.glob(getStartPath() + '\\' + dirName + '\\*.png')))
    return len(list_of_files)

def getLiveFake(fake=False):
    path = getStartPath()
    folderPath = ""
    if path and not fake:
        for folder in os.scandir(path):
            if folder.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?$", folder.name)):
                folderPath = path + "\\" + folder.name
                return folderPath
    elif path and fake:
        for folder in os.scandir(path):
            if folder.is_dir() and  bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?_FAKE$", folder.name)):
                folderPath = path + "\\" + folder.name
                return folderPath
    else:
        for folder in os.scandir(path):
            if folder.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?$", folder.name)):
                folderPath = path + "\\" + folder.name
                return folderPath

def getDir(fake=False):
    path = getStartPath()
    folderPath = ""
    if path and not fake:
        for folder in os.scandir(path):
            if folder.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?$", folder.name)) and not "FakeTrails" in folder.name:
                folderPath = path + "\\" + folder.name
        if folderPath != "":
            subfolders = [ f.name for f in os.scandir(folderPath) if f.is_dir()]
            return subfolders
    elif path and fake:
        for folder in os.scandir(path):
            if folder.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?_FAKE$", folder.name)) and not "FakeTrails" in folder.name:
                folderPath = path + "\\" + folder.name
        if not folderPath:
            folderName = ""
            for folder in os.scandir(path):
                if folder.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?$", folder.name)) and not "FakeTrails" in folder.name:
                    folderName = folder.name + "_FAKE"
            folderPath = path + "\\" + folderName
            os.mkdir(folderPath)
        if folderPath != "":
            subfolders = [ f.name for f in os.scandir(folderPath) if f.is_dir() and bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?_FAKE$", f.name))]
            return subfolders
    else:
        for folder in os.scandir(resetPath):
            if folder.is_dir() and  bool(re.search(r"[\d]{3,}[\w]?(-[\d]{2,3})?$", folder.name)):
                folderPath = resetPath + "\\" + folder.name
        if folderPath != "":
            subfolders = [f.name for f in os.scandir(folderPath) if f.is_dir()]
            return subfolders

class PicCollector:
    def __init__(self):
        super().__init__()
        # this is a placeholder
        self.width = getPicWidth()

    def listPics(self, event, filename):
        if not event.is_set():
            im = Image.open(filename)
            w, h = im.size
            ratio = h/w
            new_height = round(ratio * self.width)
            new_width = self.width
            resized_img = im.resize((new_width, new_height))
            return (resized_img, filename)
        else:
            return

    def getPics(self, folder, update):
        global pictures, opened, picDict, event
        with Manager() as manager:
            self.event = manager.Event()
            for key in picDict.keys():
                if folder is key:
                    update.setProgress(0.5, "searching for picture List")
                    time.sleep(1)
                    print('There are <' + str(len(picDict[key])) + '> Pictures in this Folder')
                    return picDict[key]
            list_of_files = sorted(filter(os.path.isfile,
                                          glob.glob(getLiveFake() + '\\' + folder + '\\*.png')))
            update.setProgress(0.5, "setting fixed Image width")
            time.sleep(1)
            with concurrent.futures.ProcessPoolExecutor() as executor:
                func = partial(self.listPics, self.event)
                images = executor.map(func, list_of_files)
                pictures = list(images)
                if not self.event.is_set():
                    picDict[folder] = pictures
                    print('There are <' + str(len(picDict[folder])) + '> Pictures in this Folder')
                    return picDict[folder]
                else:
                    return

    def stopPics(self):
        self.event.set()
        print('Stopped image collecting process')

